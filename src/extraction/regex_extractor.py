"""
src/extraction/regex_extractor.py

Regex Based Information Extraction

Used Before GROQ Processing
"""

import re

from src.utils.config import (
    EMAIL_REGEX,
    PHONE_REGEX,
    URL_REGEX,
    SOCIAL_DOMAINS
)

# =====================================================
# EMAIL EXTRACTION
# =====================================================

def extract_emails(text):

    if not text:
        return []

    emails = re.findall(
        EMAIL_REGEX,
        str(text),
        flags=re.IGNORECASE
    )

    return sorted(
        list(set(emails))
    )


# =====================================================
# PHONE EXTRACTION
# =====================================================

def extract_phones(text):

    if not text:
        return []

    phones = re.findall(
        PHONE_REGEX,
        str(text)
    )

    cleaned = []

    for phone in phones:

        phone = re.sub(
            r"\D",
            "",
            phone
        )

        if len(phone) >= 10:

            cleaned.append(phone)

    return sorted(
        list(set(cleaned))
    )


# =====================================================
# URL EXTRACTION
# =====================================================

def extract_urls(text):

    if not text:
        return []

    urls = re.findall(
        URL_REGEX,
        str(text)
    )

    return sorted(
        list(set(urls))
    )


# =====================================================
# SOCIAL MEDIA LINKS
# =====================================================

def extract_social_links(text):

    urls = extract_urls(text)

    social = {

        "linkedin": "",

        "facebook": "",

        "instagram": "",

        "youtube": "",

        "twitter": ""

    }

    for url in urls:

        lower_url = url.lower()

        if SOCIAL_DOMAINS["linkedin"] in lower_url:

            social["linkedin"] = url

        elif SOCIAL_DOMAINS["facebook"] in lower_url:

            social["facebook"] = url

        elif SOCIAL_DOMAINS["instagram"] in lower_url:

            social["instagram"] = url

        elif SOCIAL_DOMAINS["youtube"] in lower_url:

            social["youtube"] = url

        elif SOCIAL_DOMAINS["twitter"] in lower_url:

            social["twitter"] = url

    return social


# =====================================================
# NAAC GRADE EXTRACTION
# =====================================================

def extract_naac_grade(text):

    if not text:
        return ""

    patterns = [

        r'NAAC\s*Grade\s*[:\-]?\s*(A\+\+)',

        r'NAAC\s*Grade\s*[:\-]?\s*(A\+)',

        r'NAAC\s*Grade\s*[:\-]?\s*(A)',

        r'NAAC\s*Accredited\s*with\s*(A\+\+)',

        r'NAAC\s*Accredited\s*with\s*(A\+)',

        r'NAAC\s*Accredited\s*with\s*(A)',

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1)

    return ""


# =====================================================
# NBA STATUS
# =====================================================

def extract_nba_status(text):

    if not text:
        return ""

    if re.search(
        r"\bNBA\b",
        text,
        re.IGNORECASE
    ):

        return "Yes"

    return ""


# =====================================================
# NIRF RANKING
# =====================================================

def extract_nirf_rank(text):

    patterns = [

        r'NIRF\s*Rank\s*[:\-]?\s*(\d+)',

        r'NIRF\s*Ranking\s*[:\-]?\s*(\d+)',

        r'Ranked\s*(\d+)\s*in\s*NIRF'

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1)

    return ""


# =====================================================
# PLACEMENT PACKAGE
# =====================================================

def extract_highest_package(text):

    patterns = [

        r'Highest\s*Package\s*[:\-]?\s*(\d+\.?\d*)\s*LPA',

        r'Highest\s*Salary\s*[:\-]?\s*(\d+\.?\d*)\s*LPA',

        r'Package\s*Up\s*To\s*(\d+\.?\d*)\s*LPA'

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1)

    return ""


# =====================================================
# AVERAGE PACKAGE
# =====================================================

def extract_average_package(text):

    patterns = [

        r'Average\s*Package\s*[:\-]?\s*(\d+\.?\d*)\s*LPA',

        r'Average\s*Salary\s*[:\-]?\s*(\d+\.?\d*)\s*LPA'

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1)

    return ""


# =====================================================
# COLLEGE CODE
# =====================================================

def extract_college_code(text):

    patterns = [

        r'VTU\s*Code\s*[:\-]?\s*([A-Z0-9]+)',

        r'College\s*Code\s*[:\-]?\s*([A-Z0-9]+)',

        r'Institute\s*Code\s*[:\-]?\s*([A-Z0-9]+)'

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1)

    return ""


# =====================================================
# RECRUITERS
# =====================================================

def extract_recruiters(text):

    common_companies = [

        "TCS",
        "Infosys",
        "Wipro",
        "Accenture",
        "Cognizant",
        "Capgemini",
        "IBM",
        "Amazon",
        "Google",
        "Microsoft",
        "Oracle",
        "Deloitte",
        "Bosch",
        "HCL",
        "Tech Mahindra"
    ]

    recruiters = []

    text_lower = text.lower()

    for company in common_companies:

        if company.lower() in text_lower:

            recruiters.append(company)

    return sorted(
        list(set(recruiters))
    )


# =====================================================
# MASTER CONTACT EXTRACTOR
# =====================================================

def extract_contacts(text):

    emails = extract_emails(text)

    phones = extract_phones(text)

    urls = extract_urls(text)

    social = extract_social_links(text)

    return {

        "email":
            emails[0]
            if emails else "",

        "phone":
            phones[0]
            if phones else "",

        "all_emails":
            emails,

        "all_phones":
            phones,

        "urls":
            urls,

        **social

    }


# =====================================================
# COMPLETE REGEX EXTRACTION
# =====================================================

def extract_regex_information(text):

    contacts = extract_contacts(text)

    return {

        **contacts,

        "naac_grade":
            extract_naac_grade(text),

        "nba_status":
            extract_nba_status(text),

        "nirf_rank":
            extract_nirf_rank(text),

        "highest_package":
            extract_highest_package(text),

        "average_package":
            extract_average_package(text),

        "college_code":
            extract_college_code(text),

        "recruiters":
            extract_recruiters(text)

    }


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    sample = """

    RV College of Engineering

    Email: info@rvce.edu.in

    Phone: +91 9876543210

    Website:
    https://rvce.edu.in

    NAAC Grade A++

    NBA Accredited

    NIRF Rank 99

    Highest Package 92 LPA

    Recruiters:
    TCS Infosys Microsoft Amazon

    """

    result = extract_regex_information(
        sample
    )

    print(result)
