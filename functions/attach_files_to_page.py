import logging
import os

import config


def attach_files_to_page(files_to_upload, page_id_for_file_attaching):
    for file_path in files_to_upload:
        image_path = os.path.join(config.DOCUMENTATION_IMAGE_DIRECTORY, file_path)
        if os.path.isfile(image_path):
            logging.info("Attaching file: " + image_path + "  to the page: " + str(page_id_for_file_attaching))
            with open(image_path, 'rb') as attached_file:
                logging.debug(attached_file.read())
        # TODO implement attachFile function
        # attachFile(pageIdForFileAttaching=page_id_for_file_attaching, attachedFile=attached_file, token=token)
        else:
            logging.error("File: " + str(image_path) + "  not found. Nothing to attach")
