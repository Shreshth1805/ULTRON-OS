from langchain_huggingface import ChatHuggingFace

from app.llm.registry import register_model


hf_model = ChatHuggingFace()

register_model(

    "huggingface",

    hf_model

)