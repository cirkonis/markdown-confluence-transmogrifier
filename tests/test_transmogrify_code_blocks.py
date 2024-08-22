import pytest
from functions.transmogrify_code_blocks import transmogrify_code_blocks, replace_placeholders_with_macros


def test_single_code_block():
    content = "```python\nprint('Hello, World!')\n```"
    expected_macro = (
        '<ac:structured-macro ac:name="code">'
        '<ac:parameter ac:name="language">python</ac:parameter>'
        '<ac:plain-text-body><![CDATA[print(\'Hello, World!\')]]></ac:plain-text-body>'
        '</ac:structured-macro>'
    )

    transformed_content, macros = transmogrify_code_blocks(content)
    assert len(macros) == 1

    placeholder = list(macros.keys())[0]
    assert transformed_content == placeholder
    assert macros[placeholder] == expected_macro

    final_content = replace_placeholders_with_macros(transformed_content, macros)
    assert final_content == expected_macro


def test_multiple_code_blocks():
    content = (
        "```python\nprint('Hello, World!')\n```\n"
        "```yaml\nname: John Doe\nage: 30\n```"
    )
    transformed_content, macros = transmogrify_code_blocks(content)

    assert len(macros) == 2

    placeholders = list(macros.keys())
    assert placeholders[0] in transformed_content
    assert placeholders[1] in transformed_content

    final_content = replace_placeholders_with_macros(transformed_content, macros)

    expected_content = (
        f"{macros[placeholders[0]]}\n{macros[placeholders[1]]}"
    )

    assert final_content == expected_content


def test_code_block_with_special_characters():
    content = "```python\nprint('Hello, World! > < &')\n```"
    expected_macro = (
        '<ac:structured-macro ac:name="code">'
        '<ac:parameter ac:name="language">python</ac:parameter>'
        '<ac:plain-text-body><![CDATA[print(\'Hello, World! > < &\')]]></ac:plain-text-body>'
        '</ac:structured-macro>'
    )

    transformed_content, macros = transmogrify_code_blocks(content)
    assert len(macros) == 1

    placeholder = list(macros.keys())[0]
    assert transformed_content == placeholder
    assert macros[placeholder] == expected_macro

    final_content = replace_placeholders_with_macros(transformed_content, macros)
    assert final_content == expected_macro



def test_empty_code_block():
    content = "```\n\n```"
    expected_macro = (
        '<ac:structured-macro ac:name="code">'
        '<ac:parameter ac:name="language"></ac:parameter>'
        '<ac:plain-text-body><![CDATA[]]></ac:plain-text-body>'
        '</ac:structured-macro>'
    )

    transformed_content, macros = transmogrify_code_blocks(content)
    assert len(macros) == 1

    placeholder = list(macros.keys())[0]
    assert transformed_content == placeholder
    assert macros[placeholder] == expected_macro

    final_content = replace_placeholders_with_macros(transformed_content, macros)
    assert final_content == expected_macro


def test_mixed_content_with_code_blocks():
    content = (
        "Here is some text.\n"
        "```python\nprint('Hello, World!')\n```\n"
        "More text here.\n"
        "```yaml\nname: John Doe\nage: 30\n```"
    )
    transformed_content, macros = transmogrify_code_blocks(content)

    assert len(macros) == 2

    placeholders = list(macros.keys())
    assert placeholders[0] in transformed_content
    assert placeholders[1] in transformed_content

    final_content = replace_placeholders_with_macros(transformed_content, macros)

    expected_content = (
        f"Here is some text.\n{macros[placeholders[0]]}\nMore text here.\n{macros[placeholders[1]]}"
    )

    assert final_content == expected_content
