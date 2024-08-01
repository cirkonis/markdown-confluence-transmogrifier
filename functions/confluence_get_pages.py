import config
import logging
import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def confluence_get_pages(page_id):
    # Initialize list to store page IDs
    all_page_ids = []

    # Define function to recursively fetch pages
    url = f"{config.CONFLUENCE_BASE_URL}content/{page_id}/child/page"
    logging.info('fetch pages URL: ' + url)
    response = requests.get(url, headers=config.CONFLUENCE_AUTH_HEADERS)

    if response.status_code == 401:
        logging.error("Unauthorized access - check your authentication headers")
        logging.error("Response content: " + response.text)
        return []

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        logging.error("Failed to decode JSON response")
        logging.error("Response content: " + response.text)
        return []

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

    logging.info('Pages found: ' + str(all_page_ids))

    return all_page_ids
