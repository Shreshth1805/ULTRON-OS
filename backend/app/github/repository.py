from app.github.client import github_client


class RepositoryManager:

    def create(

        self,

        name,

        private=True

    ):

        user = github_client.client.get_user()

        repo = user.create_repo(

            name=name,

            private=private

        )

        return repo.clone_url


repository_manager = RepositoryManager()