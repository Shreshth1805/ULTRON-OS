from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime
import time

from app.tools.registry import get_agent

from app.communication import (
    agent_bus,
    Event
)

from app.orchestration.context_manager import (
    context_manager
)


@dataclass
class WorkflowTask:

    name: str

    agent: str

    action: str

    kwargs: dict = field(
        default_factory=dict
    )

    depends_on: List[str] = field(
        default_factory=list
    )

    priority: int = 100

    retries: int = 0

    max_retries: int = 2

    timeout: int = 300


class WorkflowEngine:

    # =========================================================
    # RESOLVE VALUE
    # =========================================================

    def _resolve_value(
        self,
        value,
        results
    ):

        if not isinstance(
            value,
            str
        ):

            return value

        # -----------------------------------------------------
        # $planner
        # -----------------------------------------------------

        if value.startswith("$"):

            expression = value[1:]

            parts = expression.split(
                "."
            )

            task_name = parts[0]

            if task_name not in results:

                return value

            current = results[
                task_name
            ]

            # -------------------------------------------------
            # Navigate nested result
            # -------------------------------------------------

            for part in parts[1:]:

                if isinstance(
                    current,
                    dict
                ):

                    current = current.get(
                        part
                    )

                else:

                    return None

            return current

        return value

    # =========================================================
    # RESOLVE KWARGS
    # =========================================================

    def _resolve_kwargs(
        self,
        kwargs,
        results
    ):

        resolved = {}

        for key, value in kwargs.items():

            resolved[key] = self._resolve_value(
                value,
                results
            )

        return resolved

    # =========================================================
    # EXECUTE
    # =========================================================

    def execute(
        self,
        tasks: List[WorkflowTask]
    ):

        context_manager.reset()

        results: Dict[str, dict] = {}

        completed = set()

        failed = set()

        workflow_start = time.time()

        task_map = {
            task.name: task
            for task in tasks
        }

        # =====================================================
        # MAIN LOOP
        # =====================================================

        while len(completed) < len(tasks):

            progress = False

            # -------------------------------------------------
            # Find executable tasks
            # -------------------------------------------------

            for task in tasks:

                if task.name in completed:

                    continue

                # -------------------------------------------------
                # Dependencies
                # -------------------------------------------------

                dependencies_ready = all(
                    dep in completed
                    for dep in task.depends_on
                )

                if not dependencies_ready:

                    continue

                # -------------------------------------------------
                # Agent
                # -------------------------------------------------

                agent = get_agent(
                    task.agent
                )

                if agent is None:

                    error = (
                        f"Agent '{task.agent}' "
                        f"not found."
                    )

                    result = {

                        "success": False,

                        "status": "failed",

                        "agent": task.agent,

                        "action": task.action,

                        "error": error,

                        "timestamp":
                            datetime.utcnow().isoformat()

                    }

                    results[
                        task.name
                    ] = result

                    failed.add(
                        task.name
                    )

                    completed.add(
                        task.name
                    )

                    progress = True

                    continue

                # -------------------------------------------------
                # Resolve arguments
                # -------------------------------------------------

                resolved_kwargs = self._resolve_kwargs(
                    task.kwargs,
                    results
                )

                # -------------------------------------------------
                # Execute
                # -------------------------------------------------

                started = time.time()

                try:

                    method = getattr(
                        agent,
                        task.action
                    )

                    output = method(
                        **resolved_kwargs
                    )

                    duration = round(
                        time.time() - started,
                        3
                    )

                    result = {

                        "success": True,

                        "status": "completed",

                        "agent": task.agent,

                        "action": task.action,

                        "execution_time":
                            duration,

                        "result": output

                    }

                    results[
                        task.name
                    ] = result

                    # -------------------------------------------------
                    # Save output into context
                    # -------------------------------------------------

                    context_manager.save_result(
                        task.name,
                        output
                    )

                    if isinstance(
                        output,
                        dict
                    ):

                        context_manager.update(
                            output
                        )

                    # -------------------------------------------------
                    # Event
                    # -------------------------------------------------

                    agent_bus.publish(

                        "task_completed",

                        Event(

                            sender=task.agent,

                            receiver="*",

                            action=task.action,

                            payload=result

                        )

                    )

                except Exception as error:

                    duration = round(
                        time.time() - started,
                        3
                    )

                    result = {

                        "success": False,

                        "status": "failed",

                        "agent": task.agent,

                        "action": task.action,

                        "execution_time":
                            duration,

                        "error": str(error)

                    }

                    results[
                        task.name
                    ] = result

                    failed.add(
                        task.name
                    )

                    context_manager.save_result(
                        task.name,
                        result
                    )

                    agent_bus.publish(

                        "task_failed",

                        Event(

                            sender=task.agent,

                            receiver="*",

                            action=task.action,

                            payload=result

                        )

                    )

                completed.add(
                    task.name
                )

                progress = True

            # =====================================================
            # DEADLOCK
            # =====================================================

            if not progress:

                remaining = [

                    task.name

                    for task in tasks

                    if task.name
                    not in completed

                ]

                return {

                    "success": False,

                    "error":
                        "Workflow deadlock detected.",

                    "remaining_tasks":
                        remaining,

                    "results":
                        results,

                    "context":
                        context_manager.all()

                }

        # =====================================================
        # FINISHED
        # =====================================================

        workflow_time = round(
            time.time()
            - workflow_start,
            3
        )

        context_manager.set(
            "workflow_time",
            workflow_time
        )

        context_manager.set(
            "completed_tasks",
            len(completed)
        )

        context_manager.set(
            "failed_tasks",
            len(failed)
        )

        return {

            "success":
                len(failed) == 0,

            "workflow_time":
                workflow_time,

            "total_tasks":
                len(tasks),

            "completed_tasks":
                len(completed),

            "failed_tasks":
                len(failed),

            "results":
                results,

            "context":
                context_manager.all()

        }


workflow_engine = WorkflowEngine()