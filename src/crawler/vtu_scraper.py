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
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}


def clean_text(text):

    if not text:
        return ""

    text = re.sub(
        r"\s+",
        " ",
        str(text)
    )

    return text.strip()


def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(
        pattern,
        text
    )

    return match.group(0) if match else ""


def extract_phone(text):

    pattern = r"(\+91[\-\s]?)?[6-9]\d{9}"

    match = re.search(
        pattern,
        text
    )

    return match.group(0) if match else ""


def extract_website(text):

    pattern = r"(https?://[^\s]+|www\.[^\s]+)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    return match.group(0) if match else ""


def scrape_vtu_colleges():

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

        text = soup.get_text(
            separator="\n"
        )

        lines = text.split("\n")

        for line in lines:

            line = clean_text(line)

            if len(line) < 15:
                continue

            keywords = [

                "college",
                "engineering",
                "technology",
                "institute"

            ]

            if not any(
                word in line.lower()
                for word in keywords
            ):
                continue

            colleges.append({

                "college_code": "",

                "college_name": line,

                "district": "",

                "website": extract_website(
                    line
                ),

                "email": extract_email(
                    line
                ),

                "phone": extract_phone(
                    line
                )

            })

        # Remove duplicates

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

    except Exception as e:

        print(
            f"VTU Scraper Error: {e}"
        )

        return []


def get_colleges_dataframe():

    colleges = scrape_vtu_colleges()

    return pd.DataFrame(
        colleges
    )


def save_colleges_csv(
    filepath
):

    df = get_colleges_dataframe()

    df.to_csv(
        filepath,
        index=False
    )

    return filepath


if __name__ == "__main__":

    colleges = scrape_vtu_colleges()

    print(
        f"Found {len(colleges)} colleges"
    )

    print(
        colleges[:5]
    )
    
