import unittest


def make_relationship(
    observation_id,
    target_type,
    target_id,
    attributes=None,
    relationship_id=None,
    occurrence=None,
):
    return {
        "relationship_id": relationship_id,
        "observation_id": observation_id,
        "target_type": target_type,
        "target_id": target_id,
        "attributes": attributes or {},
        "occurrence": occurrence,
    }


class TestRelationshipMutationOccurrence(unittest.TestCase):

    # ---------------------------------------------------------
    # 1. Attribute change preserves endpoints
    # ---------------------------------------------------------

    def test_01_attribute_change_can_preserve_relationship_endpoints(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"mode": "direct"},
        )

        original_endpoints = (
            relationship["observation_id"],
            relationship["target_type"],
            relationship["target_id"],
        )

        relationship["attributes"]["mode"] = "queued"

        new_endpoints = (
            relationship["observation_id"],
            relationship["target_type"],
            relationship["target_id"],
        )

        self.assertEqual(
            original_endpoints,
            new_endpoints,
        )

    def test_02_attribute_change_does_not_automatically_change_identity(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"mode": "direct"},
            relationship_id="REL1",
        )

        relationship["attributes"]["mode"] = "queued"

        self.assertEqual(
            relationship["relationship_id"],
            "REL1",
        )

    # ---------------------------------------------------------
    # 2. Mutation interpretation
    # ---------------------------------------------------------

    def test_03_same_identity_can_represent_attribute_mutation(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"status": "active"},
            relationship_id="REL1",
        )

        original_identity = relationship["relationship_id"]

        relationship["attributes"]["status"] = "inactive"

        self.assertEqual(
            relationship["relationship_id"],
            original_identity,
        )

    def test_04_mutation_can_change_attribute_without_new_occurrence(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"priority": "normal"},
            relationship_id="REL1",
            occurrence=1,
        )

        relationship["attributes"]["priority"] = "high"

        self.assertEqual(
            relationship["relationship_id"],
            "REL1",
        )

        self.assertEqual(
            relationship["occurrence"],
            1,
        )

    # ---------------------------------------------------------
    # 3. New occurrence interpretation
    # ---------------------------------------------------------

    def test_05_attribute_change_can_also_be_modelled_as_new_occurrence(self):
        relationship_a = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"mode": "direct"},
            occurrence=1,
        )

        relationship_b = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"mode": "queued"},
            occurrence=2,
        )

        self.assertEqual(
            relationship_a["observation_id"],
            relationship_b["observation_id"],
        )

        self.assertEqual(
            relationship_a["target_id"],
            relationship_b["target_id"],
        )

        self.assertNotEqual(
            relationship_a["occurrence"],
            relationship_b["occurrence"],
        )

    def test_06_new_occurrence_does_not_require_new_relationship_concept(self):
        relationship_a = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"mode": "direct"},
            occurrence=1,
        )

        relationship_b = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"mode": "queued"},
            occurrence=2,
        )

        self.assertEqual(
            relationship_a["target_type"],
            relationship_b["target_type"],
        )

        self.assertEqual(
            relationship_a["target_id"],
            relationship_b["target_id"],
        )

    # ---------------------------------------------------------
    # 4. Same endpoints do not determine mutation vs occurrence
    # ---------------------------------------------------------

    def test_07_same_endpoints_do_not_determine_mutation(self):
        relationship_a = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"state": "A"},
        )

        relationship_b = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"state": "B"},
        )

        self.assertEqual(
            (
                relationship_a["observation_id"],
                relationship_a["target_id"],
            ),
            (
                relationship_b["observation_id"],
                relationship_b["target_id"],
            ),
        )

        self.assertNotEqual(
            relationship_a["attributes"],
            relationship_b["attributes"],
        )

    def test_08_same_endpoints_do_not_determine_new_occurrence(self):
        relationship_a = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"state": "A"},
        )

        relationship_b = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"state": "B"},
        )

        self.assertIsNone(
            relationship_a["occurrence"]
        )

        self.assertIsNone(
            relationship_b["occurrence"]
        )

    # ---------------------------------------------------------
    # 5. Identity can preserve continuity
    # ---------------------------------------------------------

    def test_09_same_relationship_id_can_preserve_continuity(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"value": 1},
            relationship_id="REL1",
        )

        original_id = relationship["relationship_id"]

        relationship["attributes"]["value"] = 2

        self.assertEqual(
            relationship["relationship_id"],
            original_id,
        )

    def test_10_identity_continuity_is_distinct_from_attribute_value(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"value": 1},
            relationship_id="REL1",
        )

        relationship["attributes"]["value"] = 2

        self.assertEqual(
            relationship["relationship_id"],
            "REL1",
        )

        self.assertEqual(
            relationship["attributes"]["value"],
            2,
        )

    # ---------------------------------------------------------
    # 6. New occurrence can exist without new identity
    # ---------------------------------------------------------

    def test_11_occurrence_distinction_can_use_sequence(self):
        occurrence_a = {
            "observation_id": "O1",
            "target_id": "R1",
            "sequence": 1,
            "value": "A",
        }

        occurrence_b = {
            "observation_id": "O1",
            "target_id": "R1",
            "sequence": 2,
            "value": "B",
        }

        self.assertNotEqual(
            occurrence_a["sequence"],
            occurrence_b["sequence"],
        )

    def test_12_occurrence_distinction_does_not_require_relationship_id(self):
        occurrence_a = {
            "observation_id": "O1",
            "target_id": "R1",
            "sequence": 1,
        }

        occurrence_b = {
            "observation_id": "O1",
            "target_id": "R1",
            "sequence": 2,
        }

        self.assertNotIn(
            "relationship_id",
            occurrence_a,
        )

        self.assertNotIn(
            "relationship_id",
            occurrence_b,
        )

    # ---------------------------------------------------------
    # 7. Identity change can indicate a distinct occurrence
    # ---------------------------------------------------------

    def test_13_different_relationship_ids_can_distinguish_occurrences(self):
        relationship_a = make_relationship(
            "O1",
            "request",
            "R1",
            relationship_id="REL1",
        )

        relationship_b = make_relationship(
            "O1",
            "request",
            "R1",
            relationship_id="REL2",
        )

        self.assertNotEqual(
            relationship_a["relationship_id"],
            relationship_b["relationship_id"],
        )

    def test_14_different_identity_does_not_change_endpoints(self):
        relationship_a = make_relationship(
            "O1",
            "request",
            "R1",
            relationship_id="REL1",
        )

        relationship_b = make_relationship(
            "O1",
            "request",
            "R1",
            relationship_id="REL2",
        )

        self.assertEqual(
            relationship_a["observation_id"],
            relationship_b["observation_id"],
        )

        self.assertEqual(
            relationship_a["target_id"],
            relationship_b["target_id"],
        )

    # ---------------------------------------------------------
    # 8. Mutation vs occurrence is not determined by value alone
    # ---------------------------------------------------------

    def test_15_different_values_do_not_prove_new_occurrence(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"value": "A"},
            relationship_id="REL1",
        )

        relationship["attributes"]["value"] = "B"

        self.assertEqual(
            relationship["relationship_id"],
            "REL1",
        )

    def test_16_same_value_does_not_prove_same_occurrence(self):
        relationship_a = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"value": "A"},
            occurrence=1,
        )

        relationship_b = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"value": "A"},
            occurrence=2,
        )

        self.assertEqual(
            relationship_a["attributes"],
            relationship_b["attributes"],
        )

        self.assertNotEqual(
            relationship_a["occurrence"],
            relationship_b["occurrence"],
        )

    # ---------------------------------------------------------
    # 9. Occurrence and identity are separate dimensions
    # ---------------------------------------------------------

    def test_17_occurrence_is_not_identity(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            relationship_id="REL1",
            occurrence=1,
        )

        self.assertNotEqual(
            relationship["relationship_id"],
            relationship["occurrence"],
        )

    def test_18_identity_does_not_define_occurrence_number(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            relationship_id="REL1",
        )

        self.assertIsNone(
            relationship["occurrence"]
        )

    # ---------------------------------------------------------
    # 10. Mutation and occurrence may coexist conceptually
    # ---------------------------------------------------------

    def test_19_same_relationship_can_have_multiple_mutation_observations(self):
        observations = [
            {
                "relationship_id": "REL1",
                "value": "A",
            },
            {
                "relationship_id": "REL1",
                "value": "B",
            },
        ]

        self.assertEqual(
            observations[0]["relationship_id"],
            observations[1]["relationship_id"],
        )

        self.assertNotEqual(
            observations[0]["value"],
            observations[1]["value"],
        )

    def test_20_same_relationship_can_have_multiple_observed_values(self):
        observations = [
            {
                "relationship_id": "REL1",
                "sequence": 1,
                "value": "A",
            },
            {
                "relationship_id": "REL1",
                "sequence": 2,
                "value": "B",
            },
        ]

        self.assertEqual(
            observations[0]["relationship_id"],
            observations[1]["relationship_id"],
        )

        self.assertNotEqual(
            observations[0]["sequence"],
            observations[1]["sequence"],
        )

    # ---------------------------------------------------------
    # 11. Semantic rule is required to interpret continuity
    # ---------------------------------------------------------

    def test_21_identity_alone_does_not_define_mutation_semantics(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"value": "A"},
            relationship_id="REL1",
        )

        relationship["attributes"]["value"] = "B"

        self.assertEqual(
            relationship["relationship_id"],
            "REL1",
        )

        # Identity continuity is observable,
        # but interpretation as "mutation" is semantic.

    def test_22_new_identity_alone_does_not_define_reason_for_new_occurrence(self):
        relationship_a = make_relationship(
            "O1",
            "request",
            "R1",
            relationship_id="REL1",
        )

        relationship_b = make_relationship(
            "O1",
            "request",
            "R1",
            relationship_id="REL2",
        )

        self.assertNotEqual(
            relationship_a["relationship_id"],
            relationship_b["relationship_id"],
        )

        # Different identity distinguishes occurrences,
        # but does not explain WHY they are different.

    # ---------------------------------------------------------
    # 12. Minimal model remains possible
    # ---------------------------------------------------------

    def test_23_minimal_relationship_can_change_attribute_without_identity(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"mode": "direct"},
        )

        relationship["attributes"]["mode"] = "queued"

        self.assertEqual(
            relationship["attributes"]["mode"],
            "queued",
        )

        self.assertIsNone(
            relationship["relationship_id"]
        )

    def test_24_minimal_relationship_can_represent_multiple_occurrences(self):
        relationships = [
            {
                "observation_id": "O1",
                "target_id": "R1",
                "sequence": 1,
                "value": "A",
            },
            {
                "observation_id": "O1",
                "target_id": "R1",
                "sequence": 2,
                "value": "B",
            },
        ]

        self.assertEqual(
            len(relationships),
            2,
        )

        self.assertNotEqual(
            relationships[0]["sequence"],
            relationships[1]["sequence"],
        )


if __name__ == "__main__":
    unittest.main()