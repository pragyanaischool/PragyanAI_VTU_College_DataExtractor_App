"""
src/crawler/vtu_scraper.py

VTU Affiliated Colleges Scraper
Using Selenium + Chrome

Author: PragyanAI
"""

import re
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

VTU_URL = "https://vtu.ac.in/affiliated-institute/"


# =====================================================
# DRIVER
# =====================================================

def create_driver():

    options = webdriver.ChromeOptions()

    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=options
    )

    driver.maximize_window()

    return driver


# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =====================================================
# EMAIL
# =====================================================

def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    return match.group(0) if match else ""


# =====================================================
# PHONE
# =====================================================

def extract_phone(text):

    pattern = r"(\+91[\-\s]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    return match.group(0) if match else ""


# =====================================================
# WEBSITE
# =====================================================

def extract_website(text):

    pattern = r"(https?://[^\s]+|www\.[^\s]+)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    return match.group(0) if match else ""


# =====================================================
# SCRAPE VTU
# =====================================================

def scrape_vtu_colleges():

    driver = create_driver()

    colleges = []

    try:

        print("Opening VTU Website...")

        driver.get(VTU_URL)

        time.sleep(5)

        body_text = driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        lines = body_text.split("\n")

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

            college = {

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

            }

            colleges.append(
                college
            )

    except Exception as e:

        print(
            f"Scraping Error: {e}"
        )

    finally:

        driver.quit()

    # ----------------------------------
    # Remove Duplicates
    # ----------------------------------

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
# SEARCH COLLEGE
# =====================================================

def search_college(
    keyword
):

    df = get_colleges_dataframe()

    if df.empty:

        return df

    keyword = keyword.lower()

    return df[
        df["college_name"]
        .str.lower()
        .str.contains(
            keyword,
            na=False
        )
    ]


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print("\nCollecting VTU Colleges...\n")

    colleges = scrape_vtu_colleges()

    print(
        f"Found: {len(colleges)} Colleges"
    )

    df = pd.DataFrame(
        colleges
    )

    print(df.head())

    df.to_csv(
        "vtu_colleges.csv",
        index=False
    )

    print(
        "\nSaved: vtu_colleges.csv"
    )
    
