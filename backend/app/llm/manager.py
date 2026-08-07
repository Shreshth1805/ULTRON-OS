from app.llm.registry import (
    list_models,
    get_model
)


class LLMManager:

    def available_models(self):

        return list_models()

    def get(self, name):

        return get_model(name)

    def health(self):

        status = {}

        for model_name in list_models():

            model = get_model(model_name)

            status[model_name] = model is not None

        return status


llm_manager = LLMManager()