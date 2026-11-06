import unittest
from dataclasses import dataclass
from enum import Enum


class AdmissionDecision(Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ExecutionPermission(Enum):
    GRANTED = "granted"
    NOT_GRANTED = "not_granted"


@dataclass(frozen=True)
class Observation:
    request_id: str
    admission: AdmissionDecision
    permission: ExecutionPermission


class TestPermissionVsAdmissionReconsideration(unittest.TestCase):

    def test_permission_can_change_while_admission_remains_accepted(self):
        before = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        after = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            before.admission,
            after.admission,
        )

        self.assertNotEqual(
            before.permission,
            after.permission,
        )

    def test_permission_change_does_not_require_admission_reconsideration(self):
        before = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        after = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            before.admission,
            after.admission,
        )

    def test_admission_can_be_reconsidered_while_permission_remains_granted(self):
        before = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.GRANTED,
        )

        after = Observation(
            request_id="request-001",
            admission=AdmissionDecision.REJECTED,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(
            before.admission,
            after.admission,
        )

        self.assertEqual(
            before.permission,
            after.permission,
        )

    def test_admission_reconsideration_does_not_require_permission_change(self):
        before = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.GRANTED,
        )

        after = Observation(
            request_id="request-001",
            admission=AdmissionDecision.REJECTED,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(
            before.admission,
            after.admission,
        )

        self.assertEqual(
            before.permission,
            after.permission,
        )

    def test_request_identity_remains_stable_during_permission_change(self):
        before = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        after = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            before.request_id,
            after.request_id,
        )

    def test_request_identity_remains_stable_during_admission_reconsideration(self):
        before = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.GRANTED,
        )

        after = Observation(
            request_id="request-001",
            admission=AdmissionDecision.REJECTED,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            before.request_id,
            after.request_id,
        )

    def test_permission_change_and_admission_reconsideration_are_distinct_changes(self):
        permission_change = (
            ExecutionPermission.NOT_GRANTED,
            ExecutionPermission.GRANTED,
        )

        admission_change = (
            AdmissionDecision.ACCEPTED,
            AdmissionDecision.REJECTED,
        )

        self.assertNotEqual(
            permission_change,
            admission_change,
        )

    def test_permission_can_change_without_creating_new_request(self):
        request_id_before = "request-001"
        request_id_after = "request-001"

        self.assertEqual(
            request_id_before,
            request_id_after,
        )

    def test_admission_reconsideration_can_occur_without_creating_new_request(self):
        request_id_before = "request-001"
        request_id_after = "request-001"

        self.assertEqual(
            request_id_before,
            request_id_after,
        )

    def test_permission_observation_is_not_admission_observation(self):
        permission_observation = (
            "permission",
            ExecutionPermission.GRANTED,
        )

        admission_observation = (
            "admission",
            AdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            permission_observation,
            admission_observation,
        )

    def test_admission_reconsideration_does_not_define_permission_semantics(self):
        first = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.GRANTED,
        )

        second = Observation(
            request_id="request-001",
            admission=AdmissionDecision.REJECTED,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            first.permission,
            second.permission,
        )

    def test_permission_change_does_not_define_admission_semantics(self):
        first = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        second = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            first.admission,
            second.admission,
        )

    def test_both_changes_can_occur_in_separate_observations(self):
        observations = [
            Observation(
                request_id="request-001",
                admission=AdmissionDecision.ACCEPTED,
                permission=ExecutionPermission.NOT_GRANTED,
            ),
            Observation(
                request_id="request-001",
                admission=AdmissionDecision.ACCEPTED,
                permission=ExecutionPermission.GRANTED,
            ),
            Observation(
                request_id="request-001",
                admission=AdmissionDecision.REJECTED,
                permission=ExecutionPermission.GRANTED,
            ),
        ]

        self.assertEqual(
            observations[0].admission,
            observations[1].admission,
        )

        self.assertNotEqual(
            observations[0].permission,
            observations[1].permission,
        )

        self.assertNotEqual(
            observations[1].admission,
            observations[2].admission,
        )

        self.assertEqual(
            observations[1].permission,
            observations[2].permission,
        )

    def test_permission_and_admission_have_independent_change_axes(self):
        first = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        second = Observation(
            request_id="request-001",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.GRANTED,
        )

        third = Observation(
            request_id="request-001",
            admission=AdmissionDecision.REJECTED,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            first.admission,
            second.admission,
        )

        self.assertNotEqual(
            first.permission,
            second.permission,
        )

        self.assertNotEqual(
            second.admission,
            third.admission,
        )

        self.assertEqual(
            second.permission,
            third.permission,
        )


if __name__ == "__main__":
    unittest.main()