import unittest
from dataclasses import dataclass
from enum import Enum


class AdmissionDecision(Enum):
    ACCEPTED = "accepted"


class PreExecutionCondition(Enum):
    READY = "ready"
    NOT_READY = "not_ready"


@dataclass(frozen=True)
class Observation:
    context: str
    admission: AdmissionDecision
    condition: PreExecutionCondition


class TestConditionChangeAdmissionStability(unittest.TestCase):

    def test_context_change_can_change_condition(self):
        before = Observation(
            context="resource_unavailable",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.NOT_READY,
        )

        after = Observation(
            context="resource_available",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.READY,
        )

        self.assertNotEqual(
            before.context,
            after.context,
        )

        self.assertNotEqual(
            before.condition,
            after.condition,
        )

    def test_admission_remains_accepted_after_context_change(self):
        before = Observation(
            context="resource_unavailable",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.NOT_READY,
        )

        after = Observation(
            context="resource_available",
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

    def test_condition_change_does_not_require_admission_change(self):
        first = Observation(
            context="A",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.NOT_READY,
        )

        second = Observation(
            context="B",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.READY,
        )

        self.assertEqual(
            first.admission,
            second.admission,
        )

        self.assertNotEqual(
            first.condition,
            second.condition,
        )

    def test_same_request_can_be_observed_under_different_contexts(self):
        request_id = "request-001"

        observations = [
            (request_id, "A", PreExecutionCondition.NOT_READY),
            (request_id, "B", PreExecutionCondition.READY),
        ]

        self.assertEqual(
            observations[0][0],
            observations[1][0],
        )

        self.assertNotEqual(
            observations[0][1],
            observations[1][1],
        )

    def test_condition_is_context_sensitive_in_this_model(self):
        first = Observation(
            context="A",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.NOT_READY,
        )

        second = Observation(
            context="B",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.READY,
        )

        self.assertNotEqual(first.context, second.context)
        self.assertNotEqual(first.condition, second.condition)

    def test_admission_is_not_derived_from_condition(self):
        ready = Observation(
            context="ready_context",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.READY,
        )

        not_ready = Observation(
            context="blocked_context",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.NOT_READY,
        )

        self.assertEqual(
            ready.admission,
            not_ready.admission,
        )

    def test_condition_change_does_not_mutate_previous_observation(self):
        before = Observation(
            context="A",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.NOT_READY,
        )

        after = Observation(
            context="B",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.READY,
        )

        self.assertEqual(
            before.condition,
            PreExecutionCondition.NOT_READY,
        )

        self.assertEqual(
            after.condition,
            PreExecutionCondition.READY,
        )

    def test_observations_can_represent_temporal_change(self):
        observations = [
            Observation(
                context="A",
                admission=AdmissionDecision.ACCEPTED,
                condition=PreExecutionCondition.NOT_READY,
            ),
            Observation(
                context="B",
                admission=AdmissionDecision.ACCEPTED,
                condition=PreExecutionCondition.READY,
            ),
        ]

        self.assertEqual(len(observations), 2)

        self.assertEqual(
            observations[0].admission,
            observations[1].admission,
        )

        self.assertNotEqual(
            observations[0].condition,
            observations[1].condition,
        )

    def test_condition_does_not_define_admission_identity(self):
        admission_id = "admission-001"

        first_condition = PreExecutionCondition.NOT_READY
        second_condition = PreExecutionCondition.READY

        self.assertNotEqual(
            first_condition,
            second_condition,
        )

        self.assertEqual(
            admission_id,
            "admission-001",
        )

    def test_ready_does_not_imply_new_admission(self):
        first = Observation(
            context="A",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.NOT_READY,
        )

        second = Observation(
            context="B",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.READY,
        )

        self.assertEqual(
            first.admission,
            second.admission,
        )

    def test_not_ready_does_not_imply_rejection(self):
        observation = Observation(
            context="blocked",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.NOT_READY,
        )

        self.assertEqual(
            observation.admission,
            AdmissionDecision.ACCEPTED,
        )

    def test_ready_does_not_imply_execution(self):
        observation = Observation(
            context="ready",
            admission=AdmissionDecision.ACCEPTED,
            condition=PreExecutionCondition.READY,
        )

        execution_occurred = False

        self.assertEqual(
            observation.condition,
            PreExecutionCondition.READY,
        )

        self.assertFalse(execution_occurred)

    def test_condition_change_is_distinct_from_admission_reconsideration(self):
        condition_change = (
            PreExecutionCondition.NOT_READY,
            PreExecutionCondition.READY,
        )

        admission_reconsideration = (
            AdmissionDecision.ACCEPTED,
            AdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            condition_change,
            admission_reconsideration,
        )


if __name__ == "__main__":
    unittest.main()