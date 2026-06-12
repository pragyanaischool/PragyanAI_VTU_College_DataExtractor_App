import streamlit as st
import pandas as pd
from datetime import datetime

from src.database.crud import (
    get_all_colleges,
    save_crawl_result,
    get_crawl_results
)

from src.crawler.website_discovery import (
    discover_website
)

from src.crawler.crawl4ai_engine import (
    crawl_website
)

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="Website Crawler",
    page_icon="🌐",
    layout="wide"
)

# ---------------------------------------
# TITLE
# ---------------------------------------

st.title("🌐 VTU Website Discovery & Crawling")

st.markdown("""
Discover official college websites and crawl them using Crawl4AI.
""")

# ---------------------------------------
# LOAD COLLEGES
# ---------------------------------------

try:

    colleges_df = get_all_colleges()

except Exception as e:

    st.error(str(e))
    st.stop()

if colleges_df.empty:

    st.warning(
        "No colleges found. Run College Collector first."
    )

    st.stop()

# ---------------------------------------
# SIDEBAR
# ---------------------------------------

st.sidebar.header("Crawler Options")

crawl_limit = st.sidebar.number_input(
    "Maximum Colleges to Crawl",
    min_value=1,
    max_value=500,
    value=10
)

# ---------------------------------------
# STATS
# ---------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Colleges",
    len(colleges_df)
)

crawl_df = get_crawl_results()

col2.metric(
    "Already Crawled",
    len(crawl_df)
)

remaining = max(
    0,
    len(colleges_df) - len(crawl_df)
)

col3.metric(
    "Remaining",
    remaining
)

st.markdown("---")

# ---------------------------------------
# SELECT COLLEGE
# ---------------------------------------

college_name = st.selectbox(
    "Select College",
    colleges_df["college_name"].tolist()
)

selected_row = colleges_df[
    colleges_df["college_name"] == college_name
].iloc[0]

# ---------------------------------------
# COLLEGE INFO
# ---------------------------------------

st.subheader("College Information")

info_col1, info_col2 = st.columns(2)

with info_col1:

    st.write(
        f"**College Code:** {selected_row.get('college_code','')}"
    )

    st.write(
        f"**District:** {selected_row.get('district','')}"
    )

with info_col2:

    st.write(
        f"**Website:** {selected_row.get('website','Not Available')}"
    )

# ---------------------------------------
# DISCOVER WEBSITE
# ---------------------------------------

st.subheader("Website Discovery")

if st.button(
    "🔍 Discover Website",
    use_container_width=True
):

    with st.spinner(
        "Searching Website..."
    ):

        try:

            website = discover_website(
                college_name
            )

            st.success(
                f"Website Found: {website}"
            )

            st.session_state[
                "website"
            ] = website

        except Exception as e:

            st.error(str(e))

# ---------------------------------------
# DISPLAY WEBSITE
# ---------------------------------------

website = st.session_state.get(
    "website",
    selected_row.get(
        "website",
        ""
    )
)

if website:

    st.info(
        f"Website: {website}"
    )

# ---------------------------------------
# CRAWL SINGLE WEBSITE
# ---------------------------------------

st.subheader("Single Website Crawl")

if st.button(
    "🚀 Crawl Website",
    use_container_width=True
):

    if not website:

        st.error(
            "Website not available."
        )

    else:

        with st.spinner(
            "Crawling Website..."
        ):

            try:

                markdown = crawl_website(
                    website
                )

                st.session_state[
                    "markdown"
                ] = markdown

                save_crawl_result(
                    college_name=college_name,
                    website=website,
                    markdown=markdown
                )

                st.success(
                    "Website Crawled Successfully"
                )

            except Exception as e:

                st.error(str(e))

# ---------------------------------------
# PREVIEW MARKDOWN
# ---------------------------------------

if "markdown" in st.session_state:

    st.subheader(
        "Markdown Preview"
    )

    st.text_area(
        "Content",
        st.session_state[
            "markdown"
        ][:10000],
        height=500
    )

# ---------------------------------------
# DOWNLOAD MARKDOWN
# ---------------------------------------

if "markdown" in st.session_state:

    st.download_button(
        "⬇ Download Markdown",
        st.session_state[
            "markdown"
        ],
        file_name=f"{college_name}.md",
        mime="text/plain",
        use_container_width=True
    )

# ---------------------------------------
# BULK CRAWL
# ---------------------------------------

st.markdown("---")

st.subheader(
    "Bulk Crawl Colleges"
)

if st.button(
    "⚡ Crawl Multiple Colleges",
    use_container_width=True
):

    progress = st.progress(0)

    status = st.empty()

    subset_df = colleges_df.head(
        crawl_limit
    )

    success_count = 0

    for idx, row in enumerate(
        subset_df.itertuples()
    ):

        try:

            college = row.college_name

            website = row.website

            if not website:

                website = discover_website(
                    college
                )

            if website:

                markdown = crawl_website(
                    website
                )

                save_crawl_result(
                    college_name=college,
                    website=website,
                    markdown=markdown
                )

                success_count += 1

            progress.progress(
                (idx + 1)
                / len(subset_df)
            )

            status.info(
                f"Crawling: {college}"
            )

        except Exception:

            pass

    status.success(
        f"Completed. {success_count} websites crawled."
    )

# ---------------------------------------
# CRAWL HISTORY
# ---------------------------------------

st.markdown("---")

st.subheader(
    "Crawl History"
)

crawl_df = get_crawl_results()

if not crawl_df.empty:

    display_df = crawl_df.copy()

    if "markdown" in display_df.columns:

        display_df["content_size"] = (
            display_df["markdown"]
            .astype(str)
            .apply(len)
        )

        display_df = display_df.drop(
            columns=["markdown"]
        )

    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )

else:

    st.info(
        "No crawl results available."
    )

# ---------------------------------------
# FOOTER
# ---------------------------------------

st.markdown("---")

st.caption(
    f"Last Refresh: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

st.caption(
    "VTU College Intelligence Platform | Crawl4AI Module"
)
