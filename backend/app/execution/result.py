from dataclasses import dataclass
from typing import Any


@dataclass
class TaskResult:

    success: bool

    agent: str

    task: str

    output: Any