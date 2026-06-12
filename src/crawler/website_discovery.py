"""
website_discovery.py

Discover official college websites.

Priority:
1. Existing website from VTU
2. DuckDuckGo Search
3. URL Validation
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.parse import urlparse


HEADERS = {
    "User-Agent":
    (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}


# ---------------------------------------------------
# URL VALIDATION
# ---------------------------------------------------

def is_valid_url(url: str) -> bool:

    try:

        parsed = urlparse(url)

        return bool(
            parsed.scheme
        ) and bool(
            parsed.netloc
        )

    except Exception:

        return False


# ---------------------------------------------------
# CLEAN URL
# ---------------------------------------------------

def clean_url(url: str) -> str:

    if not url:

        return ""

    url = url.strip()

    if url.startswith("//"):

        url = "https:" + url

    if (
        not url.startswith("http://")
        and
        not url.startswith("https://")
    ):

        url = "https://" + url

    return url


# ---------------------------------------------------
# DUCKDUCKGO SEARCH
# ---------------------------------------------------

def search_duckduckgo(
    college_name: str
) -> str:

    try:

        query = quote(
            f"{college_name} official website"
        )

        url = (
            "https://duckduckgo.com/html/"
            f"?q={query}"
        )

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        results = soup.select(
            ".result__url"
        )

        for result in results:

            website = (
                result.get_text()
                .strip()
            )

            website = clean_url(
                website
            )

            if is_valid_url(
                website
            ):

                return website

        return ""

    except Exception as e:

        print(
            f"Search Error: {e}"
        )

        return ""


# ---------------------------------------------------
# WEBSITE VALIDATION
# ---------------------------------------------------

def validate_website(
    website: str
) -> bool:

    try:

        response = requests.get(
            website,
            headers=HEADERS,
            timeout=20
        )

        return (
            response.status_code
            == 200
        )

    except Exception:

        return False


# ---------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------

def discover_website(
    college_name: str
) -> str:

    website = search_duckduckgo(
        college_name
    )

    if website:

        if validate_website(
            website
        ):

            return website

    return ""


# ---------------------------------------------------
# BULK DISCOVERY
# ---------------------------------------------------

def discover_websites_bulk(
    df: pd.DataFrame
) -> pd.DataFrame:

    websites = []

    for _, row in df.iterrows():

        college_name = row.get(
            "college_name",
            ""
        )

        website = discover_website(
            college_name
        )

        websites.append(
            website
        )

    df["website"] = websites

    return df


# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    website = discover_website(
        "R V College of Engineering"
    )

    print(website)
