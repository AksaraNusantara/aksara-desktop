import unittest


def make_entity(
    entity_id=None,
    value=None,
    state=None,
    attributes=None,
    context=None,
):
    return {
        "entity_id": entity_id,
        "value": value,
        "state": state,
        "attributes": attributes or {},
        "context": context,
    }


def make_relationship(
    relationship_id=None,
    source_id=None,
    target_id=None,
    attributes=None,
):
    return {
        "relationship_id": relationship_id,
        "source_id": source_id,
        "target_id": target_id,
        "attributes": attributes or {},
    }


class TestIdentityStabilityMutation(unittest.TestCase):

    # ---------------------------------------------------------
    # 1. Attribute mutation can preserve identity
    # ---------------------------------------------------------

    def test_01_attribute_change_can_preserve_identity(self):
        entity = make_entity(
            entity_id="E1",
            attributes={
                "mode": "direct",
            },
        )

        original_id = entity["entity_id"]

        entity["attributes"]["mode"] = "queued"

        self.assertEqual(
            entity["entity_id"],
            original_id,
        )

    def test_02_multiple_attribute_changes_can_preserve_identity(self):
        entity = make_entity(
            entity_id="E1",
            attributes={
                "mode": "direct",
                "priority": "normal",
            },
        )

        entity["attributes"]["mode"] = "queued"
        entity["attributes"]["priority"] = "high"

        self.assertEqual(
            entity["entity_id"],
            "E1",
        )

    # ---------------------------------------------------------
    # 2. Value mutation can preserve identity
    # ---------------------------------------------------------

    def test_03_value_change_can_preserve_identity(self):
        entity = make_entity(
            entity_id="E1",
            value="A",
        )

        entity["value"] = "B"

        self.assertEqual(
            entity["entity_id"],
            "E1",
        )

    def test_04_same_identity_can_have_multiple_observed_values(self):
        observations = [
            {
                "entity_id": "E1",
                "value": "A",
            },
            {
                "entity_id": "E1",
                "value": "B",
            },
        ]

        self.assertEqual(
            observations[0]["entity_id"],
            observations[1]["entity_id"],
        )

        self.assertNotEqual(
            observations[0]["value"],
            observations[1]["value"],
        )

    # ---------------------------------------------------------
    # 3. State mutation can preserve identity
    # ---------------------------------------------------------

    def test_05_state_change_can_preserve_identity(self):
        entity = make_entity(
            entity_id="E1",
            state="ACTIVE",
        )

        entity["state"] = "INACTIVE"

        self.assertEqual(
            entity["entity_id"],
            "E1",
        )

    def test_06_state_is_not_identity(self):
        entity_a = make_entity(
            entity_id="E1",
            state="ACTIVE",
        )

        entity_b = make_entity(
            entity_id="E1",
            state="INACTIVE",
        )

        self.assertEqual(
            entity_a["entity_id"],
            entity_b["entity_id"],
        )

        self.assertNotEqual(
            entity_a["state"],
            entity_b["state"],
        )

    # ---------------------------------------------------------
    # 4. Context change does not automatically require
    #    identity change
    # ---------------------------------------------------------

    def test_07_context_change_can_preserve_identity(self):
        entity = make_entity(
            entity_id="E1",
            context="C1",
        )

        entity["context"] = "C2"

        self.assertEqual(
            entity["entity_id"],
            "E1",
        )

    def test_08_context_is_distinct_from_identity(self):
        entity_a = make_entity(
            entity_id="E1",
            context="C1",
        )

        entity_b = make_entity(
            entity_id="E1",
            context="C2",
        )

        self.assertEqual(
            entity_a["entity_id"],
            entity_b["entity_id"],
        )

        self.assertNotEqual(
            entity_a["context"],
            entity_b["context"],
        )

    # ---------------------------------------------------------
    # 5. Different identity can represent distinct occurrence
    # ---------------------------------------------------------

    def test_09_different_identity_can_distinguish_occurrences(self):
        entity_a = make_entity(
            entity_id="E1",
            value="A",
        )

        entity_b = make_entity(
            entity_id="E2",
            value="B",
        )

        self.assertNotEqual(
            entity_a["entity_id"],
            entity_b["entity_id"],
        )

    def test_10_different_identity_does_not_require_different_value(self):
        entity_a = make_entity(
            entity_id="E1",
            value="A",
        )

        entity_b = make_entity(
            entity_id="E2",
            value="A",
        )

        self.assertNotEqual(
            entity_a["entity_id"],
            entity_b["entity_id"],
        )

        self.assertEqual(
            entity_a["value"],
            entity_b["value"],
        )

    # ---------------------------------------------------------
    # 6. Different identity does not explain semantic reason
    # ---------------------------------------------------------

    def test_11_identity_difference_does_not_explain_reason(self):
        entity_a = make_entity(
            entity_id="E1",
            value="A",
        )

        entity_b = make_entity(
            entity_id="E2",
            value="B",
        )

        self.assertNotEqual(
            entity_a["entity_id"],
            entity_b["entity_id"],
        )

        # Identity distinguishes the entities.
        # It does not explain why they are different.

    def test_12_identity_change_does_not_define_mutation_semantics(self):
        entity_a = make_entity(
            entity_id="E1",
            value="A",
        )

        entity_b = make_entity(
            entity_id="E2",
            value="B",
        )

        self.assertNotEqual(
            entity_a["entity_id"],
            entity_b["entity_id"],
        )

        # No conclusion about mutation/new occurrence
        # follows from identity difference alone.

    # ---------------------------------------------------------
    # 7. Same identity does not prove same semantic value
    # ---------------------------------------------------------

    def test_13_same_identity_does_not_require_same_value(self):
        observations = [
            {
                "entity_id": "E1",
                "value": "A",
            },
            {
                "entity_id": "E1",
                "value": "B",
            },
        ]

        self.assertEqual(
            observations[0]["entity_id"],
            observations[1]["entity_id"],
        )

        self.assertNotEqual(
            observations[0]["value"],
            observations[1]["value"],
        )

    def test_14_same_identity_does_not_require_same_state(self):
        observations = [
            {
                "entity_id": "E1",
                "state": "ACTIVE",
            },
            {
                "entity_id": "E1",
                "state": "INACTIVE",
            },
        ]

        self.assertEqual(
            observations[0]["entity_id"],
            observations[1]["entity_id"],
        )

        self.assertNotEqual(
            observations[0]["state"],
            observations[1]["state"],
        )

    # ---------------------------------------------------------
    # 8. Relationship mutation can preserve identity
    # ---------------------------------------------------------

    def test_15_relationship_attribute_change_can_preserve_identity(self):
        relationship = make_relationship(
            relationship_id="REL1",
            source_id="E1",
            target_id="E2",
            attributes={
                "role": "source",
            },
        )

        relationship["attributes"]["role"] = "target"

        self.assertEqual(
            relationship["relationship_id"],
            "REL1",
        )

    def test_16_relationship_endpoints_can_remain_stable_while_attributes_change(self):
        relationship = make_relationship(
            relationship_id="REL1",
            source_id="E1",
            target_id="E2",
            attributes={
                "mode": "direct",
            },
        )

        original_endpoints = (
            relationship["source_id"],
            relationship["target_id"],
        )

        relationship["attributes"]["mode"] = "queued"

        self.assertEqual(
            (
                relationship["source_id"],
                relationship["target_id"],
            ),
            original_endpoints,
        )

    # ---------------------------------------------------------
    # 9. Relationship identity and entity identity are distinct
    # ---------------------------------------------------------

    def test_17_relationship_identity_is_distinct_from_source_identity(self):
        relationship = make_relationship(
            relationship_id="REL1",
            source_id="E1",
            target_id="E2",
        )

        self.assertNotEqual(
            relationship["relationship_id"],
            relationship["source_id"],
        )

    def test_18_relationship_identity_is_distinct_from_target_identity(self):
        relationship = make_relationship(
            relationship_id="REL1",
            source_id="E1",
            target_id="E2",
        )

        self.assertNotEqual(
            relationship["relationship_id"],
            relationship["target_id"],
        )

    # ---------------------------------------------------------
    # 10. Identity stability requires semantic rule
    # ---------------------------------------------------------

    def test_19_identity_stability_is_not_determined_by_attribute_change_alone(self):
        entity = make_entity(
            entity_id="E1",
            attributes={
                "kind": "A",
            },
        )

        entity["attributes"]["kind"] = "B"

        self.assertEqual(
            entity["entity_id"],
            "E1",
        )

        # This demonstrates that identity MAY remain stable.
        # It does not establish that it MUST remain stable.

    def test_20_identity_stability_is_a_semantic_interpretation(self):
        entity = make_entity(
            entity_id="E1",
            value="A",
        )

        entity["value"] = "B"

        self.assertEqual(
            entity["entity_id"],
            "E1",
        )

        # Whether this is mutation or a new semantic occurrence
        # requires a rule beyond the value change itself.

    # ---------------------------------------------------------
    # 11. New occurrence can preserve related context
    # ---------------------------------------------------------

    def test_21_new_occurrence_can_share_context(self):
        occurrence_a = {
            "entity_id": "E1",
            "context": "C1",
            "sequence": 1,
        }

        occurrence_b = {
            "entity_id": "E2",
            "context": "C1",
            "sequence": 2,
        }

        self.assertEqual(
            occurrence_a["context"],
            occurrence_b["context"],
        )

        self.assertNotEqual(
            occurrence_a["entity_id"],
            occurrence_b["entity_id"],
        )

    def test_22_new_occurrence_can_share_value(self):
        occurrence_a = {
            "entity_id": "E1",
            "value": "A",
            "sequence": 1,
        }

        occurrence_b = {
            "entity_id": "E2",
            "value": "A",
            "sequence": 2,
        }

        self.assertEqual(
            occurrence_a["value"],
            occurrence_b["value"],
        )

        self.assertNotEqual(
            occurrence_a["entity_id"],
            occurrence_b["entity_id"],
        )

    # ---------------------------------------------------------
    # 12. Identity does not define cardinality
    # ---------------------------------------------------------

    def test_23_one_identity_can_have_multiple_observations(self):
        observations = [
            {"entity_id": "E1", "sequence": 1},
            {"entity_id": "E1", "sequence": 2},
            {"entity_id": "E1", "sequence": 3},
        ]

        self.assertEqual(
            len(observations),
            3,
        )

        self.assertTrue(
            all(
                observation["entity_id"] == "E1"
                for observation in observations
            )
        )

    def test_24_multiple_identities_can_exist_in_same_context(self):
        entities = [
            {"entity_id": "E1", "context": "C1"},
            {"entity_id": "E2", "context": "C1"},
            {"entity_id": "E3", "context": "C1"},
        ]

        self.assertEqual(
            len(entities),
            3,
        )

        self.assertEqual(
            {
                entity["context"]
                for entity in entities
            },
            {"C1"},
        )

        self.assertEqual(
            len(
                {
                    entity["entity_id"]
                    for entity in entities
                }
            ),
            3,
        )


if __name__ == "__main__":
    unittest.main()