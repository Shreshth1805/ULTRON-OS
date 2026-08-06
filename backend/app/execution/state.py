from pydantic import BaseModel
from typing import List


class ExecutionStep(BaseModel):

    step: int

    agent: str

    task: str

    success: bool

    output: str


class ExecutionState(BaseModel):

    success: bool = True

    steps: List[ExecutionStep] = []