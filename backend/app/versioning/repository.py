import json
from pathlib import Path

VERSION_DIR = Path("storage/versions")
VERSION_DIR.mkdir(
    parents=True,
    exist_ok=True
)


class VersionRepository:

    def save(
        self,
        project,
        version,
        data
    ):

        folder = VERSION_DIR / project

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        path = folder / f"{version}.json"

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    def load(
        self,
        project,
        version
    ):

        path = VERSION_DIR / project / f"{version}.json"

        if not path.exists():

            return None

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)


version_repository = VersionRepository()