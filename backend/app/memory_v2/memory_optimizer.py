from collections import defaultdict
from typing import Dict

from app.memory_v2.memory_manager import memory_manager
from app.memory_v2.reasoning_cache import reasoning_cache
from app.memory_v2.episodic_memory import episodic_memory
from app.memory_v2.knowledge_graph import knowledge_graph


class MemoryOptimizer:
    """
    ULTRON Memory Optimizer

    Responsibilities

    • Remove duplicate memories
    • Compress cache
    • Remove expired cache
    • Clean knowledge graph
    • Generate optimization statistics
    """

    # =====================================================
    # Remove Duplicate Memories
    # =====================================================

    def deduplicate(self):

        seen = {}

        removed = 0

        memories = list(memory_manager.list())

        for item in memories:

            key = item.content.strip().lower()

            if key in seen:

                memory_manager.delete(item.id)

                removed += 1

            else:

                seen[key] = item.id

        return {

            "duplicates_removed": removed

        }

    # =====================================================
    # Cleanup Expired Cache
    # =====================================================

    def cleanup_cache(self):

        before = reasoning_cache.stats()["cached_items"]

        reasoning_cache.cleanup()

        after = reasoning_cache.stats()["cached_items"]

        return {

            "before": before,

            "after": after,

            "removed": before - after

        }

    # =====================================================
    # Analyze Categories
    # =====================================================

    def category_report(self):

        report = defaultdict(int)

        for item in memory_manager.list():

            report[item.category] += 1

        return dict(report)

    # =====================================================
    # Graph Validation
    # =====================================================

    def validate_graph(self):

        missing = []

        for edge in knowledge_graph.edges:

            if edge.source not in knowledge_graph.nodes:

                missing.append(edge.source)

            if edge.target not in knowledge_graph.nodes:

                missing.append(edge.target)

        return {

            "missing_nodes": list(set(missing)),

            "valid": len(missing) == 0

        }

    # =====================================================
    # Episode Statistics
    # =====================================================

    def episode_report(self):

        return episodic_memory.stats()

    # =====================================================
    # Global Statistics
    # =====================================================

    def stats(self):

        return {

            "memory": memory_manager.stats(),

            "episodes": episodic_memory.stats(),

            "knowledge_graph": knowledge_graph.stats(),

            "cache": reasoning_cache.stats(),

            "categories": self.category_report()

        }

    # =====================================================
    # Optimize Everything
    # =====================================================

    def optimize(self):

        duplicate_report = self.deduplicate()

        cache_report = self.cleanup_cache()

        graph_report = self.validate_graph()

        return {

            "success": True,

            "duplicates": duplicate_report,

            "cache": cache_report,

            "graph": graph_report,

            "statistics": self.stats()

        }


memory_optimizer = MemoryOptimizer()