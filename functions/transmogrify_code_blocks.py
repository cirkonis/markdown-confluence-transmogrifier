import re
import logging


def transmogrify_code_blocks(content):
    """
    Processes the content to convert Markdown code blocks to Confluence format block macros.

    Args:
        content (str): The content of the Markdown file.

    Returns:
        tuple: The content with placeholders for Confluence macros and a dictionary of placeholders to macros.
    """

    macros = {}

    def replace_code_block(match):
        language = match.group(1) or ''  # Capture the language, if specified
        code = match.group(2).strip()  # Capture the code block content and strip leading/trailing whitespace

        # Handle special characters inside the code block to prevent any issues
        code = code.replace("]]>", "]]]]><![CDATA[>")

        # Build the Confluence macro with CDATA wrapped around the code content
        macro = (f'<ac:structured-macro ac:name="code">'
                 f'<ac:parameter ac:name="language">{language}</ac:parameter>'
                 f'<ac:plain-text-body><![CDATA[{code}]]></ac:plain-text-body>'
                 f'</ac:structured-macro>')

        # Replace the macro with a placeholder
        placeholder = f"@@MACRO_{hash(macro)}@@"
        macros[placeholder] = macro
        return placeholder

    # Apply the regex replacement for code blocks
    content = re.sub(r'```(\w+)?\n(.*?)\n```', replace_code_block, content, flags=re.DOTALL)

    logging.debug("Code blocks transmogrified with placeholders: " + content)

    return content, macros


def replace_placeholders_with_macros(html_content, macros):
    # Replace placeholders with their corresponding macros
    for placeholder, macro in macros.items():
        html_content = html_content.replace(placeholder, macro)
    return html_content

