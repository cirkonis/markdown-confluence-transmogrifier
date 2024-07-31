from unittest.mock import patch
from functions.transmogrify_directory import transmogrify_directory


def test_transmogrify_directory():
    with patch('functions.transmogrify_directory.confluence_create_page') as mock_confluence_create_page:
        mock_confluence_create_page.return_value = 12345
        entry = type('Entry', (object,), {'name': 'test_dir', 'path': '/path/to/test_dir'})
        parent_page_id = None

        result_page_id = transmogrify_directory(entry, parent_page_id)

        assert result_page_id == 12345
        mock_confluence_create_page.assert_called_once_with(
            title='test_dir',
            content='<ac:structured-macro ac:name="children" ac:schema-version="2" ac:macro-id="80b8c33e-cc87-4987-8f88-dd36ee991b15"/>',
            parent_page_id=parent_page_id,
        )
