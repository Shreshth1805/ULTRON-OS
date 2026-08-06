from github import Github

from app.github.auth import github_auth


class GithubClient:

    def __init__(self):

        self.client = Github(
            github_auth.token
        )


github_client = GithubClient()