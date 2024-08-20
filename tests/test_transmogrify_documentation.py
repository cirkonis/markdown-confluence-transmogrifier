from unittest.mock import patch, MagicMock

from functions.transmogrify_documentation import transmogrify_documentation


# Helper function to create a fake directory entry
def create_mock_entry(path, is_dir=False, is_file=False, is_symlink=False):
    entry = MagicMock()
    entry.path = path
    entry.is_dir.return_value = is_dir
    entry.is_file.return_value = is_file
    entry.is_symlink.return_value = is_symlink
    return entry


@patch('functions.transmogrify_documentation.transmogrify_directory')
@patch('functions.transmogrify_documentation.transmogrify_file')
@patch('os.scandir')
@patch('logging.info')
def test_transmogrify_documentation(mock_logging_info, mock_scandir, mock_transmogrify_file,
                                    mock_transmogrify_directory):
    # Create mock entries for the directory and files
    mock_entries_main = [
        create_mock_entry('/path/to/DIR/file_one.md', is_file=True),
        create_mock_entry('/path/to/DIR/Directory One', is_dir=True)
    ]
    mock_entries_subdir = [
        create_mock_entry('/path/to/DIR/Directory One/directory_file_one.md', is_file=True)
    ]

    def scandir_side_effect(path):
        if path == '/path/to/DIR':
            return mock_entries_main
        elif path == '/path/to/DIR/Directory One':
            return mock_entries_subdir
        else:
            return []

    mock_scandir.side_effect = scandir_side_effect

    # Mock the behavior of transmogrify_directory and transmogrify_file
    mock_transmogrify_directory.side_effect = lambda directory, parent_page_id: (
        'new_page_id' if directory.path == '/path/to/DIR/Directory One' else 'parent_page_id'
    )
    mock_transmogrify_file.return_value = None  # No return value expected for this

    # Run the function
    transmogrify_documentation('/path/to/DIR', 'parent_page_id')

    # Assertions
    # Check that transmogrify_directory was called correctly for Directory One
    mock_transmogrify_directory.assert_called_once_with(mock_entries_main[1], 'parent_page_id')

    # Check that transmogrify_file was called for file_one.md with parent_page_id
    mock_transmogrify_file.assert_any_call(mock_entries_main[0], 'parent_page_id')

    # Check that transmogrify_file was called for directory_file_one.md with new_page_id
    mock_transmogrify_file.assert_any_call(mock_entries_subdir[0], 'new_page_id')

    # Verify logging info was called correctly
    mock_logging_info.assert_any_call('Publishing documentation from: /path/to/DIR')
    mock_logging_info.assert_any_call('Found file: /path/to/DIR/file_one.md')
    mock_logging_info.assert_any_call('Found directory: /path/to/DIR/Directory One')
    mock_logging_info.assert_any_call('Publishing documentation from: /path/to/DIR/Directory One')
    mock_logging_info.assert_any_call('Found file: /path/to/DIR/Directory One/directory_file_one.md')
