from app.agents.planner.planner import planner


class PlannerAgent:

    def run(self, request):

        plan = planner.create_plan(
            request
        )

        return {

            "success": True,

            "plan": plan.model_dump()

        }


planner_agent = PlannerAgent()