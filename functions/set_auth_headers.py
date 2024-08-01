import logging
import base64
import config


def set_auth_headers():
    logging.debug("Setting authentication headers")
    if config.CONFLUENCE_USER and config.CONFLUENCE_API_TOKEN:
        logging.debug("Using user and API token for authentication")
        credentials = f'{config.CONFLUENCE_USER}:{config.CONFLUENCE_API_TOKEN}'
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('ascii')
        config.CONFLUENCE_AUTH_HEADERS = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
    elif config.CONFLUENCE_PERSONAL_ACCESS_TOKEN:
        logging.debug("Using personal access token for authentication")
        config.CONFLUENCE_AUTH_HEADERS = {
            'Authorization': f'Bearer {config.CONFLUENCE_PERSONAL_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
    else:
        logging.error("No valid authentication method provided")
        raise ValueError(
            "An authentication method is required: either a personal access token or a user and API token.")

    logging.debug(f"Authentication headers set: {config.CONFLUENCE_AUTH_HEADERS}")
