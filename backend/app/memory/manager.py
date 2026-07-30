from typing import List, Dict


class MemoryManager:
    """
    Simple in-memory conversation manager.

    Later this can be replaced with Redis or a database
    without changing the API layer.
    """

    def __init__(self):
        self.sessions: Dict[str, List[Dict[str, str]]] = {}

    def create_session(self, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        return session_id

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):
        self.create_session(session_id)

        self.sessions[session_id].append(
            {
                "role": role,
                "content": content
            }
        )

    def get_history(
        self,
        session_id: str
    ) -> List[Dict[str, str]]:

        return self.sessions.get(
            session_id,
            []
        )

    def clear_session(
        self,
        session_id: str
    ):

        self.sessions.pop(
            session_id,
            None
        )

        return True


memory_manager = MemoryManager()