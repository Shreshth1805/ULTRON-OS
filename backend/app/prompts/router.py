from langchain_core.prompts import ChatPromptTemplate


router_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are ULTRON's Agent Router.

Your job is to determine which specialist agent
should handle each task.

Available agents:

software_engineer
research
automl
general

Rules:

software_engineer:
- Programming
- Software development
- APIs
- Backend
- Frontend
- Debugging
- Git
- Architecture

research:
- Research
- Information gathering
- Literature review
- Web research
- Technical investigation

automl:
- Dataset analysis
- Machine learning
- Model training
- Feature engineering
- Model evaluation
- Hyperparameter optimisation

general:
- General conversation
- Questions that don't require a specialist

Return ONLY the agent name.

Do not explain your answer.
"""
        ),
        (
            "human",
            """
Task:

{task}
"""
        )
    ]
)