from typing import List

from app.memory_v2.memory_manager import (
    memory_manager
)


class MemoryRetriever:
    """
    Retrieves relevant memories for ULTRON.

    Later this can be upgraded to
    vector search (FAISS/Chroma).
    """

    # =====================================================
    # Retrieve by Query
    # =====================================================

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):

        memories = memory_manager.search(query)

        return memories[:top_k]

    # =====================================================
    # Retrieve by Category
    # =====================================================

    def retrieve_category(
        self,
        category: str,
        limit: int = 10
    ):

        memories = memory_manager.list(category)

        return memories[:limit]

    # =====================================================
    # Recent Memories
    # =====================================================

    def recent(
        self,
        limit: int = 10
    ):

        memories = memory_manager.list()

        memories.sort(

            key=lambda x: x.timestamp,

            reverse=True

        )

        return memories[:limit]

    # =====================================================
    # Build Context
    # =====================================================

    def build_context(
        self,
        query: str,
        top_k: int = 5
    ) -> str:

        memories = self.retrieve(

            query=query,

            top_k=top_k

        )

        if not memories:

            return ""

        context = []

        for memory in memories:

            context.append(

                f"[{memory.category}] {memory.content}"

            )

        return "\n".join(context)


memory_retriever = MemoryRetriever()