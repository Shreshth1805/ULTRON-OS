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

            # =================================================
            # 1. PLANNER
            # =================================================

            WorkflowTask(

                name="planner",

                agent="planner_agent",

                action="create_plan",

                kwargs={
                    "prompt": prompt
                }

            ),

            # =================================================
            # 2. BUILDER
            # =================================================

            WorkflowTask(

                name="builder",

                agent="software_engineer_agent",

                action="build",

                kwargs={

                    "prompt": prompt,

                    "plan": "$planner",

                },

                depends_on=[
                    "planner"
                ]

            ),

            # =================================================
            # 3. REVIEWER
            # =================================================

            WorkflowTask(

                name="reviewer",

                agent="reviewer_agent",

                action="review_project",

                kwargs={

                    "project_path": "$builder.project_path"

                },

                depends_on=[
                    "builder"
                ]

            ),

            # =================================================
            # 4. SECURITY
            # =================================================

            WorkflowTask(

                name="security",

                agent="security_agent",

                action="review_project",

                kwargs={

                    "project_path": "$builder.project_path"

                },

                depends_on=[
                    "builder"
                ]

            ),

            # =================================================
            # 5. TESTER
            # =================================================

            WorkflowTask(

                name="tester",

                agent="tester_agent",

                action="test_project",

                kwargs={

                    "project_path": "$builder.project_path"

                },

                depends_on=[
                    "reviewer",
                    "security"
                ]

            ),

            # =================================================
            # 6. FIXER
            # =================================================

            WorkflowTask(

                name="fixer",

                agent="fixer_agent",

                action="fix_project",

                kwargs={

                    "project_path": "$builder.project_path"

                },

                depends_on=[
                    "tester"
                ]

            ),

            # =================================================
            # 7. REFLECTION
            # =================================================

            WorkflowTask(

                name="reflection",

                agent="reflection_agent",

                action="reflect",

                kwargs={

                    "project_path": "$builder.project_path"

                },

                depends_on=[
                    "fixer"
                ]

            )

        ]

        return workflow_engine.execute(
            tasks
        )


orchestrator = Orchestrator()