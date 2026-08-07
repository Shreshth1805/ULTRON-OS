from collections import defaultdict
from typing import Dict, List

from app.memory_v2.episodic_memory import episodic_memory
from app.memory_v2.memory_manager import memory_manager
from app.memory_v2.knowledge_graph import knowledge_graph


class SelfLearning:

    """
    ULTRON Self Learning Engine

    Learns from:

    • Successful projects
    • Failed executions
    • Code reviews
    • Security reviews
    • Testing
    • User feedback
    """

    def __init__(self):

        self.patterns = defaultdict(int)

    # =====================================================
    # Learn From Episode
    # =====================================================

    def learn_episode(self, episode):

        if episode is None:
            return

        key = episode.task.lower()

        self.patterns[key] += 1

        memory_manager.add(

            category="experience",

            content=f"{episode.task}",

            metadata={

                "agent": episode.agent,

                "success": episode.success

            }

        )

        knowledge_graph.add_node(

            episode.id,

            "episode",

            task=episode.task,

            success=episode.success

        )

        knowledge_graph.add_edge(

            episode.agent,

            "executed",

            episode.id

        )

    # =====================================================
    # Learn Everything
    # =====================================================

    def learn_all(self):

        for episode in episodic_memory.list():

            self.learn_episode(

                episode

            )

    # =====================================================
    # Record User Feedback
    # =====================================================

    def feedback(

        self,

        prompt: str,

        rating: int,

        comments: str = ""

    ):

        memory_manager.add(

            category="feedback",

            content=prompt,

            metadata={

                "rating": rating,

                "comments": comments

            }

        )

    # =====================================================
    # Best Patterns
    # =====================================================

    def best_patterns(

        self,

        top_k: int = 10

    ):

        return sorted(

            self.patterns.items(),

            key=lambda x: x[1],

            reverse=True

        )[:top_k]

    # =====================================================
    # Weak Patterns
    # =====================================================

    def weak_patterns(self):

        return [

            item

            for item in self.patterns.items()

            if item[1] == 1

        ]

    # =====================================================
    # Statistics
    # =====================================================

    def stats(self):

        return {

            "learned_patterns": len(self.patterns),

            "total_executions": sum(

                self.patterns.values()

            )

        }

    # =====================================================
    # Reset
    # =====================================================

    def clear(self):

        self.patterns.clear()


self_learning = SelfLearning()