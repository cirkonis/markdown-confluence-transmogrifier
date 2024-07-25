# app.py

import argparse
import config


def main():
    parser = argparse.ArgumentParser(description='Run the Markdown Confluence Transmogrifier in the specified mode.')
    parser.add_argument('--token', help='Token with "" is mandatory')
    parser.add_argument('--confluence_space', help='Confluence space')
    parser.add_argument('--confluence_base_url', help='Confluence base URL')
    parser.add_argument('--confluence_parent_id', help='Confluence parent ID')
    parser.add_argument('--markdown_documentation_directory', help='Markdown documentation directory')
    parser.add_argument('--documentation_image_directory', help='Documentation image directory')

    args = parser.parse_args()

    # Override config values with command-line arguments if provided
    config.CONFLUENCE_TOKEN = args.token or config.CONFLUENCE_TOKEN
    config.CONFLUENCE_SPACE = args.confluence_space or config.CONFLUENCE_SPACE
    config.CONFLUENCE_BASE_URL = args.confluence_base_url or config.CONFLUENCE_BASE_URL
    config.CONFLUENCE_PARENT_ID = args.confluence_parent_id or config.CONFLUENCE_PARENT_ID
    config.MARKDOWN_DOCUMENTATION_DIRECTORY = args.markdown_documentation_directory or config.MARKDOWN_DOCUMENTATION_DIRECTORY
    config.DOCUMENTATION_IMAGE_DIRECTORY = args.documentation_image_directory or config.DOCUMENTATION_IMAGE_DIRECTORY

    # Validate that all required Confluence configuration values are provided

    if not all([config.CONFLUENCE_TOKEN, config.CONFLUENCE_SPACE, config.CONFLUENCE_BASE_URL,
                config.CONFLUENCE_PARENT_ID]):
        raise ValueError(
            "All Confluence-related configuration values (token, space, base URL, parent ID) must be provided either "
            "via command-line arguments or environment variables.")

    print(f"App Name: {config.APP_NAME}")
    print(f"Logging Level: {config.LOGGING_LEVEL}")
    print(f"Confluence Token: {config.CONFLUENCE_TOKEN}")
    print(f"Confluence Base URL: {config.CONFLUENCE_BASE_URL}")
    print(f"Confluence Space: {config.CONFLUENCE_SPACE}")
    print(f"Confluence Parent ID: {config.CONFLUENCE_PARENT_ID}")


if __name__ == "__main__":
    main()
