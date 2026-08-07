import difflib


class DiffEngine:

    def compare(

        self,

        old,

        new

    ):

        return "\n".join(

            difflib.unified_diff(

                old.splitlines(),

                new.splitlines(),

                lineterm=""

            )

        )


diff_engine = DiffEngine()