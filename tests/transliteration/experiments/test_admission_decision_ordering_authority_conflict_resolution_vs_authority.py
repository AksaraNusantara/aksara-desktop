import unittest
from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentalOrderingAuthority:
    authority_id: str


@dataclass(frozen=True)
class ExperimentalAuthorityConflict:
    scope: str
    authority_a: ExperimentalOrderingAuthority
    authority_b: ExperimentalOrderingAuthority


class TestAdmissionDecisionOrderingAuthorityConflictResolutionVsAuthority(
    unittest.TestCase
):

    def test_resolution_is_distinct_from_authority(self):
        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        resolution = {
            "selected_authority": authority.authority_id,
        }

        self.assertNotEqual(
            type(resolution),
            type(authority),
        )

    def test_resolution_does_not_become_selected_authority(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        resolution = {
            "selected_authority": conflict.authority_a.authority_id,
        }

        self.assertEqual(
            resolution["selected_authority"],
            authority_a.authority_id,
        )

        self.assertNotEqual(
            resolution,
            authority_a,
        )

    def test_resolution_does_not_change_authority_identity(self):
        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        resolution = {
            "selected_authority": authority.authority_id,
        }

        self.assertEqual(
            resolution["selected_authority"],
            authority.authority_id,
        )

    def test_resolution_can_reference_authority_without_owning_it(self):
        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        resolution = {
            "selected_authority": authority.authority_id,
        }

        self.assertIn(
            "selected_authority",
            resolution,
        )

        self.assertEqual(
            authority.authority_id,
            "authority-a",
        )

    def test_resolution_can_exist_without_new_authority(self):
        resolution = {
            "policy": "prefer-authority-a",
            "selected_authority": "authority-a",
        }

        self.assertIn(
            "policy",
            resolution,
        )

        self.assertIn(
            "selected_authority",
            resolution,
        )

    def test_selected_authority_remains_original_authority(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        resolution = {
            "selected_authority": authority_a.authority_id,
        }

        self.assertEqual(
            resolution["selected_authority"],
            "authority-a",
        )

    def test_resolution_does_not_create_authority_semantics(self):
        resolution = {
            "policy": "prefer-authority-a",
            "selected_authority": "authority-a",
        }

        self.assertNotIn(
            "authority_id",
            resolution,
        )

    def test_resolution_can_select_different_authorities(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        resolution_a = {
            "selected_authority": authority_a.authority_id,
        }

        resolution_b = {
            "selected_authority": authority_b.authority_id,
        }

        self.assertNotEqual(
            resolution_a["selected_authority"],
            resolution_b["selected_authority"],
        )

    def test_resolution_policy_is_not_authority_identity(self):
        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        resolution = {
            "policy": "prefer-authority-a",
            "selected_authority": authority.authority_id,
        }

        self.assertNotEqual(
            resolution["policy"],
            authority.authority_id,
        )

    def test_resolution_outcome_can_be_observed_without_authority_creation(
        self,
    ):
        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        resolution = {
            "selected_authority": authority.authority_id,
        }

        outcome = resolution["selected_authority"]

        self.assertEqual(
            outcome,
            authority.authority_id,
        )

    def test_minimal_resolution_model_needs_no_resolution_authority(
        self,
    ):
        context = {
            "authority_a": "authority-a",
            "authority_b": "authority-b",
            "resolution_policy": "prefer-authority-a",
        }

        selected_authority = (
            context["authority_a"]
            if context["resolution_policy"] == "prefer-authority-a"
            else context["authority_b"]
        )

        self.assertEqual(
            selected_authority,
            "authority-a",
        )

    def test_resolution_can_be_repeated_without_creating_new_authorities(
        self,
    ):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        first_resolution = {
            "selected_authority": authority_a.authority_id,
        }

        second_resolution = {
            "selected_authority": authority_a.authority_id,
        }

        self.assertEqual(
            first_resolution["selected_authority"],
            second_resolution["selected_authority"],
        )


if __name__ == "__main__":
    unittest.main()