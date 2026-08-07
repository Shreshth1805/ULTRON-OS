from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Message:

    sender: str

    receiver: str

    content: str

    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )