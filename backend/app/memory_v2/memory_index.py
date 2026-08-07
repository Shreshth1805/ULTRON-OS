from typing import Dict, List

from app.memory_v2.memory_manager import memory_manager
from app.memory_v2.vector_store import vector_store


class MemoryIndex:
    """
    Central memory indexing layer.

    Responsibilities
    ----------------
    • Index new memories
    • Retrieve memories
    • Semantic search
    • Category filtering
    • Statistics
    """

    # =====================================================
    # Add
    # =====================================================

    def add(
        self,
        category: str,
        content: str,
        metadata: Dict | None = None
    ) -> str:

        return memory_manager.add(
            category=category,
            content=content,
            metadata=metadata
        )

    # =====================================================
    # Get
    # =====================================================

    def get(
        self,
        memory_id: str
    ):

        return memory_manager.get(
            memory_id
        )

    # =====================================================
    # Update
    # =====================================================

    def update(
        self,
        memory_id: str,
        content: str = None,
        metadata: Dict | None = None
    ):

        return memory_manager.update(
            memory_id=memory_id,
            content=content,
            metadata=metadata
        )

    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        memory_id: str
    ):

        return memory_manager.delete(
            memory_id
        )

    # =====================================================
    # List
    # =====================================================

    def list(
        self,
        category: str = None
    ):

        return memory_manager.list(
            category
        )

    # =====================================================
    # Keyword Search
    # =====================================================

    def keyword_search(
        self,
        query: str
    ):

        return memory_manager.search(
            query
        )

    # =====================================================
    # Semantic Search
    # =====================================================

    def semantic_search(
        self,
        query: str,
        k: int = 5
    ):

        return vector_store.similarity_search(
            query=query,
            k=k
        )

    # =====================================================
    # Semantic Search with Scores
    # =====================================================

    def semantic_search_with_score(
        self,
        query: str,
        k: int = 5
    ):

        return vector_store.similarity_search_with_score(
            query=query,
            k=k
        )

    # =====================================================
    # Hybrid Search
    # =====================================================

    def hybrid_search(
        self,
        query: str,
        k: int = 5
    ):

        semantic = self.semantic_search(
            query=query,
            k=k
        )

        keyword = self.keyword_search(
            query
        )

        return {
            "semantic": semantic,
            "keyword": keyword
        }

    # =====================================================
    # Stats
    # =====================================================

    def stats(self):

        return memory_manager.stats()

    # =====================================================
    # Clear
    # =====================================================

    def clear(self):

        memory_manager.clear()


memory_index = MemoryIndex()