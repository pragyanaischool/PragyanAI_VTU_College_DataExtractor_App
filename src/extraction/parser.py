
# src/extraction/parser.py

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

def clean_text(text: str) -> str:

    if not text:
        return ""

    text = str(text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    text = re.sub(
        r"\n+",
        "\n",
        text
    )

    return text.strip()


# =====================================================
# CLEAN CONTENT
# =====================================================

def clean_content(content: str) -> str:

    if not content:
        return ""

    content = clean_text(content)

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

    content = clean_content(content)

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
# EMAIL
# =====================================================

def extract_emails(content: str):

    pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}"
    )

    return list(
        set(
            re.findall(
                pattern,
                content
            )
        )
    )


# =====================================================
# PHONE
# =====================================================

def extract_phones(content: str):

    pattern = (
        r"(?:\+91[\-\s]?)?"
        r"[6-9]\d{9}"
    )

    return list(
        set(
            re.findall(
                pattern,
                content
            )
        )
    )


# =====================================================
# WEBSITE
# =====================================================

def extract_websites(content: str):

    pattern = (
        r"https?://[^\s]+"
    )

    return list(
        set(
            re.findall(
                pattern,
                content
            )
        )
    )


# =====================================================
# PRINCIPAL
# =====================================================

def extract_principal(content: str):

    match = re.search(
        r"principal[:\-\s]+([A-Za-z .]+)",
        content,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return ""


# =====================================================
# DIRECTOR
# =====================================================

def extract_director(content: str):

    match = re.search(
        r"director[:\-\s]+([A-Za-z .]+)",
        content,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return ""


# =====================================================
# NAAC
# =====================================================

def extract_naac(content: str):

    match = re.search(
        r"NAAC\s*[:\-]?\s*([A-Z+]+)",
        content,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return ""


# =====================================================
# NBA
# =====================================================

def extract_nba(content: str):

    if "nba" in content.lower():
        return "Yes"

    return ""


# =====================================================
# NIRF
# =====================================================

def extract_nirf(content: str):

    match = re.search(
        r"NIRF.*?(\d+)",
        content,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return ""


# =====================================================
# PACKAGE
# =====================================================

def extract_highest_package(content: str):

    match = re.search(
        r"highest package.*?(\d+)",
        content,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return ""


def extract_average_package(content: str):

    match = re.search(
        r"average package.*?(\d+)",
        content,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return ""


# =====================================================
# JSON EXTRACTION
# =====================================================

def extract_json(
    response_text: str
) -> Dict:

    if not response_text:
        return {}

    try:

        response_text = response_text.strip()

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
# VALIDATION
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

    for key in validated:

        if key in data:
            validated[key] = data[key]

    return validated


# =====================================================
# MERGE
# =====================================================

def merge_json_results(
    results: List[Dict]
):

    merged = {}

    for result in results:

        if not isinstance(
            result,
            dict
        ):
            continue

        for key, value in result.items():

            if value in [
                None,
                "",
                []
            ]:
                continue

            merged[key] = value

    return merged


# =====================================================
# TITLE
# =====================================================

def extract_title(content: str):

    lines = content.split("\n")

    for line in lines[:20]:

        line = line.strip()

        if len(line) > 5:
            return line

    return ""


# =====================================================
# CONTACT SECTION
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

        if any(
            k in line.lower()
            for k in keywords
        ):
            matched.append(line)

    return "\n".join(
        matched
    )


# =====================================================
# CONTENT STATS
# =====================================================

def content_statistics(
    content: str
):

    return {

        "characters":
        len(content),

        "words":
        len(content.split()),

        "chunks":
        len(
            chunk_markdown(
                content
            )
        )
    }


# =====================================================
# QUICK EXTRACT
# =====================================================

def quick_extract(content):

    return {

        "emails":
        extract_emails(content),

        "phones":
        extract_phones(content),

        "websites":
        extract_websites(content),

        "principal":
        extract_principal(content),

        "director":
        extract_director(content),

        "naac":
        extract_naac(content),

        "nba":
        extract_nba(content),

        "nirf":
        extract_nirf(content),

        "highest_package":
        extract_highest_package(content),

        "average_package":
        extract_average_package(content)

    }
