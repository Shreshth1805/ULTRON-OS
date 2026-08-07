from app.workflow.graph import WorkflowGraph

from app.workflow.executor import workflow_executor


class WorkflowEngine:

    def execute(self, graph: WorkflowGraph):

        while True:

            ready = graph.ready_nodes()

            if not ready:

                break

            for node in ready:

                workflow_executor.run_node(node)

        return graph


workflow_engine = WorkflowEngine()