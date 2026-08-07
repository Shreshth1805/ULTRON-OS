from app.skills.models import Skill

from app.skills.repository import (
    skill_repository
)


class SkillManager:

    def save_skill(

        self,

        name,

        description,

        language,

        code,

        tags

    ):

        skill = Skill(

            name=name,

            description=description,

            language=language,

            code=code,

            tags=tags

        )

        skill_repository.save(
            skill
        )

        return {

            "success": True,

            "skill": name

        }


skill_manager = SkillManager()