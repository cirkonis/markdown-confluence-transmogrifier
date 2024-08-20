import os

import pytest
import logging

from functions.confluence_attach_file import confluence_attach_file
from functions.confluence_create_page import confluence_create_page
from functions.confluence_delete_pages import confluence_delete_pages
from functions.confluence_get_pages import confluence_get_pages
from functions.set_auth_headers import set_auth_headers
import config


@pytest.fixture(scope="session")
def setup_logging():
    logging.basicConfig(level=config.LOGGING_LEVEL.upper())
    logging.info("Logging is set up.")


@pytest.fixture(scope="session")
def setup_auth():
    set_auth_headers()
    return config.CONFLUENCE_AUTH_HEADERS


def test_create_page(setup_logging, setup_auth):
    title = "Integration Test Page"
    content = "<p>Content for integration test page.</p>"

    # Create page
    page_id = confluence_create_page(title, content, config.CONFLUENCE_PARENT_ID)

    assert page_id is not None, "Failed to create page, page_id is None"
    logging.info(f"Created page ID: {page_id}")

    # Verify the page exists
    page_ids = confluence_get_pages(config.CONFLUENCE_PARENT_ID)
    assert page_id in page_ids, "Created page ID not found in parent page's child pages"

    # Clean up
    deleted_pages = confluence_delete_pages([page_id])
    assert page_id in deleted_pages, "Failed to delete the created page"


def test_get_pages(setup_logging, setup_auth):
    page_ids = confluence_get_pages(config.CONFLUENCE_PARENT_ID)
    assert isinstance(page_ids, list), "Expected page_ids to be a list"
    logging.info(f"Fetched page IDs: {page_ids}")


def test_delete_pages(setup_logging, setup_auth):
    title = "Integration Test Page for Deletion"
    content = "<p>Content for deletion test page.</p>"

    # Create page
    page_id = confluence_create_page(title, content, config.CONFLUENCE_PARENT_ID)
    assert page_id is not None, "Failed to create page, page_id is None"
    logging.info(f"Created page ID: {page_id}")

    # Delete page
    deleted_pages = confluence_delete_pages([page_id])
    assert page_id in deleted_pages, "Failed to delete the page"
    logging.info(f"Deleted page IDs: {deleted_pages}")

    # Verify the page is deleted
    page_ids = confluence_get_pages(config.CONFLUENCE_PARENT_ID)
    assert page_id not in page_ids, "Deleted page ID still found in parent page's child pages"


def test_attach_file(setup_logging, setup_auth):
    title = "Integration Test Page for Attachment"
    content = "<p>Content for attachment test page.</p>"

    # Create page
    page_id = confluence_create_page(title, content, config.CONFLUENCE_PARENT_ID)
    assert page_id is not None, "Failed to create page, page_id is None"
    logging.info(f"Created page ID: {page_id}")

    try:
        # Path to the file to be attached (make sure the file exists at this path)
        file_path = os.path.join(config.DOCUMENTATION_IMAGE_DIRECTORY, "transmogrify.jpg")

        # Attach file
        with open(file_path, 'rb') as attached_file:
            attachment_id = confluence_attach_file(page_id, attached_file)
            assert attachment_id is not None, "Failed to attach file, attachment_id is None"
            logging.info(f"Attached file ID: {attachment_id}")

    finally:
        # Ensure the page is deleted regardless of the test outcome
        deleted_pages = confluence_delete_pages([page_id])
        assert page_id in deleted_pages, "Failed to delete the page"
        logging.info(f"Deleted page IDs: {deleted_pages}")