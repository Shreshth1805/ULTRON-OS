from pathlib import Path

from app.agents.reviewer.service import review_service


class ReviewerAgent:

    def review_project(
        self,
        project_path
    ):

        results = []

        for file in Path(project_path).rglob("*.py"):

            code = file.read_text(
                encoding="utf-8"
            )

            review = review_service.review(
                file.name,
                code
            )

            results.append({

                "file": str(file),

                "review": review

            })

        return {

            "success": True,

            "reviews": results

        }


reviewer_agent = ReviewerAgent()