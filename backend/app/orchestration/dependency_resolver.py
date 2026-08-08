"""
ULTRON Workflow Dependency Resolver

Allows workflow tasks to reference values produced by
previous tasks.

Example:

    kwargs={
        "project_path": "$project_path"
    }

The resolver searches the shared workflow context and
returns the actual value.

Supported:

    "$project_path"
    "$project_name"
    "$plan"
    "$review"

Also supports nested dictionaries, lists and tuples.
"""

from __future__ import annotations

from typing import Any, Dict

from app.orchestration.context_manager import (
    context_manager
)


class DependencyResolver:
    """
    Resolves references between workflow tasks.
    """

    # =========================================================
    # RESOLVE KWARGS
    # =========================================================

    def resolve(
        self,
        kwargs: Dict[str, Any] | None
    ) -> Dict[str, Any]:

        if not kwargs:
            return {}

        return {
            key: self.resolve_value(
                value
            )
            for key, value in kwargs.items()
        }

    # =========================================================
    # RESOLVE VALUE
    # =========================================================

    def resolve_value(
        self,
        value: Any
    ):

        # -----------------------------------------------------
        # String
        # -----------------------------------------------------

        if isinstance(value, str):

            if value.startswith("$"):

                reference = value[1:].strip()

                if not reference:

                    raise ValueError(
                        "Empty workflow dependency reference."
                    )

                return self._get_context_value(
                    reference
                )

            return value

        # -----------------------------------------------------
        # Dictionary
        # -----------------------------------------------------

        if isinstance(value, dict):

            return {
                key: self.resolve_value(
                    item
                )
                for key, item in value.items()
            }

        # -----------------------------------------------------
        # List
        # -----------------------------------------------------

        if isinstance(value, list):

            return [
                self.resolve_value(
                    item
                )
                for item in value
            ]

        # -----------------------------------------------------
        # Tuple
        # -----------------------------------------------------

        if isinstance(value, tuple):

            return tuple(
                self.resolve_value(
                    item
                )
                for item in value
            )

        # -----------------------------------------------------
        # Everything else
        # -----------------------------------------------------

        return value

    # =========================================================
    # GET CONTEXT VALUE
    # =========================================================

    def _get_context_value(
        self,
        key: str
    ):

        # -----------------------------------------------------
        # 1. Direct context lookup
        # -----------------------------------------------------

        value = context_manager.get(
            key
        )

        if value is not None:

            return value

        # -----------------------------------------------------
        # 2. Get complete context
        # -----------------------------------------------------

        try:

            context = context_manager.all()

        except Exception:

            context = {}

        if not isinstance(
            context,
            dict
        ):

            context = {}

        # -----------------------------------------------------
        # 3. Direct dictionary lookup
        # -----------------------------------------------------

        if key in context:

            return context[key]

        # -----------------------------------------------------
        # 4. Search recursively
        # -----------------------------------------------------

        found, exists = self._search_nested(
            context,
            key
        )

        if exists:

            return found

        # -----------------------------------------------------
        # 5. Special handling for project path
        # -----------------------------------------------------

        # Some agents return:
        #
        # {
        #     "project": {
        #         "project_path": "workspace/..."
        #     }
        # }
        #
        # or:
        #
        # {
        #     "project_path": "workspace/..."
        # }

        if key == "project_path":

            found, exists = self._search_nested(
                context,
                "path"
            )

            if exists:

                return found

        # -----------------------------------------------------
        # 6. Special handling for project name
        # -----------------------------------------------------

        if key == "project_name":

            found, exists = self._search_nested(
                context,
                "name"
            )

            if exists:

                return found

        # -----------------------------------------------------
        # Missing dependency
        # -----------------------------------------------------

        raise ValueError(
            f"Workflow dependency '{key}' "
            f"was not found in context."
        )

    # =========================================================
    # RECURSIVE SEARCH
    # =========================================================

    def _search_nested(
        self,
        data: Any,
        key: str
    ):

        # -----------------------------------------------------
        # Dictionary
        # -----------------------------------------------------

        if isinstance(data, dict):

            if key in data:

                return (
                    data[key],
                    True
                )

            for value in data.values():

                found, exists = self._search_nested(
                    value,
                    key
                )

                if exists:

                    return (
                        found,
                        True
                    )

        # -----------------------------------------------------
        # List
        # -----------------------------------------------------

        elif isinstance(data, list):

            for item in data:

                found, exists = self._search_nested(
                    item,
                    key
                )

                if exists:

                    return (
                        found,
                        True
                    )

        # -----------------------------------------------------
        # Tuple
        # -----------------------------------------------------

        elif isinstance(data, tuple):

            for item in data:

                found, exists = self._search_nested(
                    item,
                    key
                )

                if exists:

                    return (
                        found,
                        True
                    )

        return (
            None,
            False
        )


# =========================================================
# GLOBAL RESOLVER
# =========================================================

dependency_resolver = DependencyResolver()