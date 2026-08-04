from app.orchestration.task import Task


class TaskPlanner:

    def create_plan(
        self,
        user_request: str
    ):

        request = user_request.lower()

        tasks = []

        # --------------------------------------
        # Software Projects
        # --------------------------------------

        if any(word in request for word in [
            "website",
            "web app",
            "fastapi",
            "streamlit",
            "project",
            "api",
            "python",
            "django",
            "flask"
        ]):

            tasks.append(

                Task(
                    name="Generate Project",
                    agent="software_engineer_agent",
                    description=user_request
                )

            )

        # --------------------------------------
        # AutoML
        # --------------------------------------

        elif any(word in request for word in [
            "dataset",
            "csv",
            "classification",
            "regression",
            "automl",
            "model",
            "machine learning"
        ]):

            tasks.append(

                Task(
                    name="Train Model",
                    agent="automl_agent",
                    description=user_request
                )

            )

        # --------------------------------------
        # General Chat
        # --------------------------------------

        else:

            tasks.append(

                Task(
                    name="General Chat",
                    agent="general_chat",
                    description=user_request
                )

            )

        return tasks


planner = TaskPlanner()