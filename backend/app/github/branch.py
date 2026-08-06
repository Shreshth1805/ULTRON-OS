from github import Github

from app.github.client import github_client


class BranchManager:

    def create(

        self,

        repository,

        branch

    ):

        repo = github_client.client.get_repo(
            repository
        )

        source = repo.get_branch(
            repo.default_branch
        )

        repo.create_git_ref(

            ref=f"refs/heads/{branch}",

            sha=source.commit.sha

        )

        return True


branch_manager = BranchManager()