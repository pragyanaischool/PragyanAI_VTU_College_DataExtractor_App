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
    if not text:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(text)
    ).strip()


def parse_college_record(text):

    record = {
        "college_code": "",
        "college_name": "",
        "std_code": "",
        "phone": "",
        "rural_urban": "",
        "district": "",
        "website": "",
        "email": ""
    }

    code_match = re.search(
        r"Code:\s*([A-Z0-9]+)",
        text,
        re.IGNORECASE
    )

    if code_match:
        record["college_code"] = code_match.group(1)

    college_match = re.search(
        r"College:\s*(.*?)\s*STD\s*Code:",
        text,
        re.IGNORECASE
    )

    if college_match:
        record["college_name"] = college_match.group(1).strip()

    std_match = re.search(
        r"STD\s*Code:\s*([0-9]+)",
        text,
        re.IGNORECASE
    )

    if std_match:
        record["std_code"] = std_match.group(1)

    phone_match = re.search(
        r"Phone:\s*([0-9]+)",
        text,
        re.IGNORECASE
    )

    if phone_match:
        record["phone"] = phone_match.group(1)

    rural_match = re.search(
        r"Rural/Urban:\s*(Rural|Urban)",
        text,
        re.IGNORECASE
    )

    if rural_match:
        record["rural_urban"] = rural_match.group(1)

    return record


def scrape_vtu_colleges():

    colleges = []

    try:

        response = requests.get(
            VTU_URL,
            headers=HEADERS,
            timeout=60
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        page_text = clean_text(
            soup.get_text(" ")
        )

        pattern = re.compile(
            r"\d+\s+Code:\s*[A-Z0-9]+.*?Rural/Urban:\s*(?:Rural|Urban)",
            re.IGNORECASE
        )

        matches = pattern.findall(page_text)

        for match in matches:

            record = parse_college_record(match)

            if (
                record["college_code"]
                and record["college_name"]
            ):
                colleges.append(record)

        unique_colleges = {}

        for college in colleges:

            code = college["college_code"]

            if code:
                unique_colleges[code] = college

        colleges = list(unique_colleges.values())

        colleges.sort(
            key=lambda x: x["college_name"]
        )

        return colleges

    except Exception as e:

        print(
            f"VTU Scraper Error: {e}"
        )

        return []


def get_colleges_dataframe():

    return pd.DataFrame(
        scrape_vtu_colleges()
    )


def search_colleges(keyword):

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

    for college in colleges[:10]:
        print(college)

    pd.DataFrame(
        colleges
    ).to_csv(
        "vtu_colleges.csv",
        index=False
    )
