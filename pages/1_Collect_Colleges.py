# pages/1_Collect_Colleges.py

import os
from datetime import datetime

import pandas as pd
import streamlit as st

from src.crawler.vtu_scraper import (
    scrape_vtu_colleges
)

from src.database.crud import (
    save_colleges,
    get_all_colleges,
    delete_all_colleges
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="VTU College Collector",
    page_icon="🏫",
    layout="wide"
)

# ==========================================================
# HEADER
# ==========================================================

st.title("🏫 VTU College Collector")

st.markdown("""
Collect all VTU affiliated colleges and store them in SQLite.

### Workflow
1. Collect VTU Colleges
2. Store in SQLite Database
3. Export CSV
4. Search & Filter
5. Crawl College Websites
""")

st.info(
    f"Last Updated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

# ==========================================================
# ACTION BUTTONS
# ==========================================================

st.subheader("⚙ Actions")

col1, col2, col3 = st.columns(3)

# ----------------------------------------------------------
# COLLECT COLLEGES
# ----------------------------------------------------------

with col1:

    if st.button(
        "🚀 Collect Colleges",
        use_container_width=True,
        type="primary"
    ):

        with st.spinner(
            "Collecting VTU colleges..."
        ):

            try:

                colleges = scrape_vtu_colleges()

                if not colleges:

                    st.error(
                        "No colleges found from VTU website."
                    )

                else:

                    df = pd.DataFrame(
                        colleges
                    )

                    # Remove old data

                    delete_all_colleges()

                    # Save fresh data

                    save_colleges(df)

                    os.makedirs(
                        "data",
                        exist_ok=True
                    )

                    df.to_csv(
                        "data/colleges.csv",
                        index=False
                    )

                    st.success(
                        f"Successfully collected {len(df)} colleges."
                    )

                    st.rerun()

            except Exception as e:

                st.error(
                    f"Collection Error: {e}"
                )

# ----------------------------------------------------------
# REFRESH
# ----------------------------------------------------------

with col2:

    if st.button(
        "🔄 Refresh",
        use_container_width=True
    ):

        st.rerun()

# ----------------------------------------------------------
# CLEAR DATABASE
# ----------------------------------------------------------

with col3:

    if st.button(
        "🗑 Clear Database",
        use_container_width=True
    ):

        try:

            delete_all_colleges()

            if os.path.exists(
                "data/colleges.csv"
            ):
                os.remove(
                    "data/colleges.csv"
                )

            st.success(
                "College database cleared."
            )

            st.rerun()

        except Exception as e:

            st.error(
                str(e)
            )

# ==========================================================
# LOAD DATA
# ==========================================================

try:

    colleges_df = get_all_colleges()

except Exception:

    colleges_df = pd.DataFrame()

# ==========================================================
# METRICS
# ==========================================================

st.markdown("---")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Total Colleges",
    len(colleges_df)
)

m2.metric(
    "Columns",
    len(colleges_df.columns)
    if not colleges_df.empty
    else 0
)

m3.metric(
    "CSV Exists",
    "Yes"
    if os.path.exists(
        "data/colleges.csv"
    )
    else "No"
)

m4.metric(
    "Database",
    "Connected"
)

# ==========================================================
# SEARCH
# ==========================================================

st.markdown("---")

st.subheader("🔍 Search Colleges")

search_text = st.text_input(
    "Enter College Name",
    placeholder="RV College"
)

filtered_df = colleges_df.copy()

if search_text and not colleges_df.empty:

    filtered_df = colleges_df[

        colleges_df["college_name"]

        .astype(str)

        .str.contains(

            search_text,

            case=False,

            na=False

        )

    ]

# ==========================================================
# COLLEGE TABLE
# ==========================================================

st.markdown("---")

st.subheader("📋 VTU Colleges")

if not filtered_df.empty:

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=600
    )

else:

    st.warning(
        "No colleges found."
    )

# ==========================================================
# DOWNLOAD CSV
# ==========================================================

if not colleges_df.empty:

    csv_data = colleges_df.to_csv(
        index=False
    )

    st.download_button(

        label="⬇ Download Colleges CSV",

        data=csv_data,

        file_name="vtu_colleges.csv",

        mime="text/csv"

    )

# ==========================================================
# PREVIEW
# ==========================================================

st.markdown("---")

st.subheader("📊 Preview")

if not colleges_df.empty:

    preview_columns = [

        col for col in [

            "college_code",

            "college_name",

            "std_code",

            "phone",

            "rural_urban"

        ]

        if col in colleges_df.columns

    ]

    st.dataframe(

        colleges_df[
            preview_columns
        ].head(20),

        use_container_width=True

    )

# ==========================================================
# DEBUG
# ==========================================================

with st.expander(
    "⚙ Debug Information"
):

    st.write(
        "Total Records:",
        len(colleges_df)
    )

    if not colleges_df.empty:

        st.write(
            "Columns:"
        )

        st.write(
            list(
                colleges_df.columns
            )
        )

        st.write(
            "First Record:"
        )

        st.json(
            colleges_df.iloc[0].to_dict()
        )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "VTU College Intelligence Platform"
)

