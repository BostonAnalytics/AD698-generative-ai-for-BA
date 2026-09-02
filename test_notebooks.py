import subprocess
from pathlib import Path

notebooks = [
    "help-code/Rag/2_rag_simpler.ipynb",
    "help-code/Rag/3_rag_simpler_langsmith.ipynb",
    "help-code/Rag/4_rag_simpler_langsmith.ipynb",
    "help-code/Rag/5_rag_simpler_langsmith.ipynb",
    "help-code/Rag/6_ragas_evaluation.ipynb",
    "help-code/Rag/7_ragas_huggingface_model_comparison.ipynb"
]

results = {}
for nb in notebooks:
    print(f"Running {nb}...")
    result = subprocess.run(['uv', 'run', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', nb], capture_output=True, text=True)
    if result.returncode == 0:
        results[nb] = "Success"
        print(f"SUCCESS: {nb}")
    else:
        results[nb] = "Failed"
        print(f"FAILED: {nb}")
        print("ERROR DETAILS:")
        print(result.stderr[-2000:])
