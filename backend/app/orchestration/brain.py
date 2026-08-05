from app.orchestration.router import detect_intent
from app.orchestration.llm_router import general_chat
from app.orchestration.orchestrator import orchestrator

from app.tools.registry import get_agent

from app.memory.memory import memory
from app.memory.service import (
    save_message,
    get_history
)


def process_request(
    message: str,
    session_id: str = "default"
):
    """
    ULTRON Brain

    Flow

    User
      ↓
    Detect Intent
      ↓
    Route Request
      ↓
    Orchestrator / AutoML / Chat
      ↓
    Save Memory
      ↓
    Return Response
    """

    # =====================================================
    # LOAD HISTORY
    # =====================================================

    history = get_history(
        session_id=session_id,
        limit=20
    )

    # =====================================================
    # DETECT INTENT
    # =====================================================

    intent = detect_intent(
        message
    )

    # =====================================================
    # SOFTWARE / PROJECT REQUESTS
    # =====================================================

    if intent in [

        "software_engineer",

        "project",

        "coding"

    ]:

        result = orchestrator.execute(
            message
        )

    # =====================================================
    # AUTOML
    # =====================================================

    elif intent == "automl":

        automl = get_agent(
            "automl_agent"
        )

        if automl:

            result = automl.run(
                message
            )

        else:

            result = {

                "success": False,

                "response": "AutoML Agent not available."

            }

    # =====================================================
    # GENERAL CHAT
    # =====================================================

    else:

        result = general_chat(

            message=message,

            history=history

        )

    # =====================================================
    # RESPONSE TEXT
    # =====================================================

    if isinstance(result, dict):

        response_text = result.get(

            "response",

            str(result)

        )

    else:

        response_text = str(result)

    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    save_message(

        session_id=session_id,

        role="user",

        message=message

    )

    # =====================================================
    # SAVE ASSISTANT MESSAGE
    # =====================================================

    save_message(

        session_id=session_id,

        role="assistant",

        message=response_text

    )

    # =====================================================
    # LIVE MEMORY
    # =====================================================

    memory.remember(

        message,

        response_text

    )

    # =====================================================
    # RETURN
    # =====================================================

    return result