from app.tools.registry import get_agent


class Dispatcher:

    def dispatch(self, task):

        agent = get_agent(task.agent)

        if agent is None:

            raise Exception(
                f"Unknown agent: {task.agent}"
            )

        return agent


dispatcher = Dispatcher()