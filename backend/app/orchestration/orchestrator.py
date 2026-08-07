from app.orchestration.workflow_engine import (
    workflow_engine,
    WorkflowTask
)


class Orchestrator:

    def execute(
        self,
        prompt: str
    ):

        tasks = [

            # ===========================================
            # Planner
            # ===========================================

            WorkflowTask(

                name="planner",

                agent="planner_agent",

                action="create_plan",

                kwargs={

                    "prompt": prompt

                }

            ),

            # ===========================================
            # Project Builder
            # ===========================================

            WorkflowTask(

                name="builder",

                agent="project_builder",

                action="build",

                kwargs={

                    "prompt": prompt

                },

                depends_on=["planner"]

            ),

            # ===========================================
            # Reviewer
            # ===========================================

            WorkflowTask(

                name="reviewer",

                agent="reviewer_agent",

                action="review_project",

                kwargs={

                    "project_path": ""

                },

                depends_on=["builder"]

            ),

            # ===========================================
            # Security
            # ===========================================

            WorkflowTask(

                name="security",

                agent="security_agent",

                action="review_project",

                kwargs={

                    "project_path": ""

                },

                depends_on=["builder"]

            ),

            # ===========================================
            # Tester
            # ===========================================

            WorkflowTask(

                name="tester",

                agent="tester_agent",

                action="test_project",

                kwargs={

                    "project_path": ""

                },

                depends_on=[

                    "reviewer",
                    "security"

                ]

            ),

            # ===========================================
            # Auto Fix
            # ===========================================

            WorkflowTask(

                name="fixer",

                agent="fixer_agent",

                action="fix_project",

                kwargs={

                    "project_path": ""

                },

                depends_on=["tester"]

            ),

            # ===========================================
            # Reflection
            # ===========================================

            WorkflowTask(

                name="reflection",

                agent="reflection_agent",

                action="reflect",

                kwargs={},

                depends_on=["fixer"]

            ),

            # ===========================================
            # GitHub Publish
            # ===========================================

            WorkflowTask(

                name="github",

                agent="github_agent",

                action="publish",

                kwargs={

                    "project_name": "",

                    "project_path": ""

                },

                depends_on=["reflection"]

            )

        ]

        return workflow_engine.execute(tasks)


orchestrator = Orchestrator()