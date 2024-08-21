import config
import json
import logging
import requests


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