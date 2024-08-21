import pytest
import base64
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
        'Authorization': 'Bearer personal_access_token',
        'Content-Type': 'application/json'
    }


def test_set_auth_headers_with_api_token():
    # Setup
    config.CONFLUENCE_PERSONAL_ACCESS_TOKEN = None
    config.CONFLUENCE_USER = "user@example.com"
    config.CONFLUENCE_API_TOKEN = "api_token"

    # Call the function
    set_auth_headers()

    # Assert
    credentials = f'user@example.com:api_token'
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('ascii')
    expected_auth_value = f'Basic {encoded_credentials}'
    assert config.CONFLUENCE_AUTH_HEADERS == {
        'Authorization': expected_auth_value,
        'Content-Type': 'application/json'
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

    # Assert that basic auth takes priority
    credentials = f'user@example.com:api_token'
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('ascii')
    expected_auth_value = f'Basic {encoded_credentials}'
    assert config.CONFLUENCE_AUTH_HEADERS == {
        'Authorization': expected_auth_value,
        'Content-Type': 'application/json'
    }
