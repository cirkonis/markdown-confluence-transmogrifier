import re
import logging


def transmogrify_images(line):
    """
    Processes a line to convert image markdown to Confluence format and extract image paths.

    Args:
        line (str): The line of text from the Markdown file.

    Returns:
        tuple: A tuple containing the processed line and a list of image file paths.
    """
    image_paths = re.findall(r"\A!\[.*]\((?!http)(.*)\)", line)
    files_to_upload = []

    for image_path in image_paths:
        image_filename = image_path.split('/')[-1]
        logging.debug("Found file for attaching: " + image_filename)

        images_dir_index = image_path.find('images/')
        if images_dir_index != -1:
            relative_image_path = image_path[images_dir_index + len('images/'):]
            image_filename = relative_image_path.split('/')[-1]
        files_to_upload.append(relative_image_path)
        line = re.sub(r"!\[.*]\((?!http)(.*)\)",
                      f'<ac:image><ri:attachment ri:filename="{image_filename}" /></ac:image>', line)

    return line, files_to_upload
