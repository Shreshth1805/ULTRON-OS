from app.orchestration.router import detect_intent
from app.orchestration.llm_router import general_chat
from app.orchestration.orchestrator import orchestrator

from app.tools.registry import get_agent

from app.memory.memory import memory

from app.memory.service import (
    save_message,
    get_history
)

from app.memory_v2 import (
    memory_manager
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
    Load History
        ↓
    Detect Intent
        ↓
    Route Request
        ↓
    Execute Agent / Chat
        ↓
    Save SQL Memory
        ↓
    Save Vector Memory
        ↓
    Return Response
    """

    # =====================================================
    # LOAD CHAT HISTORY
    # =====================================================

    history = get_history(
        session_id=session_id,
        limit=20
    )

    # =====================================================
    # DETECT INTENT
    # =====================================================

    intent = detect_intent(message)

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
    # EXTRACT RESPONSE
    # =====================================================

    if isinstance(result, dict):

        response_text = result.get(
            "response",
            str(result)
        )

    else:

        response_text = str(result)

    # =====================================================
    # SAVE SQL HISTORY
    # =====================================================

    save_message(
        session_id=session_id,
        role="user",
        message=message
    )

    save_message(
        session_id=session_id,
        role="assistant",
        message=response_text
    )

    # =====================================================
    # SAVE VECTOR MEMORY
    # =====================================================

    try:

        memory_manager.remember(
            session_id=session_id,
            role="user",
            message=message
        )

        memory_manager.remember(
            session_id=session_id,
            role="assistant",
            message=response_text
        )

    except Exception as e:

        print(f"Vector memory error: {e}")

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