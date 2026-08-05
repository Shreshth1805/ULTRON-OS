from app.core.llm import llm

from app.agents.planner.prompts import PLANNER_PROMPT
from app.agents.planner.parser import planner_parser


class PlannerAgent:

    def create_plan(
        self,
        prompt: str
    ):

        message = f"""
{PLANNER_PROMPT}

User Request:

{prompt}
"""

        response = llm.invoke(
            message
        )

        return planner_parser.parse(
            response.content
        )


planner_agent = PlannerAgent()