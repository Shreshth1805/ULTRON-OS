from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class WorkflowNode:

    id: str

    agent: str

    action: str

    payload: Dict[str, Any] = field(default_factory=dict)

    depends_on: List[str] = field(default_factory=list)

    completed: bool = False

    result = None