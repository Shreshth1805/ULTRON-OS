from app.github.manager import github_manager


class GithubAgent:
    """
    GitHub Agent

    Responsible for:
    - Creating repositories
    - Initializing git
    - Committing code
    - Pushing to GitHub
    - Creating branches
    - Opening Pull Requests
    """

    def publish(
        self,
        project_name: str,
        project_path: str
    ):

        try:

            result = github_manager.publish(

                project_name=project_name,

                project_path=project_path

            )

            return {

                "success": True,

                "response": "Project published successfully.",

                "github": result

            }

        except Exception as e:

            return {

                "success": False,

                "response": "Failed to publish project.",

                "error": str(e)

            }


github_agent = GithubAgent()