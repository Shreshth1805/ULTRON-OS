from app.execution.scheduler import scheduler

from app.tools.registry import get_agent


class ExecutionEngine:

    def run(self):

        results = []

        while True:

            task = scheduler.next_task()

            if task is None:

                break

            agent = get_agent(
                task.agent
            )

            if agent is None:

                task.status = "failed"

                task.result = {

                    "error": "Agent not found."

                }

                results.append(task)

                continue

            try:

                if hasattr(agent, task.action):

                    fn = getattr(
                        agent,
                        task.action
                    )

                    task.result = fn(
                        **task.payload
                    )

                else:

                    task.result = agent.run(
                        **task.payload
                    )

                task.status = "completed"

            except Exception as e:

                task.status = "failed"

                task.result = {

                    "error": str(e)

                }

            results.append(task)

        return results


execution_engine = ExecutionEngine()