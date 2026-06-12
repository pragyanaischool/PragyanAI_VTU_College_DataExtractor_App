# pages/2_Crawl_Websites.py

import streamlit as st
import pandas as pd

from src.database.crud import (
    get_all_colleges,
    get_crawl_results,
    save_crawl_result,
    update_college_website
)

from src.crawler.google_discovery import (
    find_official_website
)

from src.crawler.scrapegraph_engine import (
    scrape_website
)

from src.utils.config import (
    GROQ_API_KEY
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Crawl Websites",
    page_icon="🌐",
    layout="wide"
)

# ==========================================================
# HEADER
# ==========================================================

st.title("🌐 Crawl College Websites")

st.markdown("""
This page:

1. Finds official college websites
2. Crawls websites
3. Stores website content
4. Prepares data for extraction
""")

# ==========================================================
# LOAD COLLEGES
# ==========================================================

colleges_df = get_all_colleges()

if colleges_df.empty:

    st.warning(
        "No colleges found.\n\nRun Step 1: Collect Colleges."
    )

    st.stop()

crawl_df = get_crawl_results()

# ==========================================================
# SUMMARY
# ==========================================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Colleges",
    len(colleges_df)
)

website_count = len(
    colleges_df[
        colleges_df["website"]
        .fillna("") != ""
    ]
)

col2.metric(
    "Websites Found",
    website_count
)

col3.metric(
    "Already Crawled",
    len(crawl_df)
)

# ==========================================================
# COLLEGE TABLE
# ==========================================================

st.subheader(
    "🏫 VTU Colleges"
)

display_columns = []

for column in [

    "college_code",

    "college_name",

    "website"

]:

    if column in colleges_df.columns:

        display_columns.append(
            column
        )

st.dataframe(

    colleges_df[
        display_columns
    ],

    use_container_width=True

)

# ==========================================================
# WEBSITE DISCOVERY
# ==========================================================

st.markdown("---")

st.subheader(
    "🔍 Find Official Websites"
)

if st.button(
    "🔍 Search Websites",
    use_container_width=True
):

    progress = st.progress(0)

    status = st.empty()

    found_count = 0

    total = len(colleges_df)

    for idx, row in colleges_df.iterrows():

        college_name = row.get(
            "college_name",
            ""
        )

        college_code = row.get(
            "college_code",
            ""
        )

        existing_website = row.get(
            "website",
            ""
        )

        if existing_website:

            continue

        status.info(
            f"Searching: {college_name}"
        )

        try:

            website = find_official_website(
                college_name
            )

            if website:

                update_college_website(
                    college_code,
                    website
                )

                found_count += 1

        except Exception as e:

            print(
                f"Website Search Error: {e}"
            )

        progress.progress(
            (idx + 1) / total
        )

    status.success(
        f"Found {found_count} websites"
    )

    st.rerun()

# ==========================================================
# CRAWL SETTINGS
# ==========================================================

st.markdown("---")

st.subheader(
    "🌐 Crawl Websites"
)

max_sites = st.number_input(

    "Number of Websites to Crawl",

    min_value=1,

    max_value=max(
        1,
        len(colleges_df)
    ),

    value=min(
        20,
        len(colleges_df)
    )

)

# ==========================================================
# START CRAWL
# ==========================================================

if st.button(
    "🚀 Start Crawling",
    use_container_width=True
):

    crawl_targets = colleges_df[
        colleges_df["website"]
        .fillna("") != ""
    ]

    crawl_targets = crawl_targets.head(
        max_sites
    )

    if crawl_targets.empty:

        st.warning(
            "No websites available. Run Website Discovery first."
        )

        st.stop()

    progress = st.progress(0)

    status = st.empty()

    results = []

    total = len(crawl_targets)

    for count, (_, row) in enumerate(
        crawl_targets.iterrows(),
        start=1
    ):

        college_name = row.get(
            "college_name",
            ""
        )

        website = row.get(
            "website",
            ""
        )

        status.info(
            f"Crawling: {college_name}"
        )

        try:

            result = scrape_website(
                website,
                groq_api_key=GROQ_API_KEY
            )

            if result.get(
                "success",
                False
            ):

                save_crawl_result(

                    college_name=
                    college_name,

                    website=
                    website,

                    markdown=
                    result.get(
                        "content",
                        ""
                    ),

                    title=
                    result.get(
                        "title",
                        ""
                    ),

                    crawl_time=
                    result.get(
                        "crawl_time",
                        0
                    )

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
                        result.get(
                            "content",
                            ""
                        )
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
                f"Error: {str(e)}",

                "Characters":
                0

            })

        progress.progress(
            count / total
        )

    status.success(
        "Website Crawling Completed"
    )

    st.subheader(
        "Crawl Results"
    )

    st.dataframe(

        pd.DataFrame(
            results
        ),

        use_container_width=True

    )

# ==========================================================
# EXTRACTION
# ==========================================================

st.markdown("---")

if st.button(
    "🤖 Go To Extraction",
    use_container_width=True
):

    st.switch_page(
        "pages/3_Extract_Data.py"
    )

# ==========================================================
# STORED RESULTS
# ==========================================================

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

# ==========================================================
# CONTENT PREVIEW
# ==========================================================

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

            height=500

        )
