from app.tools.registry import get_agent

from app.execution.task_executor import (
    task_executor
)

from app.orchestration.report import (
    ExecutionReport
)

from app.orchestration.task import Task


class Orchestrator:

    def execute(
        self,
        prompt: str
    ):

        report = ExecutionReport()

        # =====================================================
        # STEP 1 : CREATE PLAN
        # =====================================================

        planner = get_agent(
            "planner_agent"
        )

        plan = {}

        if planner:

            try:

                plan = planner.create_plan(
                    prompt
                )

                report.add(

                    name="Planning",

                    success=True,

                    output=plan

                )

            except Exception as e:

                report.add(

                    name="Planning",

                    success=False,

                    output=str(e)

                )

        # =====================================================
        # STEP 2 : BUILD PROJECT
        # =====================================================

        build_task = Task(

            name="Project Builder",

            success=False,

            output=None

        )

        build_task.agent = "project_builder"

        build_task.description = prompt

        try:

            result = task_executor.execute(
                build_task
            )

            report.add(

                name="Project Builder",

                success=result.success,

                output=result.output

            )

        except Exception as e:

            report.add(

                name="Project Builder",

                success=False,

                output=str(e)

            )

        # =====================================================
        # RETURN REPORT
        # =====================================================

        return report.summary()


orchestrator = Orchestrator()