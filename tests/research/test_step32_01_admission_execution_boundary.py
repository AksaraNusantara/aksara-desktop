import unittest
from enum import Enum
from dataclasses import dataclass


class AdmissionDecision(Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class PreExecutionCondition(Enum):
    READY = "ready"
    NOT_READY = "not_ready"


@dataclass(frozen=True)
class Scenario:
    admission: AdmissionDecision
    condition: PreExecutionCondition


class TestAdmissionExecutionBoundary(unittest.TestCase):

    def test_accepted_can_coexist_with_not_ready_condition(self):
        scenario = Scenario(
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.NOT_READY,
        )

        self.assertEqual(
            scenario.admission,
            AdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            scenario.condition,
            PreExecutionCondition.NOT_READY,
        )

    def test_accepted_can_coexist_with_ready_condition(self):
        scenario = Scenario(
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.READY,
        )

        self.assertEqual(
            scenario.admission,
            AdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            scenario.condition,
            PreExecutionCondition.READY,
        )

    def test_same_admission_can_have_different_conditions(self):
        ready = Scenario(
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.READY,
        )

        not_ready = Scenario(
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.NOT_READY,
        )

        self.assertEqual(
            ready.admission,
            not_ready.admission,
        )

        self.assertNotEqual(
            ready.condition,
            not_ready.condition,
        )

    def test_admission_and_condition_are_distinct_value_spaces(self):
        self.assertNotEqual(
            set(AdmissionDecision),
            set(PreExecutionCondition),
        )

    def test_condition_does_not_mean_execution_occurred(self):
        scenario = Scenario(
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.READY,
        )

        execution_occurred = False

        self.assertEqual(
            scenario.condition,
            PreExecutionCondition.READY,
        )

        self.assertFalse(execution_occurred)

    def test_accepted_does_not_mean_execution_occurred(self):
        scenario = Scenario(
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.NOT_READY,
        )

        execution_occurred = False

        self.assertEqual(
            scenario.admission,
            AdmissionDecision.ACCEPTED,
        )

        self.assertFalse(execution_occurred)

    def test_condition_can_be_observed_after_admission(self):
        observations = [
            ("admission", AdmissionDecision.ACCEPTED),
            ("condition", PreExecutionCondition.NOT_READY),
        ]

        self.assertEqual(
            observations[0][0],
            "admission",
        )

        self.assertEqual(
            observations[1][0],
            "condition",
        )

    def test_admission_and_condition_are_distinct_observations(self):
        admission_observation = (
            "admission",
            AdmissionDecision.ACCEPTED,
        )

        condition_observation = (
            "condition",
            PreExecutionCondition.NOT_READY,
        )

        self.assertNotEqual(
            admission_observation,
            condition_observation,
        )

    def test_condition_can_change_without_changing_admission(self):
        admission = AdmissionDecision.ACCEPTED

        first_condition = PreExecutionCondition.NOT_READY
        second_condition = PreExecutionCondition.READY

        self.assertEqual(
            admission,
            AdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            first_condition,
            second_condition,
        )

    def test_admission_remains_accepted_when_condition_changes(self):
        before = Scenario(
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.NOT_READY,
        )

        after = Scenario(
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.READY,
        )

        self.assertEqual(
            before.admission,
            AdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            after.admission,
            AdmissionDecision.ACCEPTED,
        )

    def test_ready_condition_does_not_mean_execution_occurred(self):
        scenario = Scenario(
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.READY,
        )

        execution_occurred = False

        self.assertEqual(
            scenario.condition,
            PreExecutionCondition.READY,
        )

        self.assertFalse(execution_occurred)

    def test_rejected_is_not_a_pre_execution_condition(self):
        scenario = Scenario(
            admission=AdmissionDecision.REJECTED,
            condition=PreExecutionCondition.NOT_READY,
        )

        self.assertEqual(
            scenario.admission,
            AdmissionDecision.REJECTED,
        )

        self.assertEqual(
            scenario.condition,
            PreExecutionCondition.NOT_READY,
        )

    def test_three_questions_remain_distinct(self):
        questions = [
            "Was the request admitted?",
            "Is the request currently ready for execution?",
            "Did execution actually occur?",
        ]

        self.assertEqual(len(questions), 3)
        self.assertEqual(len(set(questions)), 3)


if __name__ == "__main__":
    unittest.main()