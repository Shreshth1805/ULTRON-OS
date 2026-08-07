import json

from pathlib import Path

from app.skills.models import Skill


SKILL_DIR = Path(
    "storage/skills"
)

SKILL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


class SkillRepository:

    def save(
        self,
        skill: Skill
    ):

        path = SKILL_DIR / f"{skill.name}.json"

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                skill.__dict__,
                f,
                indent=4
            )

    def load(
        self,
        name
    ):

        path = SKILL_DIR / f"{name}.json"

        if not path.exists():

            return None

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def all(self):

        return [

            file.stem

            for file in SKILL_DIR.glob("*.json")

        ]


skill_repository = SkillRepository()