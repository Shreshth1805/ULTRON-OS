from app.orchestration.router import detect_intent
from app.orchestration.llm_router import general_chat

from app.tools.registry import get_agent

from app.memory.service import (
    save_message,
    get_history
)


def process_request(
    message: str,
    session_id: str = "default"
):

    # Get previous conversation first
    history = get_history(
        session_id=session_id,
        limit=20
    )

    # Detect request type
    intent = detect_intent(
        message
    )

    # =====================================================
    # SOFTWARE ENGINEER
    # =====================================================

    if intent == "software_engineer":

        agent = get_agent(
            "software_engineer_agent"
        )

        if agent is None:

            result = {
                "success": False,
                "error": "Software Engineer agent unavailable."
            }

        else:

            result = agent.run(
                message
            )

    # =====================================================
    # AUTOML
    # =====================================================

    elif intent == "automl":

        agent = get_agent(
            "automl_agent"
        )

        if agent is None:

            result = {
                "success": False,
                "error": "AutoML agent unavailable."
            }

        else:

            result = agent.run(
                message
            )

    # =====================================================
    # GENERAL GROQ
    # =====================================================

    else:

        result = general_chat(
            message=message,
            history=history
        )

    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    save_message(
        session_id=session_id,
        role="user",
        message=message
    )

    # =====================================================
    # SAVE ASSISTANT RESPONSE
    # =====================================================

    if isinstance(result, dict):

        response_text = result.get(
            "response",
            str(result)
        )

    else:

        response_text = str(result)

    save_message(
        session_id=session_id,
        role="assistant",
        message=response_text
    )

    return result