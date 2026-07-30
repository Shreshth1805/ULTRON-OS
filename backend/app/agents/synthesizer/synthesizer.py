from app.ai.llm import llm_manager


llm = llm_manager.get_llm()


def synthesizer_node(state):

    task = state["task"]

    results = state.get(
        "agent_results",
        []
    )

    if not results:

        return {
            **state,
            "result": "No agent produced a result.",
            "completed": True
        }

    formatted_results = []

    for item in results:

        formatted_results.append(
            f"""
AGENT: {item["agent"]}

TASK:
{item["task"]}

RESULT:
{item["result"]}
"""
        )

    combined_results = "\n\n".join(
        formatted_results
    )

    prompt = f"""
You are ULTRON's central intelligence.

The user requested:

{task}

Multiple specialist agents worked on this request.

Their results are:

{combined_results}

Your job is to synthesise these results into
one high-quality final response.

Requirements:

1. Do not blindly repeat the agents.
2. Remove contradictions where possible.
3. Preserve useful technical details.
4. Organise the answer clearly.
5. If code is required, provide complete code.
6. If multiple approaches exist, explain the trade-offs.
7. Do not mention internal agent routing.
"""

    response = llm.invoke(prompt)

    return {
        **state,
        "result": response.content,
        "completed": True
    }