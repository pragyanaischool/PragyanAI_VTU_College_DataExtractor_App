"""
pages/1_Collect_Colleges.py

VTU College Collector
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from src.crawler.vtu_scraper import (
    scrape_vtu_colleges,
    get_colleges_dataframe
)

from src.database.crud import (
    save_colleges,
    get_all_colleges,
    delete_all_colleges
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Collect Colleges",
    page_icon="🏫",
    layout="wide"
)

# =====================================================
# HEADER
# =====================================================

st.title("🏫 VTU College Collector")

st.markdown("""
Collect all affiliated colleges from VTU website and store them in SQLite Database.
""")

# =====================================================
# LAST UPDATED
# =====================================================

st.info(
    f"Last Updated: {datetime.now().strftime('%d-%m-%Y')}"
)

# =====================================================
# ACTION BUTTONS
# =====================================================

col1, col2, col3 = st.columns(3)

# -----------------------------------------------------

with col1:

    if st.button(
        "🚀 Collect Colleges",
        use_container_width=True
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
                        "No colleges found. Check scraper."
                    )

                else:

                    df = pd.DataFrame(
                        colleges
                    )

                    # Clear existing data
                    delete_all_colleges()

                    # Save fresh data
                    save_colleges(df)

                    # Save CSV
                    df.to_csv(
                        "data/colleges.csv",
                        index=False
                    )

                    st.success(
                        f"Successfully collected {len(df)} colleges."
                    )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

# -----------------------------------------------------

with col2:

    if st.button(
        "🔄 Refresh Database",
        use_container_width=True
    ):

        try:

            colleges = scrape_vtu_colleges()

            df = pd.DataFrame(
                colleges
            )

            delete_all_colleges()

            save_colleges(df)

            st.success(
                "Database Refreshed."
            )

        except Exception as e:

            st.error(str(e))

# -----------------------------------------------------

with col3:

    if st.button(
        "🗑 Clear Database",
        use_container_width=True
    ):

        try:

            delete_all_colleges()

            st.success(
                "College Table Cleared."
            )

        except Exception as e:

            st.error(str(e))

# =====================================================
# LOAD DATABASE
# =====================================================

try:

    df = get_all_colleges()

except Exception:

    df = pd.DataFrame()

# =====================================================
# METRICS
# =====================================================

st.markdown("---")

c1, c2 = st.columns(2)

c1.metric(
    "Total Colleges",
    len(df)
)

c2.metric(
    "Columns",
    len(df.columns)
    if not df.empty
    else 0
)

# =====================================================
# SEARCH
# =====================================================

st.markdown("---")

st.subheader("🔍 Search Colleges")

search_text = st.text_input(
    "Enter College Name"
)

filtered_df = df.copy()

if search_text:

    filtered_df = filtered_df[

        filtered_df[
            "college_name"
        ]

        .astype(str)

        .str.contains(

            search_text,

            case=False,

            na=False

        )

    ]

# =====================================================
# DATA TABLE
# =====================================================

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

# =====================================================
# DOWNLOAD CSV
# =====================================================

if not df.empty:

    st.download_button(

        label="⬇ Download CSV",

        data=df.to_csv(
            index=False
        ),

        file_name=
        "vtu_colleges.csv",

        mime="text/csv"

    )

# =====================================================
# PREVIEW
# =====================================================

st.markdown("---")

st.subheader("📊 Data Preview")

if not df.empty:

    st.write(
        df.head()
    )

else:

    st.info(
        "Collect colleges first."
    )

# =====================================================
# DEBUG
# =====================================================

with st.expander(
    "⚙ Debug Information"
):

    st.write(
        "Database Records:",
        len(df)
    )

    if not df.empty:

        st.write(
            "Columns:"
        )

        st.write(
            list(df.columns)
        )

        st.write(
            "Sample:"
        )

        st.json(
            df.iloc[0].to_dict()
        )
        
