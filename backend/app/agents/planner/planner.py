from app.core.llm import llm


SYSTEM_PROMPT = """
You are the central planner of an AI operating system
called ULTRON.

Your job is to analyze the user's request and select
the most appropriate specialized agent.

Available agents:

software_engineer
automl
research
general

Use:

software_engineer
for:
- programming
- coding
- debugging
- software development
- APIs
- backend development
- frontend development
- architecture
- Git
- databases

automl
for:
- datasets
- machine learning
- training models
- preprocessing
- feature engineering
- model selection
- model evaluation
- predictions

research
for:
- research
- explanations
- information gathering
- technical investigation

general
for:
- normal conversation
- greetings
- general questions

Return ONLY ONE of these values:

software_engineer
automl
research
general
"""


def planner_node(user_message: str) -> str:

    response = llm.invoke(
        [
            (
                "system",
                SYSTEM_PROMPT
            ),
            (
                "human",
                user_message
            )
        ]
    )

    result = response.content.strip().lower()

    valid_agents = {
        "software_engineer",
        "automl",
        "research",
        "general"
    }

    if result not in valid_agents:

        return "general"

    return result