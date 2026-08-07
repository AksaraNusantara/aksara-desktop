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

    def start(
        self,
    ) -> None:
        """
        Start a new Flashcard session.
        """

        self._characters = (
            self._engine.get_characters()
        )

        self._current_index = 0

    def reset(
        self,
    ) -> None:
        """
        Reset the Flashcard session.
        """

        self._current_index = 0

    def reset(
        self,
    ) -> None:
        """
        Reset the Flashcard session.
        """

        self._current_index = 0

    def current(
        self,
    ) -> dict:
        """
        Return the current character.

        Returns
        -------
        dict
            Current character.
        """

        return self._characters[
            self._current_index
        ]
    
    def count(
        self,
    ) -> int:
        """
        Return the number of characters
        in the current session.
        """

        return len(
            self._characters
        )

    def index(
        self,
    ) -> int:
        """
        Return the current character index.
        """

        return self._current_index

    def has_next(
        self,
    ) -> bool:
        """
        Return whether another character
        exists after the current one.
        """

        return (
            self._current_index
            < len(self._characters) - 1
        )

    def has_previous(
        self,
    ) -> bool:
        """
        Return whether another character
        exists before the current one.
        """

        return (
            self._current_index > 0
        )

    def next(
        self,
    ) -> bool:
        """
        Move to the next character.

        Returns
        -------
        bool
            True if the current character
            changed.
        """

        if not self.has_next():
            return False

        self._current_index += 1

        return True

    def previous(
        self,
    ) -> bool:
        """
        Move to the previous character.

        Returns
        -------
        bool
            True if the current character
            changed.
        """

        if not self.has_previous():
            return False

        self._current_index -= 1

        return True

