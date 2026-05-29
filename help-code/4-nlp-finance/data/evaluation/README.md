# Apple 2025 SEC 10-K Evaluation Sets

These small datasets support the `4-nlp-finance` notebooks with concrete SEC filing tasks.
They are intended for teaching and lightweight evaluation, not for benchmark claims.

## Files

- `apple_2025_sentence_pool.jsonl`: reusable Apple 10-K sentence pool with tokenized text.
- `apple_2025_sentence_classification.csv`: weakly labeled train/validation/test sentence classification set.
- `apple_2025_qa.jsonl`: curated extractive QA examples over Apple 2025 filing facts.
- `apple_2025_summarization.jsonl`: short source/summary pairs for disclosure summarization.
- `apple_2025_keywords_gold.csv`: gold-style keyword list with rationales.
- `apple_2025_ner_tokens.csv`: BIO token labels for ORG, MONEY, DATE, GEO, PRODUCT, and FIN_METRIC.
- `apple_2025_translation_pairs.csv`: short English-to-German financial disclosure translation pairs.
- `apple_2025_lm_corpus.txt`: sentence-per-line corpus for n-gram/RNN/GPT-style language modeling examples.
- `apple_2025_vocabulary.csv`: token frequency vocabulary from the LM corpus.

## Source

Apple Inc. fiscal 2025 Form 10-K, filed October 31, 2025, for fiscal year ended September 27, 2025.
