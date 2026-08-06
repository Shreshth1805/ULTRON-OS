from app.base_agent import BaseAgent

from app.agents.security.prompts import SYSTEM_PROMPT


class SecurityAgent(BaseAgent):

    def review(
        self,
        code: str
    ):

        prompt = f"""
{SYSTEM_PROMPT}

Code

{code}
"""

        return self.generate(prompt)


security_agent = SecurityAgent()