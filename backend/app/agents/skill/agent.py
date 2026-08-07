from app.skills.manager import (
    skill_manager
)

from app.skills.search import (
    skill_search
)


class SkillAgent:

    def save_skill(

        self,

        **kwargs

    ):

        return skill_manager.save_skill(
            **kwargs
        )

    def search(

        self,

        keyword

    ):

        return skill_search.search(
            keyword
        )


skill_agent = SkillAgent()