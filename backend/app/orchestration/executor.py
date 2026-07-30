from typing import Any

from app.tools.registry import get_agent


# =========================================================
# ULTRON EXECUTOR
# =========================================================

def execute_request(
    message: str,
    agent_name: str
) -> Any:

    agent = get_agent(agent_name)

    if agent is None:
        return {
            "success": False,
            "error": f"Agent '{agent_name}' not found."
        }

    # -----------------------------------------------------
    # AutoML Agent
    # -----------------------------------------------------

    if agent_name == "automl_agent":

        return {
            "success": True,
            "agent": agent_name,
            "message": (
                "AutoML agent is available. "
                "Provide a dataset filename and target column "
                "to start training."
            )
        }

    # -----------------------------------------------------
    # Software Engineer Agent
    # -----------------------------------------------------

    if agent_name == "software_engineer_agent":

        if hasattr(agent, "generate_code"):

            return agent.generate_code(
                code=message,
                filename="generated.py"
            )

    # -----------------------------------------------------
    # Generic Agent
    # -----------------------------------------------------

    if callable(agent):

        return agent(message)

    if hasattr(agent, "run"):

        return agent.run(message)

    if hasattr(agent, "process"):

        return agent.process(message)

    return {
        "success": False,
        "error": f"Agent '{agent_name}' has no executable interface."
    }