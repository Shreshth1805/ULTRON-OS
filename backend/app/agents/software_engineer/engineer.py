from app.core.llm import llm


class SoftwareEngineerAgent:

    def generate_code(
        self,
        code: str,
        filename: str = "main.py"
    ):

        prompt = f"""
You are ULTRON, an AI software engineer.

Generate clean, production-quality code.

Requested task:
{code}

Target filename:
{filename}

Return ONLY the code.
Do not use Markdown code fences.
Do not explain the code.
"""

        response = llm.invoke(prompt)

        generated_code = response.content

        return {
            "filename": filename,
            "code": generated_code
        }


    def test_code(self, code: str):

        prompt = f"""
You are a senior software engineer.

Review the following code:

{code}

Identify:
1. Syntax errors
2. Logical errors
3. Potential bugs
4. Improvements

Give a concise technical review.
"""

        response = llm.invoke(prompt)

        return {
            "review": response.content
        }
    def run(
            self,
            message: str
        ):

            return self.generate_code(
                code=message,
                filename="generated.py"
            )


software_engineer_agent = SoftwareEngineerAgent()
