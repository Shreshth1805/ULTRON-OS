from typing import Callable


class ToolManager:

    def __init__(self):

        self.tools = {}

    def register(self, name: str, tool: Callable):

        self.tools[name] = tool

    def execute(self, name: str, *args, **kwargs):

        if name not in self.tools:

            raise Exception(f"{name} tool not found")

        return self.tools[name](*args, **kwargs)

    def list_tools(self):

        return list(self.tools.keys())


tool_manager = ToolManager()