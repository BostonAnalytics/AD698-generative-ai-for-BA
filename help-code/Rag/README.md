# Module 5 RAG Helper Notebooks

These notebooks use Tesla 10-K filings from 2015 through 2025 as a shared multi-year SEC corpus.

The notebooks are designed to be run in order:

1. `1_rag_simpler.ipynb`: baseline multi-year Tesla RAG with FAISS and Hugging Face embeddings
2. `2_rag_simpler.ipynb`: similarity retrieval, MMR retrieval, and optional Cohere reranking
3. `3_rag_simpler_langsmith.ipynb`: query decomposition with optional LangSmith tracing
4. `4_rag_simpler_langsmith.ipynb`: tool-style retrieval over all years, early years, recent years, and single years
5. `5_rag_simpler_langsmith.ipynb`: reflective RAG with draft, critique, and revision
6. `6_ragas_evaluation.ipynb`: RAGAS evaluation using current `EvaluationDataset` rows
7. `7_ragas_huggingface_model_comparison.ipynb`: RAGAS comparison across four Hugging Face embedding models

Each notebook keeps the SEC/RAG helper code inline rather than importing it from a shared module. This makes the notebooks more demonstrative for teaching. The visible helper code includes:

- the Tesla SEC filing URL list
- download/cache helpers
- HTML-to-text cleaning
- chunking helpers with year-aware metadata
- shared evaluation questions
- retrieval diagnostics
- context formatting and fallback extractive answers

Most notebooks can run retrieval diagnostics without `OPENAI_API_KEY`. Generated answers and RAGAS scoring require an evaluator LLM key.
