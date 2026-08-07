from typing import Dict, List

from app.memory_v2.memory_index import (
    memory_index
)


class SemanticSearch:
    """
    High-level semantic retrieval.

    Features
    --------
    • Semantic Search
    • Hybrid Search
    • Metadata Filtering
    • Context Builder
    """

    # =====================================================
    # Semantic Search
    # =====================================================

    def search(
        self,
        query: str,
        top_k: int = 5
    ):

        return memory_index.semantic_search(

            query=query,

            k=top_k

        )

    # =====================================================
    # Search With Scores
    # =====================================================

    def search_with_score(
        self,
        query: str,
        top_k: int = 5
    ):

        return memory_index.semantic_search_with_score(

            query=query,

            k=top_k

        )

    # =====================================================
    # Hybrid Search
    # =====================================================

    def hybrid_search(
        self,
        query: str,
        top_k: int = 5
    ):

        return memory_index.hybrid_search(

            query=query,

            k=top_k

        )

    # =====================================================
    # Filter By Metadata
    # =====================================================

    def filter_by_category(
        self,
        query: str,
        category: str,
        top_k: int = 5
    ):

        docs = self.search(

            query=query,

            top_k=top_k

        )

        filtered = []

        for doc in docs:

            if doc.metadata.get("category") == category:

                filtered.append(doc)

        return filtered

    # =====================================================
    # Build Context
    # =====================================================

    def build_context(
        self,
        query: str,
        top_k: int = 5
    ) -> str:

        docs = self.search(

            query=query,

            top_k=top_k

        )

        if not docs:

            return ""

        context = []

        for doc in docs:

            context.append(

                doc.page_content

            )

        return "\n\n".join(context)

    # =====================================================
    # Agent Prompt Context
    # =====================================================

    def build_agent_prompt(
        self,
        query: str,
        top_k: int = 5
    ) -> str:

        context = self.build_context(

            query,

            top_k

        )

        if not context:

            return ""

        return f"""

Relevant ULTRON Memory

----------------------

{context}

----------------------

Use the above information whenever it helps answer the user's request.

"""


semantic_search = SemanticSearch()