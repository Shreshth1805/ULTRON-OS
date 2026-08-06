import subprocess
from pathlib import Path


class CommitManager:

    def commit(

        self,

        project,

        message

    ):

        subprocess.run(

            ["git", "add", "."],

            cwd=project

        )

        subprocess.run(

            [

                "git",

                "commit",

                "-m",

                message

            ],

            cwd=project

        )

        return True


commit_manager = CommitManager()