from app.workflow.node import WorkflowNode
from app.workflow.graph import WorkflowGraph


class WorkflowPlanner:

    def create(self, prompt):

        graph = WorkflowGraph()

        graph.add(

            WorkflowNode(

                id="generate",

                agent="software_engineer_agent",

                action="run",

                payload={

                    "prompt": prompt

                }

            )

        )

        graph.add(

            WorkflowNode(

                id="review",

                agent="reviewer_agent",

                action="review_project",

                depends_on=["generate"]

            )

        )

        graph.add(

            WorkflowNode(

                id="security",

                agent="security_agent",

                action="review",

                depends_on=["generate"]

            )

        )

        graph.add(

            WorkflowNode(

                id="performance",

                agent="performance_agent",

                action="analyze",

                depends_on=["generate"]

            )

        )

        graph.add(

            WorkflowNode(

                id="testing",

                agent="tester_agent",

                action="test_project",

                depends_on=["generate"]

            )

        )

        graph.add(

            WorkflowNode(

                id="reflection",

                agent="reflection_agent",

                action="reflect",

                depends_on=[

                    "review",

                    "security",

                    "performance",

                    "testing"

                ]

            )

        )

        return graph


workflow_planner = WorkflowPlanner()