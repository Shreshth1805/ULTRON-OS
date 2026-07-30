from app.tools.code_tools import CODE_TOOLS
from app.tools.dataset_tools import DATASET_TOOLS


# =========================================================
# TOOL REGISTRY
# =========================================================

_TOOLS = {}

_TOOLS.update(CODE_TOOLS)
_TOOLS.update(DATASET_TOOLS)


def register_tool(name, tool):

    _TOOLS[name] = tool

    return tool


def get_tool(name):

    return _TOOLS.get(name)


def list_tools():

    return list(_TOOLS.keys())


def get_code_tools():

    return {
        name: tool
        for name, tool in _TOOLS.items()
        if name in [
            "write_file",
            "read_file",
            "validate_python_code"
        ]
    }


# =========================================================
# AGENT REGISTRY
# =========================================================

_AGENTS = {}


def register_agent(name, agent):

    _AGENTS[name] = agent

    return agent


def get_agent(name):

    if name in _AGENTS:
        return _AGENTS[name]

    if name == "automl_agent":

        from app.agents.automl_agent.agent import automl_agent

        _AGENTS[name] = automl_agent

    elif name == "software_engineer_agent":

        from app.agents.software_engineer.engineer import (
            software_engineer_agent
        )

        _AGENTS[name] = software_engineer_agent

    return _AGENTS.get(name)


def list_agents():

    return list(_AGENTS.keys())