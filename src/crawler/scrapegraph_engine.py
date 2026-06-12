# src/crawler/scrapegraph_engine.py

"""
ScrapeGraphAI Based Website Crawler

Returns:
{
    "url": "",
    "title": "",
    "content": "",
    "emails": [],
    "phones": [],
    "links": [],
    "contact_links": [],
    "about_links": [],
    "crawl_time": 0,
    "success": True,
    "error": ""
}
"""

import re
import time
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

try:
    from scrapegraphai.graphs import SmartScraperGraph

    SCRAPEGRAPH_AVAILABLE = True

except Exception:

    SCRAPEGRAPH_AVAILABLE = False


# =====================================================
# CONFIG
# =====================================================

HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
}

TIMEOUT = 30


# =====================================================
# HELPERS
# =====================================================

def clean_text(text):

    return re.sub(
        r"\s+",
        " ",
        text
    ).strip()


def extract_emails(text):

    pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}"
    )

    return list(
        set(
            re.findall(
                pattern,
                text
            )
        )
    )


def extract_phones(text):

    pattern = (
        r"(?:\+91[\-\s]?)?"
        r"[6-9]\d{9}"
    )

    return list(
        set(
            re.findall(
                pattern,
                text
            )
        )
    )


def extract_links(
    soup,
    base_url
):

    links = []

    for tag in soup.find_all(
        "a",
        href=True
    ):

        try:

            links.append(
                urljoin(
                    base_url,
                    tag["href"]
                )
            )

        except Exception:
            pass

    return list(
        set(links)
    )


# =====================================================
# BEAUTIFULSOUP FALLBACK
# =====================================================

def scrape_with_bs4(url):

    start_time = time.time()

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup(
            [
                "script",
                "style",
                "noscript",
                "iframe",
                "svg"
            ]
        ):
            tag.decompose()

        title = ""

        if soup.title:
            title = soup.title.text.strip()

        content = soup.get_text(
            separator=" ",
            strip=True
        )

        content = clean_text(
            content
        )

        emails = extract_emails(
            content
        )

        phones = extract_phones(
            content
        )

        links = extract_links(
            soup,
            url
        )

        contact_links = [

            link

            for link in links

            if any(

                keyword in link.lower()

                for keyword in [

                    "contact",
                    "contact-us",
                    "reach-us",
                    "get-in-touch"

                ]

            )

        ]

        about_links = [

            link

            for link in links

            if any(

                keyword in link.lower()

                for keyword in [

                    "about",
                    "about-us",
                    "profile",
                    "institution"

                ]

            )

        ]

        crawl_time = round(
            time.time() - start_time,
            2
        )

        return {

            "url": url,

            "title": title,

            "content": content[:50000],

            "emails": emails,

            "phones": phones,

            "links": links,

            "contact_links": contact_links,

            "about_links": about_links,

            "crawl_time": crawl_time,

            "success": True,

            "error": ""

        }

    except Exception as e:

        return {

            "url": url,

            "title": "",

            "content": "",

            "emails": [],

            "phones": [],

            "links": [],

            "contact_links": [],

            "about_links": [],

            "crawl_time": 0,

            "success": False,

            "error": str(e)

        }


# =====================================================
# SCRAPEGRAPHAI
# =====================================================

def scrape_with_scrapegraph(
    url,
    groq_api_key
):

    try:

        start_time = time.time()

        graph_config = {

            "llm": {

                "api_key": groq_api_key,

                "model": "groq/llama-3.3-70b-versatile"

            }

        }

        scraper = SmartScraperGraph(

            prompt="""
            Extract all useful information
            from this college website.

            Include:

            College Name
            Address
            Phone Numbers
            Email Addresses
            Principal
            Director
            Chairman
            Dean
            Courses Offered
            Departments
            Admission Information
            Placements
            Recruiters
            Highest Package
            Average Package
            Infrastructure
            Accreditation
            NAAC Grade
            NBA Status
            NIRF Ranking
            Research Centers
            Faculty Information
            Hostel Information
            Contact Information
            Social Media Links
            Important Website Links

            Return complete information.
            """,

            source=url,

            config=graph_config

        )

        result = scraper.run()

        content = str(result)

        crawl_time = round(
            time.time() - start_time,
            2
        )

        emails = extract_emails(
            content
        )

        phones = extract_phones(
            content
        )

        return {

            "url": url,

            "title": "",

            "content": content,

            "emails": emails,

            "phones": phones,

            "links": [],

            "contact_links": [],

            "about_links": [],

            "crawl_time": crawl_time,

            "success": True,

            "error": ""

        }

    except Exception as e:

        return {

            "url": url,

            "title": "",

            "content": "",

            "emails": [],

            "phones": [],

            "links": [],

            "contact_links": [],

            "about_links": [],

            "crawl_time": 0,

            "success": False,

            "error": str(e)

        }


# =====================================================
# MAIN SCRAPER
# =====================================================

def scrape_website(
    url,
    groq_api_key=None
):

    if SCRAPEGRAPH_AVAILABLE and groq_api_key:

        result = scrape_with_scrapegraph(
            url,
            groq_api_key
        )

        if result["success"]:
            return result

    return scrape_with_bs4(url)


# =====================================================
# BULK SCRAPER
# =====================================================

def scrape_multiple_websites(
    urls,
    groq_api_key=None
):

    results = []

    for idx, url in enumerate(urls):

        try:

            result = scrape_website(
                url,
                groq_api_key
            )

            results.append(result)

            print(
                f"{idx + 1}/{len(urls)} completed"
            )

        except Exception as e:

            results.append({

                "url": url,

                "title": "",

                "content": "",

                "emails": [],

                "phones": [],

                "links": [],

                "contact_links": [],

                "about_links": [],

                "crawl_time": 0,

                "success": False,

                "error": str(e)

            })

    return results


# =====================================================
# GET TITLE ONLY
# =====================================================

def get_website_title(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        if soup.title:
            return soup.title.text.strip()

        return ""

    except Exception:

        return ""


# =====================================================
# WEBSITE HEALTH
# =====================================================

def check_website(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        return {

            "url": url,

            "status_code": response.status_code,

            "available": response.status_code == 200

        }

    except Exception as e:

        return {

            "url": url,

            "status_code": 0,

            "available": False,

            "error": str(e)

        }


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    test_url = "https://rvce.edu.in"

    result = scrape_website(test_url)

    print("\nSUCCESS")
    print(result["success"])

    print("\nTITLE")
    print(result["title"])

    print("\nEMAILS")
    print(result.get("emails", []))

    print("\nPHONES")
    print(result.get("phones", []))

    print("\nLINKS")
    print(len(result.get("links", [])))

    print("\nCONTENT LENGTH")
    print(len(result.get("content", "")))
    
