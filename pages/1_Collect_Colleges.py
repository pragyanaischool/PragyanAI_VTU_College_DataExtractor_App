import streamlit as st
import pandas as pd
from datetime import datetime

from src.crawler.vtu_scraper import scrape_vtu_colleges
from src.database.crud import (
    save_colleges,
    get_all_colleges,
    delete_all_colleges
)

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="VTU College Collector",
    page_icon="🏫",
    layout="wide"
)

# ---------------------------------------
# TITLE
# ---------------------------------------

st.title("🏫 VTU College Collector")

st.markdown("""
Collect all affiliated colleges from VTU website and store them in SQLite Database.
""")

# ---------------------------------------
# SIDEBAR
# ---------------------------------------

st.sidebar.header("Options")

refresh_data = st.sidebar.button("🔄 Refresh VTU Data")

clear_db = st.sidebar.button("🗑 Clear Database")

# ---------------------------------------
# CLEAR DATABASE
# ---------------------------------------

if clear_db:

    delete_all_colleges()

    st.success("Database Cleared Successfully")

    st.rerun()

# ---------------------------------------
# COLLECT COLLEGES
# ---------------------------------------

col1, col2 = st.columns([2, 1])

with col1:

    if st.button(
        "🚀 Collect Colleges from VTU",
        use_container_width=True
    ):

        with st.spinner("Collecting colleges..."):

            try:

                df = scrape_vtu_colleges()

                if df.empty:

                    st.error(
                        "No colleges found."
                    )

                else:

                    save_colleges(df)

                    st.success(
                        f"{len(df)} Colleges Collected Successfully"
                    )

                    st.session_state["colleges"] = df

            except Exception as e:

                st.error(str(e))

with col2:

    st.metric(
        "Last Updated",
        datetime.now().strftime("%d-%m-%Y")
    )

# ---------------------------------------
# LOAD DATABASE DATA
# ---------------------------------------

try:

    db_df = get_all_colleges()

except:

    db_df = pd.DataFrame()

# ---------------------------------------
# SUMMARY
# ---------------------------------------

if not db_df.empty:

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Colleges",
        len(db_df)
    )

    if "district" in db_df.columns:

        c2.metric(
            "Districts",
            db_df["district"].nunique()
        )

    else:

        c2.metric(
            "Districts",
            0
        )

    c3.metric(
        "Records",
        len(db_df)
    )

# ---------------------------------------
# SEARCH
# ---------------------------------------

st.subheader("🔍 Search Colleges")

search_text = st.text_input(
    "Enter College Name"
)

if not db_df.empty:

    if search_text:

        filtered_df = db_df[
            db_df["college_name"]
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    else:

        filtered_df = db_df

else:

    filtered_df = pd.DataFrame()

# ---------------------------------------
# DISPLAY DATA
# ---------------------------------------

st.subheader("📋 VTU Colleges")

if not filtered_df.empty:

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=600
    )

else:

    st.info(
        "No college data available."
    )

# ---------------------------------------
# DOWNLOAD CSV
# ---------------------------------------

if not filtered_df.empty:

    csv = filtered_df.to_csv(
        index=False
    )

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="vtu_colleges.csv",
        mime="text/csv",
        use_container_width=True
    )

# ---------------------------------------
# RAW DATA
# ---------------------------------------

with st.expander("View Raw Data"):

    if not filtered_df.empty:

        st.write(filtered_df)

# ---------------------------------------
# FOOTER
# ---------------------------------------

st.markdown("---")

st.caption(
    "VTU College Intelligence Platform | College Collector Module"
)
