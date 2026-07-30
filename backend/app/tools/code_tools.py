import ast
import os


def write_file(filename: str, content: str):

    try:
        directory = os.path.dirname(filename)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

        return {
            "success": True,
            "message": "File written successfully",
            "filename": filename
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


def read_file(filename: str):

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except Exception as e:

        return f"Error reading file: {e}"


def validate_python_code(code: str):

    try:

        ast.parse(code)

        return {
            "valid": True,
            "message": "Python code is syntactically valid"
        }

    except SyntaxError as e:

        return {
            "valid": False,
            "message": "Python syntax error",
            "error": str(e)
        }

    except Exception as e:

        return {
            "valid": False,
            "message": "Validation failed",
            "error": str(e)
        }


CODE_TOOLS = {
    "write_file": write_file,
    "read_file": read_file,
    "validate_python_code": validate_python_code
}