import logging
import json
import requests
import config
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def confluence_create_page(title, content, parent_page_id):
    # describe json query
    new_page_json_query_string = """
       {
           "type": "page",
           "title": "DEFAULT PAGE TITLE",
           "ancestors": [
               {
               "id": 111
               }
           ],
           "space": {
               "key": "DEFAULT KEY"
           },
           "body": {
               "storage": {
                   "value": "DEFAULT PAGE CONTENT",
                   "representation": "storage"
               }
           }
       }
       """

    # load json from string
    new_page_json_query = json.loads(new_page_json_query_string)

    # the key of Confluence space for content publishing
    new_page_json_query['space']['key'] = config.CONFLUENCE_SPACE

    # check of input of the ParentPageID
    if parent_page_id is None:
        new_page_json_query['ancestors'][0]['id'] = config.CONFLUENCE_PARENT_ID  # this is the root of out pages tree
    else:
        new_page_json_query['ancestors'][0]['id'] = str(parent_page_id)  # this is the branch of our tree

    new_page_json_query['title'] = title

    # Add content to the body of the page directly (no wrapping in <p> or other tags)
    new_page_json_query['body']['storage']['value'] = content

    logging.info("Create new page: " + new_page_json_query['title'])

    # make call to create new page
    logging.debug("Calling URL: " + config.CONFLUENCE_BASE_URL + "content/")

    response = requests.post(
        url=config.CONFLUENCE_BASE_URL + "content/",
        json=new_page_json_query,
        headers=config.CONFLUENCE_AUTH_HEADERS,
        verify=False)

    logging.debug(response.status_code)
    if response.status_code == 200:
        logging.info(title + "- Page created successfully")
        response_data = response.json()
        # return new page id
        page_id = response_data.get('id')
        if page_id:
            logging.debug("Returning created page id: " + page_id)
            return page_id
        else:
            logging.error("Page ID not found in response")
            logging.error("Response content: " + response.text)
            return None
    else:
        logging.error(title + "- Page has not been created")
        logging.error("Response content: " + response.text)
        return None
