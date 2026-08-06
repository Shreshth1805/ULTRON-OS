from app.github.repository import repository_manager
from app.github.commit import commit_manager
from app.github.push import push_manager
from app.github.branch import branch_manager
from app.github.pull_request import pull_request_manager


class GithubManager:

    def publish(

        self,

        project_name,

        project_path

    ):

        clone_url = repository_manager.create(
            project_name
        )

        return {

            "repository": clone_url

        }


github_manager = GithubManager()