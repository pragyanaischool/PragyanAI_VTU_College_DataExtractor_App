"""
crawl4ai_engine.py

VTU College Intelligence Platform

Features:
---------
1. Crawl Single Website
2. Crawl Multiple Websites
3. Extract Markdown
4. Extract Metadata
5. Extract Internal Links
6. Streamlit Compatible
7. Async Processing
"""

import asyncio
import pandas as pd
from datetime import datetime

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode
)

# =====================================================
# CONFIGURATION
# =====================================================

BROWSER_CONFIG = BrowserConfig(
    headless=True,
    verbose=False
)

CRAWL_CONFIG = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    word_count_threshold=10,
    remove_overlay_elements=True,
    scan_full_page=True,
    page_timeout=60000
)

# =====================================================
# SINGLE WEBSITE CRAWL
# =====================================================

async def async_crawl_website(url: str):

    result_data = {
        "url": url,
        "success": False,
        "title": "",
        "markdown": "",
        "links": [],
        "metadata": {},
        "error": "",
        "crawl_time": None
    }

    start_time = datetime.now()

    try:

        async with AsyncWebCrawler(
            config=BROWSER_CONFIG
        ) as crawler:

            result = await crawler.arun(
                url=url,
                config=CRAWL_CONFIG
            )

            if not result.success:

                result_data["error"] = (
                    getattr(
                        result,
                        "error_message",
                        "Unknown Error"
                    )
                )

                return result_data

            # ------------------------------------------------
            # MARKDOWN
            # ------------------------------------------------

            try:

                markdown = (
                    result.markdown.raw_markdown
                )

            except Exception:

                markdown = str(
                    result.markdown
                )

            # ------------------------------------------------
            # TITLE
            # ------------------------------------------------

            title = ""

            try:

                title = result.metadata.get(
                    "title",
                    ""
                )

            except Exception:
                pass

            # ------------------------------------------------
            # LINKS
            # ------------------------------------------------

            links = []

            try:

                if hasattr(
                    result,
                    "links"
                ):

                    internal_links = (
                        result.links.get(
                            "internal",
                            []
                        )
                    )

                    links = [

                        link.get("href")

                        for link in internal_links

                        if isinstance(
                            link,
                            dict
                        )

                    ]

            except Exception:
                pass

            # ------------------------------------------------
            # METADATA
            # ------------------------------------------------

            metadata = {}

            try:

                metadata = result.metadata

            except Exception:
                pass

            result_data.update({

                "success": True,

                "title": title,

                "markdown": markdown,

                "links": links,

                "metadata": metadata,

                "crawl_time": (
                    datetime.now()
                    - start_time
                ).total_seconds()

            })

            return result_data

    except Exception as e:

        result_data["error"] = str(e)

        return result_data


# =====================================================
# STREAMLIT SAFE WRAPPER
# =====================================================

def crawl_website(url: str):

    try:

        return asyncio.run(
            async_crawl_website(
                url
            )
        )

    except RuntimeError:

        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(
            loop
        )

        return loop.run_until_complete(
            async_crawl_website(
                url
            )
        )


# =====================================================
# BULK CRAWL
# =====================================================

async def async_bulk_crawl(
    urls: list
):

    tasks = [

        async_crawl_website(url)

        for url in urls

    ]

    return await asyncio.gather(
        *tasks,
        return_exceptions=False
    )


def crawl_multiple_websites(
    urls: list
):

    try:

        return asyncio.run(
            async_bulk_crawl(
                urls
            )
        )

    except RuntimeError:

        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(
            loop
        )

        return loop.run_until_complete(
            async_bulk_crawl(
                urls
            )
        )


# =====================================================
# DATAFRAME CRAWLER
# =====================================================

def crawl_dataframe(df):

    if "website" not in df.columns:

        raise ValueError(
            "DataFrame must contain website column"
        )

    urls = (

        df["website"]

        .dropna()

        .astype(str)

        .unique()

        .tolist()

    )

    results = crawl_multiple_websites(
        urls
    )

    output = []

    for result in results:

        output.append({

            "url":
                result["url"],

            "success":
                result["success"],

            "title":
                result["title"],

            "markdown":
                result["markdown"],

            "crawl_time":
                result["crawl_time"],

            "links_count":
                len(
                    result["links"]
                )

        })

    return pd.DataFrame(
        output
    )


# =====================================================
# CRAWL SUMMARY
# =====================================================

def get_crawl_summary(results):

    total = len(results)

    success = sum(
        1
        for r in results
        if r["success"]
    )

    failed = total - success

    return {

        "total_urls": total,

        "successful": success,

        "failed": failed,

        "success_rate": round(
            (
                success / total
            ) * 100,
            2
        ) if total else 0

    }


# =====================================================
# SAVE MARKDOWN
# =====================================================

def save_markdown(
    markdown,
    filepath
):

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(markdown)


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    result = crawl_website(
        "https://www.rvce.edu.in"
    )

    print(
        "\nTITLE:\n",
        result["title"]
    )

    print(
        "\nMARKDOWN:\n",
        result["markdown"][:1000]
    )

    print(
        "\nLINKS:",
        len(
            result["links"]
        )
    )
  
