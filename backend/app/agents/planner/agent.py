# =========================================================
# ULTRON PLANNER AGENT
# =========================================================

from app.agents.software_engineer.planner import planner


class PlannerAgent:
    """
    High-level planning agent.

    Converts a user's project request into a
    structured development plan.
    """

    # =====================================================
    # CREATE PLAN
    # =====================================================

    def create_plan(
        self,
        prompt: str
    ):
        """
        Create a software development plan.
        """

        if not prompt or not prompt.strip():

            return {
                "success": False,
                "error": "Project prompt cannot be empty."
            }

        try:

            plan = planner.create_plan(
                prompt
            )

            return {
                "success": True,
                "plan": plan
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }


# =========================================================
# SINGLETON
# =========================================================

planner_agent = PlannerAgent()