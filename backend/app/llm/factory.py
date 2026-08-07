from app.llm.registry import get_model


class LLMFactory:

    def get(
        self,
        name
    ):

        return get_model(name)


llm_factory = LLMFactory()