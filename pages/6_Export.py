import streamlit as st
import pandas as pd
import json
import sqlite3
import zipfile
import tempfile
from io import BytesIO
from pathlib import Path

from src.database.crud import (
    get_all_colleges,
    get_crawl_results,
    get_extracted_table
)

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------

st.set_page_config(
    page_title="Export Center",
    page_icon="📤",
    layout="wide"
)

# -----------------------------------------
# TITLE
# -----------------------------------------

st.title("📤 Export Center")

st.markdown("""
Export VTU College Intelligence data in multiple formats.

Supported Formats:

✅ CSV

✅ Excel

✅ JSON

✅ SQLite Backup

✅ ZIP Package
""")

# -----------------------------------------
# LOAD DATA
# -----------------------------------------

colleges_df = get_all_colleges()
crawl_df = get_crawl_results()
extracted_df = get_extracted_table()

# -----------------------------------------
# SUMMARY
# -----------------------------------------

st.subheader("📊 Export Summary")

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

# -----------------------------------------
# DATASET SELECTION
# -----------------------------------------

dataset_option = st.selectbox(
    "Select Dataset",
    [
        "Colleges",
        "Crawl Results",
        "Extracted Data"
    ]
)

if dataset_option == "Colleges":

    df = colleges_df

elif dataset_option == "Crawl Results":

    df = crawl_df

else:

    df = extracted_df

if df.empty:

    st.warning(
        "No data available."
    )

    st.stop()

# -----------------------------------------
# PREVIEW
# -----------------------------------------

st.subheader("📋 Data Preview")

st.dataframe(
    df.head(100),
    use_container_width=True
)

# -----------------------------------------
# CSV EXPORT
# -----------------------------------------

st.markdown("---")

st.subheader("📄 CSV Export")

csv_data = df.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download CSV",
    data=csv_data,
    file_name=f"{dataset_option.lower().replace(' ','_')}.csv",
    mime="text/csv",
    use_container_width=True
)

# -----------------------------------------
# EXCEL EXPORT
# -----------------------------------------

st.subheader("📗 Excel Export")

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        index=False,
        sheet_name="Data"
    )

st.download_button(
    label="⬇ Download Excel",
    data=excel_buffer.getvalue(),
    file_name=f"{dataset_option.lower().replace(' ','_')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

# -----------------------------------------
# JSON EXPORT
# -----------------------------------------

st.subheader("📜 JSON Export")

json_data = df.to_json(
    orient="records",
    indent=4
)

st.download_button(
    label="⬇ Download JSON",
    data=json_data,
    file_name=f"{dataset_option.lower().replace(' ','_')}.json",
    mime="application/json",
    use_container_width=True
)

# -----------------------------------------
# SQLITE BACKUP
# -----------------------------------------

st.markdown("---")

st.subheader("🗄 SQLite Backup")

db_path = Path("data/vtu.db")

if db_path.exists():

    with open(
        db_path,
        "rb"
    ) as f:

        st.download_button(
            label="⬇ Download SQLite Database",
            data=f.read(),
            file_name="vtu.db",
            mime="application/octet-stream",
            use_container_width=True
        )

else:

    st.info(
        "Database file not found."
    )

# -----------------------------------------
# ZIP EXPORT
# -----------------------------------------

st.markdown("---")

st.subheader("📦 ZIP Export Package")

if st.button(
    "Generate ZIP Package",
    use_container_width=True
):

    zip_buffer = BytesIO()

    with zipfile.ZipFile(
        zip_buffer,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        # CSV

        zipf.writestr(
            "colleges.csv",
            colleges_df.to_csv(
                index=False
            )
        )

        zipf.writestr(
            "crawl_results.csv",
            crawl_df.to_csv(
                index=False
            )
        )

        zipf.writestr(
            "extracted_data.csv",
            extracted_df.to_csv(
                index=False
            )
        )

        # JSON

        zipf.writestr(
            "colleges.json",
            colleges_df.to_json(
                orient="records",
                indent=4
            )
        )

        zipf.writestr(
            "crawl_results.json",
            crawl_df.to_json(
                orient="records",
                indent=4
            )
        )

        zipf.writestr(
            "extracted_data.json",
            extracted_df.to_json(
                orient="records",
                indent=4
            )
        )

    st.download_button(
        label="⬇ Download ZIP Package",
        data=zip_buffer.getvalue(),
        file_name="vtu_export_package.zip",
        mime="application/zip",
        use_container_width=True
    )

# -----------------------------------------
# REPORT SUMMARY
# -----------------------------------------

st.markdown("---")

st.subheader("📈 Dataset Statistics")

stats = {

    "Total Colleges":
        len(colleges_df),

    "Total Crawled Websites":
        len(crawl_df),

    "Total Extracted Records":
        len(extracted_df),

    "Columns":
        len(df.columns),

    "Rows":
        len(df)

}

st.json(stats)

# -----------------------------------------
# COLUMN INFORMATION
# -----------------------------------------

st.subheader("🧾 Dataset Schema")

schema_df = pd.DataFrame({

    "Column":
        df.columns,

    "Data Type":
        [
            str(dtype)
            for dtype in df.dtypes
        ]

})

st.dataframe(
    schema_df,
    use_container_width=True
)

# -----------------------------------------
# RAW JSON VIEW
# -----------------------------------------

with st.expander(
    "View Raw JSON"
):

    st.code(
        json.dumps(
            json.loads(
                df.to_json(
                    orient="records"
                )
            ),
            indent=4
        ),
        language="json"
    )

# -----------------------------------------
# FOOTER
# -----------------------------------------

st.markdown("---")

st.caption(
    "VTU College Intelligence Platform | Export Center"
)
