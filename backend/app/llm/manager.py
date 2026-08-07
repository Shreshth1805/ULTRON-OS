from app.llm.registry import llm_registry
class LLMManager:
    """
    High-level manager for ULTRON's language models.
    Uses the central LLM registry to discover and access
    available models.
    """
    def available_models(self):
        return llm_registry.list_models()
    def get(self, name: str = "groq"):
        return llm_registry.get(name)
    def health(self):
        status = {}
        for model_name in llm_registry.list_models():
            model = llm_registry.get(model_name)
            status[model_name] = model is not None
        return status
llm_manager = LLMManager()