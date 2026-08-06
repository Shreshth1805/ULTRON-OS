from pathlib import Path


class CodePatcher:

    def read(self, filename):

        return Path(filename).read_text(
            encoding="utf-8"
        )

    def write(self, filename, code):

        Path(filename).write_text(
            code,
            encoding="utf-8"
        )


patcher = CodePatcher()