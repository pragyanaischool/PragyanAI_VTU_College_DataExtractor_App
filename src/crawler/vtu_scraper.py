"""
src/crawler/vtu_scraper.py

VTU Affiliated Colleges Scraper
"""

import re
import requests
import pandas as pd

from bs4 import BeautifulSoup

VTU_URL = "https://vtu.ac.in/affiliated-institute/"

HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# =====================================================
# DOWNLOAD PAGE
# =====================================================

def get_vtu_page():

    try:

        response = requests.get(
            VTU_URL,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        return response.text

    except Exception as e:

        print(
            f"VTU Download Error: {e}"
        )

        return ""


# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    if not text:
        return ""

    text = re.sub(
        r"\s+",
        " ",
        str(text)
    )

    return text.strip()


# =====================================================
# EXTRACT WEBSITE
# =====================================================

def extract_website(text):

    pattern = r"(https?://[^\s]+|www\.[^\s]+)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    return (
        match.group(0)
        if match
        else ""
    )


# =====================================================
# EXTRACT EMAIL
# =====================================================

def extract_email(text):

    pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}"
    )

    match = re.search(
        pattern,
        text
    )

    return (
        match.group(0)
        if match
        else ""
    )


# =====================================================
# EXTRACT PHONE
# =====================================================

def extract_phone(text):

    pattern = (
        r"(\+91[\-\s]?)?"
        r"[6-9]\d{9}"
    )

    match = re.search(
        pattern,
        text
    )

    return (
        match.group(0)
        if match
        else ""
    )


# =====================================================
# SCRAPE COLLEGES
# =====================================================

def scrape_vtu_colleges():

    html = get_vtu_page()

    if not html:

        return []

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    colleges = []

    # -------------------------------------------------
    # Get all text blocks
    # -------------------------------------------------

    blocks = soup.find_all(
        ["p", "div", "li"]
    )

    for block in blocks:

        text = clean_text(
            block.get_text(
                " ",
                strip=True
            )
        )

        if len(text) < 25:
            continue

        # engineering institutes
        keywords = [

            "engineering",

            "technology",

            "institute",

            "college"

        ]

        if not any(
            k.lower() in text.lower()
            for k in keywords
        ):
            continue

        website = extract_website(
            text
        )

        email = extract_email(
            text
        )

        phone = extract_phone(
            text
        )

        college = {

            "college_code": "",

            "college_name":
                text[:150],

            "district": "",

            "website":
                website,

            "email":
                email,

            "phone":
                phone

        }

        colleges.append(
            college
        )

    # -------------------------------------------------
    # Remove duplicates
    # -------------------------------------------------

    unique = []

    seen = set()

    for college in colleges:

        name = college[
            "college_name"
        ]

        if name in seen:
            continue

        seen.add(name)

        unique.append(
            college
        )

    return unique


# =====================================================
# DATAFRAME
# =====================================================

def get_colleges_dataframe():

    colleges = scrape_vtu_colleges()

    return pd.DataFrame(
        colleges
    )


# =====================================================
# SAVE CSV
# =====================================================

def save_colleges_csv(
    filepath
):

    df = get_colleges_dataframe()

    df.to_csv(
        filepath,
        index=False
    )

    return filepath


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    colleges = scrape_vtu_colleges()

    print()

    print(
        f"Colleges Found: {len(colleges)}"
    )

    print()

    if colleges:

        print(
            colleges[:5]
        )

    df = pd.DataFrame(
        colleges
    )

    print()

    print(
        df.head()
    )
