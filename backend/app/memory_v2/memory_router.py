from typing import List

from app.memory_v2.memory_manager import memory_manager
from app.memory_v2.episodic_memory import episodic_memory
from app.memory_v2.knowledge_graph import knowledge_graph
from app.memory_v2.semantic_search import semantic_search
from app.memory_v2.reasoning_cache import reasoning_cache


class MemoryRouter:
    """
    Unified interface for every memory subsystem.

    Handles

    • Long-term memory
    • Episodic memory
    • Knowledge graph
    • Semantic search
    • Reasoning cache
    """

    # =====================================================
    # Long-Term Memory
    # =====================================================

    def remember(

        self,

        category: str,

        content: str,

        metadata=None

    ):

        return memory_manager.add(

            category=category,

            content=content,

            metadata=metadata or {}

        )

    # =====================================================
    # Search Memories
    # =====================================================

    def search(

        self,

        query: str

    ):

        return memory_manager.search(query)

    # =====================================================
    # Semantic Search
    # =====================================================

    def semantic(

        self,

        query: str,

        top_k: int = 5

    ):

        return semantic_search.search(

            query=query,

            top_k=top_k

        )

    # =====================================================
    # Episodes
    # =====================================================

    def remember_episode(

        self,

        task,

        agent,

        success,

        result,

        metadata=None

    ):

        return episodic_memory.remember(

            task,

            agent,

            success,

            result,

            metadata

        )

    def episodes(self):

        return episodic_memory.list()

    # =====================================================
    # Knowledge Graph
    # =====================================================

    def add_node(

        self,

        node_id,

        node_type,

        **properties

    ):

        return knowledge_graph.add_node(

            node_id,

            node_type,

            **properties

        )

    def add_edge(

        self,

        source,

        relation,

        target

    ):

        return knowledge_graph.add_edge(

            source,

            relation,

            target

        )

    # =====================================================
    # Reasoning Cache
    # =====================================================

    def cache(

        self,

        prompt,

        response,

        ttl=3600

    ):

        reasoning_cache.store(

            prompt,

            response,

            ttl

        )

    def cached(

        self,

        prompt

    ):

        return reasoning_cache.get(prompt)

    # =====================================================
    # Statistics
    # =====================================================

    def stats(self):

        return {

            "memory": memory_manager.stats(),

            "episodes": episodic_memory.stats(),

            "knowledge": knowledge_graph.stats(),

            "cache": reasoning_cache.stats()

        }

    # =====================================================
    # Reset
    # =====================================================

    def clear(self):

        memory_manager.clear()

        episodic_memory.clear()

        knowledge_graph.clear()

        reasoning_cache.clear()


memory_router = MemoryRouter()