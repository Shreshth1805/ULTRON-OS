from app.orchestration.router import detect_intent
from app.orchestration.llm_router import general_chat

from app.agents.planner.planner import planner
from app.execution.executor import executor

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
    Load History
      ↓
    Detect Intent
      ↓
    Planner
      ↓
    Execution Engine
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
    # DETECT USER INTENT
    # =====================================================

    intent = detect_intent(
        message
    )

    # =====================================================
    # SOFTWARE / PROJECT / CODING
    # =====================================================

    if intent in [

        "software_engineer",

        "project",

        "coding"

    ]:

        try:

            plan = planner.create_plan(
                message
            )

            result = executor.execute(
                plan
            )

        except Exception as e:

            result = {

                "success": False,

                "response": str(e)

            }

    # =====================================================
    # AUTOML
    # =====================================================

    elif intent == "automl":

        automl = get_agent(
            "automl_agent"
        )

        if automl:

            try:

                result = automl.run(
                    message
                )

            except Exception as e:

                result = {

                    "success": False,

                    "response": str(e)

                }

        else:

            result = {

                "success": False,

                "response": "AutoML agent not registered."

            }

    # =====================================================
    # GENERAL CHAT
    # =====================================================

    else:

        try:

            result = general_chat(

                message=message,

                history=history

            )

        except Exception as e:

            result = {

                "success": False,

                "response": str(e)

            }

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
    # STORE IN LIVE MEMORY
    # =====================================================

    memory.remember(

        message,

        response_text

    )

    # =====================================================
    # RETURN
    # =====================================================

    return result