"""
src/utils/helpers.py

Common Utility Functions

Used By:
---------
- Database Layer
- GROQ Extraction
- Regex Extraction
- Crawl4AI
- Streamlit Pages
"""

import re
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


# =====================================================
# TIMESTAMP
# =====================================================

def timestamp() -> str:
    """
    Current timestamp string
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# =====================================================
# DATE STRING
# =====================================================

def current_date() -> str:

    return datetime.now().strftime(
        "%Y-%m-%d"
    )


# =====================================================
# NORMALIZE TEXT
# =====================================================

def normalize_text(
    text
) -> str:

    if text is None:
        return ""

    text = str(text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =====================================================
# REMOVE HTML TAGS
# =====================================================

def remove_html_tags(
    text
) -> str:

    if not text:
        return ""

    clean = re.sub(
        r"<.*?>",
        "",
        str(text)
    )

    return clean.strip()


# =====================================================
# CLEAN MARKDOWN
# =====================================================

def clean_markdown(
    markdown
) -> str:

    if markdown is None:
        return ""

    markdown = str(markdown)

    markdown = re.sub(
        r"\n+",
        "\n",
        markdown
    )

    markdown = re.sub(
        r"\s+",
        " ",
        markdown
    )

    return markdown.strip()


# =====================================================
# SAVE JSON
# =====================================================

def save_json(
    data: Dict,
    filepath
):

    filepath = Path(filepath)

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =====================================================
# LOAD JSON
# =====================================================

def load_json(
    filepath
):

    filepath = Path(filepath)

    if not filepath.exists():

        return {}

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =====================================================
# SAFE JSON LOADS
# =====================================================

def safe_json_loads(
    text
):

    try:

        return json.loads(text)

    except Exception:

        return {}


# =====================================================
# SAFE JSON DUMPS
# =====================================================

def safe_json_dumps(
    data
):

    try:

        return json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        )

    except Exception:

        return "{}"


# =====================================================
# SAVE DATAFRAME
# =====================================================

def save_dataframe(
    df: pd.DataFrame,
    filepath
):

    filepath = Path(filepath)

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        filepath,
        index=False
    )


# =====================================================
# LOAD DATAFRAME
# =====================================================

def load_dataframe(
    filepath
):

    filepath = Path(filepath)

    if not filepath.exists():

        return pd.DataFrame()

    return pd.read_csv(
        filepath
    )


# =====================================================
# CLEAN DATAFRAME
# =====================================================

def clean_dataframe(
    df: pd.DataFrame
):

    if df.empty:

        return df

    df = df.fillna("")

    df = df.drop_duplicates()

    return df


# =====================================================
# REMOVE EMPTY FIELDS
# =====================================================

def remove_empty_fields(
    data: Dict
):

    return {

        k: v

        for k, v in data.items()

        if v not in [

            "",
            None,
            [],
            {},
            "null",
            "None"

        ]

    }


# =====================================================
# VALIDATE EMAIL
# =====================================================

def is_valid_email(
    email
):

    pattern = (

        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}$"

    )

    return bool(
        re.match(
            pattern,
            str(email)
        )
    )


# =====================================================
# VALIDATE PHONE
# =====================================================

def is_valid_phone(
    phone
):

    phone = re.sub(
        r"\D",
        "",
        str(phone)
    )

    return len(phone) >= 10


# =====================================================
# VALIDATE URL
# =====================================================

def is_valid_url(
    url
):

    pattern = (

        r"^(https?|ftp):\/\/"
        r"[^\s/$.?#].[^\s]*$"

    )

    return bool(
        re.match(
            pattern,
            str(url)
        )
    )


# =====================================================
# CHUNK TEXT
# =====================================================

def chunk_text(
    text,
    chunk_size=10000,
    overlap=500
):

    if not text:

        return []

    text = str(text)

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += (
            chunk_size - overlap
        )

    return chunks


# =====================================================
# LIST TO STRING
# =====================================================

def list_to_string(
    value
):

    if isinstance(
        value,
        list
    ):

        return ", ".join(
            map(str, value)
        )

    return str(value)


# =====================================================
# STRING TO LIST
# =====================================================

def string_to_list(
    value
):

    if not value:

        return []

    return [

        item.strip()

        for item in str(value).split(",")

        if item.strip()

    ]


# =====================================================
# FLATTEN DICTIONARY
# =====================================================

def flatten_dict(
    data: Dict
):

    flattened = {}

    for k, v in data.items():

        if isinstance(
            v,
            list
        ):

            flattened[k] = (
                ", ".join(
                    map(str, v)
                )
            )

        else:

            flattened[k] = v

    return flattened


# =====================================================
# CREATE DIRECTORY
# =====================================================

def ensure_directory(
    folder
):

    Path(folder).mkdir(
        parents=True,
        exist_ok=True
    )


# =====================================================
# FILE EXISTS
# =====================================================

def file_exists(
    filepath
):

    return Path(
        filepath
    ).exists()


# =====================================================
# GET FILE SIZE
# =====================================================

def get_file_size_mb(
    filepath
):

    filepath = Path(filepath)

    if not filepath.exists():

        return 0

    return round(

        filepath.stat().st_size
        /
        (1024 * 1024),

        2

    )


# =====================================================
# DEBUG
# =====================================================

if __name__ == "__main__":

    sample = """

    VTU College Intelligence

    Contact:
    info@test.com

    """

    print(
        normalize_text(sample)
    )

    print(
        chunk_text(
            sample,
            20,
            5
        )
    )

    print(
        timestamp()
    )
  
