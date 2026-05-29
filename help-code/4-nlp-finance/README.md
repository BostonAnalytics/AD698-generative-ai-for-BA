# NLP Finance Companion Notebooks

This folder keeps the full 32-notebook sequence from the original help-code path, but
renames the notebooks into an `S1.1` through `S12.3` finance-edition sequence.

Each notebook preserves the original text, code, and visual explanations, then adds
Apple fiscal 2025 Form 10-K bridge cells at the top. The bridge cells load a common
Apple corpus, key statement metrics, and short labeled finance sentences so the same
NLP concepts can be discussed in financial-document context.

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
