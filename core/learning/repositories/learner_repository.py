"""Dedicated learner identity persistence boundary (ADR-0003)."""

from abc import ABC, abstractmethod

from core.learning.models.learner_identity import LearnerIdentity
from core.learning.storage.storage_adapter import StorageAdapter


class LearnerRepository(ABC):
    """Persistence interface for LearnerIdentity."""

    @abstractmethod
    def save_learner(self, learner: LearnerIdentity) -> None:
        """Persist a learner; replace an existing learner with the same ID."""
        raise NotImplementedError

    @abstractmethod
    def load_learner(self, learner_id: str) -> LearnerIdentity | None:
        """Load one learner by stable learner ID."""
        raise NotImplementedError

    @abstractmethod
    def load_learners(self) -> list[LearnerIdentity]:
        """Load all learners; return [] when the store is empty."""
        raise NotImplementedError


class StorageLearnerRepository(LearnerRepository):
    """StorageAdapter-backed LearnerRepository implementation."""

    LEARNERS_KEY = "learners"

    def __init__(self, storage: StorageAdapter) -> None:
        self.storage = storage

    def save_learner(self, learner: LearnerIdentity) -> None:
        learners = self.storage.load(self.LEARNERS_KEY)

        if learners is None:
            learners = {}

        learners[learner.learner_id] = self._serialize_learner(learner)
        self.storage.save(self.LEARNERS_KEY, learners)

    def load_learner(self, learner_id: str) -> LearnerIdentity | None:
        learners = self.storage.load(self.LEARNERS_KEY)

        if learners is None:
            return None

        data = learners.get(learner_id)

        if data is None:
            return None

        return self._deserialize_learner(data)

    def load_learners(self) -> list[LearnerIdentity]:
        learners = self.storage.load(self.LEARNERS_KEY)

        if learners is None:
            return []

        return [
            self._deserialize_learner(data)
            for data in learners.values()
        ]

    @staticmethod
    def _serialize_learner(
        learner: LearnerIdentity,
    ) -> dict[str, object]:
        return {
            "learner_id": learner.learner_id,
            "display_name": learner.display_name,
            "is_guest": learner.is_guest,
        }

    @staticmethod
    def _deserialize_learner(
        data: dict[str, object],
    ) -> LearnerIdentity:
        return LearnerIdentity(
            learner_id=str(data["learner_id"]),
            display_name=str(data["display_name"]),
            is_guest=bool(data["is_guest"]),
        )
