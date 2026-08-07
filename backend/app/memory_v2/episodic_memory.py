from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
from uuid import uuid4


@dataclass
class Episode:

    id: str

    task: str

    agent: str

    success: bool

    result: Dict

    metadata: Dict = field(default_factory=dict)

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )


class EpisodicMemory:

    """
    Stores complete execution episodes.

    Examples

    • Generated FastAPI project
    • Fixed Docker bug
    • Reviewed repository
    • Trained ML model
    • Security scan
    """

    def __init__(self):

        self._episodes: Dict[str, Episode] = {}

    # =====================================================
    # Save Episode
    # =====================================================

    def remember(

        self,

        task: str,

        agent: str,

        success: bool,

        result: Dict,

        metadata=None

    ) -> str:

        episode = Episode(

            id=str(uuid4()),

            task=task,

            agent=agent,

            success=success,

            result=result,

            metadata=metadata or {}

        )

        self._episodes[episode.id] = episode

        return episode.id

    # =====================================================
    # Get
    # =====================================================

    def get(self, episode_id):

        return self._episodes.get(episode_id)

    # =====================================================
    # List
    # =====================================================

    def list(self):

        return list(self._episodes.values())

    # =====================================================
    # By Agent
    # =====================================================

    def by_agent(

        self,

        agent: str

    ):

        return [

            e

            for e in self._episodes.values()

            if e.agent == agent

        ]

    # =====================================================
    # Successful Episodes
    # =====================================================

    def successful(self):

        return [

            e

            for e in self._episodes.values()

            if e.success

        ]

    # =====================================================
    # Failed Episodes
    # =====================================================

    def failed(self):

        return [

            e

            for e in self._episodes.values()

            if not e.success

        ]

    # =====================================================
    # Search
    # =====================================================

    def search(

        self,

        text: str

    ):

        text = text.lower()

        return [

            e

            for e in self._episodes.values()

            if text in e.task.lower()

        ]

    # =====================================================
    # Statistics
    # =====================================================

    def stats(self):

        success = len(self.successful())

        failed = len(self.failed())

        total = len(self._episodes)

        return {

            "episodes": total,

            "successful": success,

            "failed": failed

        }

    # =====================================================
    # Clear
    # =====================================================

    def clear(self):

        self._episodes.clear()


episodic_memory = EpisodicMemory()