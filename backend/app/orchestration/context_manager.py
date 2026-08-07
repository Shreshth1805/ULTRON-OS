from copy import deepcopy


class ContextManager:
    """
    Shared context for the entire workflow.

    Every agent can read/write values here.

    Example:

        context["project_path"]

        context["execution"]

        context["review"]

    """

    def __init__(self):

        self.reset()

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self._context = {}

        self._results = {}

    # =====================================================
    # Context
    # =====================================================

    def set(self, key, value):

        self._context[key] = value

    def get(self, key, default=None):

        return self._context.get(
            key,
            default
        )

    def update(self, values: dict):

        if isinstance(values, dict):

            self._context.update(values)

    def all(self):

        return deepcopy(
            self._context
        )

    # =====================================================
    # Results
    # =====================================================

    def save_result(
        self,
        task_name,
        result
    ):

        self._results[task_name] = result

    def get_result(
        self,
        task_name
    ):

        return self._results.get(
            task_name
        )

    def all_results(self):

        return deepcopy(
            self._results
        )

    # =====================================================
    # Delete
    # =====================================================

    def remove(self, key):

        if key in self._context:

            del self._context[key]

    def clear_results(self):

        self._results.clear()


context_manager = ContextManager()