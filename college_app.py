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
# INITIALIZE DATABASE
# =====================================================

initialize_database()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🎓 VTU Intelligence")

    st.markdown("---")

    st.markdown("### Modules")

    st.markdown("""
    ✅ Collect Colleges

    ✅ Crawl Websites

    ✅ Extract Data

    ✅ Database

    ✅ Analytics

    ✅ Export
    """)

    st.markdown("---")

    st.markdown("### AI Status")

    try:

        status = streamlit_status()

        if "Connected" in status:

            st.success(status)

        else:

            st.warning(status)

    except Exception:

        st.error(
            "GROQ Not Connected"
        )

    st.markdown("---")

    st.markdown(
        f"Version: {APP_VERSION}"
    )

# =====================================================
# HEADER
# =====================================================

st.title(
    "🎓 VTU College Intelligence Platform"
)

st.markdown("""
AI-Powered Engineering College Intelligence Platform

This platform helps you:

- Collect VTU Affiliated Colleges
- Discover Official Websites
- Crawl College Websites
- Extract Structured Intelligence
- Store Information in SQLite
- Analyze Colleges
- Export Results
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
# TOP METRICS
# =====================================================

st.markdown("---")

st.subheader(
    "📊 Platform Statistics"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Colleges",
    len(colleges_df)
)

col2.metric(
    "Websites Crawled",
    len(crawl_df)
)

col3.metric(
    "Records Extracted",
    len(extracted_df)
)

try:

    stats = get_statistics()

    total_records = (

        stats.get(
            "colleges",
            0
        )

        +

        stats.get(
            "crawl_results",
            0
        )

        +

        stats.get(
            "extracted_details",
            0
        )

    )

except Exception:

    total_records = 0

col4.metric(
    "Total Records",
    total_records
)

# =====================================================
# DATABASE HEALTH
# =====================================================

st.markdown("---")

st.subheader(
    "🗄 Database Health"
)

try:

    db_stats = get_database_stats()

    db_df = pd.DataFrame({

        "Table":
            list(
                db_stats.keys()
            ),

        "Records":
            list(
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

        "Collected Colleges",

        "Crawled Websites",

        "Extracted Data"

    ]

)

# =====================================================
# COLLEGES
# =====================================================

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

# =====================================================
# CRAWLED DATA
# =====================================================

with tab2:

    st.subheader(
        "Website Crawl Results"
    )

    if not crawl_df.empty:

        st.dataframe(

            crawl_df.head(100),

            use_container_width=True

        )

    else:

        st.info(
            "No websites crawled yet."
        )

# =====================================================
# EXTRACTED DATA
# =====================================================

with tab3:

    st.subheader(
        "Extracted College Intelligence"
    )

    if not extracted_df.empty:

        st.dataframe(

            extracted_df.head(100),

            use_container_width=True

        )

    else:

        st.info(
            "No extracted data available."
        )

# =====================================================
# WORKFLOW
# =====================================================

st.markdown("---")

st.subheader(
    "🔄 Platform Workflow"
)

st.markdown("""

### Step 1
Collect VTU Affiliated Colleges

⬇

### Step 2
Discover Official Websites

⬇

### Step 3
Scrape Websites using ScrapeGraphAI

⬇

### Step 4
Extract Information using GROQ

⬇

### Step 5
Store in SQLite Database

⬇

### Step 6
Analytics & Export

""")

# =====================================================
# TECHNOLOGY STACK
# =====================================================

st.markdown("---")

st.subheader(
    "⚙ Technology Stack"
)

tech_df = pd.DataFrame({

    "Component": [

        "Frontend",

        "Website Scraping",

        "AI Extraction",

        "Database",

        "Analytics",

        "Deployment"

    ],

    "Technology": [

        "Streamlit",

        "ScrapeGraphAI + BeautifulSoup",

        "GROQ Llama 3.3 70B",

        "SQLite",

        "Pandas + Plotly",

        "Streamlit Community Cloud"

    ]

})

st.dataframe(
    tech_df,
    use_container_width=True
)

# =====================================================
# QUICK STATS
# =====================================================

st.markdown("---")

st.subheader(
    "📈 Quick Insights"
)

if not extracted_df.empty:

    col1, col2 = st.columns(2)

    with col1:

        if "district" in extracted_df.columns:

            st.write(
                "Unique Districts"
            )

            st.metric(

                "Districts",

                extracted_df[
                    "district"
                ].nunique()

            )

    with col2:

        if "naac_grade" in extracted_df.columns:

            st.write(
                "NAAC Grades Available"
            )

            st.metric(

                "Grades",

                extracted_df[
                    "naac_grade"
                ].nunique()

            )

else:

    st.info(
        "Run extraction to generate analytics."
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "VTU College Intelligence Platform | Streamlit + ScrapeGraphAI + GROQ + SQLite"
)

