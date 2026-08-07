from app.llm.registry import llm_registry


class ModelRouter:
    """
    Central model-selection layer for ULTRON.
    """

    def route(
        self,
        prompt: str = ""
    ):

        model = llm_registry.default

        if model is None:

            raise RuntimeError(
                "No default LLM is available."
            )

        return model

    def get(
        self,
        name: str = "groq"
    ):

        model = llm_registry.get(
            name
        )

        if model is None:

            raise ValueError(
                f"LLM '{name}' is not registered."
            )

        return model

    def available_models(self):

        return llm_registry.list_models()


model_router = ModelRouter()