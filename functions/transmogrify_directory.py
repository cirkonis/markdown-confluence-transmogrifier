import logging


def transmogrify_directory(directory, parent_page_id=None):
    """
    Processes a line to convert image markdown to Confluence format and extract image paths.

    Args:
        line (str): The line of text from the Markdown file.

    Returns:
        tuple: A tuple containing the processed line and a list of image file paths.
        :param parent_page_id:
        :param directory:
    """
    logging.info("Found directory: " + str(directory.path))
    # TODO implement createPage function
    # current_page_id = createPage(
    #     title=str(entry.name),
    #     content="<ac:structured-macro ac:name=\"children\" ac:schema-version=\"2\" ac:macro-id=\"80b8c33e-cc87-4987-8f88-dd36ee991b15\"/>",
    #     parentPageID=parent_page_id,
    #     token=token
    # )
    # TODO remove this line
    current_page_id = 0
    logging.info('Current page ID: ' + str(current_page_id))
    return current_page_id
