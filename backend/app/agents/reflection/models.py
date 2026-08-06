from pydantic import BaseModel


class ReflectionReport(BaseModel):

    success: bool

    summary: str

    improvements: list[str]

    risk_level: str