"""
src/database/crud.py

Database CRUD Operations
"""

import pandas as pd

from sqlalchemy import text

from src.database.db import (
    engine
)

# =====================================================
# COLLEGES TABLE
# =====================================================

def save_colleges(df):

    if df.empty:
        return

    df.to_sql(
        "colleges",
        engine,
        if_exists="append",
        index=False
    )


def get_all_colleges():

    try:

        query = """
        SELECT *
        FROM colleges
        ORDER BY college_name
        """

        return pd.read_sql(
            query,
            engine
        )

    except Exception:

        return pd.DataFrame()


def get_college_by_id(
    record_id
):

    try:

        query = f"""

        SELECT *

        FROM colleges

        WHERE id={record_id}

        """

        df = pd.read_sql(
            query,
            engine
        )

        if len(df):

            return df.iloc[0].to_dict()

        return {}

    except Exception:

        return {}


def delete_college(
    record_id
):

    with engine.begin() as conn:

        conn.execute(
            text("""
            DELETE FROM colleges
            WHERE id=:id
            """),
            {
                "id": record_id
            }
        )


def delete_all_colleges():

    with engine.begin() as conn:

        conn.execute(
            text("""
            DELETE FROM colleges
            """)
        )


# =====================================================
# CRAWL RESULTS
# =====================================================

def save_crawl_result(
    college_name,
    website,
    markdown,
    title="",
    crawl_time=0
):

    df = pd.DataFrame([{

        "college_name":
            college_name,

        "website":
            website,

        "title":
            title,

        "markdown":
            markdown,

        "crawl_time":
            crawl_time

    }])

    df.to_sql(
        "crawl_results",
        engine,
        if_exists="append",
        index=False
    )


def get_crawl_results():

    try:

        query = """

        SELECT *

        FROM crawl_results

        ORDER BY id DESC

        """

        return pd.read_sql(
            query,
            engine
        )

    except Exception:

        return pd.DataFrame()


def get_crawl_result_by_id(
    record_id
):

    try:

        query = f"""

        SELECT *

        FROM crawl_results

        WHERE id={record_id}

        """

        df = pd.read_sql(
            query,
            engine
        )

        if len(df):

            return df.iloc[0].to_dict()

        return {}

    except Exception:

        return {}


def delete_crawl_result(
    record_id
):

    with engine.begin() as conn:

        conn.execute(
            text("""
            DELETE FROM crawl_results
            WHERE id=:id
            """),
            {
                "id": record_id
            }
        )


def delete_all_crawl_results():

    with engine.begin() as conn:

        conn.execute(
            text("""
            DELETE FROM crawl_results
            """)
        )


# =====================================================
# EXTRACTED DETAILS
# =====================================================

def save_extracted_data(
    data
):

    if not data:
        return

    df = pd.DataFrame(
        [data]
    )

    # Convert lists to strings

    for col in df.columns:

        if isinstance(
            df.iloc[0][col],
            list
        ):

            df[col] = df[col].apply(
                lambda x: ", ".join(
                    map(str, x)
                )
                if isinstance(x, list)
                else ""
            )

    df.to_sql(
        "extracted_details",
        engine,
        if_exists="append",
        index=False
    )


def bulk_save_extracted_data(
    data_list
):

    if not data_list:
        return

    df = pd.DataFrame(
        data_list
    )

    df.to_sql(
        "extracted_details",
        engine,
        if_exists="append",
        index=False
    )


def get_extracted_table():

    try:

        query = """

        SELECT *

        FROM extracted_details

        ORDER BY id DESC

        """

        return pd.read_sql(
            query,
            engine
        )

    except Exception:

        return pd.DataFrame()


def get_extracted_record(
    record_id
):

    try:

        query = f"""

        SELECT *

        FROM extracted_details

        WHERE id={record_id}

        """

        df = pd.read_sql(
            query,
            engine
        )

        if len(df):

            return df.iloc[0].to_dict()

        return {}

    except Exception:

        return {}


def update_extracted_record(
    record_id,
    update_data
):

    if not update_data:
        return

    fields = []

    params = {
        "id": record_id
    }

    for key, value in update_data.items():

        fields.append(
            f"{key} = :{key}"
        )

        params[key] = str(value)

    query = f"""

    UPDATE extracted_details

    SET {', '.join(fields)}

    WHERE id = :id

    """

    with engine.begin() as conn:

        conn.execute(
            text(query),
            params
        )


def delete_extracted_record(
    record_id
):

    with engine.begin() as conn:

        conn.execute(
            text("""
            DELETE FROM extracted_details
            WHERE id=:id
            """),
            {
                "id": record_id
            }
        )


def delete_all_extracted_records():

    with engine.begin() as conn:

        conn.execute(
            text("""
            DELETE FROM extracted_details
            """)
        )


# =====================================================
# SEARCH
# =====================================================

def search_colleges(
    keyword
):

    try:

        query = """

        SELECT *

        FROM extracted_details

        WHERE
            college_name LIKE :keyword
            OR district LIKE :keyword
            OR website LIKE :keyword
            OR email LIKE :keyword

        """

        return pd.read_sql(

            text(query),

            engine,

            params={
                "keyword":
                    f"%{keyword}%"
            }

        )

    except Exception:

        return pd.DataFrame()


# =====================================================
# ANALYTICS
# =====================================================

def get_statistics():

    stats = {}

    with engine.connect() as conn:

        stats["colleges"] = conn.execute(

            text(
                "SELECT COUNT(*) FROM colleges"
            )

        ).scalar()

        stats["crawl_results"] = conn.execute(

            text(
                "SELECT COUNT(*) FROM crawl_results"
            )

        ).scalar()

        stats["extracted_details"] = conn.execute(

            text(
                "SELECT COUNT(*) FROM extracted_details"
            )

        ).scalar()

    return stats


# =====================================================
# DATABASE HEALTH
# =====================================================

def database_health():

    stats = get_statistics()

    return pd.DataFrame({

        "Table": [

            "colleges",

            "crawl_results",

            "extracted_details"

        ],

        "Rows": [

            stats["colleges"],

            stats["crawl_results"],

            stats["extracted_details"]

        ]

    })


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print(
        get_statistics()
    )

    print(
        database_health()
    )
  
