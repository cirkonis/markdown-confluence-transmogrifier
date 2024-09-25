import re
import config


def transmogrify_links(line):
    """
    Processes a line to convert Markdown links to Confluence format using the base URL from the configuration.

    Args:
        line (str): The line of text from the Markdown file.

    Returns:
        str: The line with Markdown links converted to Confluence format.
    """
    confluence_base_url = config.CONFLUENCE_BASE_URL
    confluence_space = config.CONFLUENCE_SPACE

    # Remove the /rest/api/ part of the base URL and prepare for the new format
    confluence_base_url = confluence_base_url.replace("/rest/api/", f"/display/{confluence_space}/")

    link_results = re.findall(r'\[(.*?)\]\((?!http|https)(.*?)\)', line)

    for link_text, md_link_path in link_results:
        confluence_page_title = md_link_path.split('/')[-1].replace('.md', '').replace('-', ' ').replace('_',
                                                                                                         ' ').capitalize()
        # Construct the new Confluence URL
        confluence_url = f"{confluence_base_url}{confluence_page_title.replace(' ', '+')}"

        line = re.sub(r'\[.*?\]\((?!http|https).*?\)', f'[{link_text}]({confluence_url})', line)

    return line
