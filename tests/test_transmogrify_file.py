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


# New test for images
@patch('builtins.open', new_callable=mock_open,
       read_data='![image](subdir1/test_image.jpg)\nThis is a line with a [link](subdir1/test_link.md) in it.\n')
@patch('functions.transmogrify_file.confluence_create_page')
@patch('functions.transmogrify_file.attach_files_to_page')
def test_transmogrify_file_with_images(mock_attach_files_to_page, mock_create_page, mock_file):
    mock_create_page.return_value = 12345
    entry = type('Entry', (object,), {'name': 'test_file.md', 'path': '/path/to/test_file.md', 'is_file': lambda: True})
    parent_page_id = None

    transmogrify_file(entry, parent_page_id)

    mock_create_page.assert_called_once()
    mock_attach_files_to_page.assert_called_once_with(['subdir1/test_image.jpg'], 12345)
