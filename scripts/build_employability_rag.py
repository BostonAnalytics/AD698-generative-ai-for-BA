"""Regenerate self-contained employability RAG notebook/QMD pairs."""
import hashlib
import json
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "help-code" / "Employability-rag"
COMMON = Path(__file__).with_name("employability_rag_common.py").read_text(encoding="utf-8")


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": textwrap.dedent(text).strip() + "\n"}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": textwrap.dedent(text).strip() + "\n"}


SAMPLES = [
    (101, "Data Analyst", "Example Health", "hybrid", ["Python", "SQL", "Tableau"], "Analyze clinical operations using Python and SQL. Build Tableau dashboards and explain quality trends to clinicians. This hybrid position requires two office days in Boston. One year of analytics experience is required. Annual salary range is USD 70000 to 85000."),
    (102, "Business Intelligence Analyst", "Example Transit", "onsite", ["SQL", "Power BI", "Excel"], "Use SQL and Power BI to report ridership and service reliability. Validate data quality and communicate findings to operations managers. This onsite Boston role requires two years of reporting experience. Annual salary range is USD 75000 to 95000."),
    (103, "Marketing Analyst", "Example Retail", "remote", ["Python", "SQL", "A/B testing"], "Analyze campaign conversion using Python and SQL. Design A/B testing experiments and explain incremental lift. This remote role is open to Massachusetts residents. Two years of marketing analytics experience is required. Compensation is not specified."),
    (104, "Financial Analyst", "Example Finance", "hybrid", ["Excel", "Power BI", "Forecasting"], "Build budgets and forecasting models in Excel. Use Power BI to communicate variance analysis. This hybrid Boston role requires three years of financial planning experience. Annual salary range is USD 80000 to 100000."),
    (105, "Data Engineering Analyst", "Example Logistics", "remote", ["Python", "SQL", "Airflow"], "Develop Python and SQL pipelines with Airflow. Monitor warehouse data quality and resolve pipeline failures. This remote Massachusetts role requires three years of data engineering experience. Annual salary range is USD 90000 to 115000."),
    (106, "Research Analyst Intern", "Example Research", "onsite", ["Python", "Statistics", "Excel"], "Use Python and statistics to summarize survey data. Explain confidence intervals and limitations. This onsite Boston internship accepts applicants with coursework in statistics and no prior professional experience. Pay is USD 25 per hour; annual pay is not stated."),
    (107, "People Analytics Analyst", "Example Services", "hybrid", ["SQL", "Tableau", "Privacy"], "Build SQL reports and Tableau dashboards for aggregate workforce trends. Apply privacy controls to employee data. This hybrid Boston role requires two years of relevant experience. Salary and visa sponsorship are not stated."),
    (108, "Supply Chain Analyst", "Example Manufacturing", "onsite", ["Excel", "SQL", "Forecasting"], "Use Excel and SQL for inventory forecasting. Explain stockout risk to warehouse managers. This onsite Boston role requires one year of operations experience. Salary and visa sponsorship are not stated."),
]
JOBS = [{"job_id": i, "title": title, "company_name": company, "remote_status": remote,
         "skills": [{"name": s, "type": "technical", "confidence": 1.0} for s in skills],
         "description": desc, "countryiso": "US", "state": "MA", "city": "Boston",
         "employment_type": "internship" if i == 106 else "full-time", "posted_at": "2026-10-01T00:00:00Z"}
        for i, title, company, remote, skills, desc in SAMPLES]
