import unittest
from dataclasses import dataclass
from enum import Enum, auto


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
    capability: ExperimentalCapability
    state: ExperimentalExecutionState
    output: object = None
    non_execution_reason: ExperimentalNonExecutionReason = None
    failure: ExperimentalFailureClassification = None
    diagnostic: str = None


def execution_semantics(result):
    """
    Projection containing only execution-semantic information.

    Diagnostic is intentionally excluded.
    """
    return (
        result.capability,
        result.state,
        result.non_execution_reason,
        result.failure,
    )


class TestCapabilityDiagnosticIndependence(unittest.TestCase):

    def test_success_diagnostic_does_not_change_execution_semantics(self):
        result_without_diagnostic = ExperimentalExecutionResult(
            capability=ExperimentalCapability.TRANSLITERATION,
            state=ExperimentalExecutionState.SUCCESS,
            output="aksara",
        )

        result_with_diagnostic = ExperimentalExecutionResult(
            capability=ExperimentalCapability.TRANSLITERATION,
            state=ExperimentalExecutionState.SUCCESS,
            output="aksara",
            diagnostic="transliteration completed successfully",
        )

        self.assertEqual(
            execution_semantics(result_without_diagnostic),
            execution_semantics(result_with_diagnostic),
        )

        self.assertEqual(
            result_without_diagnostic.output,
            result_with_diagnostic.output,
        )

    def test_failed_diagnostic_does_not_change_failure_classification(self):
        result_without_diagnostic = ExperimentalExecutionResult(
            capability=ExperimentalCapability.AUDIO_PLAYBACK,
            state=ExperimentalExecutionState.FAILED,
            failure=ExperimentalFailureClassification.EXECUTION_ERROR,
        )

        result_with_diagnostic = ExperimentalExecutionResult(
            capability=ExperimentalCapability.AUDIO_PLAYBACK,
            state=ExperimentalExecutionState.FAILED,
            failure=ExperimentalFailureClassification.EXECUTION_ERROR,
            diagnostic="audio device unavailable",
        )

        self.assertEqual(
            execution_semantics(result_without_diagnostic),
            execution_semantics(result_with_diagnostic),
        )

    def test_not_executed_diagnostic_does_not_change_reason(self):
        result_without_diagnostic = ExperimentalExecutionResult(
            capability=ExperimentalCapability.PROGRESS_PERSISTENCE,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.PRECONDITION_NOT_MET
            ),
        )

        result_with_diagnostic = ExperimentalExecutionResult(
            capability=ExperimentalCapability.PROGRESS_PERSISTENCE,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.PRECONDITION_NOT_MET
            ),
            diagnostic="learner context was not initialized",
        )

        self.assertEqual(
            execution_semantics(result_without_diagnostic),
            execution_semantics(result_with_diagnostic),
        )

    def test_diagnostic_can_change_without_changing_semantics(self):
        result_a = ExperimentalExecutionResult(
            capability=ExperimentalCapability.TRANSLITERATION,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤ",
            diagnostic="path A",
        )

        result_b = ExperimentalExecutionResult(
            capability=ExperimentalCapability.TRANSLITERATION,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤ",
            diagnostic="path B",
        )

        self.assertNotEqual(
            result_a.diagnostic,
            result_b.diagnostic,
        )

        self.assertEqual(
            execution_semantics(result_a),
            execution_semantics(result_b),
        )

        self.assertEqual(
            result_a.output,
            result_b.output,
        )

    def test_diagnostic_is_not_required_for_any_execution_state(self):
        results = (
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.TRANSLITERATION,
                state=ExperimentalExecutionState.SUCCESS,
            ),
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.AUDIO_PLAYBACK,
                state=ExperimentalExecutionState.FAILED,
                failure=ExperimentalFailureClassification.EXECUTION_ERROR,
            ),
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.PROGRESS_PERSISTENCE,
                state=ExperimentalExecutionState.NOT_EXECUTED,
                non_execution_reason=(
                    ExperimentalNonExecutionReason.CAPABILITY_UNAVAILABLE
                ),
            ),
        )

        for result in results:
            self.assertIsNone(result.diagnostic)

    def test_diagnostic_does_not_define_execution_state(self):
        diagnostics = (
            "completed",
            "warning",
            "device unavailable",
            "precondition missing",
            "operation skipped",
        )

        for diagnostic in diagnostics:
            result = ExperimentalExecutionResult(
                capability=ExperimentalCapability.TRANSLITERATION,
                state=ExperimentalExecutionState.SUCCESS,
                output="ꦲ",
                diagnostic=diagnostic,
            )

            self.assertEqual(
                result.state,
                ExperimentalExecutionState.SUCCESS,
            )

    def test_same_diagnostic_can_accompany_different_states(self):
        diagnostic = "operation status information"

        success = ExperimentalExecutionResult(
            capability=ExperimentalCapability.TRANSLITERATION,
            state=ExperimentalExecutionState.SUCCESS,
            diagnostic=diagnostic,
        )

        failed = ExperimentalExecutionResult(
            capability=ExperimentalCapability.TRANSLITERATION,
            state=ExperimentalExecutionState.FAILED,
            failure=ExperimentalFailureClassification.EXECUTION_ERROR,
            diagnostic=diagnostic,
        )

        not_executed = ExperimentalExecutionResult(
            capability=ExperimentalCapability.TRANSLITERATION,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.PRECONDITION_NOT_MET
            ),
            diagnostic=diagnostic,
        )

        self.assertEqual(success.diagnostic, failed.diagnostic)
        self.assertEqual(failed.diagnostic, not_executed.diagnostic)

        self.assertNotEqual(success.state, failed.state)
        self.assertNotEqual(failed.state, not_executed.state)
        self.assertNotEqual(success.state, not_executed.state)


if __name__ == "__main__":
    unittest.main()