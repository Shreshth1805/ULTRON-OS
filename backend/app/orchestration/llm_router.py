from app.core.llm import llm


SYSTEM_PROMPT = """
You are ULTRON, an advanced AI software engineering assistant.

You can help with:

- Software development
- Python
- C++
- Java
- JavaScript
- FastAPI
- APIs
- Machine Learning
- AutoML
- Data Science
- Debugging
- System architecture
- DevOps

Use the conversation history when it is relevant.

Be precise and practical.

When generating code:
- Use proper formatting
- Write complete code
- Explain important decisions
- Avoid unnecessary complexity
"""


def general_chat(
    message: str,
    history=None
):

    if history is None:

        history = []

    history_text = ""

    for item in history:

        history_text += (
            f"{item['role']}: "
            f"{item['message']}\n"
        )

    prompt = f"""
{SYSTEM_PROMPT}

Previous conversation:

{history_text}

Current user request:

{message}

Answer the user based on the conversation context.
"""

    response = llm.invoke(
        prompt
    )

    return {
        "type": "general",
        "response": response.content
    }