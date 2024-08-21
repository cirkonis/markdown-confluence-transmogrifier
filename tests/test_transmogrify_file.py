from unittest import mock
from unittest.mock import patch, mock_open

from functions.transmogrify_file import transmogrify_file


# Existing test for no images
@patch('builtins.open', new_callable=mock_open, read_data='This is a line with a [link](subdir1/test_link.md) in it.\n')
@patch('functions.transmogrify_file.confluence_create_page')
@patch('functions.transmogrify_file.attach_files_to_page')
def test_transmogrify_file_no_images(mock_attach_files_to_page, mock_create_page, mock_file):
    mock_create_page.return_value = 12345
    entry = type('Entry', (object,), {'name': 'test_file.md', 'path': '/path/to/test_file.md', 'is_file': lambda: True})
    parent_page_id = None

    transmogrify_file(entry, parent_page_id)

    mock_create_page.assert_called_once()
    mock_attach_files_to_page.assert_not_called()


# Mock configuration for testing
mock_config = mock.MagicMock()
mock_config.DOCUMENTATION_IMAGE_DIRECTORY = '/mock/documentation/images'


@patch('functions.transmogrify_file.transmogrify_images')
@patch('functions.transmogrify_file.confluence_create_page')
@patch('functions.transmogrify_file.attach_files_to_page')
@patch('builtins.open', new_callable=mock_open,
       read_data='![image](subdir1/images/test_image.jpg)\nThis is a line with a [link](subdir1/test_link.md) in it.\n')
def test_transmogrify_file_with_images(mock_file, mock_attach_files_to_page, mock_create_page,
                                       mock_transmogrify_images):
    # Mock the output of confluence_create_page
    mock_create_page.return_value = 12345

    # Mock the return value of transmogrify_images to return the image path
    mock_transmogrify_images.side_effect = [
        ('Some processed line with image', ['subdir1/images/test_image.jpg']),  # First line with image
        ('Some processed line with link', [])  # Second line with link and no images
    ]

    # Mock entry for the file
    entry = type('Entry', (object,), {'name': 'test_file.md', 'path': '/path/to/test_file.md', 'is_file': lambda: True})
    parent_page_id = None

    # Call the function
    transmogrify_file(entry, parent_page_id)

    # Assertions
    mock_create_page.assert_called_once()
    mock_attach_files_to_page.assert_called_once_with(['subdir1/images/test_image.jpg'], 12345)
