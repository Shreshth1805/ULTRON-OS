from app.execution.dispatcher import dispatcher
from app.execution.result import TaskResult


class TaskExecutor:

    def execute(self, task):

        agent = dispatcher.dispatch(task)

        # ================================
        # Software Engineer
        # ================================

        if task.agent == "software_engineer_agent":

            output = agent.run(
                task.description
            )

        # ================================
        # AutoML
        # ================================

        elif task.agent == "automl_agent":

            output = agent.run(
                task.description
            )

        # ================================
        # Project Builder
        # ================================

        elif task.agent == "project_builder":

            output = agent.build(
                task.description
            )

        # ================================
        # Reviewer
        # ================================

        elif task.agent == "reviewer_agent":

            output = agent.review_project(
                task.description
            )

        # ================================
        # Tester
        # ================================

        elif task.agent == "tester_agent":

            output = agent.test_project(
                task.description
            )

        else:

            raise Exception(
                f"Unsupported agent: {task.agent}"
            )

        return TaskResult(

            success=True,

            agent=task.agent,

            task=task.description,

            output=output

        )


task_executor = TaskExecutor()