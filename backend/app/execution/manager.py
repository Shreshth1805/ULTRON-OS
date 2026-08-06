from app.execution.state import (

    ExecutionState,

    ExecutionStep

)

from app.execution.retry import (

    retry_manager

)

from app.tools.registry import (

    get_agent

)


class ExecutionManager:

    def execute(

        self,

        plan

    ):

        state = ExecutionState()

        for task in plan.steps:

            agent = get_agent(

                task.agent

            )

            if agent is None:

                state.success = False

                state.steps.append(

                    ExecutionStep(

                        step=task.id,

                        agent=task.agent,

                        task=task.task,

                        success=False,

                        output="Agent not found"

                    )

                )

                continue

            try:

                result = retry_manager.run(

                    lambda: agent.run(

                        task.task

                    )

                )

                state.steps.append(

                    ExecutionStep(

                        step=task.id,

                        agent=task.agent,

                        task=task.task,

                        success=True,

                        output=str(result)

                    )

                )

            except Exception as e:

                state.success = False

                state.steps.append(

                    ExecutionStep(

                        step=task.id,

                        agent=task.agent,

                        task=task.task,

                        success=False,

                        output=str(e)

                    )

                )

        return state


execution_manager = ExecutionManager()