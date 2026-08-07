from dataclasses import dataclass
from datetime import datetime


@dataclass
class Skill:

    name: str

    description: str

    language: str

    code: str

    tags: list

    created_at: str = datetime.now().isoformat()