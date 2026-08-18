class Debugger:

    def analyze(self, stderr: str):

        if not stderr:
            return {
                "has_error": False,
                "error": ""
            }

        if stderr.startswith("TIMEOUT:"):
            # Not something an LLM fix attempt can address - most
            # likely a generated server that started successfully and
            # is simply still running.
            return {
                "has_error": False,
                "error": stderr
            }

        return {
            "has_error": True,
            "error": stderr
        }


debugger = Debugger()