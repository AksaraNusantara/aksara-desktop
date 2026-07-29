"""
application.py

Application lifecycle coordinator.

This module implements the root Application object responsible for
coordinating the application lifecycle.

Responsibilities
----------------
- Application bootstrap.
- Runtime lifecycle.
- Application shutdown.

References
----------
APPLICATION_ARCHITECTURE.md
    - Section 5 : Application Bootstrap
    - Section 13: Startup Sequence
"""

from __future__ import annotations

from ui.main_window import MainWindow


class Application:
    """
    Application lifecycle coordinator.

    The Application class is responsible for bootstrapping the
    application and coordinating its lifecycle.

    It SHALL NOT implement business logic.
    """

    def __init__(self) -> None:
        """
        Initialize the Application.
        """

        self._initialized: bool = False
        self._main_window: MainWindow | None = None

    @property
    def initialized(self) -> bool:
        """
        Return the initialization state.

        Returns
        -------
        bool
            True if the application has been initialized.
        """

        return self._initialized

    @property
    def main_window(self) -> MainWindow | None:
        """
        Return the application's main window.

        Returns
        -------
        MainWindow | None
            The application's main window.
        """

        return self._main_window

    def initialize(self) -> None:
        """
        Initialize the application.

        This method performs all startup tasks required before the
        application can run.
        """

        if self._initialized:
            return

        self._main_window = MainWindow()

        self._initialized = True

    def run(self) -> None:
        """
        Run the application.

        Raises
        ------
        RuntimeError
            If the application has not been initialized.
        """

        if not self._initialized:
            raise RuntimeError(
                "Application has not been initialized."
            )

        assert self._main_window is not None

        self._main_window.show()

    def shutdown(self) -> None:
        """
        Shutdown the application.
        """

        if not self._initialized:
            return

        self._initialized = False