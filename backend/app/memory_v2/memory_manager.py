from typing import Dict, List
from uuid import uuid4

from app.memory_v2.memory_store import MemoryItem
from app.memory_v2.vector_store import vector_store


class MemoryManager:
    """
    Long-term memory manager for ULTRON.

    Stores:
    - User memories
    - Agent knowledge
    - Project history
    - Execution results

    Backed by:
    - In-memory dictionary
    - Chroma Vector Database
    """

    def __init__(self):

        self._memory: Dict[str, MemoryItem] = {}

    # =====================================================
    # Add Memory
    # =====================================================

    def add(
        self,
        category: str,
        content: str,
        metadata: Dict | None = None
    ) -> str:

        memory_id = str(uuid4())

        metadata = metadata or {}

        item = MemoryItem(

            id=memory_id,

            category=category,

            content=content,

            metadata=metadata

        )

        self._memory[memory_id] = item

        # -----------------------------------------------
        # Store inside Vector DB
        # -----------------------------------------------

        vector_store.add_text(

            text=content,

            metadata={

                "id": memory_id,

                "category": category,

                **metadata

            }

        )

        return memory_id

    # =====================================================
    # Get Memory
    # =====================================================

    def get(
        self,
        memory_id: str
    ):

        return self._memory.get(memory_id)

    # =====================================================
    # Delete Memory
    # =====================================================

    def delete(
        self,
        memory_id: str
    ) -> bool:

        if memory_id not in self._memory:

            return False

        del self._memory[memory_id]

        try:

            vector_store.delete([memory_id])

        except Exception:

            pass

        return True

    # =====================================================
    # Update Memory
    # =====================================================

    def update(
        self,
        memory_id: str,
        content: str = None,
        metadata: Dict = None
    ) -> bool:

        item = self._memory.get(memory_id)

        if item is None:

            return False

        if content is not None:

            item.content = content

        if metadata is not None:

            item.metadata.update(metadata)

        # -----------------------------------------------
        # Refresh Vector DB
        # -----------------------------------------------

        try:

            vector_store.delete([memory_id])

        except Exception:

            pass

        vector_store.add_text(

            text=item.content,

            metadata={

                "id": memory_id,

                "category": item.category,

                **item.metadata

            }

        )

        return True

    # =====================================================
    # List Memories
    # =====================================================

    def list(
        self,
        category: str = None
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

    # =====================================================
    # Keyword Search
    # =====================================================

    def search(
        self,
        query: str
    ) -> List[MemoryItem]:

        query = query.lower()

        return [

            item

            for item in self._memory.values()

            if query in item.content.lower()

        ]

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
    # Stats
    # =====================================================

    def stats(self):

        categories = {}

        for item in self._memory.values():

            categories[item.category] = (

                categories.get(

                    item.category,

                    0

                ) + 1

            )

        return {

            "total_memories": len(self._memory),

            "vector_memories": vector_store.count(),

            "categories": categories

        }

    # =====================================================
    # Clear Everything
    # =====================================================

    def clear(self):

        self._memory.clear()

        try:

            vector_store.clear()

        except Exception:

            pass


memory_manager = MemoryManager()