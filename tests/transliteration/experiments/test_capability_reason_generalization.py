# -*- coding: utf-8 -*-
"""
AD-TR-01 — Phase 2E-5 — Step 17
Experiment 17-2 — Reason Semantics Transfer

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
    EXECUTION_BLOCKED = auto()
    REQUEST_CANCELLED = auto()


class ExperimentalFailureClassification(Enum):
    EXECUTION_ERROR = auto()


@dataclass(frozen=True)
class ExperimentalExecutionResult:
    capability: ExperimentalCapability
    state: ExperimentalExecutionState
    output: object = None
    non_execution_reason: ExperimentalNonExecutionReason = None
    failure: ExperimentalFailureClassification = None
    diagnostic: str = None


# ============================================================
# Semantic Test Cases
# ============================================================


CAPABILITIES = (
    ExperimentalCapability.TRANSLITERATION,
    ExperimentalCapability.AUDIO_PLAYBACK,
    ExperimentalCapability.PROGRESS_PERSISTENCE,
)


NON_EXECUTION_REASONS = (
    ExperimentalNonExecutionReason.CAPABILITY_UNAVAILABLE,
    ExperimentalNonExecutionReason.PRECONDITION_NOT_MET,
    ExperimentalNonExecutionReason.EXECUTION_BLOCKED,
    ExperimentalNonExecutionReason.REQUEST_CANCELLED,
)


# ============================================================
# Experiment 17-2
# ============================================================


class TestCapabilityReasonGeneralization(unittest.TestCase):

    def test_all_reasons_produce_not_executed_state(self):
        """
        Every candidate NonExecutionReason must represent
        an execution that did not begin.
        """

        for capability in CAPABILITIES:
            for reason in NON_EXECUTION_REASONS:
                with self.subTest(
                    capability=capability,
                    reason=reason,
                ):
                    result = ExperimentalExecutionResult(
                        capability=capability,
                        state=ExperimentalExecutionState.NOT_EXECUTED,
                        non_execution_reason=reason,
                    )

                    self.assertEqual(
                        result.state,
                        ExperimentalExecutionState.NOT_EXECUTED,
                    )

                    self.assertEqual(
                        result.non_execution_reason,
                        reason,
                    )

                    self.assertIsNone(result.failure)

    def test_capability_unavailable_is_domain_independent(self):
        """
        CAPABILITY_UNAVAILABLE retains the same semantic:
        the requested capability cannot perform the operation,
        therefore execution does not begin.
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

                self.assertIs(
                    result.non_execution_reason,
                    ExperimentalNonExecutionReason.CAPABILITY_UNAVAILABLE,
                )

    def test_precondition_not_met_is_domain_independent(self):
        """
        PRECONDITION_NOT_MET retains the same semantic:
        a condition required before execution was not satisfied.
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

                self.assertIs(
                    result.non_execution_reason,
                    ExperimentalNonExecutionReason.PRECONDITION_NOT_MET,
                )

    def test_execution_blocked_requires_pre_execution_interpretation(self):
        """
        EXECUTION_BLOCKED is accepted only when 'blocked' means
        execution was prevented from beginning.
        """

        for capability in CAPABILITIES:
            with self.subTest(capability=capability):
                result = ExperimentalExecutionResult(
                    capability=capability,
                    state=ExperimentalExecutionState.NOT_EXECUTED,
                    non_execution_reason=(
                        ExperimentalNonExecutionReason.EXECUTION_BLOCKED
                    ),
                )

                self.assertEqual(
                    result.state,
                    ExperimentalExecutionState.NOT_EXECUTED,
                )

                self.assertIs(
                    result.non_execution_reason,
                    ExperimentalNonExecutionReason.EXECUTION_BLOCKED,
                )

                self.assertIsNone(result.failure)

    def test_request_cancelled_requires_pre_execution_interpretation(self):
        """
        REQUEST_CANCELLED is treated as a NonExecutionReason only
        when cancellation occurs before execution begins.
        """

        for capability in CAPABILITIES:
            with self.subTest(capability=capability):
                result = ExperimentalExecutionResult(
                    capability=capability,
                    state=ExperimentalExecutionState.NOT_EXECUTED,
                    non_execution_reason=(
                        ExperimentalNonExecutionReason.REQUEST_CANCELLED
                    ),
                )

                self.assertEqual(
                    result.state,
                    ExperimentalExecutionState.NOT_EXECUTED,
                )

                self.assertIs(
                    result.non_execution_reason,
                    ExperimentalNonExecutionReason.REQUEST_CANCELLED,
                )

                self.assertIsNone(result.failure)

    def test_post_execution_cancellation_is_not_non_execution(self):
        """
        Important boundary probe:

        Cancellation after execution has already started must NOT
        automatically be classified as NOT_EXECUTED.
        """

        for capability in CAPABILITIES:
            with self.subTest(capability=capability):
                result = ExperimentalExecutionResult(
                    capability=capability,
                    state=ExperimentalExecutionState.FAILED,
                    failure=(
                        ExperimentalFailureClassification.EXECUTION_ERROR
                    ),
                    diagnostic="execution cancelled after start",
                )

                self.assertEqual(
                    result.state,
                    ExperimentalExecutionState.FAILED,
                )

                self.assertIsNone(result.non_execution_reason)

                self.assertIsNotNone(result.failure)


if __name__ == "__main__":
    unittest.main()