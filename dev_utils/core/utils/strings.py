"""Module with strings utils."""

import re


def has_format_brackets(value: str) -> bool:
    """Check string for formatting brackets.

    Examples
    --------
    >>> has_format_brackets('{}')
    True
    >>> has_format_brackets('{some_variables}')
    True
    >>> has_format_brackets('{}}')
    False
    >>> has_format_brackets('{{}}')
    True
    >>> has_format_brackets('{!}')
    False  # because this string can't be formatted - any formats will cause error.
    """
    stack: list[str] = []
    mapping = {"}": "{"}
    balanced = True
    for char in value:
        if char == "}":
            top_element = stack.pop() if stack else "#"
            if mapping[char] != top_element:
                balanced = False
                break
        elif char == "{":
            stack.append(char)
    is_valid = not stack if balanced else balanced
    if not is_valid:
        return is_valid
    pattern = (
        r"(\{[\"\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\|\~]+\})|(\{\d+\w*\})"
    )
    if re.match(pattern, value):
        return False
    left_count = value.count("{")
    right_count = value.count("}")
    escaped_left = 0
    escaped_right = value.count("\\}")
    return (
        (left_count - (escaped_left * 2) != 0)
        and (right_count - (escaped_right * 2) != 0)
        and (left_count == right_count)
    )


def trim_and_plain_text(text: str) -> str:
    """Make text plain and trim."""
    text = text.strip()
    while "  " in text:
        text = text.replace("  ", " ")
    return text.replace("\n", " ").strip()
