from langchain_chroma import Chroma

from app.knowledge.embeddings import embeddings


vectorstore = Chroma(

    collection_name="ultron",

    embedding_function=embeddings,

    persist_directory="./vectorstore"

)