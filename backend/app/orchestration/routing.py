from typing import Dict


# =========================================================
# ULTRON REQUEST ROUTER
# =========================================================

ROUTES: Dict[str, str] = {
    "automl": "automl_agent",
    "machine learning": "automl_agent",
    "dataset": "automl_agent",
    "train model": "automl_agent",
    "model": "automl_agent",

    "code": "software_engineer_agent",
    "programming": "software_engineer_agent",
    "python": "software_engineer_agent",
    "debug": "software_engineer_agent",
    "bug": "software_engineer_agent",

    "research": "researcher_agent",
    "search": "researcher_agent",

    "chat": "chat_agent",
}


def detect_agent(message: str) -> str:
    """
    Detect which ULTRON agent should handle a request.
    """

    if not message:
        return "chat_agent"

    text = message.lower().strip()

    # Check more specific phrases first
    for keyword, agent_name in ROUTES.items():

        if keyword in text:
            return agent_name

    # Default agent
    return "chat_agent"