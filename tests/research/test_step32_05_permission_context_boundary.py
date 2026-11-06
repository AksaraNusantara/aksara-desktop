import unittest
from dataclasses import dataclass
from enum import Enum


class AdmissionDecision(Enum):
    ACCEPTED = "accepted"


class ExecutionPermission(Enum):
    GRANTED = "granted"
    NOT_GRANTED = "not_granted"


@dataclass(frozen=True)
class Observation:
    request_id: str
    context: str
    admission: AdmissionDecision
    permission: ExecutionPermission


class TestPermissionContextBoundary(unittest.TestCase):

    def test_same_request_can_have_different_permission_under_different_contexts(self):
        first = Observation(
            request_id="request-001",
            context="context-A",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        second = Observation(
            request_id="request-001",
            context="context-B",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(first.request_id, second.request_id)
        self.assertNotEqual(first.context, second.context)
        self.assertNotEqual(first.permission, second.permission)

    def test_admission_can_remain_stable_while_permission_changes(self):
        first = Observation(
            request_id="request-001",
            context="context-A",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        second = Observation(
            request_id="request-001",
            context="context-B",
            admission=AdmissionDecision.ACCEPTED,
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

    def test_request_identity_does_not_change_with_permission(self):
        first = Observation(
            request_id="request-001",
            context="context-A",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        second = Observation(
            request_id="request-001",
            context="context-B",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            first.request_id,
            second.request_id,
        )

    def test_permission_change_does_not_mutate_previous_observation(self):
        before = Observation(
            request_id="request-001",
            context="context-A",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        after = Observation(
            request_id="request-001",
            context="context-B",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            before.permission,
            ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            after.permission,
            ExecutionPermission.GRANTED,
        )

    def test_permission_can_be_observed_against_context(self):
        observations = [
            (
                "context-A",
                ExecutionPermission.NOT_GRANTED,
            ),
            (
                "context-B",
                ExecutionPermission.GRANTED,
            ),
        ]

        self.assertNotEqual(
            observations[0][0],
            observations[1][0],
        )

        self.assertNotEqual(
            observations[0][1],
            observations[1][1],
        )

    def test_same_admission_can_coexist_with_different_permissions(self):
        observations = [
            Observation(
                "request-001",
                "context-A",
                AdmissionDecision.ACCEPTED,
                ExecutionPermission.NOT_GRANTED,
            ),
            Observation(
                "request-001",
                "context-B",
                AdmissionDecision.ACCEPTED,
                ExecutionPermission.GRANTED,
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

    def test_permission_is_not_intrinsic_to_request_identity(self):
        permissions = {
            "request-001": {
                "context-A": ExecutionPermission.NOT_GRANTED,
                "context-B": ExecutionPermission.GRANTED,
            }
        }

        self.assertNotEqual(
            permissions["request-001"]["context-A"],
            permissions["request-001"]["context-B"],
        )

    def test_permission_is_not_intrinsic_to_admission_value(self):
        permissions = [
            (
                AdmissionDecision.ACCEPTED,
                "context-A",
                ExecutionPermission.NOT_GRANTED,
            ),
            (
                AdmissionDecision.ACCEPTED,
                "context-B",
                ExecutionPermission.GRANTED,
            ),
        ]

        self.assertEqual(
            permissions[0][0],
            permissions[1][0],
        )

        self.assertNotEqual(
            permissions[0][2],
            permissions[1][2],
        )

    def test_context_change_can_precede_permission_change(self):
        sequence = [
            ("context-A", ExecutionPermission.NOT_GRANTED),
            ("context-B", ExecutionPermission.GRANTED),
        ]

        self.assertNotEqual(
            sequence[0][0],
            sequence[1][0],
        )

        self.assertNotEqual(
            sequence[0][1],
            sequence[1][1],
        )

    def test_permission_change_does_not_imply_new_request(self):
        first_request = "request-001"
        second_request = "request-001"

        self.assertEqual(
            first_request,
            second_request,
        )

    def test_permission_change_does_not_imply_new_admission(self):
        first_admission = AdmissionDecision.ACCEPTED
        second_admission = AdmissionDecision.ACCEPTED

        self.assertEqual(
            first_admission,
            second_admission,
        )

    def test_granted_permission_remains_distinct_from_execution(self):
        observation = Observation(
            request_id="request-001",
            context="context-B",
            admission=AdmissionDecision.ACCEPTED,
            permission=ExecutionPermission.GRANTED,
        )

        execution_occurred = False

        self.assertEqual(
            observation.permission,
            ExecutionPermission.GRANTED,
        )

        self.assertFalse(execution_occurred)

    def test_context_can_change_without_request_change(self):
        first = "request-001"
        second = "request-001"

        self.assertEqual(first, second)

    def test_permission_is_context_dependent_in_this_experiment(self):
        first = Observation(
            "request-001",
            "context-A",
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
        )

        second = Observation(
            "request-001",
            "context-B",
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(first.context, second.context)
        self.assertNotEqual(first.permission, second.permission)


if __name__ == "__main__":
    unittest.main()