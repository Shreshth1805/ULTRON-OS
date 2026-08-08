"""
ULTRON Memory Manager

Provides a single interface for:

    - User memories
    - Project memories
    - Agent knowledge
    - Workflow history
    - Execution results

Uses:

    In-memory storage
        +
    Vector store for semantic search

This module is intentionally independent from the older
app.memory package.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.memory_v2.memory_store import MemoryItem
from app.memory_v2.vector_store import vector_store


class MemoryManager:
    """
    Central long-term memory manager for ULTRON.
    """

    def __init__(self) -> None:

        self._memory: Dict[str, MemoryItem] = {}

    # =========================================================
    # ADD MEMORY
    # =========================================================

    def add(
        self,
        category: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:

        if not category:
            raise ValueError(
                "Memory category cannot be empty."
            )

        if content is None:
            raise ValueError(
                "Memory content cannot be None."
            )

        content = str(content)

        memory_id = str(uuid4())

        metadata = dict(
            metadata or {}
        )

        item = MemoryItem(
            id=memory_id,
            category=category,
            content=content,
            metadata=metadata
        )

        self._memory[memory_id] = item

        # -----------------------------------------------------
        # Vector Store
        # -----------------------------------------------------

        try:

            vector_store.add_text(
                text=content,
                metadata={
                    "id": memory_id,
                    "category": category,
                    **metadata
                }
            )

        except Exception as exc:

            # Do not destroy the primary in-memory memory
            # if the vector database is temporarily unavailable.
            print(
                f"[MemoryManager] Vector store add failed: {exc}"
            )

        return memory_id

    # =========================================================
    # GET MEMORY
    # =========================================================

    def get(
        self,
        memory_id: str
    ) -> Optional[MemoryItem]:

        return self._memory.get(
            memory_id
        )

    # =========================================================
    # DELETE MEMORY
    # =========================================================

    def delete(
        self,
        memory_id: str
    ) -> bool:

        if memory_id not in self._memory:
            return False

        del self._memory[memory_id]

        try:

            vector_store.delete(
                [memory_id]
            )

        except Exception as exc:

            print(
                f"[MemoryManager] Vector delete failed: {exc}"
            )

        return True

    # =========================================================
    # UPDATE MEMORY
    # =========================================================

    def update(
        self,
        memory_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:

        item = self._memory.get(
            memory_id
        )

        if item is None:
            return False

        # -----------------------------------------------------
        # Update content
        # -----------------------------------------------------

        if content is not None:

            item.content = str(
                content
            )

        # -----------------------------------------------------
        # Update metadata
        # -----------------------------------------------------

        if metadata is not None:

            item.metadata.update(
                metadata
            )

        # -----------------------------------------------------
        # Refresh vector representation
        # -----------------------------------------------------

        try:

            vector_store.delete(
                [memory_id]
            )

        except Exception as exc:

            print(
                f"[MemoryManager] Vector delete failed during update: {exc}"
            )

        try:

            vector_store.add_text(
                text=item.content,
                metadata={
                    "id": memory_id,
                    "category": item.category,
                    **item.metadata
                }
            )

        except Exception as exc:

            print(
                f"[MemoryManager] Vector update failed: {exc}"
            )

        return True

    # =========================================================
    # LIST MEMORIES
    # =========================================================

    def list(
        self,
        category: Optional[str] = None
    ) -> List[MemoryItem]:

        if category is None:

            return list(
                self._memory.values()
            )

        return [
            item
            for item in self._memory.values()
            if item.category == category
        ]

    # =========================================================
    # SEARCH BY KEYWORD
    # =========================================================

    def search(
        self,
        query: str,
        category: Optional[str] = None
    ) -> List[MemoryItem]:

        if not query:
            return []

        query = query.lower()

        results = []

        for item in self._memory.values():

            if category is not None:
                if item.category != category:
                    continue

            if query in item.content.lower():

                results.append(
                    item
                )

        return results

    # =========================================================
    # SEMANTIC SEARCH
    # =========================================================

    def semantic_search(
        self,
        query: str,
        k: int = 5
    ):

        if not query:
            return []

        if k <= 0:
            return []

        try:

            return vector_store.similarity_search(
                query=query,
                k=k
            )

        except Exception as exc:

            print(
                f"[MemoryManager] Semantic search failed: {exc}"
            )

            return []

    # =========================================================
    # REMEMBER PROJECT
    # =========================================================

    def remember_project(
        self,
        project_name: str,
        project_path: str,
        description: str = ""
    ) -> str:

        return self.add(
            category="project",
            content=(
                f"Project: {project_name}\n"
                f"Path: {project_path}\n"
                f"Description: {description}"
            ),
            metadata={
                "project_name": project_name,
                "project_path": project_path
            }
        )

    # =========================================================
    # REMEMBER WORKFLOW RESULT
    # =========================================================

    def remember_workflow(
        self,
        task_name: str,
        result: Any
    ) -> str:

        return self.add(
            category="workflow",
            content=str(result),
            metadata={
                "task_name": task_name
            }
        )

    # =========================================================
    # REMEMBER AGENT RESULT
    # =========================================================

    def remember_agent_result(
        self,
        agent: str,
        action: str,
        result: Any
    ) -> str:

        return self.add(
            category="agent_result",
            content=str(result),
            metadata={
                "agent": agent,
                "action": action
            }
        )

    # =========================================================
    # STATS
    # =========================================================

    def stats(self) -> Dict[str, Any]:

        categories: Dict[str, int] = {}

        for item in self._memory.values():

            categories[item.category] = (
                categories.get(
                    item.category,
                    0
                ) + 1
            )

        try:

            vector_count = vector_store.count()

        except Exception:

            vector_count = 0

        return {
            "total_memories": len(
                self._memory
            ),
            "vector_memories": vector_count,
            "categories": categories
        }

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:

        self._memory.clear()

        try:

            vector_store.clear()

        except Exception as exc:

            print(
                f"[MemoryManager] Vector clear failed: {exc}"
            )


# =========================================================
# GLOBAL MEMORY MANAGER
# =========================================================

memory_manager = MemoryManager()