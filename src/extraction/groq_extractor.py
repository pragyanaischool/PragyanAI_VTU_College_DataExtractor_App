"""
src/extraction/groq_extractor.py

GROQ Powered College Information Extraction

Pipeline:

Crawl4AI Markdown
        ↓
Regex Extraction
        ↓
Chunking
        ↓
GROQ LLM
        ↓
JSON Validation
        ↓
Final Structured Output
"""

import json
from typing import Dict, List

from src.llm.groq_client import groq_completion
from src.llm.prompts import COLLEGE_EXTRACTION_PROMPT

from src.extraction.parser import (
    chunk_markdown,
    extract_json,
    validate_college_json,
    merge_json_results,
    clean_markdown
)

from src.extraction.regex_extractor import (
    extract_regex_information
)

from src.utils.config import (
    DEFAULT_COLLEGE_SCHEMA
)

# =====================================================
# EXTRACT SINGLE CHUNK
# =====================================================

def extract_chunk(
    markdown_chunk: str
) -> Dict:

    try:

        prompt = f"""
{COLLEGE_EXTRACTION_PROMPT}

CONTENT:

{markdown_chunk}
"""

        response = groq_completion(
            prompt=prompt
        )

        result = extract_json(
            response
        )

        return result

    except Exception as e:

        print(
            f"Chunk Extraction Error: {e}"
        )

        return {}


# =====================================================
# MERGE RESULTS
# =====================================================

def merge_results(
    base: Dict,
    new_data: Dict
) -> Dict:

    for key, value in new_data.items():

        if value is None:
            continue

        if value == "":
            continue

        if value == []:
            continue

        base[key] = value

    return base


# =====================================================
# MAIN EXTRACTION
# =====================================================

def extract_college_details(
    markdown: str
) -> Dict:

    if not markdown:

        return DEFAULT_COLLEGE_SCHEMA.copy()

    markdown = clean_markdown(
        markdown
    )

    # -------------------------------------
    # REGEX EXTRACTION
    # -------------------------------------

    regex_data = extract_regex_information(
        markdown
    )

    # -------------------------------------
    # CHUNKING
    # -------------------------------------

    chunks = chunk_markdown(
        markdown
    )

    chunk_results = []

    # -------------------------------------
    # PROCESS CHUNKS
    # -------------------------------------

    for chunk in chunks:

        result = extract_chunk(
            chunk
        )

        if result:

            chunk_results.append(
                result
            )

    # -------------------------------------
    # MERGE CHUNK OUTPUTS
    # -------------------------------------

    llm_data = merge_json_results(
        chunk_results
    )

    # -------------------------------------
    # CREATE FINAL OBJECT
    # -------------------------------------

    final_data = (
        DEFAULT_COLLEGE_SCHEMA.copy()
    )

    final_data = merge_results(
        final_data,
        llm_data
    )

    final_data = merge_results(
        final_data,
        regex_data
    )

    final_data = validate_college_json(
        final_data
    )

    return final_data


# =====================================================
# BULK EXTRACTION
# =====================================================

def extract_multiple_colleges(
    markdown_list: List[str]
) -> List[Dict]:

    results = []

    for markdown in markdown_list:

        try:

            data = extract_college_details(
                markdown
            )

            results.append(
                data
            )

        except Exception as e:

            print(
                f"Bulk Extraction Error: {e}"
            )

    return results


# =====================================================
# SAVE JSON OUTPUT
# =====================================================

def save_extraction_result(
    result: Dict,
    filepath: str
):

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=4,
            ensure_ascii=False
        )


# =====================================================
# EXTRACT PLACEMENT DATA
# =====================================================

def extract_placement_info(
    markdown: str
) -> Dict:

    prompt = f"""
Extract placement related information.

Return JSON only.

Fields:

highest_package
average_package
placement_percentage
recruiters

CONTENT:

{markdown}
"""

    response = groq_completion(
        prompt
    )

    return extract_json(
        response
    )


# =====================================================
# EXTRACT ACCREDITATION DATA
# =====================================================

def extract_accreditation_info(
    markdown: str
) -> Dict:

    prompt = f"""
Extract accreditation information.

Return JSON only.

Fields:

naac_grade
nba_status
nirf_rank

CONTENT:

{markdown}
"""

    response = groq_completion(
        prompt
    )

    return extract_json(
        response
    )


# =====================================================
# EXTRACT COURSE DATA
# =====================================================

def extract_course_info(
    markdown: str
) -> Dict:

    prompt = f"""
Extract courses offered.

Return JSON only.

Fields:

courses

CONTENT:

{markdown}
"""

    response = groq_completion(
        prompt
    )

    return extract_json(
        response
    )


# =====================================================
# DEBUG
# =====================================================

if __name__ == "__main__":

    sample_markdown = """

# RV College of Engineering

NAAC Grade A++

NBA Accredited

Email:
info@rvce.edu.in

Phone:
+91 9876543210

Highest Package:
92 LPA

Courses:

Computer Science
Artificial Intelligence
Information Science

"""

    result = extract_college_details(
        sample_markdown
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )
  
