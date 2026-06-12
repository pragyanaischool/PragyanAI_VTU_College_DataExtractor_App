import streamlit as st
import pandas as pd
from datetime import datetime

from src.database.crud import (
    get_all_colleges,
    get_crawl_results,
    get_extracted_table,
    delete_college,
    delete_extracted_record,
    update_extracted_record
)

# ------------------------------------
# PAGE CONFIG
# ------------------------------------

st.set_page_config(
    page_title="Database Manager",
    page_icon="🗄",
    layout="wide"
)

# ------------------------------------
# TITLE
# ------------------------------------

st.title("🗄 Database Manager")

st.markdown("""
Manage VTU College Database

Features:

✅ View Data

✅ Search

✅ Filter

✅ Edit Records

✅ Delete Records

✅ Export Current View
""")

# ------------------------------------
# LOAD DATA
# ------------------------------------

colleges_df = get_all_colleges()
crawl_df = get_crawl_results()
extracted_df = get_extracted_table()

# ------------------------------------
# SUMMARY
# ------------------------------------

st.subheader("📈 Database Statistics")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Colleges",
    len(colleges_df)
)

c2.metric(
    "Crawled",
    len(crawl_df)
)

c3.metric(
    "Extracted",
    len(extracted_df)
)

st.markdown("---")

# ------------------------------------
# TABLE SELECTION
# ------------------------------------

table_option = st.selectbox(
    "Select Table",
    [
        "Colleges",
        "Crawl Results",
        "Extracted Data"
    ]
)

# ------------------------------------
# CHOOSE DATAFRAME
# ------------------------------------

if table_option == "Colleges":

    df = colleges_df.copy()

elif table_option == "Crawl Results":

    df = crawl_df.copy()

else:

    df = extracted_df.copy()

# ------------------------------------
# EMPTY CHECK
# ------------------------------------

if df.empty:

    st.warning(
        "No records found."
    )

    st.stop()

# ------------------------------------
# SEARCH
# ------------------------------------

st.subheader("🔍 Search")

search_text = st.text_input(
    "Search Records"
)

if search_text:

    mask = pd.Series(
        False,
        index=df.index
    )

    for col in df.columns:

        try:

            mask = (
                mask |
                df[col]
                .astype(str)
                .str.contains(
                    search_text,
                    case=False,
                    na=False
                )
            )

        except:
            pass

    df = df[mask]

# ------------------------------------
# DISTRICT FILTER
# ------------------------------------

if "district" in df.columns:

    districts = sorted(
        df["district"]
        .dropna()
        .unique()
        .tolist()
    )

    district = st.selectbox(
        "Filter District",
        ["All"] + districts
    )

    if district != "All":

        df = df[
            df["district"] == district
        ]

# ------------------------------------
# DATAFRAME VIEW
# ------------------------------------

st.subheader("📋 Records")

st.dataframe(
    df,
    use_container_width=True,
    height=500
)

# ------------------------------------
# EXPORT
# ------------------------------------

csv = df.to_csv(
    index=False
)

st.download_button(
    "⬇ Download Current View",
    csv,
    f"{table_option}.csv",
    "text/csv"
)

# ------------------------------------
# VIEW RECORD DETAILS
# ------------------------------------

st.markdown("---")

st.subheader("🔎 Record Details")

record_index = st.number_input(
    "Row Number",
    min_value=0,
    max_value=max(
        len(df)-1,
        0
    ),
    value=0
)

selected_record = df.iloc[
    record_index
]

st.json(
    selected_record.to_dict()
)

# ------------------------------------
# EDIT SECTION
# ------------------------------------

if table_option == "Extracted Data":

    st.markdown("---")

    st.subheader("✏ Edit Record")

    record_id = selected_record.get(
        "id",
        None
    )

    if record_id:

        college_name = st.text_input(
            "College Name",
            selected_record.get(
                "college_name",
                ""
            )
        )

        district = st.text_input(
            "District",
            selected_record.get(
                "district",
                ""
            )
        )

        email = st.text_input(
            "Email",
            selected_record.get(
                "email",
                ""
            )
        )

        phone = st.text_input(
            "Phone",
            selected_record.get(
                "phone",
                ""
            )
        )

        website = st.text_input(
            "Website",
            selected_record.get(
                "website",
                ""
            )
        )

        naac = st.text_input(
            "NAAC Grade",
            selected_record.get(
                "naac_grade",
                ""
            )
        )

        if st.button(
            "💾 Update Record"
        ):

            update_extracted_record(

                record_id,

                {
                    "college_name": college_name,
                    "district": district,
                    "email": email,
                    "phone": phone,
                    "website": website,
                    "naac_grade": naac
                }

            )

            st.success(
                "Record Updated"
            )

            st.rerun()

# ------------------------------------
# DELETE SECTION
# ------------------------------------

st.markdown("---")

st.subheader("🗑 Delete Record")

delete_id = st.number_input(
    "Record ID",
    min_value=1,
    step=1
)

if st.button(
    "Delete Record"
):

    try:

        if table_option == "Colleges":

            delete_college(
                delete_id
            )

        elif table_option == "Extracted Data":

            delete_extracted_record(
                delete_id
            )

        st.success(
            "Record Deleted"
        )

        st.rerun()

    except Exception as e:

        st.error(str(e))

# ------------------------------------
# DATABASE HEALTH
# ------------------------------------

st.markdown("---")

st.subheader("⚙ Database Health")

health_df = pd.DataFrame({

    "Table": [

        "colleges",
        "crawl_results",
        "extracted_details"

    ],

    "Rows": [

        len(colleges_df),
        len(crawl_df),
        len(extracted_df)

    ]

})

st.dataframe(
    health_df,
    use_container_width=True
)

# ------------------------------------
# FOOTER
# ------------------------------------

st.markdown("---")

st.caption(
    f"Updated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

st.caption(
    "VTU College Intelligence Platform | Database Manager"
)
