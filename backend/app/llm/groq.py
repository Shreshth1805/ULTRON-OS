from langchain_groq import ChatGroq

from app.core.config import settings


groq_model = ChatGroq(
    groq_api_key=settings.GROQ_API_KEY,
    model_name=settings.GROQ_MODEL,
    temperature=0.2,
)