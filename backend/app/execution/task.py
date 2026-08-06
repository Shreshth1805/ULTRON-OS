from dataclasses import dataclass, field
from typing import Dict, Any
import uuid


@dataclass
class Task:

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    agent: str = ""

    action: str = ""

    payload: Dict[str, Any] = field(
        default_factory=dict
    )

    status: str = "pending"

    result: Any = None