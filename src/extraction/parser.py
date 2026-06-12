"""
src/extraction/parser.py

Parser Utilities for:

1. Crawl4AI Markdown Processing
2. GROQ Input Preparation
3. JSON Extraction
4. Schema Validation
"""

import re
import json
from typing import Dict, List

from src.utils.helpers import (
    normalize_text,
    safe_json_loads
)

from src.utils.config import (
    MAX_CHUNK_SIZE,
    CHUNK_OVERLAP,
    MAX_MARKDOWN_LENGTH,
    DEFAULT_COLLEGE_SCHEMA
)

# =====================================================
# TEXT CLEANER
# =====================================================

def clean_text(text: str) -> str:

    if not text:
        return ""

    text = normalize_text(text)

    text = re.sub(
        r"\n{2,}",
        "\n",
        text
    )

    text = re.sub(
        r"\t+",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =====================================================
# MARKDOWN CLEANER
# =====================================================

def clean_markdown(markdown: str) -> str:

    if not markdown:
        return ""

    markdown = str(markdown)

    # Remove images

    markdown = re.sub(
        r"!\[.*?\]\(.*?\)",
        "",
        markdown
    )

    # Convert markdown links

    markdown = re.sub(
        r"\[(.*?)\]\((.*?)\)",
        r"\1",
        markdown
    )

    # Remove code blocks

    markdown = re.sub(
        r"```.*?```",
        "",
        markdown,
        flags=re.DOTALL
    )

    markdown = clean_text(
        markdown
    )

    if len(markdown) > MAX_MARKDOWN_LENGTH:

        markdown = markdown[
            :MAX_MARKDOWN_LENGTH
        ]

    return markdown


# =====================================================
# CHUNK MARKDOWN
# =====================================================

def chunk_markdown(
    markdown: str,
    chunk_size: int = MAX_CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP
) -> List[str]:

    markdown = clean_markdown(
        markdown
    )

    if len(markdown) <= chunk_size:

        return [markdown]

    chunks = []

    start = 0

    while start < len(markdown):

        end = start + chunk_size

        chunk = markdown[
            start:end
        ]

        chunks.append(
            chunk
        )

        start += (
            chunk_size - overlap
        )

    return chunks


# =====================================================
# EXTRACT JSON FROM LLM RESPONSE
# =====================================================

def extract_json(
    text: str
) -> Dict:

    if not text:

        return {}

    try:

        start = text.find("{")

        end = text.rfind("}")

        if start == -1:

            return {}

        if end == -1:

            return {}

        json_text = text[
            start:end + 1
        ]

        return json.loads(
            json_text
        )

    except Exception:

        return {}


# =====================================================
# SAFE JSON PARSER
# =====================================================

def safe_parse_json(
    text: str
) -> Dict:

    try:

        return json.loads(text)

    except Exception:

        return {}


# =====================================================
# VALIDATE COLLEGE JSON
# =====================================================

def validate_college_json(
    data: Dict
) -> Dict:

    if not data:

        data = {}

    validated = (
        DEFAULT_COLLEGE_SCHEMA.copy()
    )

    for key in validated.keys():

        if key in data:

            validated[key] = data[key]

    return validated


# =====================================================
# MERGE MULTIPLE JSONS
# =====================================================

def merge_json_results(
    results: List[Dict]
) -> Dict:

    merged = (
        DEFAULT_COLLEGE_SCHEMA.copy()
    )

    for result in results:

        for key, value in result.items():

            if value:

                merged[key] = value

    return merged


# =====================================================
# EXTRACT TITLE
# =====================================================

def extract_title(
    markdown: str
) -> str:

    lines = markdown.split("\n")

    for line in lines:

        line = line.strip()

        if line.startswith("#"):

            return line.replace(
                "#",
                ""
            ).strip()

    return ""


# =====================================================
# EXTRACT EMAIL BLOCKS
# =====================================================

def extract_contact_section(
    markdown: str
) -> str:

    keywords = [

        "contact",
        "contact us",
        "reach us",
        "email",
        "phone"

    ]

    lines = markdown.split(
        "\n"
    )

    result = []

    for line in lines:

        lower = line.lower()

        if any(
            k in lower
            for k in keywords
        ):

            result.append(
                line
            )

    return "\n".join(
        result
    )


# =====================================================
# TRUNCATE TEXT
# =====================================================

def truncate_text(
    text: str,
    max_length: int = 5000
) -> str:

    if not text:

        return ""

    if len(text) <= max_length:

        return text

    return (
        text[:max_length]
        + " ..."
    )


# =====================================================
# EXTRACT IMPORTANT SECTIONS
# =====================================================

def extract_key_sections(
    markdown: str
) -> Dict:

    sections = {

        "about": "",

        "placement": "",

        "admission": "",

        "contact": ""

    }

    text = markdown.lower()

    if "placement" in text:

        sections[
            "placement"
        ] = "Found"

    if "admission" in text:

        sections[
            "admission"
        ] = "Found"

    if "about" in text:

        sections[
            "about"
        ] = "Found"

    if "contact" in text:

        sections[
            "contact"
        ] = "Found"

    return sections


# =====================================================
# DEBUG
# =====================================================

if __name__ == "__main__":

    sample = """

# RV College of Engineering

NAAC A++

Contact:
info@rvce.edu.in

Placements:
Highest Package 92 LPA

"""

    print(
        clean_markdown(
            sample
        )
    )

    print(
        chunk_markdown(
            sample,
            100,
            20
        )
    )

    print(
        extract_title(
            sample
        )
    )

    print(
        extract_key_sections(
            sample
        )
    )
  
