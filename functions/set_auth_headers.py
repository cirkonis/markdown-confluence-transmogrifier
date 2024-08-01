# set_auth_headers.py

import config


def set_auth_headers():
    if config.CONFLUENCE_PERSONAL_ACCESS_TOKEN:
        config.CONFLUENCE_AUTH_HEADERS = {
            'Authorization': f'Bearer {config.CONFLUENCE_PERSONAL_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
    elif config.CONFLUENCE_USER and config.CONFLUENCE_API_TOKEN:
        config.CONFLUENCE_AUTH_HEADERS = {
            'Authorization': 'Basic ' + f'{config.CONFLUENCE_USER}:{config.CONFLUENCE_API_TOKEN}'.encode('utf-8').strip().decode('ascii'),
            'Content-Type': 'application/json'
        }
    else:
        raise ValueError("An authentication method is required: either a personal access token or a user and API token.")