QUESTIONS = [
    {"qid": "remote-python", "user_input": "Which remote roles use Python and SQL, and what experience do they require?", "relevant_job_ids": [103, 105], "reference": "Example Retail requires two years of marketing analytics; Example Logistics requires three years of data engineering. Both are remote roles using Python and SQL."},
    {"qid": "dashboards", "user_input": "Which roles explicitly require Tableau dashboards?", "relevant_job_ids": [101, 107], "reference": "Example Health and Example Services specify Tableau dashboards. Example Health concerns clinical operations; Example Services concerns workforce trends."},
    {"qid": "entry", "user_input": "Which internship accepts statistics coursework without prior professional experience, and what is its pay period?", "relevant_job_ids": [106], "reference": "The Example Research internship accepts statistics coursework and no prior professional experience. Pay is USD 25 per hour; annual pay is not stated."},
    {"qid": "sponsorship", "user_input": "Does the People Analytics Analyst posting promise visa sponsorship?", "relevant_job_ids": [107], "reference": "The Example Services posting does not state visa sponsorship. No sponsorship promise can be inferred."},
]


def base(title, intro):
    parts = COMMON.split("# %% Configuration\n")
    return [md(f"# {title}\n\n{intro}"), md("""
        ## Setup and execution modes

        Run cells from top to bottom. The default uses **eight synthetic job postings**, local TF-IDF retrieval,
        and cited evidence extracts. These are fictional employers and examples, not API observations or employment advice.
        No key, model download, or external request is needed in the default mode.

        Install the base packages once using the commented command below, then restart the kernel if needed.
        For dense retrieval, reranking, generation, or RAGAS, install the optional packages too.
        Set environment variables before running the configuration cell (see README). An API key by itself
        never enables a paid call. Do not paste credentials into notebook cells or save live outputs in version control.
        """), code("""
        # Uncomment only the installation you need:
        # %pip install numpy pandas requests scikit-learn
        # %pip install sentence-transformers faiss-cpu langchain-openai langsmith "ragas==0.4.3"
        """), code(parts[0]), md("""
        ## Configuration and evidence functions

        `METCH_API_USE_SAMPLE_DATA=0` enables the live student jobs endpoint using `X-API-Key`.
        The default filters are country US, state MA, and query analyst. Live collection stops at 50 jobs.
        Responses contain `results` and `meta`; detail records are under `result`. Descriptions already
        present in collection responses are reused; missing descriptions trigger a detail request.
        Descriptions may be truncated to 6,000 characters by the API. Missing text is excluded and counted.

        TF-IDF is a lexical baseline. `EMPLOYABILITY_RAG_BACKEND=hf` selects normalized MiniLM embeddings
        and a FAISS inner-product index. Chunks never cross job boundaries. Every citation combines a job ID,
        content hash, and word offset, so a changed posting gets a changed citation ID.
        """), code(parts[1]), md("""
        ## Load postings and construct evidence

        The synthetic records and reviewed evaluation references are embedded below so this notebook can run
        on its own. Live mode does not reuse synthetic reference answers. To evaluate live data, create a private
        `evaluation_questions.json` with `qid`, `user_input`, `reference`, and `relevant_job_ids` for the current snapshot.
        Relevant IDs must identify postings in that snapshot. Evaluate exact counts and salary summaries with
        structured data, rather than extrapolating from top-k text retrieval.
        """), code("SAMPLE_JOBS = json.loads(" + repr(json.dumps(JOBS)) + ")\nSAMPLE_QUESTIONS = json.loads(" + repr(json.dumps(QUESTIONS)) + ")"), code("""
        records = SAMPLE_JOBS if USE_SAMPLE_DATA else load_live_jobs(FILTERS, MAX_JOBS, PAGE_SIZE)
        source_mode = "synthetic" if USE_SAMPLE_DATA else "live_api"
        chunks = make_chunks(records, source_mode)
        excluded = sum(not clean_text(r.get("description")) for r in records)
        if not chunks:
            raise ValueError("No usable descriptions. Inspect filters and API access before building an index.")
        index = RetrievalIndex(chunks, RETRIEVAL_BACKEND)
        if USE_SAMPLE_DATA:
            questions = SAMPLE_QUESTIONS
        else:
            evaluation_path = ROOT / "evaluation_questions.json"
            questions = json.loads(evaluation_path.read_text()) if evaluation_path.exists() else []
            for item in questions:
                if not {"qid", "user_input", "reference", "relevant_job_ids"}.issubset(item):
                    raise ValueError("Evaluation rows require qid, user_input, reference, relevant_job_ids.")
                if not item["reference"] or not item["relevant_job_ids"]:
                    raise ValueError("Supply a reviewed reference and relevant job IDs.")
                if not set(map(str, item["relevant_job_ids"])).issubset({c["job_id"] for c in chunks}):
                    raise ValueError("Evaluation references contain jobs absent from the evidence snapshot.")
        manifest = {"source_mode": source_mode, "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "filters": None if USE_SAMPLE_DATA else FILTERS, "jobs": len(records), "excluded_empty_descriptions": excluded,
                    "chunks": len(chunks), "backend": RETRIEVAL_BACKEND,
                    "embedding_model": EMBEDDING_MODEL if RETRIEVAL_BACKEND == "hf" else None,
                    "chunk_words": CHUNK_WORDS, "overlap_words": OVERLAP_WORDS,
                    "corpus_sha256": hashlib.sha256(json.dumps(records, sort_keys=True).encode()).hexdigest(),
                    "generation": RUN_GENERATION, "generator_model": GENERATOR_MODEL if RUN_GENERATION else None}
        save_rows("manifest", manifest)
        print(json.dumps(manifest, indent=2))
        pd.DataFrame(chunks)[["chunk_id", "job_id", "remote_status", "source_mode"]]
        """)]


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    notebooks = []
    notebooks.append(("1_rag_simpler", base("1 - Employability Baseline RAG", "Retrieve job-posting evidence, inspect its source, and produce an answer with job-level citations.") + [
        md("""## Retrieve and answer

        Compare retrieved descriptions with the question. A relevant title alone does not establish a skill,
        experience requirement, or remote arrangement. With generation disabled, the output is explicitly an
        evidence extract. `EMPLOYABILITY_RAG_GENERATE=1` enables an LLM answer using a private `OPENAI_API_KEY`.
        """), code('''
        question = "Which remote roles use Python and SQL, and what experience do they require?"
        hits = index.search(question)
        response = answer(question, hits)
        print(response)
        print(citation_audit(response, hits))
        save_rows("baseline", {"question": question, "hits": hits, "response": response})
        '''), md("## Retrieval evaluation\n\nJob precision and recall use unique job IDs, preventing overlapping chunks from counting the same posting twice. These measures do not score answer truthfulness."), code('''
        baseline_rows = evaluate_questions(index, questions)
        save_rows("baseline_evaluation", baseline_rows)
        if baseline_rows:
            display(pd.DataFrame(baseline_rows)[["qid", "job_precision", "job_recall", "reciprocal_rank", "response_mode"]])
        else:
            print("No reviewed live evaluation questions supplied.")
        ''')]))
    notebooks.append(("2_rag_simpler", base("2 - Employability Retrieval and Reranking", "Compare relevance ranking, maximal marginal relevance, and a cross-encoder reranker on the same job evidence.") + [
        md("""## Similarity and maximal marginal relevance

        Similarity ranks chunks by query similarity. MMR balances relevance against similarity to already selected
        chunks: `weight * query_similarity - (1 - weight) * redundancy`. A lower weight favors diversity.
        Diversity does not guarantee that a posting answers the question.
        """), code('''
        question = "Which analyst roles use SQL and communicate findings through dashboards?"
        variants = {"similarity": index.search(question), "mmr": index.search(question, strategy="mmr", weight=0.5)}
        comparison = [{"method": name, "rank": rank, "job_id": hit["job_id"], "score": hit["score"]}
                      for name, hits in variants.items() for rank, hit in enumerate(hits, 1)]
        display(pd.DataFrame(comparison))
        '''), md("""## Cross-encoder reranking

        Set `EMPLOYABILITY_RAG_RERANK=1` to download and run the cross-encoder. It scores each question/passage
        pair jointly, then reranks a wider candidate set. Its scores are not calibrated probabilities and are
        not comparable with cosine similarity. Long passages can be truncated by the model tokenizer.
        """), code('''
        if RUN_RERANKER:
            from sentence_transformers import CrossEncoder
            reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
            candidates = index.search(question, k=20)
            if candidates:
                scores = reranker.predict([(question, c["text"]) for c in candidates])
                reranked = sorted([{**c, "rerank_score": float(s)} for c, s in zip(candidates, scores)],
                                  key=lambda c: c["rerank_score"], reverse=True)[:K]
                variants["cross_encoder"] = reranked
        else:
            print("Cross-encoder skipped; set EMPLOYABILITY_RAG_RERANK=1 to enable model download.")
        outputs = [{"method": name, "hits": hits, "response": answer(question, hits)} for name, hits in variants.items()]
        save_rows("retrieval_comparison", outputs)
        for row in outputs:
            print(row["method"], row["response"])
        ''')]))
    notebooks.append(("3_rag_simpler_langsmith", base("3 - Employability Query Decomposition", "Split a multi-part question into explicit retrieval queries, merge evidence, and compare with direct retrieval.") + [
        md("""## Decompose and merge

        The query plan below is explicit and deterministic. Each subquery targets a separate requirement.
        Reciprocal rank fusion adds `1 / (60 + rank)` across lists; it does not average incompatible scores.
        Duplicate chunk IDs collapse before the final evidence budget is applied.
        """), code('''
        question = "Compare remote Python roles with onsite reporting roles: tools, duties, and experience."
        subqueries = ["remote Python SQL role experience", "onsite SQL Power BI reporting experience"]
        def decomposed_retrieval(subqueries, k=K):
            fused, evidence, trace = {}, {}, []
            for subquery in subqueries:
                hits = index.search(subquery, k=k)
                trace.append({"subquery": subquery, "chunk_ids": [h["chunk_id"] for h in hits]})
                for rank, hit in enumerate(hits, 1):
                    key = hit["chunk_id"]
                    fused[key] = fused.get(key, 0) + 1 / (60 + rank)
                    evidence[key] = hit
            keys = sorted(fused, key=fused.get, reverse=True)[:k]
            return [evidence[key] for key in keys], trace
        if RUN_TRACING:
            if not os.getenv("LANGSMITH_API_KEY"):
                raise RuntimeError("Set LANGSMITH_API_KEY privately before enabling tracing.")
            from langsmith import traceable
            decomposed_retrieval = traceable(name="employability-query-decomposition")(decomposed_retrieval)
        merged, trace = decomposed_retrieval(subqueries)
        comparisons = [{"method": name, "response": answer(question, hits), "hits": hits}
                       for name, hits in {"direct": index.search(question), "decomposed": merged}.items()]
        save_rows("decomposition_trace", trace)
        save_rows("decomposition_comparison", comparisons)
        display(pd.DataFrame(trace))
        for row in comparisons:
            print(row["method"], row["response"])
        '''), md("## Trace interpretation\n\nLocal JSON records retain each subquery and selected IDs. Optional LangSmith tracing sends function inputs and outputs, including posting text, to LangSmith; enable it only for data you may share. Inspect which subquery added evidence and whether the merged set covers both halves of the question.")]))
    notebooks.append(("4_rag_simpler_langsmith", base("4 - Employability Retrieval Tools", "Route requests to all-posting, remote, hybrid, or onsite evidence tools using explicit metadata constraints.") + [
        md("""## Define tools and a bounded route

        A tool here is a callable retrieval function. The route is selected explicitly; this is not an autonomous
        model tool-calling loop. Work arrangement filters operate before the final top-k selection. Unknown
        arrangements are excluded from arrangement-specific tools instead of being guessed from job titles.
        """), code('''
        def search_jobs(question, arrangement=None):
            filters = {"remote_status": arrangement} if arrangement else None
            return index.search(question, filters=filters)
        tools = {"all": lambda q: search_jobs(q), "remote": lambda q: search_jobs(q, "remote"),
                 "hybrid": lambda q: search_jobs(q, "hybrid"), "onsite": lambda q: search_jobs(q, "onsite")}
        question = "What tools and experience are required for analyst work?"
        selected_routes = ["remote", "hybrid"]
        if not set(selected_routes).issubset(tools):
            raise ValueError("Unknown retrieval route.")
        tool_results = [{"tool": route, "hits": tools[route](question)} for route in selected_routes]
        evidence = list({h["chunk_id"]: h for result in tool_results for h in result["hits"]}.values())
        response = answer("Compare remote and hybrid analyst work: " + question, evidence)
        save_rows("tool_evidence", {"routes": tool_results, "response": response})
        display(pd.DataFrame([{"tool": r["tool"], "job_ids": [h["job_id"] for h in r["hits"]]} for r in tool_results]))
        print(response)
        '''), md("## Coverage limits\n\nAn empty tool result means no matching evidence in this snapshot. It does not establish that no such jobs exist. No applications are submitted and no research-board stimuli are mixed into this corpus.")]))
    notebooks.append(("5_rag_simpler_langsmith", base("5 - Employability Reflective RAG", "Generate a draft, audit its evidence, and revise it without adding unsupported employment claims.") + [
        md("""## Draft, critique, revise

        With generation enabled, the critique checks factual claims, citations, missing qualifications, and
        unsupported sponsorship or salary statements. The revision uses the same evidence budget. In offline
        mode the audit checks citation identifiers only; the revision remains an extract, not a simulated LLM judgment.
        """), code('''
        question = "What does the People Analytics Analyst role require, and does it promise visa sponsorship?"
        hits = index.search(question)
        draft = answer(question, hits)
        audit = citation_audit(draft, hits)
        if RUN_GENERATION:
            critique = answer(question, hits, "Critique this draft against the evidence. Identify unsupported claims and missing citations. Draft: " + draft)
            revised = answer(question, hits, "Revise the draft using the critique, but include only supported claims. Draft: " + draft + " Critique: " + critique)
        else:
            critique = json.dumps(audit) + " No semantic critique was run."
            revised = answer(question, hits)
        result = {"question": question, "draft": draft, "critique": critique, "revised": revised,
                  "revision_audit": citation_audit(revised, hits), "mode": "llm_reflection" if RUN_GENERATION else "identifier_audit_only"}
        save_rows("reflection", result)
        for key in ["draft", "critique", "revised"]:
            print(key + ":", result[key])
        '''), md("## Evaluate the revision\n\nA model can repeat its original error during critique. Compare both answers with source text; valid citation IDs alone do not prove that a cited passage supports a claim. Missing sponsorship information must remain missing.")]))
    notebooks.append(("6_ragas_evaluation", base("6 - Employability RAGAS Evaluation", "Evaluate retrieval against reviewed job IDs and evaluate answers against posting evidence and reference answers.") + [
        md("""## Build evaluation rows

        Each row has `user_input`, `response`, `retrieved_contexts`, and `reference`, plus job IDs and response mode.
        The synthetic references apply only to the embedded corpus. Precision and recall measure retrieval;
        they do not establish the quality of generated prose. Inspect low recall before changing the prompt.
        """), code('''
        eval_rows = evaluate_questions(index, questions)
        save_rows("evaluation_rows", eval_rows)
        if eval_rows:
            display(pd.DataFrame(eval_rows)[["qid", "job_precision", "job_recall", "reciprocal_rank", "response_mode"]])
        else:
            print("Supply reviewed evaluation_questions.json for the live snapshot.")
        '''), md("""## Run optional RAGAS scoring

        Enable `EMPLOYABILITY_RAG_RAGAS=1` to send evidence and answers to a paid evaluator. Faithfulness checks
        answer support in context; response relevancy checks alignment with the question; context precision
        and recall use the reference answer. The evaluator may be wrong. Review individual failures and missing
        scores. An extractive answer is labeled as such and must not be presented as generated-answer performance.
        """), code('''
        scores = ragas_scores(eval_rows)
        if not scores.empty:
            scores.to_csv(OUTPUT_DIR / "ragas_scores.csv", index=False)
            display(scores)
        ''')]))
    notebooks.append(("7_ragas_huggingface_model_comparison", base("7 - Employability Embedding Model Comparison", "Hold the job corpus, questions, chunking, top-k, and answer mode fixed while comparing four embedding models.") + [
        md("""## Controlled comparison

        The offline run records a TF-IDF control only. Set `EMPLOYABILITY_RAG_COMPARE=1` to download and run all
        four Hugging Face models. BGE uses its query instruction; document text stays unchanged. Every model
        uses normalized vectors and FAISS inner product. Longer text may be truncated differently by each
        tokenizer. Timings include model loading and can include downloads, so they are not serving-latency benchmarks.
        """), code('''
        model_options = {
            "minilm_l6": "sentence-transformers/all-MiniLM-L6-v2",
            "mpnet_base": "sentence-transformers/all-mpnet-base-v2",
            "bge_small": "BAAI/bge-small-en-v1.5",
            "bge_base": "BAAI/bge-base-en-v1.5",
        }
        comparison_rows = evaluate_questions(RetrievalIndex(chunks, "tfidf"), questions, "tfidf_control")
        timings = []
        if RUN_MODEL_COMPARISON:
            if not questions:
                raise ValueError("Supply reviewed live evaluation questions before comparison.")
            for name, model_name in model_options.items():
                started = time.perf_counter()
                model_index = RetrievalIndex(chunks, "hf", model_name)
                build_seconds = time.perf_counter() - started
                started = time.perf_counter()
                comparison_rows.extend(evaluate_questions(model_index, questions, name))
                timings.append({"variant": name, "model": model_name, "build_seconds": build_seconds,
                                "evaluation_seconds": time.perf_counter() - started})
                del model_index
        else:
            print("Four-model comparison skipped. Only the TF-IDF control ran.")
        save_rows("model_comparison", comparison_rows)
        save_rows("model_timings", timings)
        if comparison_rows:
            display(pd.DataFrame(comparison_rows).groupby("variant")[["job_precision", "job_recall", "reciprocal_rank"]].mean())
        '''), md("## RAGAS by model\n\nOptional scoring keeps question IDs and model names attached to each score. Compare per-question results before averaging. Four synthetic questions are a smoke test, not evidence that one model is generally superior."), code('''
        if RUN_RAGAS:
            if not comparison_rows:
                raise ValueError("Supply reviewed live evaluation questions before RAGAS scoring.")
            for variant in dict.fromkeys(row["variant"] for row in comparison_rows):
                subset = [row for row in comparison_rows if row["variant"] == variant]
                scores = ragas_scores(subset)
                scores.insert(0, "variant", variant)
                scores.to_csv(OUTPUT_DIR / f"ragas_{variant}.csv", index=False)
                display(scores)
        else:
            print("RAGAS model scoring skipped.")
        ''')]))
    for stem, cells in notebooks:
        for n, cell in enumerate(cells):
            cell["id"] = hashlib.sha256(f"{stem}-{n}".encode()).hexdigest()[:12]
        nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
              "language_info": {"name": "python", "version": "3.12"}}, "nbformat": 4, "nbformat_minor": 5}
        (DEST / f"{stem}.ipynb").write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        title = cells[0]["source"].splitlines()[0][2:]
        qmd = f'---\ntitle: "{title}"\njupyter: python3\nexecute:\n  eval: false\n  echo: true\n---\n\n'
        qmd += "\n".join(c["source"] if c["cell_type"] == "markdown" else "```{python}\n" + c["source"] + "```\n" for c in cells)
        (DEST / f"{stem}.qmd").write_text(qmd, encoding="utf-8")
    print("GENERATED_SEVEN_EMPLOYABILITY_NOTEBOOKS")


if __name__ == "__main__":
    main()
