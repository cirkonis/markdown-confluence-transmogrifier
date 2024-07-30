import logging

from functions.transmogrify_images import transmogrify_images
from functions.transmogrify_links import transmogrify_links


def process_file(file, parent_page_id=None):
    logging.info("Found file: " + str(file.path))
    if not str(file.path).lower().endswith('.md'):
        logging.info("File: " + str(file.path) + "  is not a MD file. Publishing has rejected")
        return

    new_file_content = ""
    files_to_upload = []
    with open(file.path, 'r', encoding="utf-8") as md_file:
        for line in md_file:
            line, images = transmogrify_images(line)
            files_to_upload.extend(images)
            line = transmogrify_links(line)
            new_file_content += line

    title = file.name.replace('.md', '').replace('-', ' ').replace('_', ' ').capitalize()


    # TODO implement createPage function
    # page_id_for_file_attaching = createPage(
    #     title=title,
    #     content=markdown.markdown(new_file_content, extensions=['markdown.extensions.tables', 'fenced_code']),
    #     parentPageID=parent_page_id,
    #     token=token
    # )
    # TODO remove this line
    page_id_for_file_attaching = 0

    attach_files_to_page(files_to_upload, page_id_for_file_attaching)
