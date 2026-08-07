from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any
import uuid


@dataclass
class Event:

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    type: str = ""

    source: str = ""

    payload: Dict[str, Any] = field(
        default_factory=dict
    )

    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )