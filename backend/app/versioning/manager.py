from datetime import datetime

from app.versioning.repository import (
    version_repository
)


class VersionManager:

    def create_version(

        self,

        project,

        files,

        message="Auto Save"

    ):

        version = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        version_repository.save(

            project,

            version,

            {

                "message": message,

                "files": files

            }

        )

        return {

            "success": True,

            "version": version

        }


version_manager = VersionManager()