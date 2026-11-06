# -*- coding: utf-8 -*-
"""
AD-TR-01 — Phase 2E-5 — Step 17
Experiment 17-1 — Cross-Capability Result Matrix

Architecture probe only.

This experiment MUST NOT import or modify production code.
"""

import unittest
from dataclasses import dataclass
from enum import Enum, auto


# ============================================================
# Experimental Vocabulary
# ============================================================


class ExperimentalCapability(Enum):
    TRANSLITERATION = auto()
    AUDIO_PLAYBACK = auto()
    PROGRESS_PERSISTENCE = auto()


class ExperimentalExecutionState(Enum):
    SUCCESS = auto()
    FAILED = auto()
    NOT_EXECUTED = auto()


class ExperimentalNonExecutionReason(Enum):
    CAPABILITY_UNAVAILABLE = auto()
    PRECONDITION_NOT_MET = auto()


class ExperimentalFailureClassification(Enum):
    EXECUTION_ERROR = auto()


@dataclass(frozen=True)
class ExperimentalExecutionResult:
    """
    Minimal experimental result model.

    This is intentionally NOT a production API.
    """

    capability: ExperimentalCapability
    state: ExperimentalExecutionState
    output: object = None
    non_execution_reason: ExperimentalNonExecutionReason = None
    failure: ExperimentalFailureClassification = None
    diagnostic: str = None


# ============================================================
# Experimental Fixtures
# ============================================================


CAPABILITIES = (
    ExperimentalCapability.TRANSLITERATION,
    ExperimentalCapability.AUDIO_PLAYBACK,
    ExperimentalCapability.PROGRESS_PERSISTENCE,
)


# ============================================================
# Experiment 17-1
# ============================================================


class TestCrossCapabilityResultMatrix(unittest.TestCase):

    def test_success_is_capability_independent(self):
        """
        SUCCESS should be meaningful for every capability.
        """

        for capability in CAPABILITIES:
            with self.subTest(capability=capability):
                result = ExperimentalExecutionResult(
                    capability=capability,
                    state=ExperimentalExecutionState.SUCCESS,
                    output="synthetic-output",
                )

                self.assertEqual(
                    result.state,
                    ExperimentalExecutionState.SUCCESS,
                )

                self.assertIsNone(result.non_execution_reason)
                self.assertIsNone(result.failure)

    def test_capability_unavailable_is_non_execution(self):
        """
        CAPABILITY_UNAVAILABLE should describe an operation
        that never started because the capability was unavailable.
        """

        for capability in CAPABILITIES:
            with self.subTest(capability=capability):
                result = ExperimentalExecutionResult(
                    capability=capability,
                    state=ExperimentalExecutionState.NOT_EXECUTED,
                    non_execution_reason=(
                        ExperimentalNonExecutionReason.CAPABILITY_UNAVAILABLE
                    ),
                )

                self.assertEqual(
                    result.state,
                    ExperimentalExecutionState.NOT_EXECUTED,
                )

                self.assertEqual(
                    result.non_execution_reason,
                    ExperimentalNonExecutionReason.CAPABILITY_UNAVAILABLE,
                )

                self.assertIsNone(result.failure)

    def test_precondition_failure_is_non_execution(self):
        """
        PRECONDITION_NOT_MET should describe an operation
        that never started because a required precondition
        was not satisfied.
        """

        for capability in CAPABILITIES:
            with self.subTest(capability=capability):
                result = ExperimentalExecutionResult(
                    capability=capability,
                    state=ExperimentalExecutionState.NOT_EXECUTED,
                    non_execution_reason=(
                        ExperimentalNonExecutionReason.PRECONDITION_NOT_MET
                    ),
                )

                self.assertEqual(
                    result.state,
                    ExperimentalExecutionState.NOT_EXECUTED,
                )

                self.assertEqual(
                    result.non_execution_reason,
                    ExperimentalNonExecutionReason.PRECONDITION_NOT_MET,
                )

                self.assertIsNone(result.failure)

    def test_execution_error_requires_execution_to_have_started(self):
        """
        EXECUTION_ERROR belongs to FAILED rather than
        NOT_EXECUTED.
        """

        for capability in CAPABILITIES:
            with self.subTest(capability=capability):
                result = ExperimentalExecutionResult(
                    capability=capability,
                    state=ExperimentalExecutionState.FAILED,
                    failure=(
                        ExperimentalFailureClassification.EXECUTION_ERROR
                    ),
                )

                self.assertEqual(
                    result.state,
                    ExperimentalExecutionState.FAILED,
                )

                self.assertIsNone(result.non_execution_reason)

                self.assertEqual(
                    result.failure,
                    ExperimentalFailureClassification.EXECUTION_ERROR,
                )

    def test_not_executed_and_failed_are_semantically_distinct(self):
        """
        NOT_EXECUTED and FAILED represent different execution histories.
        """

        for capability in CAPABILITIES:
            with self.subTest(capability=capability):

                not_executed = ExperimentalExecutionResult(
                    capability=capability,
                    state=ExperimentalExecutionState.NOT_EXECUTED,
                    non_execution_reason=(
                        ExperimentalNonExecutionReason.PRECONDITION_NOT_MET
                    ),
                )

                failed = ExperimentalExecutionResult(
                    capability=capability,
                    state=ExperimentalExecutionState.FAILED,
                    failure=(
                        ExperimentalFailureClassification.EXECUTION_ERROR
                    ),
                )

                self.assertNotEqual(
                    not_executed.state,
                    failed.state,
                )

                self.assertIsNotNone(
                    not_executed.non_execution_reason
                )

                self.assertIsNone(
                    not_executed.failure
                )

                self.assertIsNone(
                    failed.non_execution_reason
                )

                self.assertIsNotNone(
                    failed.failure
                )


if __name__ == "__main__":
    unittest.main()