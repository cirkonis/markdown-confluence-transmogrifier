import logging
import os
from functions.confluence_attach_file import confluence_attach_file


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
