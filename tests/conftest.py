# tests/conftest.py
import sys
import os
import pytest
import requests
from urllib3.exceptions import InsecureRequestWarning

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="session", autouse=True)
def disable_insecure_request_warnings():
    # Suppress only the single warning from urllib3 needed.
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
