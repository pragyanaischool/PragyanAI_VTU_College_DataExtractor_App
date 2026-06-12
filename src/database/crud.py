"""
src/database/crud.py

CRUD Operations for VTU College Intelligence
"""

import pandas as pd

from sqlalchemy import text

from src.database.db import engine


# =====================================================
# COLLEGES
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

        return pd.read_sql(
            """
            SELECT *
            FROM colleges
            ORDER BY college_name
            """,
            engine
        )

    except Exception as e:

        print(
            f"get_all_colleges Error: {e}"
        )

        return pd.DataFrame()


def delete_all_colleges():

    try:

        with engine.begin() as conn:

            conn.execute(
                text(
                    "DELETE FROM colleges"
                )
            )

    except Exception as e:

        print(
            f"delete_all_colleges Error: {e}"
        )


def delete_college(
    record_id
):

    try:

        with engine.begin() as conn:

            conn.execute(

                text(
                    """
                    DELETE FROM colleges
                    WHERE id=:id
                    """
                ),

                {
                    "id": record_id
                }

            )

    except Exception as e:

        print(
            f"delete_college Error: {e}"
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

    try:

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

    except Exception as e:

        print(
            f"save_crawl_result Error: {e}"
        )


def get_crawl_results():

    try:

        return pd.read_sql(

            """
            SELECT *
            FROM crawl_results
            ORDER BY id DESC
            """,

            engine

        )

    except Exception as e:

        print(
            f"get_crawl_results Error: {e}"
        )

        return pd.DataFrame()


def delete_all_crawl_results():

    try:

        with engine.begin() as conn:

            conn.execute(

                text(
                    """
                    DELETE FROM crawl_results
                    """
                )

            )

    except Exception as e:

        print(
            f"delete_all_crawl_results Error: {e}"
        )


# =====================================================
# EXTRACTED DETAILS
# =====================================================

def save_extracted_data(
    data
):

    try:

        if not data:

            return

        df = pd.DataFrame(
            [data]
        )

        # Convert lists to text

        for col in df.columns:

            value = df.iloc[0][col]

            if isinstance(
                value,
                list
            ):

                df[col] = df[col].apply(

                    lambda x:
                    ", ".join(
                        map(str, x)
                    )

                    if isinstance(
                        x,
                        list
                    )

                    else ""

                )

        df.to_sql(

            "extracted_details",

            engine,

            if_exists="append",

            index=False

        )

    except Exception as e:

        print(
            f"save_extracted_data Error: {e}"
        )


def bulk_save_extracted_data(
    data_list
):

    try:

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

    except Exception as e:

        print(
            f"bulk_save_extracted_data Error: {e}"
        )


def get_extracted_table():

    try:

        return pd.read_sql(

            """
            SELECT *
            FROM extracted_details
            ORDER BY id DESC
            """,

            engine

        )

    except Exception as e:

        print(
            f"get_extracted_table Error: {e}"
        )

        return pd.DataFrame()


def delete_all_extracted_records():

    try:

        with engine.begin() as conn:

            conn.execute(

                text(
                    """
                    DELETE FROM extracted_details
                    """
                )

            )

    except Exception as e:

        print(
            f"delete_all_extracted_records Error: {e}"
        )


def delete_extracted_record(
    record_id
):

    try:

        with engine.begin() as conn:

            conn.execute(

                text(
                    """
                    DELETE FROM extracted_details
                    WHERE id=:id
                    """
                ),

                {
                    "id": record_id
                }

            )

    except Exception as e:

        print(
            f"delete_extracted_record Error: {e}"
        )


# =====================================================
# SEARCH
# =====================================================

def search_colleges(
    keyword
):

    try:

        query = text(
            """
            SELECT *
            FROM extracted_details
            WHERE
            college_name LIKE :keyword
            OR district LIKE :keyword
            OR website LIKE :keyword
            OR email LIKE :keyword
            """
        )

        return pd.read_sql(

            query,

            engine,

            params={
                "keyword":
                    f"%{keyword}%"
            }

        )

    except Exception as e:

        print(
            f"search_colleges Error: {e}"
        )

        return pd.DataFrame()


# =====================================================
# STATS
# =====================================================

def get_statistics():

    stats = {

        "colleges": 0,

        "crawl_results": 0,

        "extracted_details": 0

    }

    try:

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

    except Exception as e:

        print(
            f"Statistics Error: {e}"
        )

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

    print()

    print(
        get_statistics()
    )

    print()

    print(
        database_health()
    )
    
