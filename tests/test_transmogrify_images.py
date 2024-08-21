import os
from unittest import mock

import pytest

from functions.transmogrify_images import transmogrify_images

# Mock configuration for testing
mock_config = mock.MagicMock()
mock_config.DOCUMENTATION_IMAGE_DIRECTORY = '/mock/documentation/images'


# Patching the config module within transmogrify_images
@pytest.fixture(autouse=True)
def patch_config(monkeypatch):
    monkeypatch.setattr('app.config', mock_config)


# Mocking os.path.exists to control the existence of files
@pytest.fixture(autouse=True)
def mock_os_path_exists(monkeypatch):
    def mock_exists(path):
        return 'valid' in path

    monkeypatch.setattr(os.path, 'exists', mock_exists)


def test_single_valid_image():
    line = "I am a line with one image ![Example Image](../images/valid_image.jpg)"
    expected_line = 'I am a line with one image <ac:image><ri:attachment ri:filename="valid_image.jpg" /></ac:image>'
    expected_files = ['documentation/images/valid_image.jpg']

    processed_line, files_to_upload = transmogrify_images(line)

    assert processed_line == expected_line
    assert files_to_upload == expected_files


def test_multiple_valid_images():
    line = "![Image1](valid_image1.jpg) ![Image2](/images/valid_image2.jpg)"
    expected_line = '<ac:image><ri:attachment ri:filename="valid_image1.jpg" /></ac:image> <ac:image><ri:attachment ' \
                    'ri:filename="valid_image2.jpg" /></ac:image>'
    expected_files = [
        'documentation/images/valid_image1.jpg',
        'documentation/images/valid_image2.jpg'
    ]

    processed_line, files_to_upload = transmogrify_images(line)

    assert processed_line == expected_line
    assert files_to_upload == expected_files


def test_no_image_in_line():
    line = "This is a line with no image."
    expected_line = line
    expected_files = []

    processed_line, files_to_upload = transmogrify_images(line)

    assert processed_line == expected_line
    assert files_to_upload == expected_files


def test_images_in_sub_dir():
    line = "I am a line with one image ![Example Image](../images/sub_dir/valid_image.jpg)"
    expected_line = 'I am a line with one image <ac:image><ri:attachment ri:filename="valid_image.jpg" /></ac:image>'
    expected_files = ['documentation/images/sub_dir/valid_image.jpg']

    processed_line, files_to_upload = transmogrify_images(line)

    assert processed_line == expected_line
    assert files_to_upload == expected_files


def test_various():
    # Input markdown line with various relative paths
    line = "![Image1](./valid_image1.jpg) ![Image2](../images/valid_image2.jpg) ![Image3](../../images/sub_dir/valid_image3.jpg)"

    # Expected output after processing the line
    expected_line = '<ac:image><ri:attachment ri:filename="valid_image1.jpg" /></ac:image> ' \
                    '<ac:image><ri:attachment ri:filename="valid_image2.jpg" /></ac:image> ' \
                    '<ac:image><ri:attachment ri:filename="valid_image3.jpg" /></ac:image>'

    # Expected files to upload, with paths correctly resolved
    expected_files = [
        'documentation/images/valid_image1.jpg',
        'documentation/images/valid_image2.jpg',
        'documentation/images/sub_dir/valid_image3.jpg'
    ]

    # Call the transmogrify_images function with the input line
    processed_line, files_to_upload = transmogrify_images(line)

    # Assert that the processed line matches the expected line
    assert processed_line == expected_line

    # Assert that the files to upload match the expected files
    assert files_to_upload == expected_files



