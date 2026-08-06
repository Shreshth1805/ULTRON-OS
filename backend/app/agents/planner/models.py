from pydantic import BaseModel
from typing import List


class PlanStep(BaseModel):

    id: int

    agent: str

    task: str


class Plan(BaseModel):

    steps: List[PlanStep]