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
    """
    Register a new tool.
    """

    _TOOLS[name] = tool

    return tool


def get_tool(name):
    """
    Get a registered tool.
    """

    return _TOOLS.get(name)


def list_tools():
    """
    Return all registered tools.
    """

    return sorted(
        _TOOLS.keys()
    )


def get_code_tools():
    """
    Return only coding-related tools.
    """

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
    """
    Register an agent.
    """

    _AGENTS[name] = agent

    return agent


def get_agent(name):
    """
    Lazy-load an agent when requested.
    """

    if name in _AGENTS:

        return _AGENTS[name]

    try:

        # =================================================
        # SOFTWARE ENGINEER
        # =================================================

        if name == "software_engineer_agent":

            from app.agents.software_engineer.engineer import (
                software_engineer_agent
            )

            register_agent(
                name,
                software_engineer_agent
            )

        # =================================================
        # AUTOML
        # =================================================

        elif name == "automl_agent":

            from app.agents.automl_agent.agent import (
                automl_agent
            )

            register_agent(
                name,
                automl_agent
            )

        # =================================================
        # REVIEWER
        # =================================================

        elif name == "reviewer_agent":

            from app.agents.reviewer.agent import (
                reviewer_agent
            )

            register_agent(
                name,
                reviewer_agent
            )

        # =================================================
        # TESTER
        # =================================================

        elif name == "tester_agent":

            from app.agents.tester.agent import (
                tester_agent
            )

            register_agent(
                name,
                tester_agent
            )

        # =================================================
        # PLANNER
        # =================================================

        elif name == "planner_agent":

            from app.agents.planner.agent import (
                planner_agent
            )

            register_agent(
                name,
                planner_agent
            )

        # =================================================
        # FIXER
        # =================================================

        elif name == "fixer_agent":

            from app.agents.fixer.agent import (
                fixer_agent
            )

            register_agent(
                name,
                fixer_agent
            )

        # =================================================
        # VERSION
        # =================================================

        elif name == "version_agent":

            from app.agents.version.agent import (
                version_agent
            )

            register_agent(
                name,
                version_agent
            )

        # =================================================
        # SKILL
        # =================================================

        elif name == "skill_agent":

            from app.agents.skill.agent import (
                skill_agent
            )

            register_agent(
                name,
                skill_agent
            )

        # =================================================
        # LEARNER
        # =================================================

        elif name == "learner_agent":

            from app.agents.learner.agent import (
                learner_agent
            )

            register_agent(
                name,
                learner_agent
            )

        # =================================================
        # PERFORMANCE
        # =================================================

        elif name == "performance_agent":

            from app.agents.performance.agent import (
                performance_agent
            )

            register_agent(
                name,
                performance_agent
            )

        # =================================================
        # SECURITY
        # =================================================

        elif name == "security_agent":

            from app.agents.security.agent import (
                security_agent
            )

            register_agent(
                name,
                security_agent
            )

        # =================================================
        # DOCKER
        # =================================================

        elif name == "docker_agent":

            from app.agents.docker.agent import (
                docker_agent
            )

            register_agent(
                name,
                docker_agent
            )

        # =================================================
        # GITHUB
        # =================================================

        elif name == "github_agent":

            from app.agents.github.agent import (
                github_agent
            )

            register_agent(
                name,
                github_agent
            )

        # =================================================
        # REFLECTION
        # =================================================

        elif name == "reflection_agent":

            from app.agents.reflection.agent import (
                reflection_agent
            )

            register_agent(
                name,
                reflection_agent
            )

        # =================================================
        # DEVOPS
        # =================================================

        elif name == "devops_agent":

            from app.agents.devops.agent import (
                devops_agent
            )

            register_agent(
                name,
                devops_agent
            )

    except ImportError as e:

        print(
            f"[Registry] Failed to load "
            f"'{name}': {e}"
        )

        return None

    return _AGENTS.get(
        name
    )


def list_agents():
    """
    Return all currently loaded agents.
    """

    return sorted(
        _AGENTS.keys()
    )