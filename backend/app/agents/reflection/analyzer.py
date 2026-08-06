import json


def parse_reflection(text):

    start = text.find("{")
    end = text.rfind("}") + 1

    return json.loads(text[start:end])