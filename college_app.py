"""
app.py

VTU College Intelligence Platform

Main Dashboard
"""

import streamlit as st
import pandas as pd

from src.database.db import (
    initialize_database,
    get_database_stats
)

from src.database.crud import (
    get_all_colleges,
    get_crawl_results,
    get_extracted_table,
    get_statistics
)

from src.llm.groq_client import (
    streamlit_status
)

from src.utils.config import (
    APP_NAME,
    APP_VERSION
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="VTU College Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# DATABASE INIT
# =====================================================

initialize_database()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🎓 VTU Intelligence")

    st.markdown("---")

    st.markdown("### Navigation")

    st.markdown("""
    1️⃣ Collect Colleges

    2️⃣ Crawl Websites

    3️⃣ Extract Data

    4️⃣ Database

    5️⃣ Analytics

    6️⃣ Export
    """)

    st.markdown("---")

    st.markdown("### System Status")

    try:

        st.success(
            streamlit_status()
        )

    except Exception:

        st.error(
            "GROQ Not Connected"
        )

# =====================================================
# HEADER
# =====================================================

st.title("🎓 VTU College Intelligence Platform")

st.caption(
    f"Version {APP_VERSION}"
)

st.markdown("""
AI-Powered VTU College Intelligence System

Features:

✅ VTU Affiliated College Collection

✅ Website Discovery

✅ Crawl4AI Website Crawling

✅ GROQ AI Extraction

✅ SQLite Database

✅ Analytics Dashboard

✅ CSV / Excel / JSON Export
""")

# =====================================================
# LOAD DATA
# =====================================================

try:

    colleges_df = get_all_colleges()

except Exception:

    colleges_df = pd.DataFrame()

try:

    crawl_df = get_crawl_results()

except Exception:

    crawl_df = pd.DataFrame()

try:

    extracted_df = get_extracted_table()

except Exception:

    extracted_df = pd.DataFrame()

# =====================================================
# METRICS
# =====================================================

st.markdown("---")

st.subheader("📊 Platform Statistics")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Colleges",
    len(colleges_df)
)

c2.metric(
    "Crawled Sites",
    len(crawl_df)
)

c3.metric(
    "Extracted Records",
    len(extracted_df)
)

try:

    stats = get_statistics()

    total_records = (
        stats["colleges"]
        +
        stats["crawl_results"]
        +
        stats["extracted_details"]
    )

except Exception:

    total_records = 0

c4.metric(
    "Total Records",
    total_records
)

# =====================================================
# DATABASE STATUS
# =====================================================

st.markdown("---")

st.subheader("🗄 Database Status")

try:

    db_stats = get_database_stats()

    db_df = pd.DataFrame({

        "Table": list(
            db_stats.keys()
        ),

        "Records": list(
            db_stats.values()
        )

    })

    st.dataframe(
        db_df,
        use_container_width=True
    )

except Exception as e:

    st.error(
        f"Database Error: {e}"
    )

# =====================================================
# DATA PREVIEW
# =====================================================

st.markdown("---")

tab1, tab2, tab3 = st.tabs(

    [

        "Colleges",

        "Crawl Results",

        "Extracted Data"

    ]

)

# -----------------------------------------------------

with tab1:

    st.subheader(
        "Collected Colleges"
    )

    if not colleges_df.empty:

        st.dataframe(
            colleges_df.head(100),
            use_container_width=True
        )

    else:

        st.info(
            "No colleges collected yet."
        )

# -----------------------------------------------------

with tab2:

    st.subheader(
        "Crawled Websites"
    )

    if not crawl_df.empty:

        st.dataframe(
            crawl_df.head(100),
            use_container_width=True
        )

    else:

        st.info(
            "No crawl data available."
        )

# -----------------------------------------------------

with tab3:

    st.subheader(
        "Extracted College Data"
    )

    if not extracted_df.empty:

        st.dataframe(
            extracted_df.head(100),
            use_container_width=True
        )

    else:

        st.info(
            "No extracted records available."
        )

# =====================================================
# PROJECT WORKFLOW
# =====================================================

st.markdown("---")

st.subheader("🔄 Workflow")

st.markdown("""

### Step 1
Collect VTU Affiliated Colleges

⬇

### Step 2
Discover College Websites

⬇

### Step 3
Crawl Websites using Crawl4AI

⬇

### Step 4
Extract Information using GROQ

⬇

### Step 5
Store Results in SQLite

⬇

### Step 6
Analyze & Export Data

""")

# =====================================================
# TECHNOLOGY STACK
# =====================================================

st.markdown("---")

st.subheader("⚙ Technology Stack")

tech_df = pd.DataFrame({

    "Component": [

        "Frontend",
        "Crawler",
        "AI Extraction",
        "Database",
        "Analytics",
        "Deployment"

    ],

    "Technology": [

        "Streamlit",
        "Crawl4AI",
        "GROQ Llama 3.3 70B",
        "SQLite",
        "Pandas + Plotly",
        "Streamlit Cloud"

    ]

})

st.dataframe(
    tech_df,
    use_container_width=True
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "VTU College Intelligence Platform | Crawl4AI + GROQ + SQLite"
)
