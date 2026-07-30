from app.ai.llm import llm_manager


llm = llm_manager.get_llm()


def research_node(state):

    outputs = []

    for item in state["routed_tasks"]:

        if item["agent"] != "research":

            continue

        response = llm.invoke(
            f"""
You are ULTRON's Research Agent.

Research and analyse the following task:

{item["task"]}

Provide:

1. Key findings
2. Important concepts
3. Technical details
4. Useful conclusions
"""
        )

        outputs.append(
            response.content
        )

    result = "\n\n".join(outputs)

    return {
        **state,
        "result": result,
        "completed": True
    }