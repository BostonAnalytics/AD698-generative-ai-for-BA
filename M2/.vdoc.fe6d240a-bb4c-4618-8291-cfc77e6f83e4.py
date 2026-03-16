# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

import os
import re
import pandas as pd
import numpy as np
from tqdm import tqdm
from pathlib import Path
import json
import unicodedata
from typing import Optional, Dict, List

from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from sentence_transformers import SentenceTransformer

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("CUDA version:", torch.version.cuda)
    print("GPU name:", torch.cuda.get_device_name(0))
    print("GPU count:", torch.cuda.device_count())
else:
    print("Running on CPU")
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap


DATA_DIR = Path("../data/SEC-10K-2024-HTML")
OUTPUT_DIR = Path("../data/outputs/sec_10k_sections")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ALL_HTML_FILES = sorted(DATA_DIR.rglob("*.html")) + sorted(DATA_DIR.rglob("*.htm"))
print(f"Total HTML files found: {len(ALL_HTML_FILES)}")
#
#
#
#
#
#| echo: true       
#| eval: false
#| code-overflow: wrap

from google.colab import drive

drive.mount("/content/drive")

DATA_DIR = Path("/content/drive/MyDrive/Colab Notebooks/data/SEC-10K-2024-HTML")

assert os.path.exists(DATA_DIR), (
    "Google Drive is not mounted or the dataset path is incorrect. "
    "Did you run drive.mount()?"
)

print("Drive mounted successfully. Data directory found.")

OUTPUT_DIR = Path("/content/drive/MyDrive/Colab Notebooks/data/outputs/sec_10k_sections")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

assert os.path.exists(OUTPUT_DIR), (
    "Google Drive is not mounted or the dataset path is incorrect. "
    "Did you run drive.mount()?"
)

ALL_HTML_FILES = sorted(DATA_DIR.rglob("*.html")) + sorted(DATA_DIR.rglob("*.htm"))
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap


def select_html_files(
    files: List[Path],
    sample_n: Optional[int] = None, # set sample to none
    random_sample: bool = False,
    random_state: int = 42
) -> List[Path]:
    """
    Select all files or a smaller subset for debugging and development.

    Parameters
    ----------
    files : list[Path]
        Complete list of HTML filing paths.
    sample_n : int | None
        Number of files to process. If None, process all files.
    random_sample : bool
        If True, randomly sample files. Otherwise take the first sample_n files.
    random_state : int
        Seed for reproducibility when random_sample=True.
    """
    if sample_n is None:
        return files

    sample_n = min(sample_n, len(files))

    if random_sample:
        rng = random.Random(random_state)
        selected = rng.sample(files, sample_n)
        selected = sorted(selected)
    else:
        selected = files[:sample_n]

    return selected
#
#
#
#| echo: true
#| eval: false

# Activate your function here
html_files = select_html_files(
    SET_NAME_OF_YOUR_HTML_FILE_LIST,
    sample_n= SET_YOUR_DESIRED_SAMPLE_SIZE_OR_NONE,
    random_sample=False
)

print(f"Files selected for processing: {len(html_files)}")

# Do not show the html_files list use it as a diagnostic feature
# html_files[:5]
#
#
#
#| echo: false
#| eval: true
html_files = select_html_files(
    ALL_HTML_FILES,
    sample_n=25,
    random_sample=False
)

print(f"Files selected for processing: {len(html_files)}, this should say the number you set in sample_n")
html_files[:5]
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

