"""
src/utils/config.py

VTU College Intelligence Platform
Central Configuration File

Used By:
---------
- Database Layer
- Crawl4AI Layer
- GROQ Layer
- Streamlit Pages
- Export Modules
"""

from pathlib import Path
import os

# =====================================================
# PROJECT ROOT
# =====================================================

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# =====================================================
# FOLDERS
# =====================================================

DATA_DIR = ROOT_DIR / "data"
ASSETS_DIR = ROOT_DIR / "assets"

DATA_DIR.mkdir(exist_ok=True)

# =====================================================
# DATABASE
# =====================================================

DATABASE_NAME = "vtu.db"

DATABASE_PATH = DATA_DIR / DATABASE_NAME

SQLITE_CONNECTION_STRING = (
    f"sqlite:///{DATABASE_PATH}"
)

# =====================================================
# DATA FILES
# =====================================================

COLLEGES_CSV = (
    DATA_DIR / "colleges.csv"
)

EXTRACTED_DATA_CSV = (
    DATA_DIR / "extracted_data.csv"
)

# =====================================================
# EXPORT SETTINGS
# =====================================================

EXPORT_FOLDER = (
    DATA_DIR / "exports"
)

EXPORT_FOLDER.mkdir(
    exist_ok=True
)

# =====================================================
# TABLE NAMES
# =====================================================

COLLEGES_TABLE = "colleges"

CRAWL_RESULTS_TABLE = (
    "crawl_results"
)

EXTRACTED_TABLE = (
    "extracted_details"
)

# =====================================================
# VTU SETTINGS
# =====================================================

VTU_URL = (
    "https://vtu.ac.in/"
    "affiliated-institute/"
)

REQUEST_TIMEOUT = 60

# =====================================================
# CRAWL4AI SETTINGS
# =====================================================

CRAWL_TIMEOUT = 60

HEADLESS_BROWSER = True

MAX_CONCURRENT_CRAWLS = 5

WORD_COUNT_THRESHOLD = 10

REMOVE_OVERLAYS = True

SCAN_FULL_PAGE = True

CACHE_ENABLED = False

# =====================================================
# GROQ SETTINGS
# =====================================================

GROQ_MODEL = (
    "llama-3.3-70b-versatile"
)

GROQ_TEMPERATURE = 0.1

GROQ_MAX_TOKENS = 4000

# =====================================================
# EXTRACTION SETTINGS
# =====================================================

MAX_MARKDOWN_LENGTH = 50000

MAX_CHUNK_SIZE = 12000

CHUNK_OVERLAP = 500

MIN_TEXT_LENGTH = 100

# =====================================================
# STREAMLIT SETTINGS
# =====================================================

APP_NAME = (
    "VTU College Intelligence Platform"
)

APP_VERSION = "1.0.0"

PAGE_LAYOUT = "wide"

# =====================================================
# LOGO
# =====================================================

LOGO_PATH = (
    ASSETS_DIR / "logo.png"
)

# =====================================================
# EXPORT FORMATS
# =====================================================

SUPPORTED_EXPORTS = [

    "csv",
    "excel",
    "json",
    "sqlite",
    "zip"

]

# =====================================================
# EMAIL REGEX
# =====================================================

EMAIL_REGEX = (
    r"[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+"
    r"\.[A-Za-z]{2,}"
)

# =====================================================
# PHONE REGEX
# =====================================================

PHONE_REGEX = (
    r"(?:\+91[\-\s]?)?"
    r"[6-9]\d{9}"
)

# =====================================================
# URL REGEX
# =====================================================

URL_REGEX = (
    r"https?://"
    r"(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
)

# =====================================================
# SOCIAL DOMAINS
# =====================================================

SOCIAL_DOMAINS = {

    "linkedin":
        "linkedin.com",

    "facebook":
        "facebook.com",

    "instagram":
        "instagram.com",

    "twitter":
        "twitter.com",

    "youtube":
        "youtube.com"

}

# =====================================================
# DEFAULT EXTRACTION SCHEMA
# =====================================================

DEFAULT_COLLEGE_SCHEMA = {

    "college_name": "",

    "college_code": "",

    "district": "",

    "website": "",

    "address": "",

    "email": "",

    "phone": "",

    "principal": "",

    "director": "",

    "naac_grade": "",

    "nba_status": "",

    "nirf_rank": "",

    "courses": [],

    "placement_percentage": "",

    "highest_package": "",

    "average_package": "",

    "recruiters": [],

    "linkedin": "",

    "facebook": "",

    "instagram": ""

}

# =====================================================
# ENVIRONMENT VARIABLES
# =====================================================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    ""
)

# =====================================================
# HELPER FUNCTION
# =====================================================

def get_database_path():
    """
    Returns SQLite DB Path
    """
    return str(DATABASE_PATH)


def get_export_folder():
    """
    Returns Export Folder Path
    """
    return str(EXPORT_FOLDER)


def get_logo_path():
    """
    Returns Logo Path
    """
    return str(LOGO_PATH)


# =====================================================
# DEBUG
# =====================================================

if __name__ == "__main__":

    print("ROOT:", ROOT_DIR)

    print(
        "DATABASE:",
        DATABASE_PATH
    )

    print(
        "EXPORT:",
        EXPORT_FOLDER
    )

    print(
        "MODEL:",
        GROQ_MODEL
    )
  
