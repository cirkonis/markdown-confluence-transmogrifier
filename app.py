# app.py

import argparse
import config
import logging

from functions.confluence_delete_pages import confluence_delete_pages
from functions.confluence_get_pages import confluence_get_pages
from functions.set_auth_headers import set_auth_headers
from functions.transmogrify_documentation import transmogrify_documentation


def main():
    parser = argparse.ArgumentParser(description='Run the Markdown Confluence Transmogrifier in the specified mode.')
    parser.add_argument('--confluence_user', help='Confluence user')
    parser.add_argument('--confluence_personal_access_token', help='personal access token')
    parser.add_argument('--confluence_api_token', help='API token')
    parser.add_argument('--confluence_space', help='Confluence space')
    parser.add_argument('--confluence_base_url', help='Confluence base URL')
    parser.add_argument('--confluence_parent_id', help='Confluence parent ID')
    parser.add_argument('--markdown_documentation_directory', help='Markdown documentation directory')
    parser.add_argument('--documentation_image_directory', help='Documentation image directory')

    args = parser.parse_args()

    # Override config values with command-line arguments if provided
    config.CONFLUENCE_USER = args.confluence_user or config.CONFLUENCE_USER
    config.CONFLUENCE_PERSONAL_ACCESS_TOKEN = args.confluence_personal_access_token or config.CONFLUENCE_PERSONAL_ACCESS_TOKEN
    config.CONFLUENCE_API_TOKEN = args.confluence_api_token or config.CONFLUENCE_API_TOKEN
    config.CONFLUENCE_SPACE = args.confluence_space or config.CONFLUENCE_SPACE
    config.CONFLUENCE_BASE_URL = args.confluence_base_url or config.CONFLUENCE_BASE_URL
    config.CONFLUENCE_PARENT_ID = args.confluence_parent_id or config.CONFLUENCE_PARENT_ID
    config.MARKDOWN_DOCUMENTATION_DIRECTORY = args.markdown_documentation_directory or config.MARKDOWN_DOCUMENTATION_DIRECTORY
    config.DOCUMENTATION_IMAGE_DIRECTORY = args.documentation_image_directory or config.DOCUMENTATION_IMAGE_DIRECTORY

    """
    Configure the logging settings.
    """
    logging.basicConfig(
        level=config.LOGGING_LEVEL.upper(),  # Set logging level based on configuration
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # Output to console
        ]
    )

    logging.info(f"App Name: {config.APP_NAME}")
    logging.info(f"Logging Level: {config.LOGGING_LEVEL}")
    logging.info(f"Confluence Base URL: {config.CONFLUENCE_BASE_URL}")
    logging.info(f"Confluence Space: {config.CONFLUENCE_SPACE}")
    logging.info(f"Confluence Parent ID: {config.CONFLUENCE_PARENT_ID}")
    logging.info(f"Markdown Documentation Directory: {config.MARKDOWN_DOCUMENTATION_DIRECTORY}")
    logging.info(f"Documentation Image Directory: {config.DOCUMENTATION_IMAGE_DIRECTORY}")

    # Set authentication headers
    set_auth_headers()

    # THE MEAT AND POTATOES
    confluence_delete_pages(confluence_get_pages(config.CONFLUENCE_PARENT_ID))
    transmogrify_documentation(config.MARKDOWN_DOCUMENTATION_DIRECTORY, config.CONFLUENCE_PARENT_ID)


if __name__ == "__main__":
    main()
