import logging

from functions.confluence_create_page import confluence_create_page


def transmogrify_directory(directory, parent_page_id=None):
    current_page_id = confluence_create_page(
        title=str(directory.name),
        content="<ac:structured-macro ac:name=\"children\" ac:schema-version=\"2\" ac:macro-id=\"80b8c33e-cc87-4987-8f88-dd36ee991b15\"/>",
        parent_page_id=parent_page_id,
    )
    logging.info('Current page ID: ' + str(current_page_id))
    return current_page_id
