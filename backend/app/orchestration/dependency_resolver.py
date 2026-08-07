# =========================================================
# DEPENDENCY RESOLVER
# =========================================================

from typing import Any

from app.orchestration.context_manager import (
    context_manager
)


class DependencyResolver:
    """
    Resolves values passed between workflow tasks.

    Example:

        {
            "project_path": "$project_path"
        }

    becomes:

        {
            "project_path": "workspace/my_project"
        }

    Values beginning with `$` are treated as references
    to the shared workflow context.
    """

    # =====================================================
    # RESOLVE COMPLETE KWARGS
    # =====================================================

    def resolve(
        self,
        kwargs: dict
    ) -> dict:

        if not kwargs:
            return {}

        resolved = {}

        for key, value in kwargs.items():

            resolved[key] = self.resolve_value(
                value
            )

        return resolved

    # =====================================================
    # RESOLVE VALUE
    # =====================================================

    def resolve_value(
        self,
        value: Any
    ):

        # -------------------------------------------------
        # String reference
        # -------------------------------------------------

        if isinstance(value, str):

            if value.startswith("$"):

                reference = value[1:]

                return self._get_context_value(
                    reference
                )

            return value

        # -------------------------------------------------
        # Dictionary
        # -------------------------------------------------

        if isinstance(value, dict):

            return {
                key: self.resolve_value(item)
                for key, item in value.items()
            }

        # -------------------------------------------------
        # List
        # -------------------------------------------------

        if isinstance(value, list):

            return [
                self.resolve_value(item)
                for item in value
            ]

        # -------------------------------------------------
        # Tuple
        # -------------------------------------------------

        if isinstance(value, tuple):

            return tuple(
                self.resolve_value(item)
                for item in value
            )

        # -------------------------------------------------
        # Everything else
        # -------------------------------------------------

        return value

    # =====================================================
    # GET CONTEXT VALUE
    # =====================================================

    def _get_context_value(
        self,
        key: str
    ):

        value = context_manager.get(
            key
        )

        if value is not None:

            return value

        # -------------------------------------------------
        # Try task result history
        # -------------------------------------------------

        history = context_manager.all()

        if key in history:

            return history[key]

        # -------------------------------------------------
        # Search nested dictionaries
        # -------------------------------------------------

        found = self._search_nested(
            history,
            key
        )

        if found is not None:

            return found

        # -------------------------------------------------
        # Missing dependency
        # -------------------------------------------------

        raise ValueError(
            f"Workflow dependency '{key}' "
            f"was not found in context."
        )

    # =====================================================
    # SEARCH NESTED
    # =====================================================

    def _search_nested(
        self,
        data,
        key: str
    ):

        if isinstance(data, dict):

            if key in data:

                return data[key]

            for value in data.values():

                result = self._search_nested(
                    value,
                    key
                )

                if result is not None:

                    return result

        elif isinstance(data, list):

            for item in data:

                result = self._search_nested(
                    item,
                    key
                )

                if result is not None:

                    return result

        return None


# =========================================================
# SINGLETON
# =========================================================

dependency_resolver = DependencyResolver()