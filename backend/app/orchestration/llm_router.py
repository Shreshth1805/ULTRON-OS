from app.llm import model_router


SYSTEM_PROMPT = """
You are ULTRON, an advanced AI software engineering assistant.

You can help with:

- Software Development
- Python
- C++
- Java
- JavaScript
- TypeScript
- FastAPI
- APIs
- Machine Learning
- Deep Learning
- AutoML
- Data Science
- DevOps
- Cloud Computing
- Docker
- Kubernetes
- Software Architecture
- Debugging
- Code Review
- Performance Optimization
- Security Analysis

Guidelines:

- Be practical.
- Give production-quality code.
- Explain important decisions.
- Follow best practices.
- Keep responses concise unless detailed explanation is requested.
- Use previous conversation whenever it helps.
"""


def build_prompt(
    message: str,
    history=None
) -> str:
    """
    Build the complete prompt including conversation history.
    """

    if history is None:
        history = []

    history_text = ""

    for item in history:

        role = item.get(
            "role",
            "user"
        )

        content = item.get(
            "message",
            ""
        )

        history_text += f"{role}: {content}\n"

    prompt = f"""
{SYSTEM_PROMPT}

Conversation History:

{history_text}

Current User Request:

{message}

Answer the user professionally.
"""

    return prompt


def general_chat(
    message: str,
    history=None
):
    """
    Route the request to the most suitable LLM.
    """

    prompt = build_prompt(
        message,
        history
    )

    try:

        # Automatically choose the best model
        model = model_router.route(
            message
        )

        if model is None:

            return {
                "success": False,
                "type": "general",
                "response": "No language model is available."
            }

        response = model.invoke(
            prompt
        )

        text = getattr(
            response,
            "content",
            str(response)
        )

        return {

            "success": True,

            "type": "general",

            "model": model.__class__.__name__,

            "response": text

        }

    except Exception as e:

        return {

            "success": False,

            "type": "general",

            "response": str(e)

        }