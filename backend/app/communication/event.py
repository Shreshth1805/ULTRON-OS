from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict


@dataclass
class Event:

    sender: str

    receiver: str

    action: str

    payload: Dict = field(default_factory=dict)

    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )