import streamlit as st
import pandas as pd
import json

from datetime import datetime

from src.database.crud import (
    get_crawl_results,
    save_extracted_data,
    get_extracted_table
)

from src.extraction.regex_extractor import (
    extract_contacts
)

from src.extraction.parser import (
    quick_extract,
    content_statistics
)

from src.extraction.groq_extractor import (
    extract_college_details
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="College Data Extraction",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# HEADER
# =====================================================

st.title(
    "🤖 College Data Extraction"
)

st.markdown(
    """
    Extract structured information from crawled college websites.

    Extraction Methods:

    • Regex Extraction
    • Parser Extraction
    • GROQ LLM Extraction
    • JSON Validation
    """
)

# =====================================================
# LOAD DATA
# =====================================================

crawl_df = get_crawl_results()

if crawl_df.empty:

    st.warning(
        "No crawled websites found."
    )

    st.stop()

history_df = get_extracted_table()

# =====================================================
# STATS
# =====================================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Crawled Websites",
    len(crawl_df)
)

col2.metric(
    "Extracted Records",
    len(history_df)
)

col3.metric(
    "Pending",
    max(
        0,
        len(crawl_df) - len(history_df)
    )
)

st.markdown("---")

# =====================================================
# COLLEGE SELECTION
# =====================================================

college_name = st.selectbox(
    "Select College",
    crawl_df[
        "college_name"
    ].tolist()
)

selected = crawl_df[
    crawl_df["college_name"]
    == college_name
].iloc[0]

markdown = selected["markdown"]

# =====================================================
# CONTENT PREVIEW
# =====================================================

st.subheader(
    "📄 Crawled Content"
)

st.text_area(
    "Website Content",
    markdown[:10000],
    height=300
)

# =====================================================
# CONTENT STATS
# =====================================================

stats = content_statistics(
    markdown
)

st.json(stats)

# =====================================================
# REGEX EXTRACTION
# =====================================================

st.markdown("---")

st.subheader(
    "📧 Contact Extraction"
)

if st.button(
    "Extract Contacts",
    use_container_width=True
):

    contacts = extract_contacts(
        markdown
    )

    st.session_state[
        "contacts"
    ] = contacts

if "contacts" in st.session_state:

    st.json(
        st.session_state[
            "contacts"
        ]
    )

# =====================================================
# QUICK PARSER
# =====================================================

st.markdown("---")

st.subheader(
    "⚡ Quick Parser"
)

if st.button(
    "Run Quick Parser",
    use_container_width=True
):

    parsed = quick_extract(
        markdown
    )

    st.session_state[
        "quick_extract"
    ] = parsed

if "quick_extract" in st.session_state:

    st.json(
        st.session_state[
            "quick_extract"
        ]
    )

# =====================================================
# GROQ EXTRACTION
# =====================================================

st.markdown("---")

st.subheader(
    "🧠 GROQ Structured Extraction"
)

if st.button(
    "Run GROQ Extraction",
    use_container_width=True
):

    with st.spinner(
        "Running GROQ Extraction..."
    ):

        try:

            result = (
                extract_college_details(
                    markdown
                )
            )

            st.session_state[
                "groq_output"
            ] = result

            st.success(
                "Extraction Complete"
            )

        except Exception as e:

            st.error(
                str(e)
            )

# =====================================================
# DISPLAY OUTPUT
# =====================================================

if "groq_output" in st.session_state:

    st.subheader(
        "Structured College Data"
    )

    st.json(
        st.session_state[
            "groq_output"
        ]
    )

# =====================================================
# SAVE OUTPUT
# =====================================================

if "groq_output" in st.session_state:

    if st.button(
        "💾 Save Extracted Data",
        use_container_width=True
    ):

        try:

            save_extracted_data(
                st.session_state[
                    "groq_output"
                ]
            )

            st.success(
                "Saved Successfully"
            )

        except Exception as e:

            st.error(
                str(e)
            )

# =====================================================
# BULK EXTRACTION
# =====================================================

st.markdown("---")

st.subheader(
    "⚡ Bulk Extraction"
)

bulk_limit = st.number_input(
    "Number of Colleges",
    min_value=1,
    max_value=len(crawl_df),
    value=min(
        10,
        len(crawl_df)
    )
)

if st.button(
    "Run Bulk GROQ Extraction",
    use_container_width=True
):

    progress = st.progress(0)

    status = st.empty()

    success_count = 0

    subset_df = crawl_df.head(
        bulk_limit
    )

    for idx, row in enumerate(
        subset_df.itertuples()
    ):

        try:

            result = (
                extract_college_details(
                    row.markdown
                )
            )

            save_extracted_data(
                result
            )

            success_count += 1

        except Exception:
            pass

        progress.progress(
            (idx + 1)
            / len(subset_df)
        )

        status.info(
            f"Processing: {row.college_name}"
        )

    status.success(
        f"{success_count} colleges extracted."
    )

# =====================================================
# HISTORY
# =====================================================

st.markdown("---")

st.subheader(
    "📚 Extracted Records"
)

history_df = get_extracted_table()

if not history_df.empty:

    st.dataframe(
        history_df,
        use_container_width=True,
        height=500
    )

else:

    st.info(
        "No extracted data available."
    )

# =====================================================
# EXPORT
# =====================================================

if not history_df.empty:

    json_data = history_df.to_json(
        orient="records",
        indent=4
    )

    st.download_button(
        "⬇ Download JSON",
        json_data,
        file_name="colleges.json",
        mime="application/json"
    )

# =====================================================
# RAW JSON
# =====================================================

with st.expander(
    "View Raw JSON"
):

    if "groq_output" in st.session_state:

        st.code(
            json.dumps(
                st.session_state[
                    "groq_output"
                ],
                indent=4
            ),
            language="json"
        )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    f"Last Updated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

st.caption(
    "VTU College Intelligence Platform"
)
