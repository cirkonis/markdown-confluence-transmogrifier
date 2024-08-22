
import logging
import os
import re

import config


def transmogrify_images(line):
    """
    Processes a line to convert image markdown to Confluence format and extract image file paths.

    Args:
        line (str): The line of text from the Markdown file.

    Returns:
        tuple: A tuple containing the processed line and a list of image file paths.
    """
    image_patterns = re.findall(r"!\[.*?\]\((?!http)(.*?)\)", line)
    files_to_upload = []

    for image_path in image_patterns:
        image_filename = os.path.basename(image_path)
        logging.debug("Found file for attaching: " + image_filename)

        # Step 1: Normalize the path to remove '../' and './'
        normalized_relative_path = os.path.normpath(image_path)

        # Step 2: Ensure the path starts with 'images/' and then replace it with the DOCUMENTATION_IMAGE_DIRECTORY
        if 'images/' in normalized_relative_path:
            normalized_relative_path = normalized_relative_path.split('images/', 1)[-1]
            final_path = os.path.join(config.DOCUMENTATION_IMAGE_DIRECTORY, normalized_relative_path)
        else:
            # If 'images/' is not in the path, default to DOCUMENTATION_IMAGE_DIRECTORY
            final_path = os.path.join(config.DOCUMENTATION_IMAGE_DIRECTORY, normalized_relative_path)

        # Final normalization to ensure the '../' are correctly handled
        final_path = os.path.normpath(final_path)

        if os.path.exists(final_path):
            files_to_upload.append(final_path)

            # Replace the entire Markdown image pattern with Confluence format
            line = re.sub(rf"!\[.*?\]\({re.escape(image_path)}\)",
                          f'<ac:image><ri:attachment ri:filename="{image_filename}" /></ac:image>', line)
        else:
            logging.error(f"File: {final_path} not found. Nothing to attach")

    return line, files_to_upload
