from app.orchestration.router import detect_intent
from app.orchestration.llm_router import general_chat

from app.orchestration.planner import planner
from app.orchestration.executor import executor

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

    Flow:
    1. Load conversation history
    2. Detect intent (optional)
    3. Create execution plan
    4. Execute first task
    5. Save conversation
    6. Return response
    """

    # =====================================================
    # LOAD CHAT HISTORY
    # =====================================================

    history = get_history(
        session_id=session_id,
        limit=20
    )

    live_history = memory.history()

    # =====================================================
    # DETECT INTENT
    # =====================================================

    intent = detect_intent(message)

    # =====================================================
    # CREATE EXECUTION PLAN
    # =====================================================

    tasks = planner.create_plan(message)

    if not tasks:

        result = {
            "success": False,
            "response": "Unable to create execution plan."
        }

    else:

        task = tasks[0]

        # -----------------------------------------
        # GENERAL CHAT
        # -----------------------------------------

        if task.agent == "general_chat":

            result = general_chat(
                message=message,
                history=history
            )

        # -----------------------------------------
        # EXECUTE AGENT
        # -----------------------------------------

        else:

            result = executor.execute(task)

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
    # STORE LIVE MEMORY
    # =====================================================

    memory.remember(
        message,
        response_text
    )

    # =====================================================
    # RETURN RESPONSE
    # =====================================================

    return result