"""
src/extraction/groq_extractor.py

GROQ Based College Intelligence Extraction

Input:
------
Website Content (Text)

Output:
-------
Structured College Information
"""

import json
from typing import Dict, List

from src.llm.groq_client import (
    groq_completion
)

from src.llm.prompts import (
    COLLEGE_EXTRACTION_PROMPT
)

from src.extraction.regex_extractor import (
    extract_regex_information
)

from src.extraction.parser import (
    clean_text,
    chunk_markdown,
    extract_json,
    validate_college_json,
    merge_json_results,
    quick_extract
)

from src.utils.config import (
    DEFAULT_COLLEGE_SCHEMA
)

# =====================================================
# EXTRACT SINGLE CHUNK
# =====================================================

def extract_chunk(
    content: str
) -> Dict:

    try:

        prompt = f"""
You are an expert College Intelligence Extraction System.

Analyze the college website content and extract structured information.

IMPORTANT:
- Return VALID JSON ONLY
- Do NOT return explanations
- Do NOT use markdown
- If information is not available, return empty string ""
- For list fields return []

JSON SCHEMA:

{{
    "college_name": "",
    "college_code": "",
    "district": "",
    "website": "",
    "address": "",
    "email": "",
    "phone": "",
    "principal": "",
    "director": "",
    "established_year": "",
    "ownership_type": "",
    "naac_grade": "",
    "nba_status": "",
    "nirf_rank": "",
    "campus_area": "",
    "student_strength": "",
    "faculty_count": "",
    "courses": [],
    "departments": [],
    "placement_percentage": "",
    "highest_package": "",
    "average_package": "",
    "recruiters": [],
    "research_centers": [],
    "patents": "",
    "linkedin": "",
    "facebook": "",
    "instagram": "",
    "youtube": ""
}}

COLLEGE WEBSITE CONTENT:

{content}
"""

        response = groq_completion(
            prompt
        )

        result = extract_json(
            response
        )

        if not result:

            return {}

        result = validate_college_json(
            result
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
    content: str
) -> Dict:

    if not content:

        return (
            DEFAULT_COLLEGE_SCHEMA.copy()
        )

    content = clean_text(
        content
    )

    # -------------------------------------
    # REGEX EXTRACTION
    # -------------------------------------

    regex_data = extract_regex_information(
        content
    )

    # -------------------------------------
    # QUICK PARSER EXTRACTION
    # -------------------------------------

    parser_data = quick_extract(
        content
    )

    # -------------------------------------
    # CHUNK CONTENT
    # -------------------------------------

    chunks = chunk_markdown(
        content
    )

    chunk_results = []

    for chunk in chunks:

        try:

            result = extract_chunk(
                chunk
            )

            if result:

                chunk_results.append(
                    result
                )

        except Exception as e:

            print(
                f"Chunk Error: {e}"
            )

    # -------------------------------------
    # MERGE LLM RESULTS
    # -------------------------------------

    llm_data = merge_json_results(
        chunk_results
    )

    # -------------------------------------
    # FINAL MERGE
    # -------------------------------------

    final_data = (
        DEFAULT_COLLEGE_SCHEMA.copy()
    )

    final_data = merge_results(
        final_data,
        parser_data
    )

    final_data = merge_results(
        final_data,
        regex_data
    )

    final_data = merge_results(
        final_data,
        llm_data
    )

    final_data = validate_college_json(
        final_data
    )

    return final_data

# =====================================================
# BULK EXTRACTION
# =====================================================

def extract_multiple_colleges(
    contents: List[str]
):

    results = []

    total = len(contents)

    for idx, content in enumerate(
        contents
    ):

        try:

            result = extract_college_details(
                content
            )

            results.append(
                result
            )

            print(
                f"Processed {idx+1}/{total}"
            )

        except Exception as e:

            print(
                f"Extraction Error: {e}"
            )

    return results


# =====================================================
# PLACEMENT EXTRACTION
# =====================================================

def extract_placement_info(
    content: str
):

    prompt = f"""
Extract placement information.

Return JSON only.

Schema:

{{
    "placement_percentage":"",
    "highest_package":"",
    "average_package":"",
    "recruiters":[]
}}

CONTENT:

{content}
"""

    response = groq_completion(
        prompt
    )

    return extract_json(
        response
    )


# =====================================================
# ACCREDITATION EXTRACTION
# =====================================================

def extract_accreditation_info(
    content: str
):

    prompt = f"""
Extract accreditation details.

Return JSON only.

Schema:

{{
    "naac_grade":"",
    "nba_status":"",
    "nirf_rank":""
}}

CONTENT:

{content}
"""

    response = groq_completion(
        prompt
    )

    return extract_json(
        response
    )


# =====================================================
# COURSE EXTRACTION
# =====================================================

def extract_course_info(
    content: str
):

    prompt = f"""
Extract courses offered.

Return JSON only.

Schema:

{{
    "courses":[]
}}

CONTENT:

{content}
"""

    response = groq_completion(
        prompt
    )

    return extract_json(
        response
    )


# =====================================================
# RESEARCH EXTRACTION
# =====================================================

def extract_research_info(
    content: str
):

    prompt = f"""
Extract research information.

Return JSON only.

Schema:

{{
    "research_centers":[],
    "patents":"",
    "publications":""
}}

CONTENT:

{content}
"""

    response = groq_completion(
        prompt
    )

    return extract_json(
        response
    )


# =====================================================
# SAVE RESULT
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

def extract_complete_college_profile(
    content: str
):

    result = extract_college_details(
        content
    )

    placement = extract_placement_info(
        content
    )

    accreditation = extract_accreditation_info(
        content
    )

    courses = extract_course_info(
        content
    )

    research = extract_research_info(
        content
    )

    result = merge_results(
        result,
        placement
    )

    result = merge_results(
        result,
        accreditation
    )

    result = merge_results(
        result,
        courses
    )

    result = merge_results(
        result,
        research
    )

    return result

# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    sample_content = """

    RV College of Engineering

    Bengaluru

    NAAC A++

    NBA Accredited

    Email:
    principal@rvce.edu.in

    Phone:
    +91 9876543210

    Highest Package:
    92 LPA

    Courses:

    Computer Science
    Artificial Intelligence
    Mechanical Engineering

    Recruiters:

    Microsoft
    Amazon
    Infosys
    TCS

    """

    result = extract_college_details(
        sample_content
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )
        
