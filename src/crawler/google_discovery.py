# src/crawler/google_discovery.py

"""
Google / DuckDuckGo Website Discovery

Find official college websites from college names.
"""

from urllib.parse import urlparse

from duckduckgo_search import DDGS


# ==========================================================
# FILTERS
# ==========================================================

BLOCKED_DOMAINS = [

    "wikipedia.org",

    "shiksha.com",

    "careers360.com",

    "collegedunia.com",

    "collegedekho.com",

    "getmyuni.com",

    "indiaeducation.net",

    "educationdunia.com",

    "universitykart.com",

    "justdial.com",

    "facebook.com",

    "linkedin.com",

    "instagram.com",

    "youtube.com",

    "x.com",

    "twitter.com"

]


# ==========================================================
# DOMAIN VALIDATION
# ==========================================================

def is_valid_website(url):
    """
    Check whether URL is a valid college website.
    """

    if not url:
        return False

    url = url.lower()

    for blocked in BLOCKED_DOMAINS:

        if blocked in url:
            return False

    return True


# ==========================================================
# CLEAN URL
# ==========================================================

def clean_url(url):
    """
    Normalize URL.
    """

    if not url:
        return ""

    url = url.strip()

    if not url.startswith(
        (
            "http://",
            "https://"
        )
    ):
        url = f"https://{url}"

    return url


# ==========================================================
# DOMAIN SCORE
# ==========================================================

def score_website(
    url,
    college_name
):
    """
    Score candidate websites.
    """

    score = 0

    try:

        parsed = urlparse(url)

        domain = parsed.netloc.lower()

        college_words = [

            word.lower()

            for word in college_name.split()

            if len(word) > 3

        ]

        for word in college_words:

            if word in domain:
                score += 10

        if ".edu" in domain:
            score += 20

        if ".ac.in" in domain:
            score += 25

        if ".edu.in" in domain:
            score += 25

        if ".org" in domain:
            score += 5

        if ".com" in domain:
            score += 2

    except Exception:

        pass

    return score


# ==========================================================
# SEARCH WEBSITE
# ==========================================================

def find_official_website(
    college_name,
    max_results=10
):
    """
    Find official website for a college.
    """

    try:

        query = (
            f"{college_name} official website"
        )

        candidates = []

        with DDGS() as ddgs:

            results = list(

                ddgs.text(
                    query,
                    max_results=max_results
                )

            )

        for result in results:

            url = result.get(
                "href",
                ""
            )

            url = clean_url(url)

            if not is_valid_website(url):
                continue

            score = score_website(
                url,
                college_name
            )

            candidates.append(

                {
                    "url": url,
                    "score": score
                }

            )

        if not candidates:
            return ""

        candidates = sorted(

            candidates,

            key=lambda x:
            x["score"],

            reverse=True

        )

        return candidates[0]["url"]

    except Exception as e:

        print(
            f"Website Discovery Error: {e}"
        )

        return ""


# ==========================================================
# BULK SEARCH
# ==========================================================

def find_websites_bulk(
    college_names
):
    """
    Find websites for multiple colleges.
    """

    results = []

    for college in college_names:

        website = find_official_website(
            college
        )

        results.append(

            {
                "college_name":
                college,

                "website":
                website
            }

        )

    return results


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    colleges = [

        "R V College of Engineering",

        "BMS College of Engineering",

        "PES University",

        "MS Ramaiah Institute of Technology"

    ]

    for college in colleges:

        website = find_official_website(
            college
        )

        print()

        print(
            f"College : {college}"
        )

        print(
            f"Website : {website}"
        )
