from functions.transmogrify_links import transmogrify_links
import config


def test_single_basic_link():
    # Set up environment for testing
    config.CONFLUENCE_BASE_URL = "https://randomcompany.confluence.com/rest/api/"
    config.CONFLUENCE_SPACE = "DOCS"

    line = '[example link](/path/to/page.md)'
    expected_line = '[example link](https://randomcompany.confluence.com/display/DOCS/Page)'

    processed_line = transmogrify_links(line)

    assert processed_line == expected_line, f"Expected {expected_line}, but got {processed_line}"


def test_link_with_special_characters():
    config.CONFLUENCE_BASE_URL = "https://randomcompany.confluence.com/rest/api/"
    config.CONFLUENCE_SPACE = "DOCS"

    line = '[special link](/path/to/special_page-name.md)'
    expected_line = '[special link](https://randomcompany.confluence.com/display/DOCS/Special+page+name)'

    processed_line = transmogrify_links(line)

    assert processed_line == expected_line, f"Expected {expected_line}, but got {processed_line}"


def test_no_links():
    config.CONFLUENCE_BASE_URL = "https://randomcompany.confluence.com/rest/api/"
    config.CONFLUENCE_SPACE = "DOCS"

    line = 'This line has no links'
    expected_line = 'This line has no links'

    processed_line = transmogrify_links(line)

    assert processed_line == expected_line, f"Expected {expected_line}, but got {processed_line}"


def test_absolute_url_should_remain_unchanged():
    config.CONFLUENCE_BASE_URL = "https://randomcompany.confluence.com/rest/api/"
    config.CONFLUENCE_SPACE = "DOCS"

    line = '[external link](https://external.com/page)'
    expected_line = '[external link](https://external.com/page)'

    processed_line = transmogrify_links(line)

    assert processed_line == expected_line, f"Expected {expected_line}, but got {processed_line}"


def test_different_confluence_space():
    config.CONFLUENCE_BASE_URL = "https://randomcompany.confluence.com/rest/api/"
    config.CONFLUENCE_SPACE = "TECH"

    line = '[tech link](/path/to/tech_page.md)'
    expected_line = '[tech link](https://randomcompany.confluence.com/display/TECH/Tech+page)'

    processed_line = transmogrify_links(line)

    assert processed_line == expected_line, f"Expected {expected_line}, but got {processed_line}"


def test_edge_case_empty_string():
    config.CONFLUENCE_BASE_URL = "https://randomcompany.confluence.com/rest/api/"
    config.CONFLUENCE_SPACE = "DOCS"

    line = ''
    expected_line = ''

    processed_line = transmogrify_links(line)

    assert processed_line == expected_line, f"Expected {expected_line}, but got {processed_line}"
