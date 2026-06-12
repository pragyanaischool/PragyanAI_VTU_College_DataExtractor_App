import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


VTU_URL = "https://vtu.ac.in/affiliated-institute/"


def clean_text(text):
    """Clean unwanted spaces and characters"""

    if text is None:
        return ""

    text = str(text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def scrape_vtu_colleges():

    colleges = []

    try:

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/125.0 Safari/537.36"
            )
        }

        response = requests.get(
            VTU_URL,
            headers=headers,
            timeout=60
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        tables = soup.find_all("table")

        if not tables:

            raise Exception(
                "No tables found on VTU page"
            )

        for table in tables:

            rows = table.find_all("tr")

            for row in rows:

                cols = row.find_all(["td", "th"])

                cols = [
                    clean_text(col.get_text())
                    for col in cols
                ]

                if len(cols) < 2:
                    continue

                college = {

                    "college_code":
                        cols[0] if len(cols) > 0 else "",

                    "college_name":
                        cols[1] if len(cols) > 1 else "",

                    "district":
                        cols[2] if len(cols) > 2 else "",

                    "website": "",

                    "email": "",

                    "phone": ""

                }

                if (
                    college["college_name"]
                    and
                    college["college_name"].lower()
                    != "college name"
                ):

                    colleges.append(
                        college
                    )

        df = pd.DataFrame(
            colleges
        )

        df = df.drop_duplicates(
            subset=["college_name"]
        )

        df.reset_index(
            drop=True,
            inplace=True
        )

        return df

    except Exception as e:

        print(
            f"VTU Scraping Error: {e}"
        )

        return pd.DataFrame()
      
