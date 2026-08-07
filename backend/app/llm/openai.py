from langchain_openai import ChatOpenAI

from app.core.config import settings

from app.llm.registry import register_model


openai_model = ChatOpenAI(

    model="gpt-4.1",

    api_key=settings.OPENAI_API_KEY

)

register_model(

    "openai",

    openai_model

)