from pathlib import Path
import json


MEMORY_DIR = Path("storage/learning")

MEMORY_DIR.mkdir(
    parents=True,
    exist_ok=True
)


class LearningMemory:

    def save(
        self,
        key,
        data
    ):

        path = MEMORY_DIR / f"{key}.json"

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
        key
    ):

        path = MEMORY_DIR / f"{key}.json"

        if not path.exists():

            return None

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def list_projects(self):

        return [

            file.stem

            for file in MEMORY_DIR.glob("*.json")

        ]


learning_memory = LearningMemory()