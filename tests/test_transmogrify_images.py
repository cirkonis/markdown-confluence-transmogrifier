import config
from functions.transmogrify_images import transmogrify_images


def test_transmogrify_images_with_subdirectories():
    config.DOCUMENTATION_IMAGE_DIRECTORY = "images"

    line = '![test_image](images/subdir1/subdir2/test_image.jpg)'
    expected_line = '<ac:image><ri:attachment ri:filename="test_image.jpg" /></ac:image>'
    expected_files = ["subdir1/subdir2/test_image.jpg"]

    processed_line, files_to_upload = transmogrify_images(line)

    assert processed_line == expected_line
    assert files_to_upload == expected_files


def test_transmogrify_images_without_subdirectories():
    config.DOCUMENTATION_IMAGE_DIRECTORY = "images"

    line = '![test_image](images/test_image.jpg)'
    expected_line = '<ac:image><ri:attachment ri:filename="test_image.jpg" /></ac:image>'
    expected_files = ["test_image.jpg"]

    processed_line, files_to_upload = transmogrify_images(line)

    assert processed_line == expected_line
    assert files_to_upload == expected_files


def test_transmogrify_images_with_custom_directory():
    config.DOCUMENTATION_IMAGE_DIRECTORY = "custom_images"

    line = '![test_image](custom_images/test_image.jpg)'
    expected_line = '<ac:image><ri:attachment ri:filename="test_image.jpg" /></ac:image>'
    expected_files = ["test_image.jpg"]

    processed_line, files_to_upload = transmogrify_images(line)

    assert processed_line == expected_line
    assert files_to_upload == expected_files


def test_transmogrify_images_no_image():
    config.DOCUMENTATION_IMAGE_DIRECTORY = "images"

    line = 'This is a text without any image'
    expected_line = line
    expected_files = []

    processed_line, files_to_upload = transmogrify_images(line)

    assert processed_line == expected_line
    assert files_to_upload == expected_files
