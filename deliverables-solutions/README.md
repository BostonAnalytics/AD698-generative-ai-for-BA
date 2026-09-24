# Running the solution notebooks

Use Python 3.11 or 3.12 and select that environment as your Jupyter kernel.
LangChain notebooks include a package setup cell before their examples. Run it
once, restart the kernel (or Colab session), then run the examples from the top.
`%pip` installs into the active notebook environment; a terminal's `pip` may
target a different environment.

## LangChain packages and imports

| Install with pip | Import in Python | Purpose |
| --- | --- | --- |
| `langchain-core` | `langchain_core.prompts` | Prompt templates |
| `langchain-core` | `langchain_core.documents`, `.runnables`, `.output_parsers`, `.tools` | Shared building blocks |
| `langchain-text-splitters` | `langchain_text_splitters` | Text chunking |
| `langchain-community` | `langchain_community.document_loaders`, `.vectorstores` | Loaders and vector stores |
| `langchain-huggingface` | `langchain_huggingface` | Hugging Face embeddings |
| `langchain-openai` | `langchain_openai` | OpenAI models and embeddings |
| `langchain-nvidia-ai-endpoints` | `langchain_nvidia_ai_endpoints` | NVIDIA endpoints |
| `langchain-classic` | `langchain_classic.retrievers` | Legacy retrievers used in the optional RAG helpers |

Package names use hyphens; Python module names use underscores. Install the
packages listed in each notebook rather than assuming `langchain` installs all
integrations. For example, a prompt-only notebook needs:

```python
%pip install -U langchain-core
```

After restarting the kernel, verify the import:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("Explain {topic} briefly.")
print(prompt.invoke({"topic": "retrieval"}).to_string())
```

If imports still fail, check `import sys; print(sys.executable)` in the notebook
and rerun `%pip` there. In a terminal, use `python -m pip install -U` followed by
the same package list. For dependency conflict reports, use a fresh course
environment and install the notebook's packages together.

Loaders can require extra packages: FAISS uses `faiss-cpu`, local Hugging Face
embeddings use `sentence-transformers`, arXiv loading uses `arxiv` and `pymupdf`,
and Unstructured loaders use `unstructured` (PDF support may require
`unstructured[pdf]` and additional system tools). Model API credentials and
input data must be configured separately from package installation.

See the official [LangChain migration guide](https://docs.langchain.com/oss/python/migrate/langchain-v1)
and [text splitter documentation](https://docs.langchain.com/oss/python/integrations/splitters/index).
