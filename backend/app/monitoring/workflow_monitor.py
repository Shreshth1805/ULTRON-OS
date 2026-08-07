from app.communication import (
    agent_bus,
    Event
)


class WorkflowMonitor:

    def __init__(self):

        agent_bus.subscribe(
            "task_completed",
            self.completed
        )

        agent_bus.subscribe(
            "task_failed",
            self.failed
        )

    def completed(
        self,
        event: Event
    ):

        print(
            f"[SUCCESS] {event.sender} executed {event.action}"
        )

    def failed(
        self,
        event: Event
    ):

        print(
            f"[FAILED] {event.sender}: {event.payload}"
        )


workflow_monitor = WorkflowMonitor()