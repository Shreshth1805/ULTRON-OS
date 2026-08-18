TEST_PROMPT = """
You are an expert Python Test Engineer.

Generate pytest unit tests for the following code.

The code below lives at "{filename}" and is importable as the Python
module "{module_path}". Import everything under test from exactly that
module path - do not invent, guess, or abbreviate a different module
name.

Requirements:

- Use pytest
- Cover edge cases
- Cover invalid inputs
- Cover normal inputs

Code:

{code}

Return ONLY Python code.
"""