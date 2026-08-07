from functools import lru_cache

from app.core.config import settings


class EmbeddingFactory:
    """
    Central embedding factory.

    Supported Providers

    - HuggingFace
    - OpenAI
    - Ollama
    - NVIDIA

    Controlled using:

    EMBEDDING_PROVIDER
    EMBEDDING_MODEL
    """

    @lru_cache(maxsize=1)
    def get(self):

        provider = getattr(
            settings,
            "EMBEDDING_PROVIDER",
            "huggingface"
        ).lower()

        model_name = getattr(
            settings,
            "EMBEDDING_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        # ===========================================
        # HuggingFace
        # ===========================================

        if provider == "huggingface":

            from langchain_huggingface import (
                HuggingFaceEmbeddings
            )

            return HuggingFaceEmbeddings(

                model_name=model_name

            )

        # ===========================================
        # OpenAI
        # ===========================================

        elif provider == "openai":

            from langchain_openai import (
                OpenAIEmbeddings
            )

            return OpenAIEmbeddings(

                model=model_name

            )

        # ===========================================
        # Ollama
        # ===========================================

        elif provider == "ollama":

            from langchain_ollama import (
                OllamaEmbeddings
            )

            return OllamaEmbeddings(

                model=model_name

            )

        # ===========================================
        # NVIDIA
        # ===========================================

        elif provider == "nvidia":

            from langchain_nvidia_ai_endpoints import (
                NVIDIAEmbeddings
            )

            return NVIDIAEmbeddings(

                model=model_name

            )

        raise ValueError(

            f"Unsupported embedding provider: {provider}"

        )


embedding_factory = EmbeddingFactory()

embeddings = embedding_factory.get()