def normalize_text(text: str) -> str:
    """
    Normalize unicode, spaces, and line breaks for more stable regex matching.
    """
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\xa0", " ")
    text = text.replace("&nbsp;", " ")
    text = re.sub(r"\r", "\n", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def html_to_text(html: str) -> str:
    """
    Parse HTML and return cleaned plain text.
    Removes script/style content and flattens the document.
    """
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "ix:header", "header", "footer"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    return normalize_text(text)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

ITEM_PATTERNS = {
    "item_1": re.compile(
        r"(?im)^\s*item\s*1[\.\-:\s]*\b(?!a\b)(?:business\b)?",
        re.IGNORECASE | re.MULTILINE
    ),
    "item_1a": re.compile(
        r"(?im)^\s*item\s*1a[\.\-:\s]*\b(?:risk\s+factors\b)?",
        re.IGNORECASE | re.MULTILINE
    ),
    "item_1b": re.compile(
        r"(?im)^\s*item\s*1b[\.\-:\s]*\b",
        re.IGNORECASE | re.MULTILINE
    ),
    "item_2": re.compile(
        r"(?im)^\s*item\s*2[\.\-:\s]*\b",
        re.IGNORECASE | re.MULTILINE
    ),
    "item_7": re.compile(
        r"(?im)^\s*item\s*7[\.\-:\s]*\b(?!a\b)(?:management'?s?\s+discussion\b|md&a\b)?",
        re.IGNORECASE | re.MULTILINE
    ),
    "item_7a": re.compile(
        r"(?im)^\s*item\s*7a[\.\-:\s]*\b",
        re.IGNORECASE | re.MULTILINE
    ),
    "item_8": re.compile(
        r"(?im)^\s*item\s*8[\.\-:\s]*\b",
        re.IGNORECASE | re.MULTILINE
    ),
}
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap


def find_item_positions(text: str, pattern: re.Pattern) -> List[int]:
    """
    Return all candidate start positions for a given item header.
    """
    return [m.start() for m in pattern.finditer(text)]
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap


def extract_section_by_bounds(
    text: str,
    start_pattern: re.Pattern,
    end_patterns: List[re.Pattern],
    min_chars: int = 500,
    max_chars: int = 2_000_000
) -> Optional[str]:
    start_positions = [m.start() for m in start_pattern.finditer(text)]
    if not start_positions:
        return None

    end_positions = []
    for pat in end_patterns:
        end_positions.extend([m.start() for m in pat.finditer(text)])
    end_positions = sorted(set(end_positions))

    candidates = []

    for start in start_positions:
        valid_ends = [end for end in end_positions if end > start]
        if not valid_ends:
            continue

        end = valid_ends[0]
        span_len = end - start

        if min_chars <= span_len <= max_chars:
            candidates.append((start, end, span_len))

    if not candidates:
        return None

    best_start, best_end, _ = max(candidates, key=lambda x: x[2])
    section = text[best_start:best_end].strip()
    return section if section else None
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap


def extract_target_sections(text: str) -> Dict[str, Optional[str]]:
    item_1 = extract_section_by_bounds(
        text=text,
        start_pattern=ITEM_PATTERNS["item_1"],
        end_patterns=[ITEM_PATTERNS["item_1a"], ITEM_PATTERNS["item_1b"], ITEM_PATTERNS["item_2"]],
        min_chars=1000
    )

    item_1a = extract_section_by_bounds(
        text=text,
        start_pattern=ITEM_PATTERNS["item_1a"],
        end_patterns=[ITEM_PATTERNS["item_1b"], ITEM_PATTERNS["item_2"]],
        min_chars=1000
    )

    item_7 = extract_section_by_bounds(
        text=text,
        start_pattern=ITEM_PATTERNS["item_7"],
        end_patterns=[ITEM_PATTERNS["item_7a"], ITEM_PATTERNS["item_8"]],
        min_chars=1000
    )

    return {
        "item_1": item_1,
        "item_1a": item_1a,
        "item_7": item_7,
    }
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap


def extract_basic_metadata(file_path: Path, text: str) -> Dict[str, str]:
    """
    Minimal metadata extractor.
    You can later extend this using SEC header fields.
    """
    return {
        "file_name": file_path.name,
        "file_path": str(file_path),
    }
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap


def process_html_files(
    html_files: List[Path],
    save_outputs: bool = True
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Process HTML filings and return:
    1. main extracted corpus
    2. recheck table for files needing manual review or second-pass regex

    A file is sent to recheck if:
    - parsing fails
    - Item 1 is missing
    - Item 1A is missing
    - Item 7 is missing
    """
    records = []
    recheck_records = []

    for i, file_path in enumerate(html_files, start=1):
        try:
            html = file_path.read_text(encoding="utf-8", errors="ignore")
            text = html_to_text(html)

            metadata = extract_basic_metadata(file_path, text)
            sections = extract_target_sections(text)

            item_1 = sections["item_1"]
            item_1a = sections["item_1a"]
            item_7 = sections["item_7"]

            missing_item_1 = item_1 is None
            missing_item_1a = item_1a is None
            missing_item_7 = item_7 is None

            status = "ok"
            if missing_item_1 or missing_item_1a or missing_item_7:
                status = "recheck"

            record = {
                **metadata,
                "raw_text_length": len(text),
                "item_1": item_1,
                "item_1a": item_1a,
                "item_7": item_7,
                "item_1_len": len(item_1) if item_1 else 0,
                "item_1a_len": len(item_1a) if item_1a else 0,
                "item_7_len": len(item_7) if item_7 else 0,
                "missing_item_1": missing_item_1,
                "missing_item_1a": missing_item_1a,
                "missing_item_7": missing_item_7,
                "status": status,
                "error": None,
            }
            records.append(record)

            if status == "recheck":
                recheck_records.append({
                    **metadata,
                    "raw_text_length": len(text),
                    "missing_item_1": missing_item_1,
                    "missing_item_1a": missing_item_1a,
                    "missing_item_7": missing_item_7,
                    "status": status,
                    "error": None,
                    "recheck_reason": "; ".join(
                        reason for reason, flag in [
                            ("missing Item 1", missing_item_1),
                            ("missing Item 1A", missing_item_1a),
                            ("missing Item 7", missing_item_7),
                        ] if flag
                    )
                })

        except Exception as e:
            metadata = extract_basic_metadata(file_path)

            error_record = {
                **metadata,
                "raw_text_length": None,
                "item_1": None,
                "item_1a": None,
                "item_7": None,
                "item_1_len": 0,
                "item_1a_len": 0,
                "item_7_len": 0,
                "missing_item_1": True,
                "missing_item_1a": True,
                "missing_item_7": True,
                "status": "error",
                "error": str(e),
            }
            records.append(error_record)

            recheck_records.append({
                **metadata,
                "raw_text_length": None,
                "missing_item_1": True,
                "missing_item_1a": True,
                "missing_item_7": True,
                "status": "error",
                "error": str(e),
                "recheck_reason": "parser/runtime error",
            })

        if i % 50 == 0 or i == len(html_files):
            print(f"Processed {i}/{len(html_files)} files")

    df_sections = pd.DataFrame(records)
    df_recheck = pd.DataFrame(recheck_records)

    if save_outputs:
        df_sections.to_csv(OUTPUT_DIR / "sec_10k_2024_sections.csv", index=False)
        df_sections.to_json(
            OUTPUT_DIR / "sec_10k_2024_sections.json",
            orient="records",
            force_ascii=False,
            indent=2
        )

        if not df_recheck.empty:
            df_recheck.to_csv(OUTPUT_DIR / "sec_10k_2024_recheck.csv", index=False)
            df_recheck.to_json(
                OUTPUT_DIR / "sec_10k_2024_recheck.json",
                orient="records",
                force_ascii=False,
                indent=2
            )

    return df_sections, df_recheck
#
#
#
#
#
#
#
#| echo: true
#| eval: false
#| code-overflow: wrap

# use the process_html_files function to build the corpus dataframe in a tuple of df_sections and df_recheck
df_sections, df_recheck = process_html_files(Add_the_name_of_your_html_file_list_variable_here)

# print the shapes of the resulting dataframes to check how many files were processed and how many need recheck
print("Main corpus shape:", df_sections.shape)
print("Recheck shape:", df_recheck.shape)
#
#
#
#| echo: false
#| eval: true
#| code-overflow: wrap

df_sections, df_recheck = process_html_files(html_files)

print("Main corpus shape:", df_sections.shape)
print("Recheck shape:", df_recheck.shape)
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

# Use this as diagnostic to check the df. Uncomment it for final run
df_sections.head().style.hide(axis="index")
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: false
#| code-overflow: wrap

# get the values for total files, item 1 extracted, item 1a extracted, and item 7 extracted from the df_sections dataframe and create a summary dataframe to display these metrics in a nice format

summary = pd.DataFrame({
    "metric": [

    ],
    "value": [

    ]
})

summary.style.hide(axis="index")
#
#
#
#
#| echo: false
#| eval: true
#| code-overflow: wrap

summary = pd.DataFrame({
    "metric": [
        "total_files",
        "item_1_extracted",
        "item_1a_extracted",
        "item_7_extracted",
    ],
    "value": [
        len(df_sections),
        df_sections["item_1"].notna().sum(),
        df_sections["item_1a"].notna().sum(),
        df_sections["item_7"].notna().sum(),
    ]
})

summary.style.hide(axis="index")
#
#
#
#
#
#| echo: true
#| eval: false
#| code-overflow: wrap

df_sections[[" ", " ", " "]].describe()
#
#
#
#
#| echo: false
#| eval: true
#| code-overflow: wrap

df_sections[["item_1_len", "item_1a_len", "item_7_len"]].describe()
#
#
#
#
#
#
#
#
#| echo: false
#| eval: true
#| code-overflow: wrap

df_sections.to_csv(OUTPUT_DIR / "sec_10k_2024_sections.csv", index=False)

with open(OUTPUT_DIR / "sec_10k_2024_sections.json", "w", encoding="utf-8") as f:
    json.dump(df_sections.to_dict(orient="records"), f, ensure_ascii=False, indent=2)

print("Saved outputs to:", OUTPUT_DIR.resolve())
#
#
#
#
#
#
#
#
#| echo: true
#| eval: false
#| code-overflow: wrap

section_rows = []

for _, row in df_sections.iterrows():
    for section_name in [" ", " ", " "]: # add item names here
        section_text = row[section_name]
        if isinstance(section_text, str) and section_text.strip():
            section_rows.append({
                "file_name": row["file_name"],
                "file_path": row["file_path"],
                "section_name": section_name,
                "section_text": section_text,
                "section_length": len(section_text),
            })

df_long = pd.DataFrame(section_rows)
df_long.head().style.hide(axis="index")
#
#
#
#| echo: false
#| eval: true
#| code-overflow: wrap

section_rows = []

for _, row in df_sections.iterrows():
    for section_name in ["item_1", "item_1a", "item_7"]:
        section_text = row[section_name]
        if isinstance(section_text, str) and section_text.strip():
            section_rows.append({
                "file_name": row["file_name"],
                "file_path": row["file_path"],
                "section_name": section_name,
                "section_text": section_text,
                "section_length": len(section_text),
            })

df_long = pd.DataFrame(section_rows)
df_long.head().style.hide(axis="index")
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_long.to_csv(OUTPUT_DIR / "sec_10k_2024_sections_long.csv", index=False)
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

import nltk
import re

nltk.download("punkt")
nltk.download("punkt_tab")

from nltk.tokenize import sent_tokenize

def clean_sentence(text: str) -> str:
    """
    Light cleanup for sentence text extracted from SEC filings.
    """
    text = str(text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap


def is_valid_sentence(text: str, min_chars: int = 25) -> bool:
    """
    Filter obvious noise and very short artifacts.
    """
    text = str(text).strip()

    if len(text) < min_chars:
        return False

    lowered = text.lower()
    bad_values = {
        "table of contents",
        "item 1",
        "item 1a",
        "item 7",
    }

    if lowered in bad_values:
        return False

    return True
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: false
#| code-overflow: wrap

sentence_rows = []

for _, row in df_long.iterrows():
    sentences = sent_tokenize(row[" "])

    sent_num = 0
    for sent in sentences:
        sent_clean = clean_sentence(sent)

        if not is_valid_sentence(sent_clean):
            continue

        sent_num += 1

        sentence_rows.append({
        ## Fill the dictionary with the appropriate values from row and the cleaned sentence
        })

df_sentences = pd.DataFrame(sentence_rows)

print(df_sentences.shape)
df_sentences.head().style.hide(axis="index")
#
#
#
#| echo: false
#| eval: true
#| code-overflow: wrap

sentence_rows = []

for _, row in df_long.iterrows():
    sentences = sent_tokenize(row["section_text"])

    sent_num = 0
    for sent in sentences:
        sent_clean = clean_sentence(sent)

        if not is_valid_sentence(sent_clean):
            continue

        sent_num += 1

        sentence_rows.append({
            "file_name": row["file_name"],
            "file_path": row["file_path"],
            "section_name": row["section_name"],
            "sentence_number": sent_num,
            "sentence_id": f"{row['file_name']}::{row['section_name']}::s{sent_num}",
            "sentence_text": sent_clean,
            "sentence_length_chars": len(sent_clean),
        })

df_sentences = pd.DataFrame(sentence_rows)

print(df_sentences.shape)
df_sentences.head().style.hide(axis="index")
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_sentences.to_csv(OUTPUT_DIR / "sec_10k_2024_sentences.csv", index=False)
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

def approximate_token_count(text: str) -> int:
    """
    Approximate token count using regex-based word/punctuation splitting.
    This is a lightweight stand-in for a model tokenizer.
    """
    text = str(text)
    tokens = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
    return len(tokens)
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_sentences["approx_token_count"] = df_sentences["sentence_text"].apply(approximate_token_count)

df_sentences[["sentence_text", "approx_token_count"]].head().style.hide(axis="index")
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap


from typing import List, Dict

def build_sentence_window_chunks(
    df_sentences: pd.DataFrame,
    target_tokens: int = 250,
    max_tokens: int = 320,
    overlap_sentences: int = 2,
    min_chunk_tokens: int = 40
) -> pd.DataFrame:
    """
    Build overlapping multi-sentence chunks from a sentence-level dataframe.

    Parameters
    ----------
    df_sentences : pd.DataFrame
        Sentence-level dataframe with columns:
        file_name, file_path, section_name, sentence_number, sentence_text, approx_token_count

    target_tokens : int
        Preferred chunk size in approximate tokens.

    max_tokens : int
        Hard upper bound for chunk size.

    overlap_sentences : int
        Number of trailing sentences to carry into the next chunk.

    min_chunk_tokens : int
        Minimum approximate token count required to keep a chunk.
    """
    chunk_rows: List[Dict] = []

    grouped = (
        df_sentences
        .sort_values(["file_name", "section_name", "sentence_number"])
        .groupby(["file_name", "file_path", "section_name"], as_index=False)
    )

    for (file_name, file_path, section_name), group in grouped:
        group = group.sort_values("sentence_number").reset_index(drop=True)

        n = len(group)
        start_idx = 0
        chunk_counter = 1

        while start_idx < n:
            current_sentences = []
            current_token_total = 0
            end_idx = start_idx

            while end_idx < n:
                sent_text = group.loc[end_idx, "sentence_text"]
                sent_tokens = int(group.loc[end_idx, "approx_token_count"])

                # always allow at least one sentence
                if current_token_total == 0:
                    current_sentences.append(sent_text)
                    current_token_total += sent_tokens
                    end_idx += 1
                    continue

                # stop if adding another sentence would exceed max_tokens
                if current_token_total + sent_tokens > max_tokens:
                    break

                current_sentences.append(sent_text)
                current_token_total += sent_tokens
                end_idx += 1

                # if target_tokens reached, we can stop this chunk
                if current_token_total >= target_tokens:
                    break

            chunk_text = " ".join(current_sentences).strip()

            if chunk_text and current_token_total >= min_chunk_tokens:
                start_sentence_num = int(group.loc[start_idx, "sentence_number"])
                end_sentence_num = int(group.loc[end_idx - 1, "sentence_number"])

                chunk_rows.append({
                    "chunk_id": f"{file_name}::{section_name}::c{chunk_counter}",
                    "file_name": file_name,
                    "file_path": file_path,
                    "section_name": section_name,
                    "start_sentence": start_sentence_num,
                    "end_sentence": end_sentence_num,
                    "n_sentences": end_idx - start_idx,
                    "chunk_text": chunk_text,
                    "chunk_length_chars": len(chunk_text),
                    "approx_token_count": current_token_total,
                })

                chunk_counter += 1

            # move forward with overlap
            if end_idx >= n:
                break

            next_start_idx = max(start_idx + 1, end_idx - overlap_sentences)
            if next_start_idx <= start_idx:
                next_start_idx = start_idx + 1

            start_idx = next_start_idx

    return pd.DataFrame(chunk_rows)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: false
#| code-overflow: wrap

df_chunks = build_sentence_window_chunks(
    df_sentences=df_sentences,
    target_tokens=add_your_target_token_value_here,
    max_tokens=add_your_max_token_value_here,
    overlap_sentences=add_your_overlap_sentences_value_here,
    min_chunk_tokens=add_your_min_chunk_tokens_value_here
)

print(df_chunks.shape)
df_chunks.head().style.hide(axis="index")
#
#
#
#
#| echo: false
#| eval: true
#| code-overflow: wrap

df_chunks = build_sentence_window_chunks(
    df_sentences=df_sentences,
    target_tokens=250,
    max_tokens=320,
    overlap_sentences=2,
    min_chunk_tokens=40
)

print(df_chunks.shape)
df_chunks.head().style.hide(axis="index")
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_chunks.to_csv(OUTPUT_DIR / "sec_10k_2024_sentence_window_chunks.csv", index=False)

df_chunks.to_json(
    OUTPUT_DIR / "sec_10k_2024_sentence_window_chunks.json",
    orient="records",
    force_ascii=False,
    indent=2
)

print("Saved rolling chunk corpus.")
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_chunks["section_name"].value_counts()
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap


df_chunks["approx_token_count"].describe()
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_chunks["n_sentences"].describe()
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_chunks.sample(10, random_state=42)[
    ["file_name", "section_name", "start_sentence", "end_sentence", "approx_token_count", "chunk_text"]
].style.hide(axis="index")
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: false

from pathlib import Path
import pandas as pd
import re
from collections import Counter

OUTPUT_DIR = Path("./outputs/sec_10k_sections")
CHUNKS_FILE = OUTPUT_DIR / "sec_10k_2024_sentence_window_chunks.csv"

df_chunks = pd.read_csv(CHUNKS_FILE)
print(df_chunks.shape)
df_chunks.head()
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap


TARGET_SIGNAL = "ai_investment"
# TARGET_SIGNAL = "technology_infrastructure"
# TARGET_SIGNAL = "datacenter_compute"
# TARGET_SIGNAL = "digital_transformation"
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

SIGNAL_DEFINITIONS = {
    "ai_investment": {
        "label": "Artificial Intelligence Investment",
        "description": "Language indicating spending, deployment, development, or strategic investment related to AI, machine learning, generative AI, or related systems.",
        "core_terms": [
            "artificial intelligence",
            "machine learning",
            "generative ai",
            "genai",
            "foundation model",
            "large language model",
            "llm",
            "ai model",
            "ai capability",
            "ai system",
            "automated decision",
            "intelligent automation"
        ],
        "support_terms": [
            "investment",
            "spending",
            "expense",
            "capital expenditure",
            "capex",
            "infrastructure",
            "platform",
            "development",
            "deployment",
            "training",
            "compute",
            "data center",
            "datacenter",
            "cloud",
            "model development",
            "technology investment"
        ],
        "exclude_terms": [
            "artificial flavors",
            "machine shop"
        ]
    },

    "technology_infrastructure": {
        "label": "Technology Infrastructure Spending",
        "description": "Language describing spending or strategic allocation toward enterprise systems, cloud, platforms, networks, compute, storage, or other digital infrastructure.",
        "core_terms": [
            "technology infrastructure",
            "information technology infrastructure",
            "cloud infrastructure",
            "platform infrastructure",
            "network infrastructure",
            "compute infrastructure",
            "digital infrastructure",
            "technology platform",
            "enterprise platform"
        ],
        "support_terms": [
            "investment",
            "spending",
            "expense",
            "capital expenditure",
            "capex",
            "upgrade",
            "expansion",
            "modernization",
            "migration",
            "implementation",
            "deployment",
            "storage",
            "servers",
            "compute",
            "systems"
        ],
        "exclude_terms": []
    },

    "datacenter_compute": {
        "label": "Datacenter / Compute Infrastructure Expansion",
        "description": "Language related to datacenter growth, compute capacity, server expansion, storage systems, and related infrastructure buildout.",
        "core_terms": [
            "data center",
            "datacenter",
            "compute capacity",
            "compute infrastructure",
            "server capacity",
            "gpu",
            "processing capacity",
            "storage infrastructure",
            "server infrastructure",
            "compute cluster"
        ],
        "support_terms": [
            "investment",
            "spending",
            "expense",
            "capital expenditure",
            "capex",
            "expansion",
            "construction",
            "lease",
            "facility",
            "capacity",
            "hardware",
            "cloud",
            "power",
            "cooling"
        ],
        "exclude_terms": []
    },

    "digital_transformation": {
        "label": "Digital Transformation Initiatives",
        "description": "Language describing digital modernization, enterprise transformation, platform change, automation, or technology-enabled business process redesign.",
        "core_terms": [
            "digital transformation",
            "technology transformation",
            "business transformation",
            "platform modernization",
            "enterprise modernization",
            "digital platform",
            "automation initiative",
            "systems modernization"
        ],
        "support_terms": [
            "investment",
            "spending",
            "initiative",
            "program",
            "implementation",
            "deployment",
            "upgrade",
            "migration",
            "modernization",
            "efficiency",
            "transformation"
        ],
        "exclude_terms": []
    }
}
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

signal_config = SIGNAL_DEFINITIONS[TARGET_SIGNAL]

print("Target signal:", TARGET_SIGNAL)
print("Label:", signal_config["label"])
print("Description:", signal_config["description"])
print("\nCore terms:")
print(signal_config["core_terms"])
print("\nSupport terms:")
print(signal_config["support_terms"])
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

def build_phrase_pattern(terms):
    """
    Build a case-insensitive regex pattern from a list of phrases.
    """
    escaped_terms = [re.escape(term) for term in terms]
    pattern = r"\b(?:%s)\b" % "|".join(escaped_terms)
    return re.compile(pattern, flags=re.IGNORECASE)
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

core_pattern = build_phrase_pattern(signal_config["core_terms"])
support_pattern = build_phrase_pattern(signal_config["support_terms"])

exclude_terms = signal_config.get("exclude_terms", [])
exclude_pattern = build_phrase_pattern(exclude_terms) if exclude_terms else None
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

def find_matches(pattern, text):
    """
    Return all matched phrases for a compiled regex pattern.
    """
    if pattern is None:
        return []
    return pattern.findall(str(text))
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap
def unique_lower(items):
    """
    Normalize matched items to lowercase unique values while preserving order.
    """
    seen = set()
    result = []
    for item in items:
        item_l = str(item).lower().strip()
        if item_l not in seen:
            seen.add(item_l)
            result.append(item_l)
    return result
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

def score_chunk_for_signal(text, core_pattern, support_pattern, exclude_pattern=None):
    """
    Compute weak-label signal features for a single chunk.
    """
    text = str(text)

    core_matches = unique_lower(find_matches(core_pattern, text))
    support_matches = unique_lower(find_matches(support_pattern, text))
    exclude_matches = unique_lower(find_matches(exclude_pattern, text)) if exclude_pattern else []

    n_core = len(core_matches)
    n_support = len(support_matches)
    n_exclude = len(exclude_matches)

    has_signal = n_core > 0 and n_exclude == 0

    # simple confidence heuristic
    if has_signal and n_core >= 1 and n_support >= 2:
        confidence = "high"
    elif has_signal and n_core >= 1 and n_support >= 1:
        confidence = "medium"
    elif has_signal:
        confidence = "low"
    else:
        confidence = "none"

    return {
        "has_signal": has_signal,
        "core_matches": core_matches,
        "support_matches": support_matches,
        "exclude_matches": exclude_matches,
        "n_core_matches": n_core,
        "n_support_matches": n_support,
        "n_exclude_matches": n_exclude,
        "signal_confidence": confidence
    }
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

signal_rows = []

for _, row in df_chunks.iterrows():
    score = score_chunk_for_signal(
        text=row["chunk_text"],
        core_pattern=core_pattern,
        support_pattern=support_pattern,
        exclude_pattern=exclude_pattern
    )

    signal_rows.append({
        "chunk_id": row["chunk_id"],
        "file_name": row["file_name"],
        "file_path": row["file_path"],
        "section_name": row["section_name"],
        "start_sentence": row["start_sentence"],
        "end_sentence": row["end_sentence"],
        "n_sentences": row["n_sentences"],
        "chunk_length_chars": row["chunk_length_chars"],
        "approx_token_count": row["approx_token_count"],
        "signal_type": TARGET_SIGNAL,
        "chunk_text": row["chunk_text"],
        **score
    })

df_signal = pd.DataFrame(signal_rows)

print(df_signal.shape)
df_signal.head().style.hide(axis="index")
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_signal_candidates = df_signal[df_signal["has_signal"]].copy()

print(df_signal_candidates.shape)
df_signal_candidates.head().style.hide(axis="index")
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_signal_candidates["signal_confidence"].value_counts(dropna=False)
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_signal_candidates["section_name"].value_counts(dropna=False)
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_signal_candidates.sample(
    n=min(10, len(df_signal_candidates)),
    random_state=42
)[[
    "chunk_id",
    "file_name",
    "section_name",
    "signal_confidence",
    "core_matches",
    "support_matches",
    "chunk_text"
]]
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap
def collapse_matches(values):
    if not values:
        return ""
    return "; ".join(values)
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_evidence = df_signal_candidates.copy()

df_evidence["core_matches_str"] = df_evidence["core_matches"].apply(collapse_matches)
df_evidence["support_matches_str"] = df_evidence["support_matches"].apply(collapse_matches)
df_evidence["exclude_matches_str"] = df_evidence["exclude_matches"].apply(collapse_matches)

df_evidence = df_evidence[[
    "chunk_id",
    "file_name",
    "file_path",
    "section_name",
    "signal_type",
    "signal_confidence",
    "start_sentence",
    "end_sentence",
    "n_sentences",
    "chunk_length_chars",
    "approx_token_count",
    "n_core_matches",
    "n_support_matches",
    "core_matches_str",
    "support_matches_str",
    "exclude_matches_str",
    "chunk_text"
]].copy()

print(df_evidence.shape)
df_evidence.head().style.hide(axis="index")
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

EVIDENCE_FILE = OUTPUT_DIR / f"sec_10k_2024_{TARGET_SIGNAL}_evidence_chunks.csv"
df_evidence.to_csv(EVIDENCE_FILE, index=False)

print("Saved evidence file to:", EVIDENCE_FILE)
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_evidence.to_json(
    OUTPUT_DIR / f"sec_10k_2024_{TARGET_SIGNAL}_evidence_chunks.json",
    orient="records",
    force_ascii=False,
    indent=2
)
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_company_signal_summary = (
    df_evidence
    .groupby(["file_name", "signal_type", "section_name"], as_index=False)
    .agg(
        n_signal_chunks=("chunk_id", "count"),
        avg_chunk_tokens=("approx_token_count", "mean"),
        high_conf_chunks=("signal_confidence", lambda x: (x == "high").sum())
    )
)

df_company_signal_summary.head().style.hide(axis="index")
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_company_signal_summary.to_csv(
    OUTPUT_DIR / f"sec_10k_2024_{TARGET_SIGNAL}_company_summary.csv",
    index=False
)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: false
#| code-overflow: wrap
from pathlib import Path
import pandas as pd
import re

OUTPUT_DIR = Path("./outputs/sec_10k_sections")

CHUNKS_FILE = OUTPUT_DIR / "sec_10k_2024_sentence_window_chunks.csv"
SECTIONS_FILE = OUTPUT_DIR / "sec_10k_2024_sections.csv"

df_chunks = pd.read_csv(CHUNKS_FILE)
df_sections = pd.read_csv(SECTIONS_FILE)

print("Chunks shape:", df_chunks.shape)
print("Sections shape:", df_sections.shape)
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

print("Chunk columns:")
print(df_chunks.columns.tolist())

print("\nSection columns:")
print(df_sections.columns.tolist())
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

metadata_cols = [col for col in [
    "file_name",
    "file_path",
    "company_name",
    "cik",
    "filing_date",
    "accession_number",
    "sic",
    "sector"
] if col in df_sections.columns]

df_metadata = df_sections[metadata_cols].drop_duplicates().copy()

print(df_metadata.shape)
df_metadata.head().style.hide(axis="index")
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

merge_keys = [col for col in ["file_name", "file_path"] if col in df_chunks.columns and col in df_metadata.columns]

df_retrieval = df_chunks.merge(
    df_metadata,
    on=merge_keys,
    how="left"
)

print(df_retrieval.shape)
df_retrieval.head().style.hide(axis="index")
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap
df_retrieval["document_type"] = "10-K"
df_retrieval["filing_year"] = 2024
df_retrieval["source_type"] = "sec_html_extracted"
df_retrieval["retrieval_unit"] = "sentence_window_chunk"
#
#
#
#
#
SECTION_LABELS = {
    "item_1": "Item 1 - Business",
    "item_1a": "Item 1A - Risk Factors",
    "item_7": "Item 7 - MD&A"
}

df_retrieval["section_label"] = df_retrieval["section_name"].map(SECTION_LABELS).fillna(df_retrieval["section_name"])
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

def clean_chunk_text(text: str) -> str:
    text = str(text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_retrieval["chunk_text"] = df_retrieval["chunk_text"].apply(clean_chunk_text)
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_retrieval = df_retrieval[df_retrieval["chunk_text"].str.len() > 0].copy()
print(df_retrieval.shape)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: false
#| code-overflow: wrap
TARGET_SIGNAL = "ai_investment"
EVIDENCE_FILE = OUTPUT_DIR / f"sec_10k_2024_{TARGET_SIGNAL}_evidence_chunks.csv"
#
#
#
if EVIDENCE_FILE.exists():
    df_evidence = pd.read_csv(EVIDENCE_FILE)

    signal_cols = [col for col in [
        "chunk_id",
        "signal_type",
        "signal_confidence",
        "n_core_matches",
        "n_support_matches"
    ] if col in df_evidence.columns]

    df_signal_meta = df_evidence[signal_cols].drop_duplicates().copy()

    df_retrieval = df_retrieval.merge(
        df_signal_meta,
        on="chunk_id",
        how="left"
    )

    df_retrieval["has_target_signal"] = df_retrieval["signal_type"].notna()
else:
    df_retrieval["signal_type"] = None
    df_retrieval["signal_confidence"] = None
    df_retrieval["n_core_matches"] = None
    df_retrieval["n_support_matches"] = None
    df_retrieval["has_target_signal"] = False
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap
preferred_cols = [
    "chunk_id",
    "file_name",
    "file_path",
    "company_name",
    "cik",
    "filing_date",
    "accession_number",
    "sic",
    "sector",
    "document_type",
    "filing_year",
    "source_type",
    "retrieval_unit",
    "section_name",
    "section_label",
    "start_sentence",
    "end_sentence",
    "n_sentences",
    "approx_token_count",
    "chunk_length_chars",
    "has_target_signal",
    "signal_type",
    "signal_confidence",
    "n_core_matches",
    "n_support_matches",
    "chunk_text"
]

final_cols = [col for col in preferred_cols if col in df_retrieval.columns]
df_retrieval = df_retrieval[final_cols].copy()

print(df_retrieval.shape)
df_retrieval.head().style.hide(axis="index")
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_retrieval["approx_token_count"].describe()
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_retrieval["section_name"].value_counts(dropna=False)
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

if "has_target_signal" in df_retrieval.columns:
    print(df_retrieval["has_target_signal"].value_counts(dropna=False))
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_retrieval.sample(
    n=min(10, len(df_retrieval)),
    random_state=42
)[[
    col for col in [
        "chunk_id",
        "file_name",
        "section_name",
        "approx_token_count",
        "has_target_signal",
        "signal_confidence",
        "chunk_text"
    ] if col in df_retrieval.columns
]].style.hide(axis="index")
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

RETRIEVAL_FILE = OUTPUT_DIR / "sec_10k_2024_retrieval_ready_chunks.csv"

df_retrieval.to_csv(RETRIEVAL_FILE, index=False)
print("Saved retrieval-ready dataset to:", RETRIEVAL_FILE)
#
#
#
#
#
#| echo: true
#| eval: true
#| code-overflow: wrap

df_retrieval.to_json(
    OUTPUT_DIR / "sec_10k_2024_retrieval_ready_chunks.json",
    orient="records",
    force_ascii=False,
    indent=2
)
#
#
#
#
