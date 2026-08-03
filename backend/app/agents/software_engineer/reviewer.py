from app.core.llm import llm


class CodeReviewer:

    def review(
        self,
        code
    ):

        prompt = f"""
Review this code.

Find:

bugs

security issues

performance problems

Return fixes.

Code:

{code}
"""

        response = llm.invoke(prompt)

        return response.content


reviewer = CodeReviewer()