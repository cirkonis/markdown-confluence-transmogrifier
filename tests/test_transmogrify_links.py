from functions.transmogrify_links import transmogrify_links
import config


def test_transmogrify_links():
    # Set a known base URL for testing
    config.CONFLUENCE_BASE_URL = "https://confluence.build.ingka.ikea.com/display/BASE_URL/"

    line = '[example link](/path/to/page.md)'
    expected_line = '[example link](https://confluence.build.ingka.ikea.com/display/BASE_URL/Page)'

    processed_line = transmogrify_links(line)

    assert processed_line == expected_line
