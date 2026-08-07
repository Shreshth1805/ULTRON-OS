"""
ULTRON Software Engineer Agent

Responsible for:
- Planning projects
- Determining project structure
- Generating files
- Writing files
- Reviewing code
- Executing Python files
"""

import json
import re
from pathlib import Path

from app.core.llm import llm

from app.agents.software_engineer.planner import planner
from app.agents.software_engineer.generator import generator
from app.agents.software_engineer.reviewer import reviewer
from app.agents.software_engineer.executor import executor

from app.workspace.file_manager import (
    write_project_file,
    get_project_path,
)


class SoftwareEngineerAgent:

    # =========================================================
    # BUILD
    # =========================================================

    def build(
        self,
        prompt: str,
        plan=None,
        project_name: str | None = None,
    ):
        """
        Build a complete project from a natural-language request.
        """

        # -----------------------------------------------------
        # 1. Generate project plan
        # -----------------------------------------------------

        if not plan:

            plan = planner.create_plan(
                prompt
            )

        # -----------------------------------------------------
        # 2. Determine project name
        # -----------------------------------------------------

        if not project_name:

            project_name = self._extract_project_name(
                prompt,
                plan
            )

        project_name = self._sanitize_project_name(
            project_name
        )

        # -----------------------------------------------------
        # 3. Determine required files
        # -----------------------------------------------------

        files = self._extract_files(
            plan
        )

        # -----------------------------------------------------
        # Fallback
        # -----------------------------------------------------

        if not files:

            files = self._infer_files_with_llm(
                prompt,
                plan
            )

        # -----------------------------------------------------
        # Always have basic documentation
        # -----------------------------------------------------

        if "README.md" not in files:

            files.insert(
                0,
                "README.md"
            )

        # -----------------------------------------------------
        # 4. Generate every file
        # -----------------------------------------------------

        generated_files = []

        project_path = get_project_path(
            project_name
        )

        project_path.mkdir(
            parents=True,
            exist_ok=True
        )

        for filename in files:

            filename = self._clean_filename(
                filename
            )

            if not filename:
                continue

            try:

                code = generator.generate_file(
                    filename=filename,
                    project_description=prompt,
                    project_plan=plan
                )

                # ---------------------------------------------
                # Clean LLM markdown fences
                # ---------------------------------------------

                code = self._clean_generated_code(
                    code
                )

                write_project_file(
                    project_name,
                    filename,
                    code
                )

                generated_files.append(
                    filename
                )

            except Exception as error:

                print(
                    f"[SoftwareEngineer] "
                    f"Failed generating {filename}: {error}"
                )

        # -----------------------------------------------------
        # 5. Return complete project information
        # -----------------------------------------------------

        return {

            "success": len(generated_files) > 0,

            "project": project_name,

            "project_name": project_name,

            "project_path": str(
                project_path
            ),

            "plan": plan,

            "files": generated_files,

            "file_count": len(
                generated_files
            ),

            "message": (
                f"Project '{project_name}' "
                f"created with "
                f"{len(generated_files)} files."
            )

        }

    # =========================================================
    # BUILD PROJECT
    # =========================================================

    def build_project(
        self,
        project_name,
        description
    ):
        """
        Compatibility endpoint for /ai/project/build.
        """

        return self.build(
            prompt=description,
            project_name=project_name
        )

    # =========================================================
    # REVIEW
    # =========================================================

    def review_code(
        self,
        code
    ):

        return reviewer.review(
            code
        )

    # =========================================================
    # EXECUTE
    # =========================================================

    def execute(
        self,
        file_path
    ):

        return executor.run_python(
            file_path
        )

    # =========================================================
    # PROJECT NAME
    # =========================================================

    def _extract_project_name(
        self,
        prompt,
        plan
    ):

        text = f"{plan}\n{prompt}"

        patterns = [

            r"Project Name\s*[:\-]\s*([A-Za-z0-9_\- ]+)",

            r"project\s+called\s+([A-Za-z0-9_\- ]+)",

            r"project\s+named\s+([A-Za-z0-9_\- ]+)",

            r"build\s+([A-Za-z0-9_\-]+)\s+project",

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                return match.group(1).strip()

        return "ultron_generated_project"

    # =========================================================
    # SANITIZE PROJECT NAME
    # =========================================================

    def _sanitize_project_name(
        self,
        name
    ):

        name = re.sub(
            r"[^A-Za-z0-9_\- ]",
            "",
            name
        )

        name = name.strip().replace(
            " ",
            "_"
        )

        if not name:

            name = "ultron_generated_project"

        return name[:80]

    # =========================================================
    # EXTRACT FILES FROM PLAN
    # =========================================================

    def _extract_files(
        self,
        plan
    ):

        files = []

        text = str(
            plan
        )

        # -----------------------------------------------------
        # Find common file references
        # -----------------------------------------------------

        pattern = (
            r"(?:^|\s)"
            r"([A-Za-z0-9_.\-/]+"
            r"\.(?:py|js|jsx|ts|tsx|json|yaml|yml|md|txt|"
            r"html|css|scss|sql|env|toml|ini|cfg|sh))"
        )

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for filename in matches:

            filename = self._clean_filename(
                filename
            )

            if filename and filename not in files:

                files.append(
                    filename
                )

        # -----------------------------------------------------
        # Also parse bullet/list lines
        # -----------------------------------------------------

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            line = re.sub(
                r"^[\-\*\d\.\)\s]+",
                "",
                line
            )

            line = line.strip("` ")

            if "/" in line or "\\" in line:

                candidate = line.split(
                    " ",
                    1
                )[0]

                candidate = self._clean_filename(
                    candidate
                )

                if (
                    candidate
                    and "." in candidate
                    and candidate not in files
                ):

                    files.append(
                        candidate
                    )

        return files

    # =========================================================
    # LLM FILE INFERENCE
    # =========================================================

    def _infer_files_with_llm(
        self,
        prompt,
        plan
    ):

        inference_prompt = f"""
You are a senior software architect.

User request:
{prompt}

Project plan:
{plan}

Determine the complete list of files required to build
this project.

Return ONLY valid JSON.

Format:

{{
    "files": [
        "folder/file.py",
        "folder/config.py",
        "README.md"
    ]
}}

Do not explain anything.
"""

        response = llm.invoke(
            inference_prompt
        )

        content = getattr(
            response,
            "content",
            str(response)
        )

        content = self._clean_generated_code(
            content
        )

        try:

            data = json.loads(
                content
            )

            files = data.get(
                "files",
                []
            )

            return [
                self._clean_filename(
                    f
                )
                for f in files
                if self._clean_filename(f)
            ]

        except Exception:

            return []

    # =========================================================
    # CLEAN FILENAME
    # =========================================================

    def _clean_filename(
        self,
        filename
    ):

        if not filename:

            return ""

        filename = str(
            filename
        ).strip()

        filename = filename.strip(
            "`\"' "
        )

        filename = filename.replace(
            "\\",
            "/"
        )

        filename = filename.lstrip(
            "./"
        )

        # Prevent absolute paths
        filename = filename.replace(
            ":",
            ""
        )

        # Prevent traversal
        parts = [
            p for p in filename.split("/")
            if p not in ("", ".", "..")
        ]

        return "/".join(parts)

    # =========================================================
    # CLEAN GENERATED CODE
    # =========================================================

    def _clean_generated_code(
        self,
        code
    ):

        if code is None:

            return ""

        code = str(
            code
        ).strip()

        # Remove markdown fences
        code = re.sub(
            r"^```[a-zA-Z0-9_+-]*\s*",
            "",
            code
        )

        code = re.sub(
            r"\s*```$",
            "",
            code
        )

        return code.strip()


software_engineer_agent = SoftwareEngineerAgent()