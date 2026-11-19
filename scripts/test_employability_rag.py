"""Focused contract and evidence tests; never call an external service."""
import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
os.environ["METCH_API_USE_SAMPLE_DATA"] = "1"
for key in ("GENERATE", "RAGAS", "COMPARE", "RERANK", "TRACE"):
    os.environ[f"EMPLOYABILITY_RAG_{key}"] = "0"
os.environ["EMPLOYABILITY_RAG_BACKEND"] = "tfidf"
spec = importlib.util.spec_from_file_location("rag", ROOT / "scripts/employability_rag_common.py")
rag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rag)
from build_employability_rag import JOBS


class ContractTests(unittest.TestCase):
    def test_pagination_detail_and_deduplication(self):
        calls = []
        def fake(path, params):
            calls.append((path, params))
            if path == "jobs/":
                rows = [{"job_id": 101}, {"job_id": 102, "description": "already loaded"}] if params["offset"] == 0 else [{"job_id": 102}, {"job_id": 103}]
                return {"results": rows, "meta": {"limit": 2, "next": "https://untrusted.invalid/", "has_more": True}}
            return {"result": {"job_id": int(path.split("/")[1]), "description": "detail text"}}
        rows = rag.load_live_jobs({"country": "US"}, max_jobs=4, page_size=2, get_json=fake)
        self.assertEqual([r["job_id"] for r in rows], [101, 102, 103])
        self.assertEqual([p for p, _ in calls], ["jobs/", "jobs/101/", "jobs/", "jobs/103/"])
        self.assertEqual(calls[2][1]["offset"], 2)

    def test_empty_invalid_and_bounds(self):
        self.assertEqual(rag.load_live_jobs({"country": "US"}, get_json=lambda *a: {"results": [], "meta": {}}), [])
        with self.assertRaises(ValueError):
            rag.load_live_jobs({})
        with self.assertRaises(ValueError):
            rag.load_live_jobs({"country": "US"}, max_jobs=501)
        with self.assertRaises(ValueError):
            rag.load_live_jobs({"country": "US"}, get_json=lambda *a: {"results": [], "meta": []})
        with self.assertRaises(ValueError):
            rag.RetrievalIndex([])

    def test_mismatched_detail(self):
        def fake(path, params):
            return {"results": [{"job_id": 1}], "meta": {}} if path == "jobs/" else {"result": {"job_id": 2}}
        with self.assertRaises(ValueError):
            rag.load_live_jobs({"country": "US"}, get_json=fake)

    def test_root_and_error_redaction(self):
        with patch.dict(os.environ, {"METCH_API_ROOT": "https://example.org/api/v1/student/"}):
            self.assertEqual(rag.api_root(), "https://example.org/api/v1/student")
        for value in ["http://example.org", "https://user:password@example.org", "https://example.org/?key=secret"]:
            with patch.dict(os.environ, {"METCH_API_ROOT": value}):
                with self.assertRaises(ValueError):
                    rag.api_root()
        class Session:
            def get(self, url, **kwargs):
                self.kwargs = kwargs
                return type("Response", (), {"status_code": 403})()
        session = Session()
        with patch.dict(os.environ, {"STUDENT_API_KEY": "test-secret-not-real", "METCH_API_ROOT": "https://example.org"}):
            with self.assertRaisesRegex(RuntimeError, "HTTP 403") as error:
                rag.fetch_json("jobs/", session=session)
            self.assertNotIn("test-secret", str(error.exception))
            self.assertFalse(session.kwargs["allow_redirects"])
            self.assertEqual(session.kwargs["timeout"], 45)
            with self.assertRaises(ValueError):
                rag.fetch_json("https://untrusted.invalid", session=session)

    def test_chunks_and_citations(self):
        chunks = rag.make_chunks(JOBS, "synthetic")
        self.assertEqual(len({c["chunk_id"] for c in chunks}), len(chunks))
        self.assertEqual(chunks, rag.make_chunks(JOBS, "synthetic"))
        changed = rag.make_chunks([{**JOBS[0], "description": "Changed evidence"}], "synthetic")
        self.assertNotEqual(chunks[0]["chunk_id"], changed[0]["chunk_id"])
        self.assertEqual(rag.make_chunks([{"job_id": 1, "description": ""}], "synthetic"), [])
        self.assertEqual(rag.clean_text("<style>secret</style><p>SQL &amp; Python</p>"), "SQL & Python")
        with self.assertRaises(ValueError):
            rag.make_chunks(JOBS, "synthetic", chunk_words=20, overlap=20)
        self.assertEqual(rag.citation_audit("Claim [job-invented]", chunks)["unknown_citations"], ["job-invented"])

    def test_retrieval_filters_mmr_and_metrics(self):
        index = rag.RetrievalIndex(rag.make_chunks(JOBS, "synthetic"))
        hits = index.search("Python SQL", filters={"remote_status": "remote"})
        self.assertEqual({h["job_id"] for h in hits}, {"103", "105"})
        self.assertTrue(all(h["remote_status"] == "remote" for h in hits))
        self.assertEqual(index.search("Python", filters={"remote_status": "unknown"}), [])
        self.assertEqual(index.search("zzzzunseenword"), [])
        mmr = index.search("Python SQL dashboards", strategy="mmr")
        self.assertEqual(len({h["chunk_id"] for h in mmr}), len(mmr))
        scores = rag.retrieval_metrics([hits[0], hits[0]], [hits[0]["job_id"], "missing"])
        self.assertEqual(scores["job_precision"], 1)
        self.assertEqual(scores["job_recall"], 0.5)
        self.assertEqual(scores["unique_jobs"], 1)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests))
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("EMPLOYABILITY_RAG_CHECKS_PASSED")
