from app.skills.repository import (
    skill_repository
)


class SkillSearch:

    def search(
        self,
        keyword
    ):

        results = []

        for name in skill_repository.all():

            skill = skill_repository.load(
                name
            )

            if skill is None:

                continue

            text = str(skill).lower()

            if keyword.lower() in text:

                results.append(
                    skill
                )

        return results


skill_search = SkillSearch()