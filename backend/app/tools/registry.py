# =========================================================
# TOOL IMPORTS
# =========================================================

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

    allowed = {

        "write_file",

        "read_file",

        "validate_python_code"

    }

    return {

        name: tool

        for name, tool in _TOOLS.items()

        if name in allowed

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

    # =====================================================
    # SOFTWARE ENGINEER
    # =====================================================

    if name == "software_engineer_agent":

        from app.agents.software_engineer.engineer import (
            software_engineer_agent
        )

        register_agent(
            name,
            software_engineer_agent
        )

    # =====================================================
    # AUTOML
    # =====================================================

    elif name == "automl_agent":

        from app.agents.automl_agent.agent import (
            automl_agent
        )

        register_agent(
            name,
            automl_agent
        )

    # =====================================================
    # REVIEWER
    # =====================================================

    elif name == "reviewer_agent":

        from app.agents.reviewer.reviewer import (
            reviewer_agent
        )

        register_agent(
            name,
            reviewer_agent
        )

    # =====================================================
    # TESTER
    # =====================================================

    elif name == "tester_agent":

        from app.agents.tester.agent import (
            tester_agent
        )

        register_agent(
            name,
            tester_agent
        )

    # =====================================================
    # PLANNER
    # =====================================================

    elif name == "planner_agent":

        from app.agents.planner.agent import (
            planner_agent
        )

        register_agent(
            name,
            planner_agent
        )

    # =====================================================
    # PROJECT BUILDER
    # =====================================================

    elif name == "project_builder":

        from app.orchestration.project_builder import (
            project_builder
        )

        register_agent(
            name,
            project_builder
        )

    # =====================================================
    # DEVOPS (Future)
    # =====================================================

    elif name == "devops_agent":

        try:

            from app.agents.devops.agent import (
                devops_agent
            )

            register_agent(
                name,
                devops_agent
            )

        except ImportError:

            return None

    return _AGENTS.get(name)


def list_agents():

    return list(_AGENTS.keys())