import config
import json
import logging
import requests
import os


def attach_files_to_page(files_to_upload, page_id_for_file_attaching):
    for file_path in files_to_upload:
        # Logging the full image path (already resolved by transmogrify_images)
        logging.debug('IMAGE PATH: ' + file_path)
        if os.path.isfile(file_path):
            logging.info("Attaching file: " + file_path + "  to the page: " + str(page_id_for_file_attaching))
            with open(file_path, 'rb') as attached_file:
                confluence_attach_file(page_id_for_file_attaching, attached_file)
        else:
            logging.error("File: " + str(file_path) + "  not found. Nothing to attach")


def confluence_attach_file(page_id, file):
    # make call to attach file to a page
    logging.debug("Calling URL: " + config.CONFLUENCE_BASE_URL + "content/" + str(file) + "/child/attachment")

    file = {'file': file}

    # Extract the authorization header
    auth_header = config.CONFLUENCE_AUTH_HEADERS.get('Authorization')

    # Create specific headers for attaching the file
    headers = {
        "X-Atlassian-Token": "nocheck",
        "Authorization": auth_header
    }

    response = requests.post(
        url=config.CONFLUENCE_BASE_URL + "content/" + str(page_id) + "/child/attachment",
        files=file,
        headers=headers,
        verify=False)

    logging.debug(response.status_code)
    if response.status_code == 200:
        logging.debug("File was attached successfully")
        # logging.debug(json.dumps(json.loads(response.text), indent=4, sort_keys=True))
        # return id of the attached file
        logging.debug("Returning attached file id: " + json.loads(response.text)['results'][0]['id'])
        return json.loads(response.text)['results'][0]['id']
    else:
        logging.error(str(file) + " : File has not attached")