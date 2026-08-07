from langchain_groq import ChatGroq

from app.core.config import settings

from app.llm.registry import register_model


groq = ChatGroq(

    model=settings.GROQ_MODEL,

    api_key=settings.GROQ_API_KEY

)

register_model(

    "groq",

    groq

)