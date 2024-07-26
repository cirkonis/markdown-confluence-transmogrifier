# tests/test_set_auth_headers.py

import pytest

import config
from functions.set_auth_headers import set_auth_headers


def test_set_auth_headers_with_personal_access_token():
    # Setup
    config.CONFLUENCE_PERSONAL_ACCESS_TOKEN = "personal_access_token"
    config.CONFLUENCE_USER = None
    config.CONFLUENCE_API_TOKEN = None

    # Call the function
    set_auth_headers()

    # Assert
    assert config.CONFLUENCE_AUTH_HEADERS == {
        'Authorization': 'Bearer personal_access_token'
    }


def test_set_auth_headers_with_api_token():
    # Setup
    config.CONFLUENCE_PERSONAL_ACCESS_TOKEN = None
    config.CONFLUENCE_USER = "user@example.com"
    config.CONFLUENCE_API_TOKEN = "api_token"

    # Call the function
    set_auth_headers()

    # Assert
    expected_auth_value = 'Basic ' + 'user@example.com:api_token'.encode('utf-8').strip().decode('ascii')
    assert config.CONFLUENCE_AUTH_HEADERS == {
        'Authorization': expected_auth_value
    }


def test_set_auth_headers_without_tokens():
    # Setup
    config.CONFLUENCE_PERSONAL_ACCESS_TOKEN = None
    config.CONFLUENCE_USER = None
    config.CONFLUENCE_API_TOKEN = None

    # Call the function and expect an error
    with pytest.raises(ValueError,
                       match="An authentication method is required: either a personal access token or a user and API token."):
        set_auth_headers()


def test_set_auth_headers_with_both_tokens():
    # Setup
    config.CONFLUENCE_PERSONAL_ACCESS_TOKEN = "personal_access_token"
    config.CONFLUENCE_USER = "user@example.com"
    config.CONFLUENCE_API_TOKEN = "api_token"

    # Call the function
    set_auth_headers()

    # Assert that personal access token takes priority
    assert config.CONFLUENCE_AUTH_HEADERS == {
        'Authorization': 'Bearer personal_access_token'
    }
