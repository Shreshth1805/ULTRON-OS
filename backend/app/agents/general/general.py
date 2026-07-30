from app.ai.llm import llm_manager


llm = llm_manager.get_llm()


def general_node(state):

    outputs = []

    for item in state["routed_tasks"]:

        if item["agent"] != "general":

            continue

        response = llm.invoke(
            item["task"]
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