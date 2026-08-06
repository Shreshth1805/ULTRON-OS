class ExecutionReport:

    def build(

        self,

        state

    ):

        return {

            "success": state.success,

            "steps": [

                step.model_dump()

                for step in state.steps

            ]

        }


execution_report = ExecutionReport()