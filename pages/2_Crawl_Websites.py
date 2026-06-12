"""
pages/2_Crawl_Websites.py

Website Crawling Page

Uses:
- ScrapeGraphAI
- BeautifulSoup Fallback
- SQLite Storage
"""

import streamlit as st
import pandas as pd

from src.database.crud import (
    get_all_colleges,
    save_crawl_result,
    get_crawl_results
)

from src.crawler.scrapegraph_engine import (
    scrape_website
)

from src.utils.config import (
    GROQ_API_KEY
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Crawl Websites",
    page_icon="🌐",
    layout="wide"
)

# =====================================================
# HEADER
# =====================================================

st.title("🌐 Crawl College Websites")

st.markdown("""
This page:

1. Reads collected colleges
2. Crawls official websites
3. Extracts website content
4. Stores content in SQLite
""")

# =====================================================
# LOAD COLLEGES
# =====================================================

colleges_df = get_all_colleges()

if colleges_df.empty:

    st.warning(
        "No colleges found.\n\nRun Step 1: Collect Colleges."
    )

    st.stop()

# =====================================================
# SUMMARY
# =====================================================

c1, c2 = st.columns(2)

c1.metric(
    "Total Colleges",
    len(colleges_df)
)

crawl_df = get_crawl_results()

c2.metric(
    "Already Crawled",
    len(crawl_df)
)

# =====================================================
# PREVIEW
# =====================================================

st.subheader("College Websites")

display_cols = [

    col for col in [

        "college_name",
        "website",
        "district"

    ]

    if col in colleges_df.columns

]

st.dataframe(
    colleges_df[display_cols],
    use_container_width=True
)

# =====================================================
# CRAWL OPTIONS
# =====================================================

st.subheader("Crawler Settings")

max_sites = st.number_input(

    "Number of Colleges to Crawl",

    min_value=1,

    max_value=len(colleges_df),

    value=min(20, len(colleges_df))

)

# =====================================================
# START BUTTON
# =====================================================

if st.button(
    "🚀 Start Crawling",
    use_container_width=True
):

    progress = st.progress(0)

    status = st.empty()

    results = []

    selected_df = colleges_df.head(
        max_sites
    )

    total = len(selected_df)

    for idx, row in selected_df.iterrows():

        college_name = row.get(
            "college_name",
            ""
        )

        website = row.get(
            "website",
            ""
        )

        if not website:

            continue

        status.info(
            f"Crawling: {college_name}"
        )

        try:

            result = scrape_website(

                website,

                groq_api_key=GROQ_API_KEY

            )

            if result["success"]:

                save_crawl_result(

                    college_name=
                    college_name,

                    website=
                    website,

                    markdown=
                    result["content"],

                    title=
                    result["title"],

                    crawl_time=0

                )

                results.append({

                    "College":
                        college_name,

                    "Website":
                        website,

                    "Status":
                        "Success",

                    "Characters":
                        len(
                            result[
                                "content"
                            ]
                        )

                })

            else:

                results.append({

                    "College":
                        college_name,

                    "Website":
                        website,

                    "Status":
                        "Failed",

                    "Characters":
                        0

                })

        except Exception as e:

            results.append({

                "College":
                    college_name,

                "Website":
                    website,

                "Status":
                    f"Error: {e}",

                "Characters":
                    0

            })

        progress.progress(
            (idx + 1) / total
        )

    status.success(
        "Crawling Completed"
    )

    st.subheader(
        "Results"
    )

    st.dataframe(

        pd.DataFrame(results),

        use_container_width=True

    )

# =====================================================
# DATABASE CONTENT
# =====================================================

st.markdown("---")

st.subheader(
    "Stored Crawl Results"
)

crawl_df = get_crawl_results()

if not crawl_df.empty:

    st.dataframe(

        crawl_df,

        use_container_width=True

    )

else:

    st.info(
        "No crawl data available."
    )

# =====================================================
# PREVIEW CONTENT
# =====================================================

if not crawl_df.empty:

    st.markdown("---")

    st.subheader(
        "Content Preview"
    )

    record_id = st.selectbox(

        "Select Record",

        crawl_df["id"]

    )

    selected = crawl_df[
        crawl_df["id"]
        == record_id
    ]

    if not selected.empty:

        content = selected.iloc[0][
            "markdown"
        ]

        st.text_area(

            "Website Content",

            content[:10000],

            height=400

        )
        
