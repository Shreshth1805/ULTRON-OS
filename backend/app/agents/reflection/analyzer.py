import json

from app.utils.text import strip_code_fence


def parse_reflection(text):

    text = strip_code_fence(text)

    start = text.find("{")
    end = text.rfind("}") + 1

    return json.loads(text[start:end])