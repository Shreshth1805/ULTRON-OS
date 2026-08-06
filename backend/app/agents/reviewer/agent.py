from app.core.llm import llm

from app.agents.reviewer.reviewer import reviewer

from app.agents.reviewer.prompts import REVIEW_PROMPT


class ReviewerAgent:

    def review_project(
        self,
        project_path: str
    ):

        code = reviewer.load_project(
            project_path
        )

        prompt = REVIEW_PROMPT.format(
            code=code
        )

        response = llm.invoke(
            prompt
        )

        return {

            "success": True,

            "response": response.content

        }


reviewer_agent = ReviewerAgent()