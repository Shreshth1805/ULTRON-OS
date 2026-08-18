def strip_code_fence(text: str) -> str:
    """
    Strip a single ```lang / ``` markdown code fence wrapping LLM
    output, if present. Text with no fence is returned unchanged
    (aside from surrounding whitespace).
    """

    text = text.strip()

    if "```" not in text:
        return text

    parts = text.split("```")

    if len(parts) < 2:
        return text

    content = parts[1]

    first_line, _, rest = content.partition("\n")

    if rest and first_line.strip().isalpha():
        content = rest

    return content.strip()
