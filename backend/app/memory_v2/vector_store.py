from pathlib import Path
from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import settings
from app.memory_v2.embeddings import embeddings


class VectorStore:
    """
    Central Vector Database.

    Responsibilities

    • Store documents
    • Semantic search
    • Delete documents
    • Persistent storage
    """

    def __init__(self):

        persist_dir = Path(settings.VECTOR_DB_PATH)

        persist_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.db = Chroma(

            collection_name="ultron_memory",

            persist_directory=str(persist_dir),

            embedding_function=embeddings

        )

    # =====================================================
    # Add Documents
    # =====================================================

    def add_documents(

        self,

        documents: List[Document]

    ):

        if not documents:

            return

        self.db.add_documents(documents)

    # =====================================================
    # Add Text
    # =====================================================

    def add_text(

        self,

        text: str,

        metadata=None

    ):

        doc = Document(

            page_content=text,

            metadata=metadata or {}

        )

        self.db.add_documents([doc])

    # =====================================================
    # Similarity Search
    # =====================================================

    def similarity_search(

        self,

        query: str,

        k: int = 5

    ):

        return self.db.similarity_search(

            query,

            k=k

        )

    # =====================================================
    # Search With Score
    # =====================================================

    def similarity_search_with_score(

        self,

        query: str,

        k: int = 5

    ):

        return self.db.similarity_search_with_score(

            query,

            k=k

        )

    # =====================================================
    # Delete
    # =====================================================

    def delete(

        self,

        ids: List[str]

    ):

        self.db.delete(ids=ids)

    # =====================================================
    # Count
    # =====================================================

    def count(self):

        try:

            return self.db._collection.count()

        except Exception:

            return 0

    # =====================================================
    # Reset
    # =====================================================

    def clear(self):

        try:

            collection = self.db._collection

            ids = collection.get()["ids"]

            if ids:

                collection.delete(ids)

        except Exception:

            pass


vector_store = VectorStore()