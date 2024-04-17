def trim_and_plain_text(text: str) -> str:
    """Make text plain and trim."""
    text = text.strip()
    while "  " in text:
        text = text.replace("  ", " ")
    return text.replace("\n", " ").strip()
