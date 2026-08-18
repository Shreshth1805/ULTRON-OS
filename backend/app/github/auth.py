from app.core.config import settings


class GithubAuth:

    @property
    def token(self):

        token = settings.GITHUB_TOKEN

        if not token:

            raise ValueError(
                "GITHUB_TOKEN not found."
            )

        return token


github_auth = GithubAuth()