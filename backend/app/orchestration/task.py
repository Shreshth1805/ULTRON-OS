from dataclasses import dataclass
from typing import Any


@dataclass
class Task:

    name: str

    agent: str = ""

    description: str = ""

    success: bool = False

    output: Any = None