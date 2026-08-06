import json

from app.agents.planner.models import Plan


def parse_plan(text):

    start = text.find("{")

    end = text.rfind("}") + 1

    text = text[start:end]

    data = json.loads(text)

    return Plan(**data)