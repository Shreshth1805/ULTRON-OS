from app.llm.factory import llm_factory


class ModelRouter:

    def route(
        self,
        task: str
    ):

        task = task.lower()

        if "code" in task:

            return llm_factory.get("groq")

        if "image" in task:

            return llm_factory.get("openai")

        if "offline" in task:

            return llm_factory.get("ollama")

        return llm_factory.get("groq")


model_router = ModelRouter()