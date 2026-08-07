from app.versioning.manager import (
    version_manager
)

from app.versioning.diff import (
    diff_engine
)


class VersionAgent:

    def save(

        self,

        project,

        files,

        message="Auto Save"

    ):

        return version_manager.create_version(

            project,

            files,

            message

        )

    def compare(

        self,

        old,

        new

    ):

        return diff_engine.compare(

            old,

            new

        )


version_agent = VersionAgent()