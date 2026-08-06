import subprocess


class PushManager:

    def push(

        self,

        project,

        branch="main"

    ):

        subprocess.run(

            [

                "git",

                "push",

                "-u",

                "origin",

                branch

            ],

            cwd=project

        )

        return True


push_manager = PushManager()