import unittest


def make_observation(
    observation_id=None,
    request_id=None,
    execution_id=None,
    value=None,
    state=None,
    attributes=None,
    sequence=None,
):
    return {
        "observation_id": observation_id,
        "request_id": request_id,
        "execution_id": execution_id,
        "value": value,
        "state": state,
        "attributes": attributes or {},
        "sequence": sequence,
    }


def make_relationship(
    relationship_id=None,
    observation_id=None,
    target_type=None,
    target_id=None,
    attributes=None,
):
    return {
        "relationship_id": relationship_id,
        "observation_id": observation_id,
        "target_type": target_type,
        "target_id": target_id,
        "attributes": attributes or {},
    }


class TestIdentityOccurrenceConsolidation(unittest.TestCase):

    # ---------------------------------------------------------
    # 1. Identity and observation are distinct dimensions
    # ---------------------------------------------------------

    def test_01_observation_identity_is_distinct_from_request_identity(self):
        observation = make_observation(
            observation_id="O1",
            request_id="R1",
        )

        self.assertNotEqual(
            observation["observation_id"],
            observation["request_id"],
        )

    def test_02_observation_identity_is_distinct_from_execution_identity(self):
        observation = make_observation(
            observation_id="O1",
            execution_id="E1",
        )

        self.assertNotEqual(
            observation["observation_id"],
            observation["execution_id"],
        )

    # ---------------------------------------------------------
    # 2. Multiple observations can belong to one request
    # ---------------------------------------------------------

    def test_03_multiple_observations_can_share_request(self):
        observations = [
            make_observation(
                observation_id="O1",
                request_id="R1",
                value="A",
            ),
            make_observation(
                observation_id="O2",
                request_id="R1",
                value="B",
            ),
        ]

        self.assertEqual(
            observations[0]["request_id"],
            observations[1]["request_id"],
        )

        self.assertNotEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

    def test_04_shared_request_does_not_collapse_observation_identity(self):
        observations = [
            make_observation(
                observation_id="O1",
                request_id="R1",
            ),
            make_observation(
                observation_id="O2",
                request_id="R1",
            ),
        ]

        self.assertNotEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

    # ---------------------------------------------------------
    # 3. Cardinality is independent of identity
    # ---------------------------------------------------------

    def test_05_cardinality_can_be_greater_than_one_without_new_request_identity(self):
        observations = [
            make_observation(
                observation_id="O1",
                request_id="R1",
            ),
            make_observation(
                observation_id="O2",
                request_id="R1",
            ),
            make_observation(
                observation_id="O3",
                request_id="R1",
            ),
        ]

        self.assertEqual(
            len(observations),
            3,
        )

        self.assertEqual(
            {
                observation["request_id"]
                for observation in observations
            },
            {"R1"},
        )

    def test_06_cardinality_does_not_define_observation_identity(self):
        observations = [
            make_observation(
                observation_id="O1",
                request_id="R1",
            ),
            make_observation(
                observation_id="O2",
                request_id="R1",
            ),
        ]

        self.assertEqual(
            len(observations),
            2,
        )

        self.assertNotEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

    # ---------------------------------------------------------
    # 4. Ordering is independent of identity
    # ---------------------------------------------------------

    def test_07_sequence_can_distinguish_occurrences_without_identity_change(self):
        observations = [
            make_observation(
                observation_id="O1",
                request_id="R1",
                sequence=1,
            ),
            make_observation(
                observation_id="O1",
                request_id="R1",
                sequence=2,
            ),
        ]

        self.assertEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

        self.assertNotEqual(
            observations[0]["sequence"],
            observations[1]["sequence"],
        )

    def test_08_sequence_is_not_identity(self):
        observation = make_observation(
            observation_id="O1",
            request_id="R1",
            sequence=7,
        )

        self.assertNotEqual(
            observation["observation_id"],
            observation["sequence"],
        )

    # ---------------------------------------------------------
    # 5. Attributes are independent from identity
    # ---------------------------------------------------------

    def test_09_attributes_can_change_without_identity_change(self):
        observation = make_observation(
            observation_id="O1",
            value="A",
            attributes={
                "mode": "direct",
            },
        )

        observation["attributes"]["mode"] = "queued"

        self.assertEqual(
            observation["observation_id"],
            "O1",
        )

    def test_10_attribute_difference_does_not_prove_identity_difference(self):
        observations = [
            make_observation(
                observation_id="O1",
                attributes={"mode": "direct"},
            ),
            make_observation(
                observation_id="O1",
                attributes={"mode": "queued"},
            ),
        ]

        self.assertEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

        self.assertNotEqual(
            observations[0]["attributes"],
            observations[1]["attributes"],
        )

    # ---------------------------------------------------------
    # 6. State is independent from identity
    # ---------------------------------------------------------

    def test_11_state_change_can_preserve_identity(self):
        observation = make_observation(
            observation_id="O1",
            state="ACTIVE",
        )

        observation["state"] = "INACTIVE"

        self.assertEqual(
            observation["observation_id"],
            "O1",
        )

    def test_12_state_is_not_identity(self):
        observations = [
            make_observation(
                observation_id="O1",
                state="ACTIVE",
            ),
            make_observation(
                observation_id="O1",
                state="INACTIVE",
            ),
        ]

        self.assertEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

        self.assertNotEqual(
            observations[0]["state"],
            observations[1]["state"],
        )

    # ---------------------------------------------------------
    # 7. Relationship can exist without relationship identity
    # ---------------------------------------------------------

    def test_13_relationship_can_be_represented_by_endpoints(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
        )

        self.assertEqual(
            relationship["observation_id"],
            "O1",
        )

        self.assertEqual(
            relationship["target_id"],
            "R1",
        )

        self.assertIsNone(
            relationship["relationship_id"]
        )

    def test_14_relationship_identity_is_optional(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            relationship_id="REL1",
        )

        self.assertEqual(
            relationship["relationship_id"],
            "REL1",
        )

    # ---------------------------------------------------------
    # 8. Relationship identity is distinct from endpoints
    # ---------------------------------------------------------

    def test_15_relationship_identity_is_distinct_from_observation_identity(self):
        relationship = make_relationship(
            relationship_id="REL1",
            observation_id="O1",
            target_type="request",
            target_id="R1",
        )

        self.assertNotEqual(
            relationship["relationship_id"],
            relationship["observation_id"],
        )

    def test_16_relationship_identity_is_distinct_from_request_identity(self):
        relationship = make_relationship(
            relationship_id="REL1",
            observation_id="O1",
            target_type="request",
            target_id="R1",
        )

        self.assertNotEqual(
            relationship["relationship_id"],
            relationship["target_id"],
        )

    # ---------------------------------------------------------
    # 9. Relationship attributes are independent
    # ---------------------------------------------------------

    def test_17_relationship_attributes_do_not_require_identity(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
            },
        )

        self.assertEqual(
            relationship["attributes"]["role"],
            "source",
        )

        self.assertIsNone(
            relationship["relationship_id"]
        )

    def test_18_relationship_attribute_change_can_preserve_identity(self):
        relationship = make_relationship(
            relationship_id="REL1",
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "mode": "direct",
            },
        )

        relationship["attributes"]["mode"] = "queued"

        self.assertEqual(
            relationship["relationship_id"],
            "REL1",
        )

    # ---------------------------------------------------------
    # 10. Identity can distinguish occurrences
    # ---------------------------------------------------------

    def test_19_identity_can_distinguish_same_value_occurrences(self):
        observations = [
            make_observation(
                observation_id="O1",
                value="A",
            ),
            make_observation(
                observation_id="O2",
                value="A",
            ),
        ]

        self.assertEqual(
            observations[0]["value"],
            observations[1]["value"],
        )

        self.assertNotEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

    def test_20_sequence_can_distinguish_occurrences_without_identity_change(self):
        observations = [
            make_observation(
                observation_id="O1",
                sequence=1,
                value="A",
            ),
            make_observation(
                observation_id="O1",
                sequence=2,
                value="A",
            ),
        ]

        self.assertEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

        self.assertNotEqual(
            observations[0]["sequence"],
            observations[1]["sequence"],
        )

    # ---------------------------------------------------------
    # 11. Same identity does not define same value
    # ---------------------------------------------------------

    def test_21_same_identity_can_have_different_values(self):
        observations = [
            make_observation(
                observation_id="O1",
                value="A",
            ),
            make_observation(
                observation_id="O1",
                value="B",
            ),
        ]

        self.assertEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

        self.assertNotEqual(
            observations[0]["value"],
            observations[1]["value"],
        )

    def test_22_same_identity_can_have_different_states(self):
        observations = [
            make_observation(
                observation_id="O1",
                state="A",
            ),
            make_observation(
                observation_id="O1",
                state="B",
            ),
        ]

        self.assertEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

        self.assertNotEqual(
            observations[0]["state"],
            observations[1]["state"],
        )

    # ---------------------------------------------------------
    # 12. Different identity does not explain semantic reason
    # ---------------------------------------------------------

    def test_23_different_identity_does_not_explain_change(self):
        observations = [
            make_observation(
                observation_id="O1",
                value="A",
            ),
            make_observation(
                observation_id="O2",
                value="B",
            ),
        ]

        self.assertNotEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

        # Identity distinguishes.
        # It does not explain why the semantic values differ.

    def test_24_identity_difference_does_not_define_new_occurrence_reason(self):
        observations = [
            make_observation(
                observation_id="O1",
                sequence=1,
            ),
            make_observation(
                observation_id="O2",
                sequence=2,
            ),
        ]

        self.assertNotEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

        # The model still needs semantic rules to explain
        # why these represent different occurrences.

    # ---------------------------------------------------------
    # 13. Relationship + occurrence + attributes coexist
    # ---------------------------------------------------------

    def test_25_relationship_can_connect_observation_with_request(self):
        observation = make_observation(
            observation_id="O1",
            request_id="R1",
            value="A",
        )

        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
        )

        self.assertEqual(
            observation["observation_id"],
            relationship["observation_id"],
        )

        self.assertEqual(
            observation["request_id"],
            relationship["target_id"],
        )

    def test_26_relationship_can_have_attributes_and_identity_together(self):
        relationship = make_relationship(
            relationship_id="REL1",
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
            },
        )

        self.assertEqual(
            relationship["relationship_id"],
            "REL1",
        )

        self.assertEqual(
            relationship["attributes"]["role"],
            "source",
        )

    # ---------------------------------------------------------
    # 14. Mutation and occurrence remain semantic dimensions
    # ---------------------------------------------------------

    def test_27_same_identity_can_represent_mutation(self):
        observations = [
            make_observation(
                observation_id="O1",
                value="A",
                sequence=1,
            ),
            make_observation(
                observation_id="O1",
                value="B",
                sequence=2,
            ),
        ]

        self.assertEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

        self.assertNotEqual(
            observations[0]["value"],
            observations[1]["value"],
        )

    def test_28_different_identity_can_represent_new_occurrence(self):
        observations = [
            make_observation(
                observation_id="O1",
                value="A",
            ),
            make_observation(
                observation_id="O2",
                value="B",
            ),
        ]

        self.assertNotEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

    # ---------------------------------------------------------
    # 15. Semantic interpretation remains independent
    # ---------------------------------------------------------

    def test_29_identity_does_not_define_mutation_semantics(self):
        observation = make_observation(
            observation_id="O1",
            value="A",
        )

        observation["value"] = "B"

        self.assertEqual(
            observation["observation_id"],
            "O1",
        )

        # Whether this is interpreted as mutation
        # is a semantic rule, not an identity rule.

    def test_30_relationship_identity_does_not_define_lifecycle(self):
        relationship = make_relationship(
            relationship_id="REL1",
            observation_id="O1",
            target_type="request",
            target_id="R1",
        )

        self.assertEqual(
            relationship["relationship_id"],
            "REL1",
        )

        # Identity alone does not establish lifecycle semantics.

    # ---------------------------------------------------------
    # 16. Final boundary assertions
    # ---------------------------------------------------------

    def test_31_identity_is_not_cardinality(self):
        observations = [
            make_observation(
                observation_id="O1",
                request_id="R1",
            ),
            make_observation(
                observation_id="O2",
                request_id="R1",
            ),
        ]

        self.assertEqual(
            len(observations),
            2,
        )

        self.assertNotEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

    def test_32_cardinality_is_not_ordering(self):
        observations = [
            make_observation(
                observation_id="O1",
                sequence=1,
            ),
            make_observation(
                observation_id="O2",
                sequence=2,
            ),
        ]

        self.assertEqual(
            len(observations),
            2,
        )

        self.assertNotEqual(
            observations[0]["sequence"],
            observations[1]["sequence"],
        )

    def test_33_ordering_is_not_identity(self):
        observation = make_observation(
            observation_id="O1",
            sequence=10,
        )

        self.assertNotEqual(
            observation["observation_id"],
            observation["sequence"],
        )

    def test_34_relationship_is_not_relationship_identity(self):
        relationship = make_relationship(
            relationship_id="REL1",
            observation_id="O1",
            target_type="request",
            target_id="R1",
        )

        self.assertIsNotNone(
            relationship["target_id"]
        )

        self.assertIsNotNone(
            relationship["relationship_id"]
        )

        self.assertNotEqual(
            relationship["relationship_id"],
            relationship["target_id"],
        )

    def test_35_attribute_is_not_identity(self):
        observation = make_observation(
            observation_id="O1",
            attributes={
                "mode": "direct",
            },
        )

        self.assertNotEqual(
            observation["observation_id"],
            observation["attributes"]["mode"],
        )

    def test_36_mutation_is_not_identity_change(self):
        observation = make_observation(
            observation_id="O1",
            value="A",
        )

        original_identity = observation["observation_id"]

        observation["value"] = "B"

        self.assertEqual(
            observation["observation_id"],
            original_identity,
        )


if __name__ == "__main__":
    unittest.main()