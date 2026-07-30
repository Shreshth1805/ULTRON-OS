from langchain_groq import ChatGroq

from app.core.config import settings


class LLMManager:

    def __init__(self):

        self.llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0.2
        )

    def get_llm(self):

        return self.llm


llm_manager = LLMManager()