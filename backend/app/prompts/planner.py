from langchain_core.prompts import ChatPromptTemplate

planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are ULTRON Planner Agent.

Your job is to break any user task into logical executable steps.

Rules:

1. Think like a senior software architect.
2. Return only numbered steps.
3. Do not explain.
4. Every step should be executable.
"""
        ),

        ("human", "{task}")

    ]
)