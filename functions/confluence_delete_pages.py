import logging

import requests

import config


def confluence_delete_pages(page_ids):

    deleted_pages = []

    for page_id in page_ids:
        logging.debug("Delete page: " + str(page_id))
        logging.debug("Calling delete URL: " + config.CONFLUENCE_BASE_URL + "content/" + str(page_id))
        response = requests.delete(
            url=config.CONFLUENCE_BASE_URL + "content/" + str(page_id),
            headers=config.CONFLUENCE_AUTH_HEADERS,
            verify=False)
        logging.debug("Delete status code: " + str(response.status_code))

    if response.status_code == 200:
        logging.debug(page_id + "- Page deleted successfully")
        deleted_pages.append(page_id)
    else:
        logging.error(page_id + "- Page has not been deleted")

    return deleted_pages



