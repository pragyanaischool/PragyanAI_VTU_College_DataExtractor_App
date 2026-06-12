# src/database/crud.py

import pandas as pd
from sqlalchemy import text

from src.database.db import engine


# ==========================================================
# COLLEGES
# ==========================================================

def save_colleges(df):
    """Save colleges to database."""

    if df.empty:
        return False

    required_columns = [
        "college_code",
        "college_name",
        "std_code",
        "phone",
        "rural_urban",
        "district",
        "website",
        "email"
    ]

    for column in required_columns:
        if column not in df.columns:
            df[column] = ""

    df = df[required_columns]

    df = df.drop_duplicates(
        subset=["college_code"]
    )

    df.to_sql(
        "colleges",
        con=engine,
        if_exists="append",
        index=False
    )

    return True


def get_all_colleges():
    """Get all colleges."""

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
    """Delete all colleges."""

    try:

        with engine.begin() as conn:

            conn.execute(
                text(
                    "DELETE FROM colleges"
                )
            )

        return True

    except Exception as e:

        print(
            f"delete_all_colleges Error: {e}"
        )

        return False


def delete_college(record_id):
    """Delete one college."""

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

        return True

    except Exception as e:

        print(
            f"delete_college Error: {e}"
        )

        return False


# ==========================================================
# CRAWL RESULTS
# ==========================================================

def save_crawl_result(
    college_name,
    website,
    markdown,
    title="",
    crawl_time=0
):
    """Save crawl result."""

    try:

        df = pd.DataFrame([
            {
                "college_name": college_name,
                "website": website,
                "title": title,
                "markdown": markdown,
                "crawl_time": crawl_time
            }
        ])

        df.to_sql(
            "crawl_results",
            con=engine,
            if_exists="append",
            index=False
        )

        return True

    except Exception as e:

        print(
            f"save_crawl_result Error: {e}"
        )

        return False


def get_crawl_results():
    """Get crawl results."""

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
    """Delete all crawl results."""

    try:

        with engine.begin() as conn:

            conn.execute(
                text(
                    """
                    DELETE FROM crawl_results
                    """
                )
            )

        return True

    except Exception as e:

        print(
            f"delete_all_crawl_results Error: {e}"
        )

        return False


# ==========================================================
# EXTRACTED DETAILS
# ==========================================================

def save_extracted_data(data):
    """Save extracted record."""

    try:

        if not data:
            return False

        df = pd.DataFrame([data])

        for column in df.columns:

            value = df.iloc[0][column]

            if isinstance(value, list):

                df[column] = df[column].apply(
                    lambda x: ", ".join(
                        map(str, x)
                    )
                    if isinstance(x, list)
                    else ""
                )

        df.to_sql(
            "extracted_details",
            con=engine,
            if_exists="append",
            index=False
        )

        return True

    except Exception as e:

        print(
            f"save_extracted_data Error: {e}"
        )

        return False


def bulk_save_extracted_data(data_list):
    """Save multiple extracted records."""

    try:

        if not data_list:
            return False

        df = pd.DataFrame(data_list)

        df.to_sql(
            "extracted_details",
            con=engine,
            if_exists="append",
            index=False
        )

        return True

    except Exception as e:

        print(
            f"bulk_save_extracted_data Error: {e}"
        )

        return False


def get_extracted_table():
    """Get extracted records."""

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
    """Delete all extracted records."""

    try:

        with engine.begin() as conn:

            conn.execute(
                text(
                    """
                    DELETE FROM extracted_details
                    """
                )
            )

        return True

    except Exception as e:

        print(
            f"delete_all_extracted_records Error: {e}"
        )

        return False


# ==========================================================
# SEARCH
# ==========================================================

def search_colleges(keyword):
    """Search extracted colleges."""

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


# ==========================================================
# STATISTICS
# ==========================================================

def get_statistics():
    """Database statistics."""

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


def database_health():
    """Database health report."""

    stats = get_statistics()

    return pd.DataFrame(
        {
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
        }
    )


if __name__ == "__main__":

    print(
        get_statistics()
    )

    print(
        database_health()
    )
    
    
