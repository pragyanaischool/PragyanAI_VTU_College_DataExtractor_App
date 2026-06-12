"""
src/database/db.py

Database Initialization Module

Creates:

1. colleges
2. crawl_results
3. extracted_details

Database:
data/vtu.db
"""

from sqlalchemy import create_engine
from sqlalchemy import text

from src.utils.config import (
    SQLITE_CONNECTION_STRING
)

# =====================================================
# DATABASE ENGINE
# =====================================================

engine = create_engine(
    SQLITE_CONNECTION_STRING,
    echo=False,
    future=True
)

# =====================================================
# COLLEGES TABLE
# =====================================================

COLLEGES_TABLE_SQL = """

CREATE TABLE IF NOT EXISTS colleges (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    college_code TEXT,

    college_name TEXT,

    district TEXT,

    website TEXT,

    email TEXT,

    phone TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

"""

# =====================================================
# CRAWL RESULTS TABLE
# =====================================================

CRAWL_RESULTS_TABLE_SQL = """

CREATE TABLE IF NOT EXISTS crawl_results (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    college_name TEXT,

    website TEXT,

    title TEXT,

    markdown TEXT,

    crawl_time REAL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

"""

# =====================================================
# EXTRACTED DETAILS TABLE
# =====================================================

EXTRACTED_DETAILS_TABLE_SQL = """

CREATE TABLE IF NOT EXISTS extracted_details (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    college_name TEXT,

    college_code TEXT,

    district TEXT,

    website TEXT,

    address TEXT,

    email TEXT,

    phone TEXT,

    principal TEXT,

    director TEXT,

    naac_grade TEXT,

    nba_status TEXT,

    nirf_rank TEXT,

    courses TEXT,

    placement_percentage TEXT,

    highest_package TEXT,

    average_package TEXT,

    recruiters TEXT,

    linkedin TEXT,

    facebook TEXT,

    instagram TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

"""

# =====================================================
# CREATE TABLES
# =====================================================

def create_tables():

    with engine.begin() as conn:

        conn.execute(
            text(COLLEGES_TABLE_SQL)
        )

        conn.execute(
            text(CRAWL_RESULTS_TABLE_SQL)
        )

        conn.execute(
            text(EXTRACTED_DETAILS_TABLE_SQL)
        )

# =====================================================
# DATABASE INITIALIZATION
# =====================================================

def initialize_database():

    try:

        create_tables()

        print(
            "Database Initialized Successfully"
        )

    except Exception as e:

        print(
            f"Database Error: {e}"
        )

# =====================================================
# DROP TABLES
# =====================================================

def drop_tables():

    with engine.begin() as conn:

        conn.execute(
            text(
                "DROP TABLE IF EXISTS colleges"
            )
        )

        conn.execute(
            text(
                "DROP TABLE IF EXISTS crawl_results"
            )
        )

        conn.execute(
            text(
                "DROP TABLE IF EXISTS extracted_details"
            )
        )

# =====================================================
# RESET DATABASE
# =====================================================

def reset_database():

    drop_tables()

    create_tables()

# =====================================================
# TABLE EXISTS
# =====================================================

def table_exists(
    table_name
):

    query = f"""

    SELECT name

    FROM sqlite_master

    WHERE type='table'

    AND name='{table_name}'

    """

    with engine.connect() as conn:

        result = conn.execute(
            text(query)
        )

        return result.fetchone() is not None

# =====================================================
# DATABASE STATS
# =====================================================

def get_database_stats():

    stats = {}

    tables = [

        "colleges",

        "crawl_results",

        "extracted_details"

    ]

    with engine.connect() as conn:

        for table in tables:

            try:

                query = (
                    f"SELECT COUNT(*) "
                    f"FROM {table}"
                )

                count = conn.execute(
                    text(query)
                ).scalar()

                stats[table] = count

            except Exception:

                stats[table] = 0

    return stats

# =====================================================
# GET CONNECTION
# =====================================================

def get_connection():

    return engine.connect()

# =====================================================
# INITIALIZE ON IMPORT
# =====================================================

initialize_database()

# =====================================================
# DEBUG
# =====================================================

if __name__ == "__main__":

    initialize_database()

    print()

    print("Tables Created")

    print()

    print(
        "colleges:",
        table_exists(
            "colleges"
        )
    )

    print(
        "crawl_results:",
        table_exists(
            "crawl_results"
        )
    )

    print(
        "extracted_details:",
        table_exists(
            "extracted_details"
        )
    )

    print()

    print(
        get_database_stats()
    )
  
