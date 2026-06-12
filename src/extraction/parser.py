"""
src/extraction/parser.py

Parser Utilities

Used For:

1. Website Content Cleaning
2. Text Chunking
3. JSON Extraction
4. JSON Validation
5. GROQ Response Parsing
"""

import json
import re

from typing import Dict, List

from src.utils.config import (
    MAX_CHUNK_SIZE,
    CHUNK_OVERLAP,
    MAX_MARKDOWN_LENGTH,
    DEFAULT_COLLEGE_SCHEMA
)

# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(
    text: str
) -> str:

    if not text:

        return ""

    text = str(text)

    # remove extra spaces

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # remove multiple new lines

    text = re.sub(
        r"\n+",
        "\n",
        text
    )

    return text.strip()


# =====================================================
# CLEAN CONTENT
# =====================================================

def clean_content(
    content: str
) -> str:

    if not content:

        return ""

    content = clean_text(
        content
    )

    if len(content) > MAX_MARKDOWN_LENGTH:

        content = content[
            :MAX_MARKDOWN_LENGTH
        ]

    return content


# =====================================================
# CHUNK CONTENT
# =====================================================

def chunk_markdown(
    content: str,
    chunk_size: int = MAX_CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP
) -> List[str]:

    content = clean_content(
        content
    )

    if len(content) <= chunk_size:

        return [content]

    chunks = []

    start = 0

    while start < len(content):

        end = start + chunk_size

        chunks.append(
            content[start:end]
        )

        start += (
            chunk_size - overlap
        )

    return chunks


# =====================================================
# EXTRACT JSON FROM RESPONSE
# =====================================================

def extract_json(
    response_text: str
) -> Dict:

    if not response_text:

        return {}

    try:

        response_text = response_text.strip()

        # remove markdown

        response_text = response_text.replace(
            "```json",
            ""
        )

        response_text = response_text.replace(
            "```",
            ""
        )

        start = response_text.find("{")

        end = response_text.rfind("}")

        if start == -1 or end == -1:

            return {}

        json_text = response_text[
            start:end + 1
        ]

        return json.loads(
            json_text
        )

    except Exception:

        return {}


# =====================================================
# SAFE JSON PARSE
# =====================================================

def safe_parse_json(
    text: str
):

    try:

        return json.loads(text)

    except Exception:

        return {}


# =====================================================
# VALIDATE OUTPUT
# =====================================================

def validate_college_json(
    data: Dict
) -> Dict:

    validated = (
        DEFAULT_COLLEGE_SCHEMA.copy()
    )

    if not isinstance(
        data,
        dict
    ):

        return validated

    for key in validated.keys():

        if key in data:

            validated[key] = data[key]

    return validated


# =====================================================
# MERGE MULTIPLE RESULTS
# =====================================================

def merge_json_results(
    results: List[Dict]
) -> Dict:

    merged = {}

    for result in results:

        if not isinstance(
            result,
            dict
        ):

            continue

        for key, value in result.items():

            if value is None:
                continue

            if value == "":
                continue

            if value == []:
                continue

            merged[key] = value

    return merged


# =====================================================
# TITLE EXTRACTION
# =====================================================

def extract_title(
    content: str
):

    if not content:

        return ""

    lines = content.split("\n")

    for line in lines[:20]:

        line = line.strip()

        if len(line) > 5:

            return line

    return ""


# =====================================================
# CONTACT BLOCK
# =====================================================

def extract_contact_section(
    content: str
):

    keywords = [

        "contact",
        "phone",
        "email",
        "address",
        "reach us"

    ]

    lines = content.split("\n")

    matched = []

    for line in lines:

        lower = line.lower()

        if any(

            keyword in lower

            for keyword in keywords

        ):

            matched.append(
                line
            )

    return "\n".join(
        matched
    )


# =====================================================
# TRUNCATE TEXT
# =====================================================

def truncate_text(
    text: str,
    max_length: int = 5000
):

    if not text:

        return ""

    if len(text) <= max_length:

        return text

    return (

        text[:max_length]

        + " ..."

    )


# =====================================================
# SECTION DETECTOR
# =====================================================

def extract_key_sections(
    content: str
):

    sections = {

        "about": False,

        "placement": False,

        "admission": False,

        "research": False,

        "contact": False

    }

    text = content.lower()

    if "about" in text:

        sections["about"] = True

    if "placement" in text:

        sections["placement"] = True

    if "admission" in text:

        sections["admission"] = True

    if "research" in text:

        sections["research"] = True

    if "contact" in text:

        sections["contact"] = True

    return sections


# =====================================================
# CONTENT STATISTICS
# =====================================================

def content_statistics(
    content: str
):

    if not content:

        return {}

    return {

        "characters":
            len(content),

        "words":
            len(
                content.split()
            ),

        "chunks":
            len(
                chunk_markdown(
                    content
                )
            )

    }


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    sample = """

    RV College of Engineering

    Bengaluru

    NAAC A++

    Email:
    principal@rvce.edu.in

    Phone:
    +91 9876543210

    """

    print()

    print(
        content_statistics(
            sample
        )
    )

    print()

    print(
        chunk_markdown(
            sample,
            50,
            10
        )
    )

    print()

    print(
        extract_title(
            sample
        )
    )
    
