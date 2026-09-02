import subprocess
import sys

notebooks = [
    "help-code/Rag/3_rag_simpler_langsmith.ipynb",
    "help-code/Rag/4_rag_simpler_langsmith.ipynb",
    "help-code/Rag/5_rag_simpler_langsmith.ipynb",
    "help-code/Rag/6_ragas_evaluation.ipynb",
    "help-code/Rag/7_ragas_huggingface_model_comparison.ipynb"
]

for nb in notebooks:
    print(f"--- Running {nb} ---", flush=True)
    result = subprocess.run(
        ["uv", "run", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", nb],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"SUCCESS: {nb}\n", flush=True)
    else:
        print(f"FAILED: {nb}", flush=True)
        print("ERROR DETAILS:", flush=True)
        print(result.stderr[-2500:], flush=True)
        sys.exit(1)
