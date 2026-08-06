from app.knowledge.loader import loader
from app.knowledge.chunker import split_documents
from app.knowledge.vectorstore import vectorstore


def index_document(filename):

    docs = loader.load(filename)

    docs = split_documents(docs)

    vectorstore.add_documents(docs)

    return {
        "success": True,
        "chunks": len(docs)
    }