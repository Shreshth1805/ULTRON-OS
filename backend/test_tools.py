from app.tools.registry import (
    list_tools
)


print(
    "Available ULTRON tools:"
)

for tool in list_tools():

    print(
        f"- {tool}"
    )