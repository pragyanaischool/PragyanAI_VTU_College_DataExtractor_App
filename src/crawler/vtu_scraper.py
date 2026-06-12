# src/crawler/vtu_scraper.py

import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

VTU_URL = "https://vtu.ac.in/affiliated-institute/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}


def clean_text(text):
    """
    Clean extracted text.
    """

    if not text:
        return ""

    text = str(text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def is_college_name(text):
    """
    Check if text looks like a college name.
    """

    if not text:
        return False

    keywords = [

        "college",

        "engineering",

        "technology",

        "institute",

        "polytechnic"

    ]

    text = text.lower()

    return any(
        keyword in text
        for keyword in keywords
    )


def extract_email(text):
    """
    Extract email address.
    """

    pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}"
    )

    match = re.search(
        pattern,
        text
    )

    if match:
        return match.group(0)

    return ""


def extract_phone(text):
    """
    Extract phone number.
    """

    pattern = (
        r"(\+91[\-\s]?)?"
        r"[6-9]\d{9}"
    )

    match = re.search(
        pattern,
        text
    )

    if match:
        return match.group(0)

    return ""


def extract_website(text):
    """
    Extract website URL.
    """

    pattern = (
        r"(https?://[^\s]+|www\.[^\s]+)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(0)

    return ""


def scrape_vtu_colleges():
    """
    Scrape VTU affiliated colleges.

    Returns:
        list
    """

    colleges = []

    try:

        response = requests.get(
            VTU_URL,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        candidates = set()

        # ------------------------------
        # Links
        # ------------------------------

        for tag in soup.find_all("a"):

            text = clean_text(
                tag.get_text()
            )

            if len(text) < 5:
                continue

            if is_college_name(text):
                candidates.add(text)

        # ------------------------------
        # Headings
        # ------------------------------

        for tag in soup.find_all(
            [
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "p",
                "li",
                "div"
            ]
        ):

            text = clean_text(
                tag.get_text()
            )

            if len(text) < 5:
                continue

            if is_college_name(text):
                candidates.add(text)

        # ------------------------------
        # Create Records
        # ------------------------------

        for college_name in sorted(candidates):

            colleges.append({

                "college_code": "",

                "college_name": college_name,

                "district": "",

                "website": "",

                "email": "",

                "phone": ""

            })

        return colleges

    except Exception as e:

        print(
            f"VTU Scraper Error: {e}"
        )

        return []


def get_colleges_dataframe():
    """
    Return colleges as dataframe.
    """

    colleges = scrape_vtu_colleges()

    return pd.DataFrame(
        colleges
    )


def search_colleges(keyword):
    """
    Search colleges by keyword.
    """

    df = get_colleges_dataframe()

    if df.empty:
        return df

    return df[
        df["college_name"].str.contains(
            keyword,
            case=False,
            na=False
        )
    ]


def save_colleges_csv(filepath):
    """
    Save colleges to CSV.
    """

    df = get_colleges_dataframe()

    df.to_csv(
        filepath,
        index=False
    )

    return filepath


if __name__ == "__main__":

    colleges = scrape_vtu_colleges()

    print(
        f"Total Colleges Found: {len(colleges)}"
    )

    if colleges:

        print("\nFirst 10 Colleges:\n")

        for college in colleges[:10]:

            print(college)

    df = pd.DataFrame(
        colleges
    )

    df.to_csv(
        "vtu_colleges.csv",
        index=False
    )

    print(
        "\nSaved: vtu_colleges.csv"
    )
    
