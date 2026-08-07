from app.tools.registry import get_agent


class WorkflowExecutor:

    def run_node(self, node):

        agent = get_agent(node.agent)

        if agent is None:

            node.result = {

                "success": False,

                "error": "Agent not found"

            }

            node.completed = True

            return

        try:

            fn = getattr(agent, node.action)

            node.result = fn(**node.payload)

        except Exception as e:

            node.result = {

                "success": False,

                "error": str(e)

            }

        node.completed = True


workflow_executor = WorkflowExecutor()