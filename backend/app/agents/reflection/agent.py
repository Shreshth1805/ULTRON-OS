from app.core.llm import llm

from app.agents.reflection.prompts import REFLECTION_PROMPT

from app.agents.reflection.analyzer import parse_reflection


class ReflectionAgent:

    def reflect(

        self,

        project,

        execution,

        testing,

        review

    ):

        prompt = REFLECTION_PROMPT.format(

            project=project,

            execution=execution,

            testing=testing,

            review=review

        )

        response = llm.invoke(prompt)

        data = parse_reflection(

            response.content

        )

        data["success"] = True

        return data


reflection_agent = ReflectionAgent()