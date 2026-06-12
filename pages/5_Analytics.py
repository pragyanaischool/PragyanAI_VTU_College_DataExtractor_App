import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.database.crud import (
    get_extracted_table
)

# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------
# TITLE
# ----------------------------------------

st.title("📊 VTU College Analytics Dashboard")

st.markdown("""
Analyze VTU affiliated colleges extracted from Crawl4AI and GROQ.
""")

# ----------------------------------------
# LOAD DATA
# ----------------------------------------

df = get_extracted_table()

if df.empty:

    st.warning(
        "No extracted data available."
    )

    st.stop()

# ----------------------------------------
# CLEAN DATA
# ----------------------------------------

df = df.fillna("Unknown")

# ----------------------------------------
# FILTERS
# ----------------------------------------

st.sidebar.header("Filters")

if "district" in df.columns:

    districts = sorted(
        df["district"]
        .astype(str)
        .unique()
        .tolist()
    )

    selected_district = st.sidebar.multiselect(
        "District",
        districts,
        default=districts
    )

    df = df[
        df["district"]
        .isin(selected_district)
    ]

# ----------------------------------------
# KPIs
# ----------------------------------------

st.subheader("📈 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Colleges",
    len(df)
)

if "district" in df.columns:

    c2.metric(
        "Districts",
        df["district"].nunique()
    )

if "naac_grade" in df.columns:

    c3.metric(
        "NAAC Grades",
        df["naac_grade"].nunique()
    )

if "courses" in df.columns:

    c4.metric(
        "Course Records",
        len(df)
    )

st.markdown("---")

# ----------------------------------------
# DISTRICT ANALYSIS
# ----------------------------------------

if "district" in df.columns:

    st.subheader(
        "🏙 District Wise Colleges"
    )

    district_df = (
        df.groupby("district")
        .size()
        .reset_index(name="count")
        .sort_values(
            "count",
            ascending=False
        )
    )

    fig = px.bar(
        district_df,
        x="district",
        y="count",
        title="District Wise College Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------------
# NAAC ANALYSIS
# ----------------------------------------

if "naac_grade" in df.columns:

    st.subheader(
        "🏅 NAAC Grade Distribution"
    )

    naac_df = (
        df.groupby("naac_grade")
        .size()
        .reset_index(name="count")
    )

    fig = px.pie(
        naac_df,
        names="naac_grade",
        values="count",
        title="NAAC Grade Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------------
# NBA ANALYSIS
# ----------------------------------------

if "nba_status" in df.columns:

    st.subheader(
        "🎓 NBA Accreditation"
    )

    nba_df = (
        df.groupby("nba_status")
        .size()
        .reset_index(name="count")
    )

    fig = px.pie(
        nba_df,
        names="nba_status",
        values="count",
        title="NBA Accreditation Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------------
# PLACEMENT ANALYSIS
# ----------------------------------------

if "placement_percentage" in df.columns:

    st.subheader(
        "💼 Placement Percentage"
    )

    placement_df = df.copy()

    placement_df[
        "placement_percentage"
    ] = pd.to_numeric(
        placement_df[
            "placement_percentage"
        ],
        errors="coerce"
    )

    placement_df = placement_df.dropna(
        subset=[
            "placement_percentage"
        ]
    )

    if not placement_df.empty:

        fig = px.histogram(
            placement_df,
            x="placement_percentage",
            nbins=20,
            title="Placement Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ----------------------------------------
# HIGHEST PACKAGE ANALYSIS
# ----------------------------------------

if "highest_package" in df.columns:

    st.subheader(
        "💰 Highest Package Analysis"
    )

    package_df = df.copy()

    package_df[
        "highest_package"
    ] = (
        package_df[
            "highest_package"
        ]
        .astype(str)
        .str.replace(
            "LPA",
            "",
            regex=False
        )
    )

    package_df[
        "highest_package"
    ] = pd.to_numeric(
        package_df[
            "highest_package"
        ],
        errors="coerce"
    )

    package_df = package_df.dropna(
        subset=[
            "highest_package"
        ]
    )

    if not package_df.empty:

        top_package = (
            package_df
            .sort_values(
                "highest_package",
                ascending=False
            )
            .head(20)
        )

        fig = px.bar(
            top_package,
            x="college_name",
            y="highest_package",
            title="Top Colleges by Highest Package"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ----------------------------------------
# COURSE ANALYSIS
# ----------------------------------------

if "courses" in df.columns:

    st.subheader(
        "📚 Course Analysis"
    )

    course_counts = {}

    for item in df["courses"]:

        try:

            course_list = str(item).split(",")

            for course in course_list:

                course = course.strip()

                if course:

                    course_counts[
                        course
                    ] = (
                        course_counts.get(
                            course,
                            0
                        ) + 1
                    )

        except:
            pass

    if course_counts:

        course_df = pd.DataFrame(

            {
                "Course":
                course_counts.keys(),

                "Count":
                course_counts.values()
            }

        )

        course_df = course_df.sort_values(
            "Count",
            ascending=False
        )

        fig = px.bar(
            course_df.head(20),
            x="Course",
            y="Count",
            title="Top Courses"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ----------------------------------------
# RECRUITERS ANALYSIS
# ----------------------------------------

if "recruiters" in df.columns:

    st.subheader(
        "🏢 Recruiters Analysis"
    )

    recruiter_counts = {}

    for item in df["recruiters"]:

        try:

            companies = str(item).split(",")

            for company in companies:

                company = company.strip()

                if company:

                    recruiter_counts[
                        company
                    ] = (
                        recruiter_counts.get(
                            company,
                            0
                        ) + 1
                    )

        except:
            pass

    if recruiter_counts:

        recruiter_df = pd.DataFrame(

            {
                "Recruiter":
                recruiter_counts.keys(),

                "Count":
                recruiter_counts.values()
            }

        )

        recruiter_df = recruiter_df.sort_values(
            "Count",
            ascending=False
        )

        fig = px.bar(
            recruiter_df.head(20),
            x="Recruiter",
            y="Count",
            title="Most Common Recruiters"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ----------------------------------------
# DATA TABLE
# ----------------------------------------

st.markdown("---")

st.subheader(
    "📋 Analytics Dataset"
)

st.dataframe(
    df,
    use_container_width=True,
    height=400
)

# ----------------------------------------
# DOWNLOAD DATA
# ----------------------------------------

csv = df.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download Analytics Dataset",
    data=csv,
    file_name="analytics_dataset.csv",
    mime="text/csv"
)

# ----------------------------------------
# SUMMARY
# ----------------------------------------

st.markdown("---")

st.subheader(
    "📑 Summary"
)

summary = {

    "Total Colleges":
    len(df),

    "Districts":
    df["district"].nunique()
    if "district" in df.columns
    else 0,

    "NAAC Grades":
    df["naac_grade"].nunique()
    if "naac_grade" in df.columns
    else 0

}

st.json(summary)

# ----------------------------------------
# FOOTER
# ----------------------------------------

st.markdown("---")

st.caption(
    "VTU College Intelligence Platform | Analytics Dashboard"
)
