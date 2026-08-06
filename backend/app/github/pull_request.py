from app.github.client import github_client


class PullRequestManager:

    def create(

        self,

        repository,

        title,

        body,

        head,

        base="main"

    ):

        repo = github_client.client.get_repo(
            repository
        )

        pr = repo.create_pull(

            title=title,

            body=body,

            head=head,

            base=base

        )

        return pr.html_url


pull_request_manager = PullRequestManager()