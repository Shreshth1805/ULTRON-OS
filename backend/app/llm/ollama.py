from langchain_ollama import ChatOllama

from app.llm.registry import register_model


ollama = ChatOllama(

    model="llama3"

)

register_model(

    "ollama",

    ollama

)