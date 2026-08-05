import json

from app.core.llm import llm
from app.agents.reviewer.prompts import SYSTEM_PROMPT


class ReviewService:

    def review(
        self,
        filename,
        code
    ):

        prompt = f"""
{SYSTEM_PROMPT}

Filename:

{filename}

Code:

{code}
"""

        response = llm.invoke(prompt)

        try:

            return json.loads(
                response.content
            )

        except Exception:

            return {

                "score":0,

                "issues":[
                    "Invalid LLM response"
                ],

                "recommendations":[]
            }


review_service = ReviewService()