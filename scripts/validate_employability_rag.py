"""Execute the seven offline notebooks in separate processes without servers."""
import ast
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "help-code/Employability-rag"
ARTIFACTS = ROOT / "artifacts/employability-rag"


def execute(path):
    import nbformat
    from unittest.mock import patch
    from check_course_language import violations
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    namespace = {"__name__": "__main__", "display": print}
    cells = 0
    # No sockets are needed by this code path, including model downloads.
    with patch("socket.socket.connect", side_effect=AssertionError("Offline validation attempted a network connection")):
        for number, cell in enumerate(notebook.cells):
            if violations(cell.source):
                raise AssertionError(f"Authoring-language violation in {path.name} cell {number}")
            if cell.cell_type != "code":
                continue
            tree = ast.parse(cell.source)
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
                last = tree.body.pop() if tree.body and isinstance(tree.body[-1], ast.Expr) else None
                exec(compile(tree, f"{path.name}:cell-{number}", "exec"), namespace)
                if last:
                    value = eval(compile(ast.Expression(last.value), f"{path.name}:cell-{number}", "eval"), namespace)
                    if value is not None:
                        print(value)
            cell.execution_count = cells + 1
            cell.outputs = [nbformat.v4.new_output("stream", name="stdout", text=stream.getvalue())] if stream.getvalue() else []
            cells += 1
    assert namespace["source_mode"] == "synthetic"
    assert len(namespace["records"]) == 8
    assert len(namespace["questions"]) == 4
    assert not any(namespace[k] for k in ["RUN_GENERATION", "RUN_RAGAS", "RUN_MODEL_COMPARISON", "RUN_RERANKER", "RUN_TRACING"])
    assert namespace["RETRIEVAL_BACKEND"] == "tfidf"
    # Source parity includes exact code cells, not merely matching file names.
    qmd = path.with_suffix(".qmd").read_text(encoding="utf-8")
    for cell in notebook.cells:
        assert cell.source in qmd
    nbformat.write(notebook, ARTIFACTS / path.name)
    print(f"PASS {path.name}: {cells} code cells, 8 synthetic jobs, 4 references")


def main():
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    if len(sys.argv) == 2:
        execute(Path(sys.argv[1]))
        return
    env = dict(os.environ, METCH_API_USE_SAMPLE_DATA="1", EMPLOYABILITY_RAG_BACKEND="tfidf")
    for flag in ["GENERATE", "RAGAS", "COMPARE", "RERANK", "TRACE"]:
        env[f"EMPLOYABILITY_RAG_{flag}"] = "0"
    notebooks = sorted(FOLDER.glob("*.ipynb"))
    assert len(notebooks) == 7
    results = []
    for path in notebooks:
        result = subprocess.run([sys.executable, str(Path(__file__).resolve()), str(path)], cwd=ROOT,
                                env=env, capture_output=True, text=True, timeout=120)
        print(result.stdout, end="")
        if result.returncode:
            print(result.stderr)
            raise SystemExit(result.returncode)
        results.append({"notebook": path.name, "exit_code": result.returncode, "output": result.stdout.strip()})
    (ARTIFACTS / "execution_report.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("SEVEN_NOTEBOOKS_EXECUTED")


if __name__ == "__main__":
    main()
