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

from app.orchestration.dependency_resolver import (
    dependency_resolver
)
import traceback

from app.orchestration.scheduler import (
    task_scheduler
)

@dataclass
class WorkflowTask:

    name: str

    agent: str

    action: str

    kwargs: dict = field(default_factory=dict)

    depends_on: List[str] = field(default_factory=list)

    priority: int = 100

    retries: int = 0

    max_retries: int = 2

    timeout: int = 300

class WorkflowEngine:

    def execute(
        self,
        tasks: List[WorkflowTask]
    ):

        # =====================================================
        # Initialize
        # =====================================================

        context_manager.reset()

        results: Dict[str, dict] = {}

        completed = set()

        failed = set()

        workflow_start = time.time()

        # =====================================================
        # Execute Workflow
        # =====================================================

        while len(completed) < len(tasks):

            progress = False
            task = task_scheduler.next()

            if task is None:
                break
            for task in tasks:

                task_scheduler.add(

                    task,

                    priority=task.priority

                )

            while not task_scheduler.empty():
                # --------------------------------------------
                # Wait for dependencies
                # --------------------------------------------

                if any(
                    dep not in completed
                    for dep in task.depends_on
                ):
                    continue

                # --------------------------------------------
                # Get Agent
                # --------------------------------------------

                agent = get_agent(task.agent)

                if agent is None:

                    error = f"Agent '{task.agent}' not found."

                    result = {

                        "success": False,

                        "status": "failed",

                        "agent": task.agent,

                        "action": task.action,

                        "error": error,

                        "timestamp": datetime.utcnow().isoformat()

                    }

                    results[task.name] = result

                    context_manager.save_result(
                        task.name,
                        result
                    )

                    if task.retries < task.max_retries:

                        task.retries += 1

                        task_scheduler.retry(

                            task,

                            task.retries,

                            priority=task.priority

                        )

                    else:

                        failed.add(task.name)

                    completed.add(task.name)

                    progress = True

                    agent_bus.publish(

                        "task_failed",

                        Event(

                            sender="workflow_engine",

                            receiver="*",

                            action=task.action,

                            payload=result

                        )

                    )

                    continue

                # --------------------------------------------
                # Resolve Dependencies
                # --------------------------------------------

                resolved_kwargs = dependency_resolver.resolve(
                    task.kwargs
                )

                # --------------------------------------------
                # Execute
                # --------------------------------------------

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

                        "execution_time": duration,

                        "result": output

                    }

                    results[task.name] = result
                    context_manager.set(

                            f"history_{task.name}",

                            result

                        )
                    # ----------------------------------------
                    # Save Result
                    # ----------------------------------------

                    context_manager.save_result(
                        task.name,
                        output
                    )

                    # ----------------------------------------
                    # Update Shared Context
                    # ----------------------------------------

                    if isinstance(output, dict):

                        context_manager.update(output)

                        mappings = {

                            "project": "project_name",

                            "path": "project_path",

                            "plan": "plan",

                            "execution": "execution",

                            "review": "review",

                            "security": "security",

                            "testing": "testing",

                            "fixes": "fixes",

                            "reflection": "reflection",

                            "github": "github"

                        }

                        for key, ctx_key in mappings.items():

                            if key in output:

                                context_manager.set(
                                    ctx_key,
                                    output[key]
                                )

                    # ----------------------------------------
                    # Publish Event
                    # ----------------------------------------

                    agent_bus.publish(

                        "task_completed",

                        Event(

                            sender=task.agent,

                            receiver="*",

                            action=task.action,

                            payload=result

                        )

                    )

                except Exception as e:

                    duration = round(
                        time.time() - started,
                        3
                    )

                    result = {

                        "success": False,

                        "status": "failed",

                        "agent": task.agent,

                        "action": task.action,

                        "execution_time": duration,

                        "error": str(e)

                    }

                    results[task.name] = result

                    context_manager.save_result(
                        task.name,
                        result
                    )

                    failed.add(task.name)

                    agent_bus.publish(

                        "task_failed",

                        Event(

                            sender=task.agent,

                            receiver="*",

                            action=task.action,

                            payload=result

                        )

                    )

                completed.add(task.name)

                progress = True

            # =================================================
            # Deadlock Detection
            # =================================================

            if not progress:

                remaining = [

                    task.name

                    for task in tasks

                    if task.name not in completed

                ]

                return {

                    "success": False,

                    "error": "Workflow deadlock detected.",

                    "remaining_tasks": remaining,

                    "results": results,

                    "context": context_manager.all()

                }
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

        # =====================================================
        # Workflow Finished
        # =====================================================

        workflow_time = round(

            time.time() - workflow_start,

            3

        )

        return {

            "success": len(failed) == 0,

            "workflow_time": workflow_time,

            "total_tasks": len(tasks),

            "completed_tasks": len(completed),

            "failed_tasks": len(failed),

            "results": results,

            "context": context_manager.all()

        }


workflow_engine = WorkflowEngine()