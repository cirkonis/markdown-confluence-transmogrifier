import logging
import re
import os
import config


def transmogrify_images(line):
    """
    Processes a line to convert image markdown to Confluence format and extract image paths.

    Args:
        line (str): The line of text from the Markdown file.

    Returns:
        tuple: A tuple containing the processed line and a list of image file paths.
    """
    image_paths = re.findall(r"!\[.*\]\((?!http)(.*?)\)", line)
    files_to_upload = []

    for image_path in image_paths:
        image_filename = os.path.basename(image_path)
        logging.debug("Found file for attaching: " + image_filename)

        # Normalize the relative path
        relative_image_path = os.path.normpath(os.path.relpath(image_path, config.DOCUMENTATION_IMAGE_DIRECTORY))

        files_to_upload.append(relative_image_path)
        line = re.sub(r"!\[.*\]\((?!http)(.*?)\)",
                      f'<ac:image><ri:attachment ri:filename="{image_filename}" /></ac:image>', line)

    return line, files_to_upload
