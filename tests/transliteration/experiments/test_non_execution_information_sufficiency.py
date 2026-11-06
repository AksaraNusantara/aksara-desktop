import unittest
from enum import Enum


class ExecutionState(Enum):
    NOT_EXECUTED = "not_executed"
    SUCCESS = "success"
    FAILED = "failed"


class NonExecutionReason(Enum):
    PRECONDITION_NOT_MET = "precondition_not_met"
    EXECUTION_BLOCKED = "execution_blocked"
    UNKNOWN = "unknown"


class ExecutionResult:
    def __init__(
        self,
        state,
        non_execution_reason=None,
    ):
        self.state = state
        self.non_execution_reason = non_execution_reason


class InformationAssessment:

    @staticmethod
    def what_happened(result):
        if result.state == ExecutionState.NOT_EXECUTED:
            return "execution_did_not_start"

        if result.state == ExecutionState.SUCCESS:
            return "execution_succeeded"

        if result.state == ExecutionState.FAILED:
            return "execution_failed"

        return "unknown"

    @staticmethod
    def why_it_happened(result):
        if result.state != ExecutionState.NOT_EXECUTED:
            return "not_applicable"

        if result.non_execution_reason is None:
            return "reason_not_available"

        if result.non_execution_reason == NonExecutionReason.UNKNOWN:
            return "reason_unknown"

        return result.non_execution_reason.value


class TestNonExecutionInformationSufficiency(unittest.TestCase):

    def test_not_executed_always_answers_what_happened(self):
        results = [
            ExecutionResult(
                ExecutionState.NOT_EXECUTED,
                NonExecutionReason.PRECONDITION_NOT_MET,
            ),
            ExecutionResult(
                ExecutionState.NOT_EXECUTED,
                NonExecutionReason.EXECUTION_BLOCKED,
            ),
            ExecutionResult(
                ExecutionState.NOT_EXECUTED,
                NonExecutionReason.UNKNOWN,
            ),
            ExecutionResult(
                ExecutionState.NOT_EXECUTED,
                None,
            ),
        ]

        for result in results:
            self.assertEqual(
                InformationAssessment.what_happened(result),
                "execution_did_not_start",
            )

    def test_known_reason_answers_why(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.PRECONDITION_NOT_MET,
        )

        self.assertEqual(
            InformationAssessment.why_it_happened(result),
            "precondition_not_met",
        )

    def test_another_known_reason_answers_why(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.EXECUTION_BLOCKED,
        )

        self.assertEqual(
            InformationAssessment.why_it_happened(result),
            "execution_blocked",
        )

    def test_unknown_reason_answers_why_at_knowledge_level(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.UNKNOWN,
        )

        self.assertEqual(
            InformationAssessment.why_it_happened(result),
            "reason_unknown",
        )

    def test_none_reports_reason_not_available(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            None,
        )

        self.assertEqual(
            InformationAssessment.why_it_happened(result),
            "reason_not_available",
        )

    def test_none_does_not_change_execution_state_information(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            None,
        )

        self.assertEqual(
            InformationAssessment.what_happened(result),
            "execution_did_not_start",
        )

    def test_unknown_does_not_change_execution_state_information(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.UNKNOWN,
        )

        self.assertEqual(
            InformationAssessment.what_happened(result),
            "execution_did_not_start",
        )

    def test_reason_is_additional_information_not_execution_state(self):
        known = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.PRECONDITION_NOT_MET,
        )

        unknown = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.UNKNOWN,
        )

        none = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            None,
        )

        self.assertEqual(
            InformationAssessment.what_happened(known),
            InformationAssessment.what_happened(unknown),
        )

        self.assertEqual(
            InformationAssessment.what_happened(unknown),
            InformationAssessment.what_happened(none),
        )

    def test_absent_reason_does_not_make_not_executed_ambiguous(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            None,
        )

        self.assertEqual(
            InformationAssessment.what_happened(result),
            "execution_did_not_start",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)