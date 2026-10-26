# NLP Finance Companion Notebooks

This folder adapts the original help-code sequence into an `S1.1` through
`S12.3` finance edition, followed by the `S13.1` through `S13.3` fine-tuning notebooks.

The notebooks combine the original examples with
Apple fiscal 2025 Form 10-K bridge cells. The bridge cells load a common
Apple corpus, key statement metrics, and short labeled finance sentences so the same
NLP concepts can be discussed in financial-document context.

## Local data and shared helpers

The setup cells select the original `1-foundations`, `2-core-tasks`, or
`3-neural-nlp` directory for the original examples and their `src` imports.
Keep those directories alongside this folder. Duplicate neural helper files
are not needed in this folder's `src/`; it contains the finance-specific helpers.
Existing setup cells contain a local checkout path; adjust it when using a
different checkout location.

Use `S9.3 - Data Preparation LM SA.ipynb` for both language-model and
sentiment preprocessing. It includes sentence segmentation, UTF-8 input,
and Unicode normalization; the former `S9.3a` working copy is consolidated
there. Downloaded IMDB corpora and optional pretrained embeddings are local
artifacts. The small Apple evaluation fixtures remain versioned.

S9.4 can train with randomly initialized embeddings when `model.txt` is
absent. Loaded vectors must match the embedding layer shape before copying.
Full corpus preprocessing and model training remain explicit notebook steps.

## SEC 10-K Evaluation Sets

The folder now includes `data/evaluation/`, a small Apple 2025 SEC filing task pack:

- `apple_2025_sentence_pool.jsonl`: reusable Apple 10-K sentence pool.
- `apple_2025_sentence_classification.csv`: train/validation/test sentence labels.
- `apple_2025_qa.jsonl`: extractive QA examples over Apple filing facts.
- `apple_2025_summarization.jsonl`: source/summary pairs.
- `apple_2025_keywords_gold.csv`: keyword labels and rationales.
- `apple_2025_ner_tokens.csv`: BIO token labels for finance NER examples.
- `apple_2025_translation_pairs.csv`: short financial disclosure translation pairs.
- `apple_2025_lm_corpus.txt`: sentence-per-line language modeling corpus.
- `apple_2025_vocabulary.csv`: token frequency vocabulary.

Use `list_evaluation_sets()`, `load_evaluation_csv(...)`, and
`load_evaluation_jsonl(...)` from `src/finance_nlp_utils.py` inside any notebook.

## Section Map

- `S1.1`: setup
- `S2.1`-`S2.5`: text preparation foundations
- `S3.1`-`S3.2`: n-gram language models
- `S4.1`-`S4.3`: vector spaces and classic classification
- `S5.1`: HMM POS tagging
- `S6.1`-`S6.3`: CYK, constituency, and dependency parsing
- `S7.1`-`S7.2`: lexical semantics and logic rules
- `S8.1`-`S8.2`: keyword extraction and summarization
- `S9.1`-`S9.5`: MLP/RNN foundations and sequence data
- `S10.1`-`S10.3`: Word2Vec, CBOW, and Skipgram
- `S11.1`-`S11.2`: RNN machine translation sequence
- `S12.1`-`S12.3`: transformer, machine translation, and GPT
- `S13.1`: full fine-tuning an SEC 10-K sentence classifier
- `S13.2`: LoRA financial instruction tuning
- `S13.3`: QLoRA financial instruction tuning with 4-bit loading
