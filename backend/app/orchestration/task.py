from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:

    name: str

    agent: str

    description: str

    status: str = "pending"

    result: Optional[dict] = None