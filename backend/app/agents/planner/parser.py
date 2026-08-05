import json


class PlannerParser:

    def parse(self, text: str):

        try:
            return json.loads(text)

        except Exception:

            return {

                "project_name": "",

                "description": "",

                "tech_stack": [],

                "files": [],

                "tasks": []

            }


planner_parser = PlannerParser()