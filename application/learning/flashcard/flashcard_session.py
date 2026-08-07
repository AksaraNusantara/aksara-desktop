"""
Flashcard learning session.

This module contains the session logic used by the Flashcard
module. The session is responsible for navigating characters
provided by the Core Engine while remaining independent from
the user interface.

---

#
# TODO
#
# start()
# reset()
# current()
# next()
# previous()
# has_next()
# has_previous()
# count()
# index()
#
"""

from __future__ import annotations

from core.engine import CoreEngine


class FlashcardSession:
    """
    Manage a Flashcard learning session.
    """

    def __init__(
        self,
        engine: CoreEngine,
    ) -> None:
        """
        Initialize a Flashcard session.

        Parameters
        ----------
        engine:
            Shared Core Engine instance.
        """

        self._engine = engine

        self._characters: list[dict] = []

        self._current_index = 0