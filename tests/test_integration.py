import pytest
import config

from functions.confluence_create_page import confluence_create_page
from functions.confluence_delete_pages import confluence_delete_pages


import pytest
import requests
import config
from functions.confluence_create_page import confluence_create_page
from functions.confluence_delete_pages import confluence_delete_pages


@pytest.fixture(scope="session")
def setup_logging():
    import logging
    logging.basicConfig(level=config.LOGGING_LEVEL.upper(), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info("Logging is set up.")
    return logging


def test_create_page(setup_logging):
    logging = setup_logging
    title = "Integration Test Page"
    content = "<p>Content for integration test page.</p>"

    # Create page
    page_id = confluence_create_page(title, content, config.CONFLUENCE_PARENT_ID)

    assert page_id is not None, "Failed to create page, page_id is None"
    logging.info(f"Created page ID: {page_id}")

    # Clean up
    if page_id:
        confluence_delete_pages([page_id])
