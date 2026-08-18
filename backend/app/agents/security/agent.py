from app.core.llm import llm

from app.agents.security.prompts import SYSTEM_PROMPT


class SecurityAgent:

    def review(
        self,
        code: str
    ):

        prompt = f"""
{SYSTEM_PROMPT}

Code

{code}
"""

        response = llm.invoke(prompt)

        return {

            "success": True,

            "response": response.content

        }


security_agent = SecurityAgent()