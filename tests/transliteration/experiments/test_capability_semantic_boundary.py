# -*- coding: utf-8 -*-
"""
AD-TR-01 — Phase 2E-5 — Step 17
Experiment 17-3 — Capability Semantic Boundary

Architecture probe only.

This experiment MUST NOT import or modify production code.
"""

import unittest
from dataclasses import dataclass
from enum import Enum, auto


# ============================================================
# Experimental Capability Categories
# ============================================================


class ExperimentalCapabilityType(Enum):
    TRANSFORMATION = auto()
    ACTION = auto()
    PERSISTENCE = auto()
    QUERY = auto()
    DISCOVERY = auto()


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
    Generic execution-result probe model.

    This is NOT a production API.
    """

    capability_type: ExperimentalCapabilityType
    state: ExperimentalExecutionState
    output: object = None
    non_execution_reason: ExperimentalNonExecutionReason = None
    failure: ExperimentalFailureClassification = None
    diagnostic: str = None


# ============================================================
# Capability Classification
# ============================================================


EXECUTABLE_CAPABILITIES = (
    ExperimentalCapabilityType.TRANSFORMATION,
    ExperimentalCapabilityType.ACTION,
    ExperimentalCapabilityType.PERSISTENCE,
)

OBSERVATIONAL_CAPABILITIES = (
    ExperimentalCapabilityType.QUERY,
    ExperimentalCapabilityType.DISCOVERY,
)


# ============================================================
# Experiment 17-3
# ============================================================


class TestCapabilitySemanticBoundary(unittest.TestCase):

    def test_transformation_capability_supports_execution_model(self):
        """
        A transformation capability naturally represents an
        operation that starts and produces an output.
        """

        result = ExperimentalExecutionResult(
            capability_type=ExperimentalCapabilityType.TRANSFORMATION,
            state=ExperimentalExecutionState.SUCCESS,
            output="transformed-value",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertIsNotNone(result.output)
        self.assertIsNone(result.failure)
        self.assertIsNone(result.non_execution_reason)

    def test_action_capability_supports_execution_model(self):
        """
        An action capability naturally represents an operation
        that starts and completes.
        """

        result = ExperimentalExecutionResult(
            capability_type=ExperimentalCapabilityType.ACTION,
            state=ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

    def test_persistence_capability_supports_execution_model(self):
        """
        A persistence capability naturally represents an operation
        whose execution can succeed or fail.
        """

        result = ExperimentalExecutionResult(
            capability_type=ExperimentalCapabilityType.PERSISTENCE,
            state=ExperimentalExecutionState.SUCCESS,
            output="saved",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

    def test_executable_capabilities_share_same_state_semantics(self):
        """
        Transformation, action, and persistence capabilities
        can share the same execution-state semantics.
        """

        for capability_type in EXECUTABLE_CAPABILITIES:
            with self.subTest(capability_type=capability_type):

                success = ExperimentalExecutionResult(
                    capability_type=capability_type,
                    state=ExperimentalExecutionState.SUCCESS,
                )

                failed = ExperimentalExecutionResult(
                    capability_type=capability_type,
                    state=ExperimentalExecutionState.FAILED,
                    failure=(
                        ExperimentalFailureClassification.EXECUTION_ERROR
                    ),
                )

                not_executed = ExperimentalExecutionResult(
                    capability_type=capability_type,
                    state=ExperimentalExecutionState.NOT_EXECUTED,
                    non_execution_reason=(
                        ExperimentalNonExecutionReason.PRECONDITION_NOT_MET
                    ),
                )

                self.assertEqual(
                    success.state,
                    ExperimentalExecutionState.SUCCESS,
                )

                self.assertEqual(
                    failed.state,
                    ExperimentalExecutionState.FAILED,
                )

                self.assertEqual(
                    not_executed.state,
                    ExperimentalExecutionState.NOT_EXECUTED,
                )

    def test_query_can_be_modeled_as_an_execution(self):
        """
        Probe whether a query operation can still have an
        execution lifecycle.

        A query may execute work even though its purpose is
        observational/read-oriented.
        """

        result = ExperimentalExecutionResult(
            capability_type=ExperimentalCapabilityType.QUERY,
            state=ExperimentalExecutionState.SUCCESS,
            output="lookup-result",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            result.output,
            "lookup-result",
        )

    def test_discovery_can_be_modeled_as_an_execution(self):
        """
        Capability discovery may itself be an executable operation:
        the system performs a discovery request and produces a result.
        """

        result = ExperimentalExecutionResult(
            capability_type=ExperimentalCapabilityType.DISCOVERY,
            state=ExperimentalExecutionState.SUCCESS,
            output="capability-list",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            result.output,
            "capability-list",
        )

    def test_observational_capabilities_do_not_automatically_escape_execution_model(
        self,
    ):
        """
        Query/discovery semantics do not automatically invalidate
        the execution-result model.

        Their purpose may be observational, while the operation
        itself can still execute.
        """

        for capability_type in OBSERVATIONAL_CAPABILITIES:
            with self.subTest(capability_type=capability_type):

                result = ExperimentalExecutionResult(
                    capability_type=capability_type,
                    state=ExperimentalExecutionState.SUCCESS,
                    output="observed-result",
                )

                self.assertEqual(
                    result.state,
                    ExperimentalExecutionState.SUCCESS,
                )

    def test_non_execution_remains_meaningful_for_any_capability_type(
        self,
    ):
        """
        Even an observational/query-oriented capability can be
        NOT_EXECUTED if the operation was never started.
        """

        for capability_type in (
            ExperimentalCapabilityType.TRANSFORMATION,
            ExperimentalCapabilityType.ACTION,
            ExperimentalCapabilityType.PERSISTENCE,
            ExperimentalCapabilityType.QUERY,
            ExperimentalCapabilityType.DISCOVERY,
        ):
            with self.subTest(capability_type=capability_type):

                result = ExperimentalExecutionResult(
                    capability_type=capability_type,
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

                self.assertIsNone(result.failure)


if __name__ == "__main__":
    unittest.main()