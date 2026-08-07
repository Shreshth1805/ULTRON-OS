from dataclasses import dataclass
from datetime import datetime


@dataclass
class MemoryRecord:

    session_id: str

    role: str

    message: str

    timestamp: str = datetime.now().isoformat()