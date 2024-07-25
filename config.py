# config.py

from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = "Markdown Confluence Transmogrifier"
CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN")
CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
CONFLUENCE_SPACE = os.getenv("CONFLUENCE_SPACE")
CONFLUENCE_PARENT_ID = os.getenv("CONFLUENCE_PARENT_ID")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")
