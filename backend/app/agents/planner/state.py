from typing import TypedDict


class PlannerState(TypedDict):

    task: str

    plan: list[str]

    routed_tasks: list[dict]

    selected_agents: list[str]

    agent_results: list[dict]

    result: str

    completed: bool