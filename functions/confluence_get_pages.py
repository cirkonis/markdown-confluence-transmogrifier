import config
import logging
import requests


def confluence_get_pages(page_id):
    # Initialize list to store page IDs
    all_page_ids = []

    # Define function to recursively fetch pages
    url = f"{config.CONFLUENCE_BASE_URL}/content/{page_id}/child/page"
    logging.info('fetch pages URL: ' + url)
    response = requests.get(url, headers=config.CONFLUENCE_AUTH_HEADERS)
    data = response.json()

    # Check if 'results' key exists in data
    if 'results' in data:
        # Add IDs of current pages
        for page in data["results"]:
            all_page_ids.append(page["id"])
            # Check if page has child pages
            if 'children' in page.get('_expandable', {}):
                # Recursively fetch child pages
                confluence_get_pages(page["id"])
    else:
        # Log a warning if 'results' key is missing
        logging.warning("No 'results' key found in response")

    logging.info('Pages found: ' + str(all_page_ids))  # Moved logging outside of the fetch_pages function

    return all_page_ids
