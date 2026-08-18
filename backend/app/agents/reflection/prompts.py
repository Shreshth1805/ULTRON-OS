REFLECTION_PROMPT = """
You are ULTRON's Self Reflection Engine.

Analyze the project execution.

Project:

{project}

Execution:

{execution}

Testing:

{testing}

Review:

{review}

Return JSON:

{{
  "summary":"",
  "risk_level":"",
  "improvements":[]
}}
"""