class Debugger:

    def analyze(self, stderr: str):

        if not stderr:
            return {
                "has_error": False,
                "error": ""
            }

        return {
            "has_error": True,
            "error": stderr
        }


debugger = Debugger()