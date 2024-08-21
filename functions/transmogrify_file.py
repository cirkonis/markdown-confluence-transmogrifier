import logging

import markdown

from functions.attach_files_to_page import attach_files_to_page
from functions.confluence_create_page import confluence_create_page
from functions.transmogrify_images import transmogrify_images
from functions.transmogrify_links import transmogrify_links


def transmogrify_file(file, parent_page_id):
    new_file_content = ""
    files_to_upload = []
    with open(file.path, 'r', encoding="utf-8") as md_file:
        for line in md_file:
            line, images = transmogrify_images(line)
            files_to_upload.extend(images)
            line = transmogrify_links(line)
            new_file_content += line

    title = file.name.replace('.md', '').replace('-', ' ').replace('_', ' ').capitalize()

    page_id_for_file_attaching = confluence_create_page(
        title=title,
        content=markdown.markdown(new_file_content, extensions=['markdown.extensions.tables', 'fenced_code']),
        parent_page_id=parent_page_id,
    )

    logging.debug("Page id for file attaching: " + str(page_id_for_file_attaching))

    if not files_to_upload:
        logging.debug("No files to upload")
        return

    attach_files_to_page(files_to_upload, page_id_for_file_attaching)
