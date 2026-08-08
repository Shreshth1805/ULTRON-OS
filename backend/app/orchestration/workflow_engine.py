# =========================================================
# ULTRON WORKFLOW ENGINE
# =========================================================

import inspect
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.tools.registry import get_agent
from app.orchestration.dependency_resolver import (
    dependency_resolver
)


# =========================================================
# WORKFLOW TASK
# =========================================================

@dataclass
class WorkflowTask:

    name: str

    agent: str

    action: str

    kwargs: Dict[str, Any] = field(
        default_factory=dict
    )

    depends_on: List[str] = field(
        default_factory=list
    )


# =========================================================
# WORKFLOW ENGINE
# =========================================================

class WorkflowEngine:

    def __init__(self):

        self.results: Dict[str, Any] = {}

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(
        self,
        tasks: List[WorkflowTask]
    ):

        self.results = {}

        start_time = time.time()

        completed = 0
        failed = 0

        for task in tasks:

            # ---------------------------------------------
            # Dependency check
            # ---------------------------------------------

            dependency_failed = False

            for dependency in task.depends_on:

                dependency_result = self.results.get(
                    dependency
                )

                if not dependency_result:
                    dependency_failed = True
                    break

                if isinstance(
                    dependency_result,
                    dict
                ):

                    if dependency_result.get(
                        "success"
                    ) is False:

                        dependency_failed = True
                        break

            if dependency_failed:

                result = {
                    "success": False,
                    "status": "skipped",
                    "agent": task.agent,
                    "action": task.action,
                    "error": (
                        "Dependency failed."
                    )
                }

                self.results[
                    task.name
                ] = result

                print(
                    f"[SKIPPED] {task.agent}: "
                    f"dependency failed"
                )

                failed += 1

                continue

            # ---------------------------------------------
            # Load agent
            # ---------------------------------------------

            try:

                agent = get_agent(
                    task.agent
                )

                if agent is None:

                    raise RuntimeError(
                        f"Agent '{task.agent}' "
                        f"could not be loaded."
                    )

            except Exception as exc:

                result = {
                    "success": False,
                    "status": "failed",
                    "agent": task.agent,
                    "action": task.action,
                    "error": str(exc)
                }

                self.results[
                    task.name
                ] = result

                print(
                    f"[FAILED] {task.agent}: "
                    f"{exc}"
                )

                failed += 1

                continue

            # ---------------------------------------------
            # Find action
            # ---------------------------------------------

            action_method = getattr(
                agent,
                task.action,
                None
            )

            # ---------------------------------------------
            # Compatibility aliases
            # ---------------------------------------------

            if action_method is None:

                aliases = {

                    "fix_project": [
                        "fix",
                        "repair",
                        "run"
                    ],

                    "review_project": [
                        "review"
                    ],

                    "test_project": [
                        "test"
                    ],

                    "build": [
                        "build_project"
                    ],

                    "publish": [
                        "push",
                        "publish_project"
                    ]

                }

                for alternative in aliases.get(
                    task.action,
                    []
                ):

                    candidate = getattr(
                        agent,
                        alternative,
                        None
                    )

                    if candidate is not None:

                        action_method = candidate
                        break

            if action_method is None:

                result = {
                    "success": False,
                    "status": "failed",
                    "agent": task.agent,
                    "action": task.action,
                    "error": (
                        f"Agent '{task.agent}' "
                        f"does not have action "
                        f"'{task.action}'."
                    )
                }

                self.results[
                    task.name
                ] = result

                print(
                    f"[FAILED] {task.agent}: "
                    f"{result['error']}"
                )

                failed += 1

                continue

            # ---------------------------------------------
            # Resolve dependencies
            # ---------------------------------------------

            try:

                resolved_kwargs = (
                    dependency_resolver.resolve(
                        task.kwargs
                    )
                )

            except Exception as exc:

                result = {
                    "success": False,
                    "status": "failed",
                    "agent": task.agent,
                    "action": task.action,
                    "error": (
                        f"Dependency resolution failed: "
                        f"{exc}"
                    )
                }

                self.results[
                    task.name
                ] = result

                print(
                    f"[FAILED] {task.agent}: "
                    f"{exc}"
                )

                failed += 1

                continue

            # ---------------------------------------------
            # Signature-safe arguments
            # ---------------------------------------------

            try:

                resolved_kwargs = (
                    self._filter_kwargs(
                        action_method,
                        resolved_kwargs
                    )

                )

            except Exception:

                pass

            # ---------------------------------------------
            # Execute
            # ---------------------------------------------

            task_start = time.time()

            try:

                output = action_method(
                    **resolved_kwargs
                )

                execution_time = (
                    time.time() - task_start
                )

                result = self._normalize_result(
                    output,
                    task,
                    execution_time
                )

                self.results[
                    task.name
                ] = result

                # -----------------------------------------
                # Store useful outputs in shared context
                # -----------------------------------------

                self._store_context(
                    task,
                    result
                )

                if result.get(
                    "success",
                    True
                ):

                    completed += 1

                    print(
                        f"[SUCCESS] "
                        f"{task.agent} "
                        f"executed "
                        f"{task.action}"
                    )

                else:

                    failed += 1

                    print(
                        f"[FAILED] "
                        f"{task.agent}: "
                        f"{result}"
                    )

            except Exception as exc:

                execution_time = (
                    time.time() - task_start
                )

                result = {

                    "success": False,

                    "status": "failed",

                    "agent": task.agent,

                    "action": task.action,

                    "execution_time": (
                        execution_time
                    ),

                    "error": str(exc)

                }

                self.results[
                    task.name
                ] = result

                failed += 1

                print(
                    f"[FAILED] {task.agent}: "
                    f"{result}"
                )

        # =================================================
        # FINAL RESULT
        # =================================================

        return {

            "success": (
                failed == 0
            ),

            "workflow_time": (
                time.time() - start_time
            ),

            "total_tasks": len(tasks),

            "completed_tasks": completed,

            "failed_tasks": failed,

            "results": self.results

        }

    # =====================================================
    # FILTER KWARGS
    # =====================================================

    def _filter_kwargs(
        self,
        method,
        kwargs: Dict[str, Any]
    ):

        try:

            signature = inspect.signature(
                method
            )

        except Exception:

            return kwargs

        parameters = signature.parameters

        # ---------------------------------------------
        # If **kwargs exists, keep everything
        # ---------------------------------------------

        accepts_kwargs = any(

            parameter.kind
            == inspect.Parameter.VAR_KEYWORD

            for parameter
            in parameters.values()

        )

        if accepts_kwargs:

            return kwargs

        # ---------------------------------------------
        # Keep only supported arguments
        # ---------------------------------------------

        return {

            key: value

            for key, value in kwargs.items()

            if key in parameters

        }

    # =====================================================
    # NORMALIZE RESULT
    # =====================================================

    def _normalize_result(
        self,
        output,
        task: WorkflowTask,
        execution_time: float
    ):

        if isinstance(
            output,
            dict
        ):

            result = dict(
                output
            )

            result.setdefault(
                "success",
                True
            )

            result.setdefault(
                "status",
                "completed"
            )

            result.setdefault(
                "agent",
                task.agent
            )

            result.setdefault(
                "action",
                task.action
            )

            result.setdefault(
                "execution_time",
                execution_time
            )

            return result

        return {

            "success": True,

            "status": "completed",

            "agent": task.agent,

            "action": task.action,

            "execution_time": (
                execution_time
            ),

            "result": output

        }

    # =====================================================
    # STORE CONTEXT
    # =====================================================

    def _store_context(
        self,
        task: WorkflowTask,
        result: Dict[str, Any]
    ):

        try:

            from app.orchestration.context_manager import (
                context_manager
            )

            # Store complete task result

            context_manager.set(
                task.name,
                result
            )

            # ---------------------------------------------
            # Automatically expose common project values
            # ---------------------------------------------

            if isinstance(
                result,
                dict
            ):

                for key in (
                    "project_path",
                    "project_name",
                    "workspace",
                    "path"
                ):

                    if key in result:

                        context_manager.set(
                            key,
                            result[key]
                        )

                # -----------------------------------------
                # Nested result
                # -----------------------------------------

                nested = result.get(
                    "result"
                )

                if isinstance(
                    nested,
                    dict
                ):

                    for key in (
                        "project_path",
                        "project_name",
                        "workspace",
                        "path"
                    ):

                        if key in nested:

                            context_manager.set(
                                key,
                                nested[key]
                            )

        except Exception as exc:

            print(
                f"[Workflow] "
                f"Context storage warning: "
                f"{exc}"
            )


# =========================================================
# GLOBAL ENGINE
# =========================================================

workflow_engine = WorkflowEngine()