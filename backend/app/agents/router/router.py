from app.ai.llm import llm_manager

from app.prompts.router import router_prompt


llm = llm_manager.get_llm()

router_chain = router_prompt | llm


ALLOWED_AGENTS = {
    "software_engineer",
    "research",
    "automl",
    "general"
}


def router_node(state):

    routed_tasks = []

    selected_agents = []

    for task in state["plan"]:

        response = router_chain.invoke(
            {
                "task": task
            }
        )

        agent = response.content.strip().lower()

        # Clean accidental formatting
        agent = agent.replace(
            "`",
            ""
        ).strip()

        if agent not in ALLOWED_AGENTS:

            agent = "general"

        routed_tasks.append(
            {
                "agent": agent,
                "task": task
            }
        )

        if agent not in selected_agents:

            selected_agents.append(
                agent
            )

    return {
        **state,

        "routed_tasks":
            routed_tasks,

        "selected_agents":
            selected_agents
    }