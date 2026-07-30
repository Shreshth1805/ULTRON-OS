from app.agents.software_engineer.engineer import (
    software_engineer_agent
)


code = """
def add(a, b):
    return a + b

print(add(10, 20))
"""


result = software_engineer_agent.test_code(
    code
)

print(result)