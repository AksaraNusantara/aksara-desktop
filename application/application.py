"""
application.py

Application lifecycle coordinator.

This module implements the root Application object responsible for
coordinating the application lifecycle.

Responsibilities
----------------
- Application bootstrap.
- Runtime lifecycle.
- Core Engine lifecycle.
- Application shutdown.

References
----------
APPLICATION_ARCHITECTURE.md
    - Section 5 : Application Bootstrap
    - Section 13: Startup Sequence
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from core.engine import CoreEngine
from core.services.audio_service import AudioService
from application.learning.flashcard.flashcard_session import (
    FlashcardSession,
)
from core.learning.models.learner_identity import LearnerIdentity
from core.learning.models.learner_setup_result import (
    LearnerSetupMode,
    LearnerSetupResult,
)
from core.learning.repositories.learner_repository import (
    LearnerRepository,
    StorageLearnerRepository,
)
from core.learning.repositories.learning_repository import (
    StorageLearningRepository,
)
from core.learning.services.learning_service import LearningService
from core.learning.storage.json_adapter import JSONAdapter
from application.paths import ApplicationPaths
from application.application_state import ApplicationStateStorage
from ui.learner_setup_dialog import LearnerSetupDialog
from ui.main_window import MainWindow


class Application:
    """
    Application lifecycle coordinator.
    """

    def __init__(
        self,
        learner_repository: LearnerRepository | None = None,
        application_state: ApplicationStateStorage | None = None,
    ) -> None:
        """Initialize the Application lifecycle coordinator."""

        self._initialized: bool = False

        self._engine = CoreEngine()

        self._audio: AudioService | None = None
        self._flashcard_session: FlashcardSession | None = None
        self._learning_service: LearningService | None = None
        self._main_window: MainWindow | None = None

        self._learner_repository = learner_repository
        self._application_state = application_state
        self._active_learner: LearnerIdentity | None = None

    @property
    def initialized(self) -> bool:
        """Return the application initialization state."""

        return self._initialized

    @property
    def engine(self) -> CoreEngine:
        """Return the application's Core Engine."""

        return self._engine

    @property
    def main_window(self) -> MainWindow | None:
        """Return the application's MainWindow instance."""

        return self._main_window

    @property
    def active_learner(self) -> LearnerIdentity | None:
        """Return the application's Active Learner."""

        return self._active_learner

    def initialize(self) -> None:
        """Initialize the application and establish an Active Learner."""

        if self._initialized:
            return

        #
        # Initialize Core Engine.
        #

        self._engine.initialize(
            Path("scriptpacks")
        )

        #
        # Register UI assets provided by every ScriptPack.
        #

        for identifier in self._engine.list():
            scriptpack = self._engine.get(
                identifier,
            )

            scriptpack.register_assets()

        project_root = Path(__file__).resolve().parent.parent

        #
        # Initialize shared services.
        #

        self._audio = AudioService(
            cache_root=(
                project_root
                / "cache"
                / "audio"
            )
        )

        #
        # Initialize session services.
        #

        self._flashcard_session = FlashcardSession(
            self._engine,
        )

        #
        # Initialize Learning Engine persistence.
        #

        learning_storage = JSONAdapter(
            ApplicationPaths.learning_data_dir(),
        )

        if self._learner_repository is None:
            self._learner_repository = StorageLearnerRepository(
                learning_storage,
            )

        if self._application_state is None:
            self._application_state = ApplicationStateStorage(
                learning_storage,
            )

        learning_repository = StorageLearningRepository(
            learning_storage,
        )

        self._learning_service = LearningService(
            learning_repository,
            self._learner_repository,
        )

        #
        # Restore an existing Active Learner, or establish one through
        # the initial Learner Setup flow.
        #

        self.restore_active_learner()
        self._ensure_active_learner()

        #
        # Create Main Window only after an Active Learner exists.
        #

        self._main_window = MainWindow(
            engine=self._engine,
            audio=self._audio,
            flashcard_session=self._flashcard_session,
            learning_service=self._learning_service,
            active_learner=self._active_learner,
        )

        self._initialized = True

    def run(self) -> None:
        """Show the main application window."""

        if not self._initialized:
            raise RuntimeError(
                "Application has not been initialized."
            )

        assert self._main_window is not None

        self._main_window.show()

    def shutdown(self) -> None:
        """Shut down the application lifecycle."""

        if not self._initialized:
            return

        self._initialized = False

    def _ensure_active_learner(self) -> None:
        """Establish an Active Learner when none was restored."""

        if self._active_learner is not None:
            return

        dialog = LearnerSetupDialog()

        if dialog.exec() != 1:
            raise RuntimeError(
                "Learner setup was cancelled before an Active Learner "
                "could be established."
            )

        setup_result = dialog.result()

        if setup_result is None:
            raise RuntimeError(
                "Learner setup completed without a result."
            )

        learner = self.activate_learner_from_setup(
            setup_result,
        )

        if learner is None:
            raise RuntimeError(
                "Learner setup did not establish an Active Learner."
            )

    def activate_learner_from_setup(
        self,
        setup_result: LearnerSetupResult,
    ) -> LearnerIdentity | None:
        """
        Translate a LearnerSetupResult into a LearnerIdentity and activate it.
        """

        if setup_result.mode is LearnerSetupMode.CANCELLED:
            return None

        if setup_result.mode is LearnerSetupMode.GUEST:
            learner = LearnerIdentity(
                learner_id=str(uuid4()),
                display_name="Guest",
                is_guest=True,
            )

        elif setup_result.mode is LearnerSetupMode.NAMED:
            if not setup_result.display_name:
                raise ValueError(
                    "Named learner setup requires a display name."
                )

            learner = LearnerIdentity(
                learner_id=str(uuid4()),
                display_name=setup_result.display_name,
                is_guest=False,
            )

        else:
            raise ValueError(
                f"Unsupported learner setup mode: {setup_result.mode!r}"
            )

        self.set_active_learner(
            learner,
        )

        return learner

    def set_active_learner(
        self,
        learner: LearnerIdentity,
    ) -> None:
        """Set, persist, and remember the Active Learner."""

        if self._learner_repository is None:
            raise RuntimeError(
                "Application learner repository is not initialized."
            )

        self._learner_repository.save_learner(
            learner,
        )

        self._active_learner = learner

        if self._application_state is not None:
            self._application_state.save(
                {
                    "active_learner_id": learner.learner_id,
                }
            )

    def restore_active_learner(self) -> None:
        """Restore the Active Learner from application state."""

        if self._application_state is None:
            self._active_learner = None
            return

        state = self._application_state.load()

        if not state:
            self._active_learner = None
            return

        learner_id = state.get("active_learner_id")

        if not learner_id:
            self._active_learner = None
            return

        if self._learner_repository is None:
            self._active_learner = None
            return

        learner = self._learner_repository.load_learner(
            learner_id,
        )

        self._active_learner = learner
