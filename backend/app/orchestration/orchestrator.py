# =========================================================
# ULTRON ORCHESTRATOR
# =========================================================

import os

from app.orchestration.workflow_engine import (
    workflow_engine,
    WorkflowTask
)


class Orchestrator:
    """
    Main ULTRON workflow coordinator.

    Flow:

        User Request
             ↓
          Planner
             ↓
        Engineer
             ↓
          Reviewer
             ↓
         Security
             ↓
          Tester
             ↓
           Fixer
             ↓
        Reflection
             ↓
          GitHub
    """

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(
        self,
        prompt: str
    ):

        tasks = []

        # =================================================
        # 1. PLANNER
        # =================================================

        tasks.append(

            WorkflowTask(

                name="planner",

                agent="planner_agent",

                action="create_plan",

                kwargs={
                    "prompt": prompt
                }

            )

        )

        # =================================================
        # 2. SOFTWARE ENGINEER
        # =================================================

        tasks.append(

            WorkflowTask(

                name="builder",

                agent="software_engineer_agent",

                action="build",

                # IMPORTANT:
                # Do NOT pass plan= here.
                #
                # Your current SoftwareEngineerAgent.build()
                # does not accept a "plan" keyword argument.
                #
                # The engineer can retrieve the planner result
                # from workflow context if required.

                kwargs={
                    "prompt": prompt
                },

                depends_on=[
                    "planner"
                ]

            )

        )

        # =================================================
        # 3. REVIEWER
        # =================================================

        tasks.append(

            WorkflowTask(

                name="reviewer",

                agent="reviewer_agent",

                action="review_project",

                kwargs={

                    "project_path": "$project_path"

                },

                depends_on=[
                    "builder"
                ]

            )

        )

        # =================================================
        # 4. SECURITY
        # =================================================

        # Security is optional for now.
        #
        # Your current security agent has:
        #
        #     No module named 'app.base_agent'
        #
        # Therefore we only add it when explicitly enabled.

        security_enabled = os.getenv(
            "ULTRON_ENABLE_SECURITY",
            "false"
        ).lower() in {
            "1",
            "true",
            "yes",
            "on"
        }

        if security_enabled:

            tasks.append(

                WorkflowTask(

                    name="security",

                    agent="security_agent",

                    action="review_project",

                    kwargs={
                        "project_path": "$project_path"
                    },

                    depends_on=[
                        "builder"
                    ]

                )

            )

        # =================================================
        # 5. TESTER
        # =================================================

        tester_dependencies = [
            "reviewer"
        ]

        if security_enabled:
            tester_dependencies.append(
                "security"
            )

        tasks.append(

            WorkflowTask(

                name="tester",

                agent="tester_agent",

                action="test_project",

                kwargs={
                    "project_path": "$project_path"
                },

                depends_on=tester_dependencies

            )

        )

        # =================================================
        # 6. FIXER
        # =================================================

        tasks.append(

            WorkflowTask(

                name="fixer",

                agent="fixer_agent",

                # Your current FixerAgent does not expose
                # fix_project().
                #
                # Use "fix" if available.
                action="fix",

                kwargs={
                    "project_path": "$project_path"
                },

                depends_on=[
                    "tester"
                ]

            )

        )

        # =================================================
        # 7. REFLECTION
        # =================================================

        tasks.append(

            WorkflowTask(

                name="reflection",

                agent="reflection_agent",

                action="reflect",

                # Do not pass project_path here.
                # Your current reflect() does not accept it.
                kwargs={},

                depends_on=[
                    "fixer"
                ]

            )

        )

        # =================================================
        # 8. GITHUB
        # =================================================

        # NEVER load GitHub unless a token exists.
        #
        # Otherwise importing github_client raises:
        #
        # ValueError:
        # GITHUB_TOKEN not found.

        github_enabled = bool(
            os.getenv("GITHUB_TOKEN")
        )

        if github_enabled:

            tasks.append(

                WorkflowTask(

                    name="github",

                    agent="github_agent",

                    action="publish",

                    kwargs={

                        "project_name": "$project_name",

                        "project_path": "$project_path"

                    },

                    depends_on=[
                        "reflection"
                    ]

                )

            )

        # =================================================
        # EXECUTE WORKFLOW
        # =================================================

        result = workflow_engine.execute(
            tasks
        )

        return result


# =========================================================
# GLOBAL ORCHESTRATOR
# =========================================================

orchestrator = Orchestrator()