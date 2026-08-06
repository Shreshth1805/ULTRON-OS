import os


class GithubAuth:

    @property
    def token(self):

        token = os.getenv("GITHUB_TOKEN")

        if not token:

            raise ValueError(
                "GITHUB_TOKEN not found."
            )

        return token


github_auth = GithubAuth()