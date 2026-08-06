from app.core.llm import llm

from app.agents.planner.prompts import PLANNER_PROMPT

from app.agents.planner.parser import parse_plan


class Planner:

    def create_plan(self, request):

        prompt = PLANNER_PROMPT.format(
            request=request
        )

        response = llm.invoke(prompt)

        return parse_plan(
            response.content
        )


planner = Planner()