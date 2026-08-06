TEST_PROMPT = """
You are an expert Python Test Engineer.

Generate pytest unit tests for the following code.

Requirements:

- Use pytest
- Cover edge cases
- Cover invalid inputs
- Cover normal inputs

Code:

{code}

Return ONLY Python code.
"""