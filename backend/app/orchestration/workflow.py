# app/orchestration/workflow.py

from app.orchestration.brain import process_request


class ULTRONWorkflow:

    def run(
        self,
        message: str
    ):

        return process_request(
            message
        )


workflow = ULTRONWorkflow()