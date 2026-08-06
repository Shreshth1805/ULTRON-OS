from app.base_agent import BaseAgent

from app.agents.performance.prompts import (
    SYSTEM_PROMPT
)


class PerformanceAgent(BaseAgent):

    def analyze(
        self,
        code: str
    ):

        prompt = f"""
{SYSTEM_PROMPT}

Code:

{code}
"""

        return self.generate(prompt)


performance_agent = PerformanceAgent()