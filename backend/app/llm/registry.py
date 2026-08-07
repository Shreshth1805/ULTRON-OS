from typing import Dict

from app.core.groq import groq_model


class LLMRegistry:
    """
    Central registry for ULTRON language models.
    """

    def __init__(self):

        self._models: Dict[str, object] = {
            "groq": groq_model
        }

    # =====================================================
    # GET MODEL
    # =====================================================

    def get(
        self,
        name: str = "groq"
    ):

        return self._models.get(name)

    # =====================================================
    # REGISTER
    # =====================================================

    def register(
        self,
        name: str,
        model
    ):

        self._models[name] = model

    # =====================================================
    # REMOVE
    # =====================================================

    def unregister(
        self,
        name: str
    ):

        self._models.pop(
            name,
            None
        )

    # =====================================================
    # EXISTS
    # =====================================================

    def exists(
        self,
        name: str
    ) -> bool:

        return name in self._models

    # =====================================================
    # LIST
    # =====================================================

    def list_models(self):

        return list(
            self._models.keys()
        )

    # =====================================================
    # DEFAULT
    # =====================================================

    @property
    def default(self):

        return self._models.get(
            "groq"
        )


# =========================================================
# GLOBAL REGISTRY
# =========================================================

llm_registry = LLMRegistry()


# =========================================================
# COMPATIBILITY FUNCTIONS
# =========================================================

def get_model(
    name: str = "groq"
):

    return llm_registry.get(
        name
    )


def list_models():

    return llm_registry.list_models()


def register_model(
    name: str,
    model
):

    llm_registry.register(
        name,
        model
    )


def remove_model(
    name: str
):

    llm_registry.unregister(
        name
    )