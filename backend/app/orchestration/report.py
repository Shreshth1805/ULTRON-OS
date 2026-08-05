class ExecutionReport:

    def __init__(self):

        self.tasks = []

    def add(

        self,

        name,

        success,

        output

    ):

        self.tasks.append({

            "task": name,

            "success": success,

            "output": output

        })

    def summary(self):

        return {

            "success": all(

                task["success"]

                for task in self.tasks

            ),

            "tasks": self.tasks

        }