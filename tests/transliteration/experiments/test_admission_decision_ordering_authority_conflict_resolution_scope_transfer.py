import unittest
from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentalScope:
    scope_id: str


@dataclass(frozen=True)
class ExperimentalResolution:
    selected_authority: str


class TestAdmissionDecisionOrderingAuthorityConflictResolutionScopeTransfer(
    unittest.TestCase
):

    def test_resolution_can_be_referenced_by_scope_a(self):
        scope_a = ExperimentalScope(
            scope_id="scope-a"
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        context = {
            "scope": scope_a,
            "resolution": resolution,
        }

        self.assertIs(
            context["resolution"],
            resolution,
        )

    def test_same_resolution_can_be_referenced_by_scope_b(self):
        scope_b = ExperimentalScope(
            scope_id="scope-b"
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        context = {
            "scope": scope_b,
            "resolution": resolution,
        }

        self.assertIs(
            context["resolution"],
            resolution,
        )

    def test_scope_transfer_does_not_mutate_resolution(self):
        scope_a = ExperimentalScope(
            scope_id="scope-a"
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b"
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        context_a = {
            "scope": scope_a,
            "resolution": resolution,
        }

        before = context_a["resolution"]

        context_b = {
            "scope": scope_b,
            "resolution": resolution,
        }

        self.assertIs(
            before,
            context_b["resolution"],
        )

    def test_scope_transfer_does_not_change_selected_authority(self):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        scope_a = ExperimentalScope(
            scope_id="scope-a"
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b"
        )

        outcome_a = {
            "scope": scope_a,
            "selected_authority":
                resolution.selected_authority,
        }

        outcome_b = {
            "scope": scope_b,
            "selected_authority":
                resolution.selected_authority,
        }

        self.assertEqual(
            outcome_a["selected_authority"],
            outcome_b["selected_authority"],
        )

    def test_scope_identity_changes_but_resolution_identity_does_not(self):
        scope_a = ExperimentalScope(
            scope_id="scope-a"
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b"
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        context_a = {
            "scope": scope_a,
            "resolution": resolution,
        }

        context_b = {
            "scope": scope_b,
            "resolution": resolution,
        }

        self.assertNotEqual(
            context_a["scope"].scope_id,
            context_b["scope"].scope_id,
        )

        self.assertIs(
            context_a["resolution"],
            context_b["resolution"],
        )

    def test_resolution_can_be_shared_across_multiple_scopes(self):
        scope_a = ExperimentalScope(
            scope_id="scope-a"
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b"
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        contexts = [
            {
                "scope": scope_a,
                "resolution": resolution,
            },
            {
                "scope": scope_b,
                "resolution": resolution,
            },
        ]

        self.assertIs(
            contexts[0]["resolution"],
            contexts[1]["resolution"],
        )

    def test_scope_transfer_does_not_create_new_resolution_identity(
        self,
    ):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        transferred = resolution

        self.assertIs(
            resolution,
            transferred,
        )

    def test_scope_can_change_without_resolution_mutation(self):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        scope_a = ExperimentalScope(
            scope_id="scope-a"
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b"
        )

        first = (
            scope_a.scope_id,
            resolution.selected_authority,
        )

        second = (
            scope_b.scope_id,
            resolution.selected_authority,
        )

        self.assertNotEqual(first[0], second[0])
        self.assertEqual(first[1], second[1])

    def test_scope_transfer_can_preserve_resolution_type(self):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        scope_a = ExperimentalScope(
            scope_id="scope-a"
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b"
        )

        context_a = {
            "scope": scope_a,
            "resolution": resolution,
        }

        context_b = {
            "scope": scope_b,
            "resolution": resolution,
        }

        self.assertIs(
            type(context_a["resolution"]),
            type(context_b["resolution"]),
        )

    def test_scope_is_not_required_as_resolution_identity(self):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        self.assertEqual(
            resolution.selected_authority,
            "authority-a",
        )

        self.assertFalse(
            hasattr(resolution, "scope_id")
        )

    def test_multiple_scope_contexts_can_reference_one_resolution(
        self,
    ):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        scopes = [
            ExperimentalScope("scope-a"),
            ExperimentalScope("scope-b"),
            ExperimentalScope("scope-c"),
        ]

        contexts = [
            {
                "scope": scope,
                "resolution": resolution,
            }
            for scope in scopes
        ]

        for context in contexts:
            self.assertIs(
                context["resolution"],
                resolution,
            )

    def test_minimal_scope_transfer_requires_no_transfer_object(self):
        context_a = {
            "scope": "scope-a",
            "selected_authority": "authority-a",
        }

        context_b = {
            "scope": "scope-b",
            "selected_authority":
                context_a["selected_authority"],
        }

        self.assertEqual(
            context_b["selected_authority"],
            "authority-a",
        )


if __name__ == "__main__":
    unittest.main()