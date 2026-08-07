from dataclasses import dataclass
from datetime import datetime


@dataclass
class Version:

    project: str

    version: str

    message: str

    timestamp: str = datetime.now().isoformat()