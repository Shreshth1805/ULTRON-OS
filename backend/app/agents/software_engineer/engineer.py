# =========================================================
# SOFTWARE ENGINEER AGENT
# =========================================================

import re
import time
from pathlib import Path
from typing import List

from app.core.llm import llm

from app.workspace.file_manager import (
    get_project_path,
    write_project_file,
    list_project_files,
)


class SoftwareEngineerAgent:
    """
    ULTRON Software Engineer.

    Responsibilities:
        1. Understand the project request.
        2. Determine the project name.
        3. Create an isolated workspace.
        4. Extract the required files from the plan.
        5. Generate code for every file.
        6. Write files into the correct project directory.
        7. Return the project path to the workflow context.

    IMPORTANT:
        This agent never writes to a global/fixed project such as
        'ultron_generated_project'.
    """

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        self.workspace_root = Path("workspace")

        self.workspace_root.mkdir(
            parents=True,
            exist_ok=True
        )

    # =====================================================
    # BUILD
    # =====================================================

    def build(
        self,
        prompt: str
    ):

        return self.build_project(
            request=prompt
        )

    # =====================================================
    # BUILD PROJECT
    # =====================================================

    def build_project(
        self,
        request: str,
        project_name: str = None,
        project_description: str = None,
        plan: str = None
    ):

        start_time = time.time()

        # -------------------------------------------------
        # Normalize request
        # -------------------------------------------------

        if not request:
            request = project_description or ""

        if not request:
            raise ValueError(
                "Project request cannot be empty."
            )

        # -------------------------------------------------
        # Use supplied name or generate one
        # -------------------------------------------------

        if project_name:

            project_name = self._sanitize_project_name(
                project_name
            )

        elif plan:

            project_name = self._extract_project_name(
                plan,
                request
            )

        else:

            project_name = self._generate_project_name(
                request
            )

        # -------------------------------------------------
        # NEVER use ultron_generated_project
        # -------------------------------------------------

        if project_name.lower() == "ultron_generated_project":

            project_name = self._generate_project_name(
                request
            )

        # -------------------------------------------------
        # Create isolated project directory
        # -------------------------------------------------

        project_name = self._get_available_project_name(
            project_name
        )

        project_path = get_project_path(
            project_name
        )

        project_path.mkdir(
            parents=True,
            exist_ok=True
        )

        # -------------------------------------------------
        # Create plan if one wasn't supplied
        # -------------------------------------------------

        if not plan:

            plan = self._create_plan(
                request
            )

        # -------------------------------------------------
        # Extract files
        # -------------------------------------------------

        files = self._extract_files(
            plan
        )

        # -------------------------------------------------
        # Safety fallback
        # -------------------------------------------------

        if not files:

            files = self._generate_file_list(
                request,
                plan
            )

        # -------------------------------------------------
        # Remove duplicates
        # -------------------------------------------------

        files = self._unique_files(
            files
        )

        generated_files = []
        failed_files = []

        # =================================================
        # GENERATE EACH FILE
        # =================================================

        for filename in files:

            try:

                # -----------------------------------------
                # Validate filename
                # -----------------------------------------

                filename = self._sanitize_filename(
                    filename
                )

                if not filename:
                    continue

                # -----------------------------------------
                # Generate code
                # -----------------------------------------

                code = self._generate_file(
                    filename=filename,
                    project_description=request,
                    project_plan=plan
                )

                # -----------------------------------------
                # Clean LLM response
                # -----------------------------------------

                code = self._clean_code(
                    code
                )

                # -----------------------------------------
                # Write file
                # -----------------------------------------

                result = write_project_file(
                    project_name=project_name,
                    filename=filename,
                    content=code
                )

                if result.get("success"):

                    generated_files.append(
                        filename
                    )

                else:

                    failed_files.append(
                        {
                            "filename": filename,
                            "error": result.get(
                                "error",
                                "Unknown error"
                            )
                        }
                    )

            except Exception as exc:

                failed_files.append(
                    {
                        "filename": filename,
                        "error": str(exc)
                    }
                )

        # =================================================
        # FINAL FILE SCAN
        # =================================================

        actual_files = list_project_files(
            project_name
        )

        execution_time = round(
            time.time() - start_time,
            3
        )

        # =================================================
        # RESULT
        # =================================================

        return {

            "success": (
                len(actual_files) > 0
                and len(failed_files) == 0
            ),

            "project": project_name,

            "project_name": project_name,

            "project_path": str(
                project_path
            ),

            "path": str(
                project_path
            ),

            "description": request,

            "plan": plan,

            "files": actual_files,

            "generated_files": generated_files,

            "failed_files": failed_files,

            "file_count": len(actual_files),

            "execution_time": execution_time,

            "message": (
                f"Project '{project_name}' created "
                f"with {len(actual_files)} files."
            )
        }

    # =====================================================
    # PROJECT NAME
    # =====================================================

    def _extract_project_name(
        self,
        plan: str,
        prompt: str
    ) -> str:

        patterns = [

            r"Project Name\s*[:\-]\s*(.+)",

            r"Project\s+Name\s*[:\-]\s*(.+)",

            r"project_name\s*[:\-]\s*(.+)",

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                plan,
                re.IGNORECASE
            )

            if match:

                name = match.group(1).strip()

                name = name.split(
                    "\n"
                )[0].strip()

                name = name.strip(
                    "`*_#:- "
                )

                if name:

                    return self._sanitize_project_name(
                        name
                    )

        return self._generate_project_name(
            prompt
        )

    # =====================================================
    # GENERATE PROJECT NAME
    # =====================================================

    def _generate_project_name(
        self,
        prompt: str
    ) -> str:

        prompt_lower = prompt.lower()

        # -----------------------------------------------
        # Common application types
        # -----------------------------------------------

        keywords = [

            "todo",
            "chat",
            "blog",
            "ecommerce",
            "e-commerce",
            "authentication",
            "auth",
            "fastapi",
            "api",
            "dashboard",
            "video",
            "image",
            "ml",
            "machine learning",
            "data",
            "database",
            "inventory",
            "school",
            "student",
            "finance",

        ]

        selected = []

        for keyword in keywords:

            if keyword in prompt_lower:

                cleaned = keyword.replace(
                    "-",
                    "_"
                ).replace(
                    " ",
                    "_"
                )

                if cleaned not in selected:

                    selected.append(
                        cleaned
                    )

        if selected:

            name = "_".join(
                selected[:4]
            )

        else:

            words = re.findall(
                r"[a-zA-Z0-9]+",
                prompt_lower
            )

            name = "_".join(
                words[:5]
            )

        if not name:

            name = "ultron_project"

        return self._sanitize_project_name(
            name
        )

    # =====================================================
    # SANITIZE PROJECT NAME
    # =====================================================

    def _sanitize_project_name(
        self,
        name: str
    ) -> str:

        name = str(name).strip()

        name = name.replace(
            "`",
            ""
        )

        name = re.sub(
            r"[^a-zA-Z0-9_\-]+",
            "_",
            name
        )

        name = re.sub(
            r"_+",
            "_",
            name
        )

        name = name.strip(
            "_-"
        )

        if not name:

            name = "ultron_project"

        return name.lower()

    # =====================================================
    # AVAILABLE PROJECT NAME
    # =====================================================

    def _get_available_project_name(
        self,
        project_name: str
    ) -> str:

        candidate = project_name

        counter = 1

        while get_project_path(
            candidate
        ).exists():

            candidate = (
                f"{project_name}_{counter}"
            )

            counter += 1

        return candidate

    # =====================================================
    # CREATE PLAN
    # =====================================================

    def _create_plan(
        self,
        request: str
    ) -> str:

        prompt = f"""
You are a Senior Software Architect.

Design a complete software project for:

{request}

Return a detailed development plan.

The plan MUST contain:

Project Name:
Folder Structure:
Files:
Development Steps:

Under Files, list EVERY important file that must be
created for the project.

Do not limit the project to only three files.

Include:
- application source code
- configuration
- models
- schemas
- services
- routes/controllers
- database files
- tests
- README
- requirements/dependencies
- Docker files when appropriate
- frontend files when appropriate

Make the project production-oriented.
"""

        response = llm.invoke(
            prompt
        )

        return getattr(
            response,
            "content",
            str(response)
        )

    # =====================================================
    # EXTRACT FILES FROM PLAN
    # =====================================================

    def _extract_files(
        self,
        plan: str
    ) -> List[str]:

        files = []

        # -------------------------------------------------
        # Look for explicit file paths
        # -------------------------------------------------

        extensions = (
            r"py|js|ts|tsx|jsx|html|css|json|yaml|yml|"
            r"md|txt|sql|env|ini|toml|sh|bat|dockerfile"
        )

        matches = re.findall(
            rf"""
            (?:
                [\w\-.]+/
            )*
            [\w\-.]+
            \.(?:{extensions})
            """,
            plan,
            re.IGNORECASE |
            re.VERBOSE
        )

        files.extend(
            matches
        )

        # -------------------------------------------------
        # Backtick paths
        # -------------------------------------------------

        backtick_matches = re.findall(
            r"`([^`]+)`",
            plan
        )

        for item in backtick_matches:

            item = item.strip()

            if self._looks_like_file(
                item
            ):

                files.append(
                    item
                )

        return self._unique_files(
            files
        )

    # =====================================================
    # FALLBACK FILE GENERATOR
    # =====================================================

    def _generate_file_list(
        self,
        request: str,
        plan: str
    ) -> List[str]:

        prompt = f"""
Project request:

{request}

Project plan:

{plan}

Return ONLY a list of file paths that must be created.

One file per line.

Do not explain anything.

Create a COMPLETE project, not a three-file demo.
"""

        response = llm.invoke(
            prompt
        )

        text = getattr(
            response,
            "content",
            str(response)
        )

        files = []

        for line in text.splitlines():

            line = line.strip()

            line = re.sub(
                r"^[\-\*\d\.\)\s]+",
                "",
                line
            )

            line = line.strip(
                "` "
            )

            if self._looks_like_file(
                line
            ):

                files.append(
                    line
                )

        return self._unique_files(
            files
        )

    # =====================================================
    # LOOKS LIKE FILE
    # =====================================================

    def _looks_like_file(
        self,
        value: str
    ) -> bool:

        if not value:
            return False

        value = value.strip()

        if "/" not in value and "\\" not in value:

            return bool(
                re.search(
                    r"\.[a-zA-Z0-9]{1,10}$",
                    value
                )
            )

        return bool(
            re.search(
                r"\.[a-zA-Z0-9]{1,10}$",
                value
            )
        )

    # =====================================================
    # UNIQUE FILES
    # =====================================================

    def _unique_files(
        self,
        files: List[str]
    ) -> List[str]:

        result = []

        seen = set()

        for filename in files:

            filename = self._sanitize_filename(
                filename
            )

            if not filename:
                continue

            key = filename.lower()

            if key in seen:
                continue

            seen.add(
                key
            )

            result.append(
                filename
            )

        return result

    # =====================================================
    # SANITIZE FILE NAME
    # =====================================================

    def _sanitize_filename(
        self,
        filename: str
    ) -> str:

        filename = str(
            filename
        ).strip()

        filename = filename.strip(
            "`\"'"
        )

        filename = filename.replace(
            "\\",
            "/"
        )

        # -------------------------------------------------
        # Remove accidental leading project directory
        # -------------------------------------------------

        filename = re.sub(
            r"^workspace/[^/]+/",
            "",
            filename,
            flags=re.IGNORECASE
        )

        # -------------------------------------------------
        # Remove ./ 
        # -------------------------------------------------

        filename = re.sub(
            r"^\./+",
            "",
            filename
        )

        # -------------------------------------------------
        # Prevent absolute paths
        # -------------------------------------------------

        filename = filename.lstrip(
            "/"
        )

        # -------------------------------------------------
        # Prevent directory traversal
        # -------------------------------------------------

        parts = []

        for part in filename.split("/"):

            if part in (
                "",
                "."
            ):

                continue

            if part == "..":

                continue

            parts.append(
                part
            )

        filename = "/".join(
            parts
        )

        return filename

    # =====================================================
    # GENERATE FILE
    # =====================================================

    def _generate_file(
        self,
        filename: str,
        project_description: str,
        project_plan: str
    ) -> str:

        prompt = f"""
You are ULTRON's Senior Software Engineer.

PROJECT DESCRIPTION:
{project_description}

PROJECT PLAN:
{project_plan}

Generate the COMPLETE production-quality source code
for this file:

{filename}

Requirements:

1. Return ONLY the file contents.
2. Do NOT use Markdown code fences.
3. Do NOT explain the code.
4. Make the code executable.
5. Follow the architecture described in the plan.
6. Ensure imports match the project structure.
7. Do not create placeholder implementations unless
   absolutely necessary.
8. Include proper error handling.
9. Use secure coding practices.
10. Keep the implementation consistent with the other
    project files.
"""

        response = llm.invoke(
            prompt
        )

        return getattr(
            response,
            "content",
            str(response)
        )

    # =====================================================
    # CLEAN CODE
    # =====================================================

    def _clean_code(
        self,
        code: str
    ) -> str:

        if code is None:

            return ""

        code = str(
            code
        ).strip()

        # -------------------------------------------------
        # Remove Markdown fences
        # -------------------------------------------------

        code = re.sub(
            r"^```(?:python|py|javascript|js|typescript|"
            r"ts|json|html|css|sql|yaml|yml|bash|sh)?\s*",
            "",
            code,
            flags=re.IGNORECASE
        )

        code = re.sub(
            r"\s*```$",
            "",
            code
        )

        return code.strip()


# =========================================================
# GLOBAL AGENT INSTANCE
# =========================================================

software_engineer_agent = SoftwareEngineerAgent()