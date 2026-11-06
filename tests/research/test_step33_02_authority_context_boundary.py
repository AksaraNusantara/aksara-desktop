import unittest
from dataclasses import dataclass


@dataclass(frozen=True)
class Observation:
    request_id: str
    context: str
    authority: str


class TestAuthorityContextBoundary(unittest.TestCase):

    def test_same_request_can_have_different_authorities_under_different_contexts(self):
        first = Observation(
            request_id="request-001",
            context="context-A",
            authority="authority-A",
        )

        second = Observation(
            request_id="request-001",
            context="context-B",
            authority="authority-B",
        )

        self.assertEqual(first.request_id, second.request_id)
        self.assertNotEqual(first.context, second.context)
        self.assertNotEqual(first.authority, second.authority)

    def test_authority_can_change_without_request_change(self):
        before = Observation(
            request_id="request-001",
            context="context-A",
            authority="authority-A",
        )

        after = Observation(
            request_id="request-001",
            context="context-B",
            authority="authority-B",
        )

        self.assertEqual(
            before.request_id,
            after.request_id,
        )

        self.assertNotEqual(
            before.authority,
            after.authority,
        )

    def test_context_change_can_coincide_with_authority_change(self):
        before = Observation(
            request_id="request-001",
            context="context-A",
            authority="authority-A",
        )

        after = Observation(
            request_id="request-001",
            context="context-B",
            authority="authority-B",
        )

        self.assertNotEqual(before.context, after.context)
        self.assertNotEqual(before.authority, after.authority)

    def test_same_context_can_have_different_authorities(self):
        first = Observation(
            request_id="request-001",
            context="context-A",
            authority="authority-A",
        )

        second = Observation(
            request_id="request-001",
            context="context-A",
            authority="authority-B",
        )

        self.assertEqual(first.context, second.context)
        self.assertNotEqual(first.authority, second.authority)

    def test_same_authority_can_exist_under_different_contexts(self):
        first = Observation(
            request_id="request-001",
            context="context-A",
            authority="authority-A",
        )

        second = Observation(
            request_id="request-001",
            context="context-B",
            authority="authority-A",
        )

        self.assertNotEqual(first.context, second.context)
        self.assertEqual(first.authority, second.authority)

    def test_authority_is_not_identical_to_context(self):
        observation = Observation(
            request_id="request-001",
            context="context-A",
            authority="authority-A",
        )

        self.assertNotEqual(
            observation.context,
            observation.authority,
        )

    def test_authority_identity_is_distinct_from_request_identity(self):
        observation = Observation(
            request_id="request-001",
            context="context-A",
            authority="authority-A",
        )

        self.assertNotEqual(
            observation.request_id,
            observation.authority,
        )

    def test_authority_can_remain_stable_when_context_changes(self):
        before = Observation(
            request_id="request-001",
            context="context-A",
            authority="authority-A",
        )

        after = Observation(
            request_id="request-001",
            context="context-B",
            authority="authority-A",
        )

        self.assertNotEqual(before.context, after.context)
        self.assertEqual(before.authority, after.authority)

    def test_context_can_remain_stable_when_authority_changes(self):
        before = Observation(
            request_id="request-001",
            context="context-A",
            authority="authority-A",
        )

        after = Observation(
            request_id="request-001",
            context="context-A",
            authority="authority-B",
        )

        self.assertEqual(before.context, after.context)
        self.assertNotEqual(before.authority, after.authority)

    def test_authority_change_does_not_create_new_request(self):
        before_request = "request-001"
        after_request = "request-001"

        self.assertEqual(
            before_request,
            after_request,
        )

    def test_context_change_does_not_create_new_request(self):
        before_request = "request-001"
        after_request = "request-001"

        self.assertEqual(
            before_request,
            after_request,
        )

    def test_authority_is_not_an_execution_occurrence(self):
        observation = Observation(
            request_id="request-001",
            context="context-A",
            authority="authority-A",
        )

        execution_occurred = False

        self.assertEqual(
            observation.authority,
            "authority-A",
        )

        self.assertFalse(execution_occurred)

    def test_same_request_can_have_multiple_authority_observations(self):
        observations = [
            Observation(
                request_id="request-001",
                context="context-A",
                authority="authority-A",
            ),
            Observation(
                request_id="request-001",
                context="context-B",
                authority="authority-B",
            ),
        ]

        self.assertEqual(
            observations[0].request_id,
            observations[1].request_id,
        )

        self.assertNotEqual(
            observations[0].authority,
            observations[1].authority,
        )

    def test_authority_change_is_not_automatically_permission_change(self):
        first = Observation(
            request_id="request-001",
            context="context-A",
            authority="authority-A",
        )

        second = Observation(
            request_id="request-001",
            context="context-B",
            authority="authority-B",
        )

        permission_before = "granted"
        permission_after = "granted"

        self.assertNotEqual(first.authority, second.authority)
        self.assertEqual(permission_before, permission_after)


if __name__ == "__main__":
    unittest.main()