import logging
import os
from functions.transmogrify_directory import transmogrify_directory
from functions.transmogrify_file import transmogrify_file


def transmogrify_documentation(thing_to_transmogrify, parent_page_id):
    logging.info("Publishing documentation from: " + thing_to_transmogrify)

    for entry in os.scandir(thing_to_transmogrify):
        logging.info(f"Processing entry: {entry.path}")
        if entry.is_dir():
            logging.info("Found directory: " + str(entry.path))
            current_page_id = transmogrify_directory(entry, parent_page_id)
            # Recursively process subdirectories
            transmogrify_documentation(entry.path, current_page_id)
        elif entry.is_file():
            logging.info("Found file: " + str(entry.path))
            if str(entry.path).lower().endswith('.md'):
                transmogrify_file(entry, parent_page_id)
            else:
                logging.info("File: " + str(entry.path) + " is not an MD file. Publishing has been rejected")
        elif entry.is_symlink():
            logging.info("Found symlink: " + str(entry.path))
        else:
            logging.info("Found unknown type of entry (not file, not directory, not symlink): " + str(entry.path))
