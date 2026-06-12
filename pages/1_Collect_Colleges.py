# pages/1_Collect_Colleges.py

import os
from datetime import datetime

import pandas as pd
import streamlit as st

from src.crawler.vtu_scraper import (
    scrape_vtu_colleges,
    get_colleges_dataframe,
)

from src.database.crud import (
    save_colleges,
    get_all_colleges,
    delete_all_colleges,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="VTU College Collector",
    page_icon="🏫",
    layout="wide",
)

# ==========================================================
# HEADER
# ==========================================================

st.title("🏫 VTU College Collector")

st.markdown(
    """
Collect all VTU affiliated colleges and store them in SQLite.

### Workflow
1. Scrape VTU Affiliated Institutes
2. Store in SQLite Database
3. Save CSV File
4. Search & Filter Colleges
"""
)

# ==========================================================
# LAST UPDATED
# ==========================================================

st.info(
    f"Last Updated: {datetime.now().strftime('%d-%m-%Y')}"
)

# ==========================================================
# ACTIONS
# ==========================================================

st.subheader("⚙️ Actions")

col1, col2, col3 = st.columns(3)

# ----------------------------------------------------------

with col1:

    if st.button(
        "🚀 Collect Colleges",
        use_container_width=True,
        type="primary",
    ):

        with st.spinner(
            "Collecting colleges from VTU..."
        ):

            try:

                colleges = scrape_vtu_colleges()

                st.write(
                    f"Records Found: {len(colleges)}"
                )

                if len(colleges) == 0:

                    st.error(
                        "No colleges found."
                    )

                else:

                    df = pd.DataFrame(
                        colleges
                    )

                    delete_all_colleges()

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
                        f"{len(df)} colleges collected successfully."
                    )

                    st.rerun()

            except Exception as e:

                st.error(
                    f"Collection Error: {e}"
                )

# ----------------------------------------------------------

with col2:

    if st.button(
        "🔄 Refresh",
        use_container_width=True,
    ):

        st.rerun()

# ----------------------------------------------------------

with col3:

    if st.button(
        "🗑 Clear Database",
        use_container_width=True,
    ):

        try:

            delete_all_colleges()

            st.success(
                "College table cleared."
            )

            st.rerun()

        except Exception as e:

            st.error(str(e))

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

m1, m2, m3 = st.columns(3)

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

# ==========================================================
# SEARCH
# ==========================================================

st.markdown("---")

st.subheader("🔍 Search Colleges")

search_text = st.text_input(
    "Enter College Name",
    placeholder="RVCE"
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
# TABLE
# ==========================================================

st.markdown("---")

st.subheader("📋 VTU Colleges")

if not filtered_df.empty:

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=600,
    )

else:

    st.warning(
        "No colleges found."
    )

# ==========================================================
# DOWNLOAD
# ==========================================================

if not colleges_df.empty:

    csv_data = colleges_df.to_csv(
        index=False
    )

    st.download_button(
        label="⬇ Download CSV",
        data=csv_data,
        file_name="vtu_colleges.csv",
        mime="text/csv",
    )

# ==========================================================
# PREVIEW
# ==========================================================

st.markdown("---")

st.subheader("📊 Data Preview")

if not colleges_df.empty:

    st.dataframe(
        colleges_df.head(10),
        use_container_width=True,
    )

else:

    st.info(
        "Collect colleges first."
    )

# ==========================================================
# DEBUG
# ==========================================================

with st.expander(
    "⚙ Debug Information"
):

    st.write(
        "Database Records:",
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

