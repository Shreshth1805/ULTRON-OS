from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class MemoryItem:

    id: str

    category: str

    content: str

    metadata: Dict

    timestamp: str = datetime.utcnow().isoformat()