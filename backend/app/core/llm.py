"""
Compatibility Layer

Older modules use:

    from app.core.llm import llm

New architecture uses:

    app.llm.model_router

This file keeps both working.
"""

from app.llm import model_router


class LLMProxy:
    """
    Compatibility wrapper around the new Model Router.
    """

    def invoke(self, prompt: str):

        model = model_router.route(prompt)

        if model is None:
            raise RuntimeError(
                "No LLM has been registered."
            )

        return model.invoke(prompt)

    def predict(self, prompt: str):

        response = self.invoke(prompt)

        return getattr(
            response,
            "content",
            str(response)
        )

    def generate(self, prompt: str):

        response = self.invoke(prompt)

        return getattr(
            response,
            "content",
            str(response)
        )


llm = LLMProxy()