import json
from pathlib import Path
from typing import Dict

from app.memory_v2.memory_manager import memory_manager
from app.memory_v2.episodic_memory import episodic_memory
from app.memory_v2.knowledge_graph import knowledge_graph
from app.memory_v2.reasoning_cache import reasoning_cache


class MemorySync:
    """
    ULTRON Memory Synchronization

    Handles

    • Backup
    • Restore
    • Export
    • Import
    • Synchronization
    """

    # =====================================================
    # Export
    # =====================================================

    def export(self) -> Dict:

        return {

            "memories": [

                vars(item)

                for item in memory_manager.list()

            ],

            "episodes": [

                vars(item)

                for item in episodic_memory.list()

            ],

            "knowledge": {

                "nodes": {

                    key: {

                        "id": node.id,

                        "type": node.type,

                        "properties": node.properties

                    }

                    for key, node in knowledge_graph.nodes.items()

                },

                "edges": [

                    {

                        "source": edge.source,

                        "relation": edge.relation,

                        "target": edge.target

                    }

                    for edge in knowledge_graph.edges

                ]

            },

            "cache": reasoning_cache.stats()

        }

    # =====================================================
    # Backup
    # =====================================================

    def backup(

        self,

        path: str

    ):

        data = self.export()

        Path(path).parent.mkdir(

            parents=True,

            exist_ok=True

        )

        with open(

            path,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                data,

                f,

                indent=4

            )

        return {

            "success": True,

            "backup": path

        }

    # =====================================================
    # Restore
    # =====================================================

    def restore(

        self,

        path: str

    ):

        if not Path(path).exists():

            return {

                "success": False,

                "error": "Backup file not found."

            }

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as f:

            data = json.load(f)

        memory_manager.clear()

        episodic_memory.clear()

        knowledge_graph.clear()

        reasoning_cache.clear()

        # ------------------------
        # Restore Memories
        # ------------------------

        for item in data.get(

            "memories",

            []

        ):

            memory_manager.add(

                category=item["category"],

                content=item["content"],

                metadata=item.get(

                    "metadata",

                    {}

                )

            )

        # ------------------------
        # Restore Episodes
        # ------------------------

        for ep in data.get(

            "episodes",

            []

        ):

            episodic_memory.remember(

                task=ep["task"],

                agent=ep["agent"],

                success=ep["success"],

                result=ep["result"],

                metadata=ep.get(

                    "metadata",

                    {}

                )

            )

        # ------------------------
        # Restore Graph
        # ------------------------

        graph = data.get(

            "knowledge",

            {}

        )

        for node in graph.get(

            "nodes",

            {}

        ).values():

            knowledge_graph.add_node(

                node["id"],

                node["type"],

                **node.get(

                    "properties",

                    {}

                )

            )

        for edge in graph.get(

            "edges",

            []

        ):

            knowledge_graph.add_edge(

                edge["source"],

                edge["relation"],

                edge["target"]

            )

        return {

            "success": True,

            "message": "Memory restored successfully."

        }

    # =====================================================
    # Synchronize
    # =====================================================

    def synchronize(self):

        return {

            "success": True,

            "memory": memory_manager.stats(),

            "episodes": episodic_memory.stats(),

            "knowledge": knowledge_graph.stats(),

            "cache": reasoning_cache.stats()

        }


memory_sync = MemorySync()