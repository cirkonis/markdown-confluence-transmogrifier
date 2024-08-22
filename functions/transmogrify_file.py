import logging

import markdown

from functions.attach_files_to_page import attach_files_to_page
from functions.confluence_create_page import confluence_create_page
from functions.transmogrify_code_blocks import transmogrify_code_blocks, replace_placeholders_with_macros
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

    # Apply the code block conversion to the entire content after processing images and links
    new_file_content, macros = transmogrify_code_blocks(new_file_content)

    # Convert the fully processed Markdown to HTML
    html_content = markdown.markdown(new_file_content, extensions=['markdown.extensions.tables', 'fenced_code'])

    # Replace the placeholders with the actual Confluence macros
    html_content = replace_placeholders_with_macros(html_content, macros)

    title = file.name.replace('.md', '').replace('-', ' ').replace('_', ' ').capitalize()

    page_id_for_file_attaching = confluence_create_page(
        title=title,
        content=html_content,
        parent_page_id=parent_page_id,
    )

    logging.debug("Page id for file attaching: " + str(page_id_for_file_attaching))

    if not files_to_upload:
        logging.debug("No files to upload")
        return

    attach_files_to_page(files_to_upload, page_id_for_file_attaching)
