from app.automl.pipeline import run_automl


class AutoMLAgent:
    """
    ULTRON AutoML Agent.

    Responsible for receiving AutoML requests
    and forwarding them to the AutoML pipeline.
    """

    name = "automl_agent"

    def train(
        self,
        filename: str,
        target_column: str
    ):

        return run_automl(
            filename=filename,
            target_column=target_column
        )
    def run(
        self,
        message: str
    ):

        return {
            "success": True,
            "agent": "automl_agent",
            "message": message,
            "status": "AutoML request received",
            "next_step": (
                "Provide the dataset filename and target column "
                "to start training."
            )
        }

automl_agent = AutoMLAgent()