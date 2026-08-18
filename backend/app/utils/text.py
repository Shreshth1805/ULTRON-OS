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


_EXTENSIONLESS_FILENAMES = {
    "Dockerfile", "Makefile", "LICENSE", "Procfile", "Jenkinsfile"
}


def looks_like_file_path(line: str) -> bool:
    """
    Best-effort check that a line of LLM output is a plausible relative
    file path, not a shell command, comment, or prose the model returned
    despite being asked for "only a file list". Rejects anything with
    whitespace (real paths don't have spaces; commands and sentences do),
    comment markers, and lines with no extension unless the bare filename
    is a well-known extensionless one (Dockerfile, LICENSE, ...) or a
    dotfile (.gitignore, ...).
    """

    line = line.strip().strip("`*- ").strip()

    if not line or " " in line or "\t" in line:
        return False

    if line.startswith(("#", "//", ">", "$")):
        return False

    name = line.rsplit("/", 1)[-1]

    if name.startswith("."):
        return True

    if name in _EXTENSIONLESS_FILENAMES:
        return True

    return "." in name
