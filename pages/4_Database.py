"""
pages/4_Database.py

Database Management
"""

import streamlit as st
import pandas as pd

from src.database.db import (
    get_database_stats,
    get_database_info
)

from src.database.crud import (
    get_all_colleges,
    get_crawl_results,
    get_extracted_table,
    delete_all_colleges,
    delete_all_crawl_results,
    delete_all_extracted_records,
    search_colleges
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Database",
    page_icon="🗄",
    layout="wide"
)

# =====================================================
# HEADER
# =====================================================

st.title("🗄 Database Management")

st.markdown("""
View and manage SQLite database records.
""")

# =====================================================
# DATABASE INFO
# =====================================================

st.subheader("📊 Database Information")

try:

    db_info = get_database_info()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Database Exists",
        "Yes" if db_info["database_exists"] else "No"
    )

    col2.metric(
        "Size (MB)",
        db_info["database_size_mb"]
    )

    col3.metric(
        "Path",
        "data/vtu.db"
    )

except Exception as e:

    st.error(str(e))

# =====================================================
# DATABASE STATS
# =====================================================

st.markdown("---")

st.subheader("📈 Table Statistics")

try:

    stats = get_database_stats()

    stats_df = pd.DataFrame({

        "Table": list(stats.keys()),

        "Records": list(stats.values())

    })

    st.dataframe(
        stats_df,
        use_container_width=True
    )

except Exception as e:

    st.error(str(e))

# =====================================================
# TABLE SELECTION
# =====================================================

st.markdown("---")

table_name = st.selectbox(

    "Select Table",

    [

        "colleges",

        "crawl_results",

        "extracted_details"

    ]

)

# =====================================================
# LOAD TABLE
# =====================================================

if table_name == "colleges":

    df = get_all_colleges()

elif table_name == "crawl_results":

    df = get_crawl_results()

else:

    df = get_extracted_table()

# =====================================================
# SEARCH
# =====================================================

st.markdown("---")

st.subheader("🔍 Search")

search_text = st.text_input(
    "Enter keyword"
)

if search_text:

    try:

        search_df = search_colleges(
            search_text
        )

        if not search_df.empty:

            st.success(
                f"{len(search_df)} records found"
            )

            st.dataframe(
                search_df,
                use_container_width=True
            )

        else:

            st.warning(
                "No matching records found."
            )

    except Exception as e:

        st.error(str(e))

# =====================================================
# TABLE DATA
# =====================================================

st.markdown("---")

st.subheader(
    f"📋 {table_name}"
)

if not df.empty:

    st.metric(
        "Records",
        len(df)
    )

    st.dataframe(

        df,

        use_container_width=True,

        height=600

    )

else:

    st.warning(
        "No records available."
    )

# =====================================================
# DOWNLOAD
# =====================================================

if not df.empty:

    st.download_button(

        label=f"⬇ Download {table_name}.csv",

        data=df.to_csv(
            index=False
        ),

        file_name=f"{table_name}.csv",

        mime="text/csv"

    )

# =====================================================
# TABLE ACTIONS
# =====================================================

st.markdown("---")

st.subheader("⚠ Table Actions")

col1, col2, col3 = st.columns(3)

# -----------------------------------------------------

with col1:

    if st.button(
        "Clear Colleges"
    ):

        delete_all_colleges()

        st.success(
            "Colleges table cleared."
        )

        st.rerun()

# -----------------------------------------------------

with col2:

    if st.button(
        "Clear Crawl Results"
    ):

        delete_all_crawl_results()

        st.success(
            "Crawl results cleared."
        )

        st.rerun()

# -----------------------------------------------------

with col3:

    if st.button(
        "Clear Extracted Data"
    ):

        delete_all_extracted_records()

        st.success(
            "Extracted data cleared."
        )

        st.rerun()

# =====================================================
# DATA PREVIEW
# =====================================================

st.markdown("---")

st.subheader("🔎 Record Preview")

if not df.empty:

    row_id = st.number_input(

        "Row Number",

        min_value=0,

        max_value=len(df)-1,

        value=0

    )

    st.json(

        df.iloc[row_id].to_dict()

    )

# =====================================================
# COLUMN SUMMARY
# =====================================================

st.markdown("---")

st.subheader("📑 Columns")

if not df.empty:

    col_df = pd.DataFrame({

        "Column Name":
            df.columns,

        "Data Type":
            [
                str(dtype)
                for dtype
                in df.dtypes
            ]

    })

    st.dataframe(

        col_df,

        use_container_width=True

    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "VTU College Intelligence Database Manager"
)

