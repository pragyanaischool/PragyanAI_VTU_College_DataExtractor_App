"""
src/llm/prompts.py

Prompt Templates for VTU College Intelligence Platform
"""

# =====================================================
# MAIN COLLEGE EXTRACTION PROMPT
# =====================================================

COLLEGE_EXTRACTION_PROMPT = """
You are an expert Educational Intelligence Extraction System.

Your task is to extract structured information from engineering college websites.

IMPORTANT RULES:

1. Return ONLY valid JSON.
2. No explanation.
3. No markdown.
4. No code block.
5. Do not invent information.
6. Missing values should be empty string "".
7. Lists should be [].
8. Extract only information present in the content.

Return JSON in this schema:

{
    "college_name":"",
    "college_code":"",
    "district":"",
    "website":"",
    "address":"",
    "email":"",
    "phone":"",
    "principal":"",
    "director":"",
    "established_year":"",
    "ownership_type":"",
    "naac_grade":"",
    "nba_status":"",
    "nirf_rank":"",
    "campus_area":"",
    "student_strength":"",
    "faculty_count":"",
    "courses":[],
    "departments":[],
    "placement_percentage":"",
    "highest_package":"",
    "average_package":"",
    "recruiters":[],
    "research_centers":[],
    "patents":"",
    "linkedin":"",
    "facebook":"",
    "instagram":"",
    "youtube":""
}

Extract as much information as possible.
"""

# =====================================================
# CONTACT INFORMATION PROMPT
# =====================================================

CONTACT_EXTRACTION_PROMPT = """
Extract contact information.

Return ONLY JSON.

Schema:

{
    "college_name":"",
    "website":"",
    "address":"",
    "email":"",
    "phone":"",
    "linkedin":"",
    "facebook":"",
    "instagram":"",
    "youtube":""
}
"""

# =====================================================
# PLACEMENT EXTRACTION PROMPT
# =====================================================

PLACEMENT_EXTRACTION_PROMPT = """
You are a placement data extraction expert.

Extract placement information.

Return ONLY JSON.

Schema:

{
    "placement_percentage":"",
    "highest_package":"",
    "average_package":"",
    "median_package":"",
    "total_offers":"",
    "recruiters":[]
}

Rules:
- Recruiters must be a list.
- No explanation.
- No markdown.
"""
# =====================================================
# COURSE EXTRACTION PROMPT
# =====================================================

COURSE_EXTRACTION_PROMPT = """
Extract academic programs.

Return ONLY JSON.

Schema:

{
    "courses":[],
    "departments":[]
}

Include:

- BE Programs
- BTech Programs
- MTech Programs
- MBA
- MCA
- PhD Programs
"""
# =====================================================
# ACCREDITATION EXTRACTION PROMPT
# =====================================================

ACCREDITATION_EXTRACTION_PROMPT = """
Extract accreditation and ranking information.

Return ONLY JSON.

Schema:

{
    "naac_grade":"",
    "nba_status":"",
    "nirf_rank":"",
    "autonomous_status":"",
    "ugc_status":""
}
"""

# =====================================================
# FACULTY EXTRACTION PROMPT
# =====================================================

FACULTY_EXTRACTION_PROMPT = """
Extract faculty and leadership information.

Return ONLY JSON.

Schema:

{
    "principal":"",
    "director":"",
    "faculty_count":"",
    "hods":[]
}
"""

# =====================================================
# RESEARCH EXTRACTION PROMPT
# =====================================================

RESEARCH_EXTRACTION_PROMPT = """
Extract research information.

Return ONLY JSON.

Schema:

{
    "research_centers":[],
    "patents":"",
    "publications":"",
    "funded_projects":""
}
"""

# =====================================================
# INFRASTRUCTURE EXTRACTION PROMPT
# =====================================================

INFRASTRUCTURE_EXTRACTION_PROMPT = """
Extract infrastructure information.

Return ONLY JSON.

Schema:

{
    "campus_area":"",
    "hostel_available":"",
    "library":"",
    "sports_facilities":"",
    "labs":[]
}
"""

# =====================================================
# ADMISSION EXTRACTION PROMPT
# =====================================================

ADMISSION_EXTRACTION_PROMPT = """
Extract admission information.

Return ONLY JSON.

Schema:

{
    "admission_process":"",
    "entrance_exams":[],
    "eligibility":""
}
"""

# =====================================================
# COLLEGE PROFILE SUMMARY PROMPT
# =====================================================

COLLEGE_SUMMARY_PROMPT = """
Create a structured summary.

Return ONLY JSON.

Schema:

{
    "college_type":"",
    "strengths":[],
    "specializations":[],
    "industry_collaborations":[],
    "research_focus":[],
    "placement_strength":""
}
"""

# =====================================================
# VTU ANALYTICS PROMPT
# =====================================================

VTU_ANALYTICS_PROMPT = """
Analyze the engineering college profile.

Return ONLY JSON.

Schema:

{
    "overall_rating":"",
    "academic_strength":"",
    "placement_strength":"",
    "research_strength":"",
    "industry_connect":"",
    "student_opportunities":"",
    "recommendation":""
}
"""

# =====================================================
# WEBSITE CLASSIFICATION PROMPT
# =====================================================

WEBSITE_CLASSIFICATION_PROMPT = """
Classify webpage content.

Return ONLY JSON.

Schema:

{
    "page_type":"",
    "confidence":""
}

Possible page types:

- Home
- About
- Admissions
- Placements
- Departments
- Faculty
- Research
- Contact
- Rankings
- Accreditation
- Infrastructure
- Other
"""
