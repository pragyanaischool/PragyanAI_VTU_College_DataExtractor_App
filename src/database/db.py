# src/database/db.py

import os

from sqlalchemy import create_engine
from sqlalchemy import text

# ==========================================================
# DATABASE CONFIG
# ==========================================================

DATABASE_DIR = "data"
DATABASE_NAME = "vtu.db"

os.makedirs(
    DATABASE_DIR,
    exist_ok=True
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    DATABASE_NAME
)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# ==========================================================
# SQLALCHEMY ENGINE
# ==========================================================

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# ==========================================================
# TABLE DEFINITIONS
# ==========================================================

COLLEGES_TABLE = """
CREATE TABLE IF NOT EXISTS colleges (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    college_code TEXT UNIQUE,

    college_name TEXT,

    std_code TEXT,

    phone TEXT,

    rural_urban TEXT,

    district TEXT,

    website TEXT,

    email TEXT,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP

)
"""

CRAWL_RESULTS_TABLE = """
CREATE TABLE IF NOT EXISTS crawl_results (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    college_name TEXT,

    website TEXT,

    title TEXT,

    markdown TEXT,

    crawl_time REAL,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP

)
"""

EXTRACTED_DETAILS_TABLE = """
CREATE TABLE IF NOT EXISTS extracted_details (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    college_code TEXT,

    college_name TEXT,

    district TEXT,

    website TEXT,

    address TEXT,

    email TEXT,

    phone TEXT,

    principal TEXT,

    director TEXT,

    established_year TEXT,

    ownership_type TEXT,

    naac_grade TEXT,

    nba_status TEXT,

    nirf_rank TEXT,

    campus_area TEXT,

    student_strength TEXT,

    faculty_count TEXT,

    courses TEXT,

    departments TEXT,

    placement_percentage TEXT,

    highest_package TEXT,

    average_package TEXT,

    recruiters TEXT,

    research_centers TEXT,

    patents TEXT,

    linkedin TEXT,

    facebook TEXT,

    instagram TEXT,

    youtube TEXT,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP

)
"""

# ==========================================================
# CREATE TABLES
# ==========================================================

def create_tables():

    with engine.begin() as conn:

        conn.execute(
            text(COLLEGES_TABLE)
        )

        conn.execute(
            text(CRAWL_RESULTS_TABLE)
        )

        conn.execute(
            text(EXTRACTED_DETAILS_TABLE)
        )

# ==========================================================
# DATABASE MIGRATION
# ==========================================================

def migrate_database():

    try:

        with engine.begin() as conn:

            columns = conn.execute(
                text(
                    "PRAGMA table_info(colleges)"
                )
            ).fetchall()

            existing_columns = [
                column[1]
                for column in columns
            ]

            if "std_code" not in existing_columns:

                conn.execute(
                    text(
                        """
                        ALTER TABLE colleges
                        ADD COLUMN std_code TEXT
                        """
                    )
                )

                print(
                    "Added column: std_code"
                )

            if "rural_urban" not in existing_columns:

                conn.execute(
                    text(
                        """
                        ALTER TABLE colleges
                        ADD COLUMN rural_urban TEXT
                        """
                    )
                )

                print(
                    "Added column: rural_urban"
                )

            if "phone" not in existing_columns:

                conn.execute(
                    text(
                        """
                        ALTER TABLE colleges
                        ADD COLUMN phone TEXT
                        """
                    )
                )

            if "district" not in existing_columns:

                conn.execute(
                    text(
                        """
                        ALTER TABLE colleges
                        ADD COLUMN district TEXT
                        """
                    )
                )

            if "website" not in existing_columns:

                conn.execute(
                    text(
                        """
                        ALTER TABLE colleges
                        ADD COLUMN website TEXT
                        """
                    )
                )

            if "email" not in existing_columns:

                conn.execute(
                    text(
                        """
                        ALTER TABLE colleges
                        ADD COLUMN email TEXT
                        """
                    )
                )

    except Exception as e:

        print(
            f"Migration Error: {e}"
        )

# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def initialize_database():

    try:

        create_tables()

        migrate_database()

        print(
            "Database Initialized"
        )

    except Exception as e:

        print(
            f"Database Error: {e}"
        )

# ==========================================================
# RESET DATABASE
# ==========================================================

def reset_database():

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

    create_tables()

    migrate_database()

# ==========================================================
# TABLE EXISTS
# ==========================================================

def table_exists(table_name):

    query = """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    AND name=:table_name
    """

    with engine.connect() as conn:

        result = conn.execute(
            text(query),
            {
                "table_name": table_name
            }
        )

        return result.fetchone() is not None

# ==========================================================
# DATABASE STATS
# ==========================================================

def get_database_stats():

    tables = [
        "colleges",
        "crawl_results",
        "extracted_details"
    ]

    stats = {}

    with engine.connect() as conn:

        for table in tables:

            try:

                count = conn.execute(
                    text(
                        f"SELECT COUNT(*) FROM {table}"
                    )
                ).scalar()

                stats[table] = count

            except Exception:

                stats[table] = 0

    return stats

# ==========================================================
# DATABASE INFO
# ==========================================================

def get_database_info():

    return {

        "database_path":
            DATABASE_PATH,

        "database_exists":
            os.path.exists(
                DATABASE_PATH
            ),

        "database_size_mb":
            round(
                (
                    os.path.getsize(
                        DATABASE_PATH
                    ) / (1024 * 1024)
                ),
                2
            )
            if os.path.exists(
                DATABASE_PATH
            )
            else 0

    }

# ==========================================================
# CONNECTION
# ==========================================================

def get_connection():

    return engine.connect()

# ==========================================================
# INITIALIZE ON IMPORT
# ==========================================================

initialize_database()

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print(
        get_database_info()
    )

    print(
        get_database_stats()
    )
    
