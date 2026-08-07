from copy import deepcopy

from app.orchestration.context_manager import (
    context_manager
)


class DependencyResolver:
    """
    Resolves task kwargs from the shared workflow context.

    Example:
        "$context.project_path"
            -> "/projects/my_app"

        "$context.project_name"
            -> "my_app"

        "$result.builder"
            -> builder task output
    """

    CONTEXT_PREFIX = "$context."
    RESULT_PREFIX = "$result."

    def resolve(self, kwargs: dict) -> dict:

        kwargs = deepcopy(kwargs)

        return self._resolve(kwargs)

    def _resolve(self, value):

        # ----------------------------------------
        # Dictionary
        # ----------------------------------------

        if isinstance(value, dict):

            return {

                k: self._resolve(v)

                for k, v in value.items()

            }

        # ----------------------------------------
        # List
        # ----------------------------------------

        if isinstance(value, list):

            return [

                self._resolve(v)

                for v in value

            ]

        # ----------------------------------------
        # Context Variable
        # ----------------------------------------

        if isinstance(value, str):

            if value.startswith(self.CONTEXT_PREFIX):

                key = value.replace(

                    self.CONTEXT_PREFIX,

                    ""

                )

                return context_manager.get(key)

            if value.startswith(self.RESULT_PREFIX):

                task = value.replace(

                    self.RESULT_PREFIX,

                    ""

                )

                return context_manager.get_result(task)

        return value


dependency_resolver = DependencyResolver()