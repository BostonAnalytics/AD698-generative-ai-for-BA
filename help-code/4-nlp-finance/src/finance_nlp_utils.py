from __future__ import annotations

import csv
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
EVALUATION_DIR = DATA_DIR / "evaluation"


def load_apple_10k() -> str:
    return (DATA_DIR / "apple_2025_10k_excerpt.txt").read_text(encoding="utf-8")


def load_metrics():
    with (DATA_DIR / "apple_2025_metrics.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_labeled_sentences():
    with (DATA_DIR / "apple_2025_labeled_sentences.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_evaluation_csv(name: str):
    """Load a CSV file from data/evaluation by filename."""
    with (EVALUATION_DIR / name).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_evaluation_jsonl(name: str):
    """Load a JSONL file from data/evaluation by filename."""
    import json

    with (EVALUATION_DIR / name).open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def list_evaluation_sets():
    """Return available SEC 10-K evaluation set filenames."""
    return sorted(p.name for p in EVALUATION_DIR.iterdir() if p.is_file() and p.name != "README.md")


def sent_tokenize(text: str):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text) if s.strip()]


def word_tokenize(text: str, lower: bool = True):
    tokens = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+(?:\.\d+)?%?|\$?\d[\d,]*(?:\.\d+)?", text)
    return [t.lower() for t in tokens] if lower else tokens


def normalize_number(token: str):
    if re.fullmatch(r"\$?\d[\d,]*(?:\.\d+)?%?", token):
        return "<NUM>"
    return token.lower()


def normalized_tokens(text: str):
    return [normalize_number(t) for t in word_tokenize(text, lower=False)]


def sample_sentences(n=6, seed=7):
    random.seed(seed)
    sents = sent_tokenize(load_apple_10k())
    return random.sample(sents, min(n, len(sents)))


def top_terms(text: str, n=20, stopwords=None):
    stopwords = set(stopwords or BASIC_STOPWORDS)
    counts = Counter(t for t in word_tokenize(text) if t not in stopwords and len(t) > 2)
    return counts.most_common(n)


def ngrams(tokens, n):
    return list(zip(*[tokens[i:] for i in range(n)]))


def cosine(a, b):
    keys = set(a) | set(b)
    dot = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return 0.0 if na == 0 or nb == 0 else dot / (na * nb)


def bow(text: str):
    return Counter(t for t in normalized_tokens(text) if t not in BASIC_STOPWORDS)


def naive_sentiment(sentence: str):
    positive = {"increase", "increased", "growth", "strong", "higher", "improved", "benefit"}
    negative = {"risk", "decline", "decrease", "lower", "adverse", "loss", "disruption", "uncertain"}
    tokens = set(word_tokenize(sentence))
    return sum(t in positive for t in tokens) - sum(t in negative for t in tokens)


BASIC_STOPWORDS = {
    "the", "and", "or", "of", "to", "in", "for", "a", "an", "is", "are", "was", "were",
    "with", "by", "as", "on", "at", "from", "that", "this", "it", "its", "be", "may",
    "company", "apple", "inc", "could", "would", "also", "not", "have", "has", "had",
}
