import logging
import os
import transmogrify_directory
import transmogrify_file


def transmogrify_documentation(thing_to_transmogrify, parent_page_id=None):
    logging.info("Publishing documentation from: " + thing_to_transmogrify)
    for entry in os.scandir(thing_to_transmogrify):
        if entry.is_dir():
            current_page_id = transmogrify_directory(entry)
            transmogrify_documentation(thing_to_transmogrify=entry.path, parent_page_id=current_page_id)
        elif entry.is_file():
            transmogrify_file(entry, parent_page_id)
        elif entry.is_symlink():
            logging.info("Found symlink: " + str(entry.path))
        else:
            logging.info("Found unknown type of entry (not file, not directory, not symlink) " + str(entry.path))
