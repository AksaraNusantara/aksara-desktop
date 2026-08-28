"""
Application path definitions.

This module defines filesystem locations owned by the Application Layer.

Responsibilities
----------------
- Determine the application user-data directory.
- Provide paths for application-owned persistent data.

This module SHALL NOT contain Learning Engine business logic.
"""

from __future__ import annotations

import os
from pathlib import Path


class ApplicationPaths:
    """
    Provide filesystem paths used by the application.
    """

    APPLICATION_NAME = "AksaraNusantara"

    @classmethod
    def user_data_dir(cls) -> Path:
        """
        Return the application's persistent user-data directory.

        On Windows, user data is stored under LOCALAPPDATA.
        """

        local_app_data = os.environ.get("LOCALAPPDATA")

        if local_app_data:
            return (
                Path(local_app_data)
                / cls.APPLICATION_NAME
            )

        # Fallback for environments where LOCALAPPDATA
        # is not defined, such as certain test environments.
        return (
            Path.home()
            / ".local"
            / cls.APPLICATION_NAME
        )

    @classmethod
    def learning_data_dir(cls) -> Path:
        """
        Return the persistent Learning Engine data directory.
        """

        return (
            cls.user_data_dir()
            / "learning"
        )