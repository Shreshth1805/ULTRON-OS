def extract_python(text):

    if "```python" in text:

        text = text.split("```python")[1]

        text = text.split("```")[0]

    elif "```" in text:

        text = text.split("```")[1]

        text = text.split("```")[0]

    return text.strip()