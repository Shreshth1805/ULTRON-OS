from app.core.llm import llm

from app.agents.performance.prompts import (
    SYSTEM_PROMPT
)


class PerformanceAgent:

    def analyze(
        self,
        code: str
    ):

        prompt = f"""
{SYSTEM_PROMPT}

Code:

{code}
"""

        response = llm.invoke(prompt)

        return {

            "success": True,

            "response": response.content

        }


performance_agent = PerformanceAgent()