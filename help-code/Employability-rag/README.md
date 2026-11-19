# Employability RAG notebooks

Seven self-contained notebooks apply the Module 5 RAG sequence to the MET employability student API.
Each `.ipynb` has a matching `.qmd` source. Run any notebook independently from top to bottom.

| Notebook | Pipeline |
|---|---|
| [1_rag_simpler.ipynb](1_rag_simpler.ipynb) | Ingestion, chunking, retrieval, cited answers |
| [2_rag_simpler.ipynb](2_rag_simpler.ipynb) | Similarity, MMR, optional cross-encoder reranking |
| [3_rag_simpler_langsmith.ipynb](3_rag_simpler_langsmith.ipynb) | Explicit query decomposition, rank fusion, optional LangSmith tracing |
| [4_rag_simpler_langsmith.ipynb](4_rag_simpler_langsmith.ipynb) | Retrieval tools constrained by remote, hybrid, or onsite metadata |
| [5_rag_simpler_langsmith.ipynb](5_rag_simpler_langsmith.ipynb) | Draft, critique, revision; citation audit in offline mode |
| [6_ragas_evaluation.ipynb](6_ragas_evaluation.ipynb) | Reviewed references, job retrieval metrics, optional RAGAS |
| [7_ragas_huggingface_model_comparison.ipynb](7_ragas_huggingface_model_comparison.ipynb) | TF-IDF control and optional four-model embedding comparison |

## Run offline first

Install Python 3.10+ and the base dependencies:

```text
python -m pip install numpy pandas requests scikit-learn
```

Open a notebook in Jupyter, VS Code, or Colab and run its cells in order. The default mode uses eight
embedded **synthetic** postings, local TF-IDF retrieval, and evidence extracts. The fictional postings
are not a live API cache. Offline mode neither downloads models nor calls a hosted service.
In Colab, the files in `outputs/sample/` are temporary unless you download them.

Every notebook contains the complete data-loading and retrieval code. JSON outputs include source mode,
corpus hash, job IDs, and chunk IDs. Outputs are separated into `outputs/sample/` and `outputs/live/`.
Saved notebook outputs are cleared in the distributed files.

## Connect to the employability API

Set these environment variables privately before running the configuration cell:

| Variable | Value or purpose |
|---|---|
| `METCH_API_USE_SAMPLE_DATA` | `0` enables live requests; default `1` |
| `EMPLOYABILITY_API_KEY` | Your assigned API key; never place it in a shared cell |
| `EMPLOYABILITY_API_BASE_URL` | Default `https://met-employability-services.azurewebsites.net` |

`STUDENT_API_KEY` overrides `EMPLOYABILITY_API_KEY`. `METCH_API_ROOT` or `STUDENT_API_BASE_URL`
overrides the base URL and may contain the host, `/api/v1`, or `/api/v1/student`.
Historical `/met-career-match` roots are normalized. These notebooks use `/api/v1/student` directly;
they do not read `EMPLOYABILITY_API_PATH_PREFIX`. A private `.env` can be loaded explicitly with
`python-dotenv` before the configuration cell; it is not loaded automatically. In Colab, load secrets
from Colab userdata into the environment without displaying them. Restart a kernel after changing credentials.

The public schema is at `/api/v1/student/schema/`. Protected GET requests send `X-API-Key`:

- `/api/v1/student/jobs/?country=US&q=analyst&state=MA&limit=25&offset=0`
- `/api/v1/student/jobs/{job_id}/?include_raw=0`

The loader reads `results` and `meta.has_more`/`meta.next`. It reconstructs page requests rather than
following returned URLs. If a collection record lacks `description`, it reads the detail response's `result`.
There are at most two collection calls and 50 detail calls with the default configuration. Repeated IDs are
deduplicated. Missing descriptions are counted and excluded; an empty corpus stops with a clear message.
The page budget can return fewer than 50 unique jobs if records repeat or the API caps page size.
Descriptions may be capped at 6,000 characters by the API. No raw payload, credentials, or API response headers
are written to artifacts. The job endpoints exclude research-board stimuli.

Change `FILTERS`, `MAX_JOBS`, and `PAGE_SIZE` in the configuration cell to select a bounded corpus.
`country` is mandatory. The API supports country/region and posting-date or year filters; consult its schema
for the current options. The bounded sample is not a representative estimate of the whole labor market.
HTTP 401 means a missing or invalid key; 403 requires checking access and key/batch expiry;
429 means wait before retrying. Requests time out after 45 seconds and do not retry automatically.

## Enable optional pipeline stages

```text
python -m pip install sentence-transformers faiss-cpu langchain-openai langsmith "ragas==0.4.3"
```

| Variable | Effect when enabled |
|---|---|
| `EMPLOYABILITY_RAG_BACKEND=hf` | Download MiniLM; use normalized embeddings and FAISS |
| `EMPLOYABILITY_RAG_RERANK=1` | Run the cross-encoder in notebook 2 |
| `EMPLOYABILITY_RAG_GENERATE=1` | Generate answers using private `OPENAI_API_KEY` |
| `EMPLOYABILITY_RAG_MODEL` | Generator/evaluator model; default `gpt-4o-mini` |
| `EMPLOYABILITY_RAG_RAGAS=1` | Paid RAGAS evaluation using private `OPENAI_API_KEY` |
| `EMPLOYABILITY_RAG_COMPARE=1` | Run MiniLM, MPNet, BGE-small, and BGE-base in notebook 7 |
| `EMPLOYABILITY_RAG_TRACE=1` | Enable LangSmith tracing with private `LANGSMITH_API_KEY` |

All flags default to off. A configured key alone does not activate generation or evaluation.
Generation and RAGAS transmit retrieved text to the model provider; tracing can transmit inputs and outputs
to LangSmith. Use these stages only with evidence you may send to those services. Clear live notebook outputs
before sharing. Do not infer sponsorship, work authorization, salary currency, or hiring guarantees from missing text.

The offline path exercises ingestion, retrieval, decomposition, tool routing, citation auditing, and local metrics.
It does **not** execute semantic critique, RAGAS scoring, neural reranking, or the four-model comparison.
Enabling RAGAS alone scores the labeled extractive responses; enable generation as well to evaluate generated answers.

## Evaluation

The four embedded questions have manually authored reference answers and relevant job IDs for the synthetic corpus.
Live mode deliberately does not use those labels. Create a private `evaluation_questions.json` next to the notebook:

```json
[
  {
    "qid": "your-question-id",
    "user_input": "A question answered by your retrieved job snapshot",
    "reference": "An answer you have checked against those postings",
    "relevant_job_ids": [123]
  }
]
```

Replace the example ID with an actual job ID from your snapshot. JSON outputs retain the evaluation rows
and evidence. Job precision and recall deduplicate chunk-level hits into unique job IDs. RAGAS uses
`EvaluationDataset` and explicit LangChain model wrappers. Missing evaluation labels are reported;
requested RAGAS or model comparison stops when labels are absent. Citation auditing verifies identifiers,
not claim entailment. Model download/build times are reported separately from evaluation time.

## API and library references

The API contract was checked against `met-employability-services` on November 1, 2026:
`met_career_match/services/student_api.py` and `scripts/build_student_api_starter_notebooks.py`.
See the [RAGAS LangChain integration](https://github.com/vibrantlabsai/ragas/blob/main/docs/howtos/integrations/langchain.md)
and [Sentence Transformers CrossEncoder API](https://sbert.net/docs/package_reference/cross_encoder/model.html)
for the optional evaluation and reranking interfaces.

