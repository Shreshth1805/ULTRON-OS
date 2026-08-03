from app.agents.software_engineer.planner import planner

from app.agents.software_engineer.generator import generator

from app.agents.software_engineer.reviewer import reviewer

from app.agents.software_engineer.executor import executor

from app.workspace.file_manager import (
    write_project_file
)


class SoftwareEngineerAgent:

    def build_project(

        self,

        project_name,

        description

    ):

        plan = planner.create_plan(description)

        files = [

            "README.md",

            "requirements.txt",

            "main.py"

        ]

        generated = {}

        for file in files:

            code = generator.generate_file(

                filename=file,

                project_description=description,

                project_plan=plan

            )

            write_project_file(

                project_name,

                file,

                code

            )

            generated[file] = code

        return {

            "success": True,

            "plan": plan,

            "files": list(generated.keys())

        }

    def review_code(

        self,

        code

    ):

        return reviewer.review(code)

    def execute(

        self,

        file_path

    ):

        return executor.run_python(file_path)


software_engineer_agent = SoftwareEngineerAgent()