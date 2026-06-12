"""
src/crawler/scrapegraph_engine.py

ScrapeGraphAI Based Website Crawler

Returns:
--------
{
    "url": "",
    "title": "",
    "content": "",
    "success": True,
    "error": ""
}
"""

import requests
from bs4 import BeautifulSoup

# ScrapeGraphAI
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
# BEAUTIFULSOUP FALLBACK
# =====================================================

def scrape_with_bs4(url):

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

                "iframe"

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

        return {

            "url": url,

            "title": title,

            "content": content[:50000],

            "success": True,

            "error": ""

        }

    except Exception as e:

        return {

            "url": url,

            "title": "",

            "content": "",

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
            Phone
            Email
            Courses
            Placements
            Accreditation
            Faculty
            Infrastructure
            Research
            """,

            source=url,

            config=graph_config

        )

        result = scraper.run()

        content = str(result)

        return {

            "url": url,

            "title": "",

            "content": content,

            "success": True,

            "error": ""

        }

    except Exception as e:

        return {

            "url": url,

            "title": "",

            "content": "",

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
                f"{idx+1}/{len(urls)} "
                f"completed"
            )

        except Exception as e:

            results.append({

                "url": url,

                "title": "",

                "content": "",

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

            "status_code":
                response.status_code,

            "available":
                response.status_code == 200

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

    result = scrape_website(
        test_url
    )

    print()

    print("TITLE")

    print(result["title"])

    print()

    print("CONTENT LENGTH")

    print(len(result["content"]))

    print()

    print("SUCCESS")

    print(result["success"])
