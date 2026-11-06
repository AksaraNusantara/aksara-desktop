import unittest


def make_observation(
    observation_id=None,
    request_id=None,
    execution_id=None,
    value=None,
    context=None,
):
    return {
        "observation_id": observation_id,
        "request_id": request_id,
        "execution_id": execution_id,
        "value": value,
        "context": context,
    }


def make_relationship(
    observation_id,
    target_type,
    target_id,
    relationship_id=None,
    attributes=None,
):
    return {
        "relationship_id": relationship_id,
        "observation_id": observation_id,
        "target_type": target_type,
        "target_id": target_id,
        "attributes": attributes or {},
    }


class TestRelationshipIdentityBoundary(unittest.TestCase):

    # ---------------------------------------------------------
    # 1. Relationship membership can be represented by reference
    # ---------------------------------------------------------

    def test_01_observation_can_belong_to_request_without_relationship_id(self):
        observation = make_observation(
            observation_id="O1",
            request_id="R1",
            value="ACCEPTED",
        )

        self.assertEqual(observation["request_id"], "R1")
        self.assertIsNone(
            make_relationship(
                "O1",
                "request",
                "R1",
            )["relationship_id"]
        )

    def test_02_observation_can_belong_to_execution_without_relationship_id(self):
        observation = make_observation(
            observation_id="O1",
            execution_id="E1",
            value="SUCCESS",
        )

        self.assertEqual(observation["execution_id"], "E1")

        relationship = make_relationship(
            "O1",
            "execution",
            "E1",
        )

        self.assertIsNone(relationship["relationship_id"])

    def test_03_relationship_can_be_identified_by_endpoints(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
        )

        self.assertEqual(
            (
                relationship["observation_id"],
                relationship["target_type"],
                relationship["target_id"],
            ),
            ("O1", "request", "R1"),
        )

    # ---------------------------------------------------------
    # 2. Relationship identity is distinct from endpoint identity
    # ---------------------------------------------------------

    def test_04_relationship_identity_is_not_observation_identity(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            relationship_id="REL1",
        )

        self.assertNotEqual(
            relationship["relationship_id"],
            relationship["observation_id"],
        )

    def test_05_relationship_identity_is_not_request_identity(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            relationship_id="REL1",
        )

        self.assertNotEqual(
            relationship["relationship_id"],
            relationship["target_id"],
        )

    def test_06_relationship_identity_is_not_execution_identity(self):
        relationship = make_relationship(
            "O1",
            "execution",
            "E1",
            relationship_id="REL1",
        )

        self.assertNotEqual(
            relationship["relationship_id"],
            relationship["target_id"],
        )

    # ---------------------------------------------------------
    # 3. One observation can participate in multiple relationships
    # ---------------------------------------------------------

    def test_07_same_observation_can_reference_request_and_execution(self):
        observation = make_observation(
            observation_id="O1",
            request_id="R1",
            execution_id="E1",
            value="SUCCESS",
        )

        self.assertEqual(observation["request_id"], "R1")
        self.assertEqual(observation["execution_id"], "E1")

    def test_08_request_and_execution_membership_are_distinct_relationships(self):
        relationships = [
            make_relationship("O1", "request", "R1"),
            make_relationship("O1", "execution", "E1"),
        ]

        self.assertEqual(len(relationships), 2)
        self.assertNotEqual(
            relationships[0]["target_type"],
            relationships[1]["target_type"],
        )

    # ---------------------------------------------------------
    # 4. Relationship membership does not change semantic value
    # ---------------------------------------------------------

    def test_09_relationship_reference_does_not_change_observation_value(self):
        observation = make_observation(
            observation_id="O1",
            request_id="R1",
            value="ACCEPTED",
        )

        original_value = observation["value"]

        relationship = make_relationship(
            "O1",
            "request",
            "R1",
        )

        self.assertEqual(observation["value"], original_value)
        self.assertEqual(relationship["target_id"], "R1")

    def test_10_changing_membership_does_not_require_new_observation_concept(self):
        observation = make_observation(
            observation_id="O1",
            request_id="R1",
            value="ACCEPTED",
        )

        original_value = observation["value"]

        observation["request_id"] = "R2"

        self.assertEqual(observation["value"], original_value)
        self.assertEqual(observation["request_id"], "R2")

    # ---------------------------------------------------------
    # 5. Relationship can have attributes without proving
    #    dedicated relationship identity
    # ---------------------------------------------------------

    def test_11_relationship_can_have_attributes(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={
                "role": "source",
            },
        )

        self.assertEqual(
            relationship["attributes"]["role"],
            "source",
        )

    def test_12_relationship_attributes_are_distinct_from_endpoint_identity(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={
                "role": "source",
            },
        )

        self.assertEqual(relationship["target_id"], "R1")
        self.assertEqual(
            relationship["attributes"]["role"],
            "source",
        )

    # ---------------------------------------------------------
    # 6. Multiple observations can share the same relationship
    # ---------------------------------------------------------

    def test_13_multiple_observations_can_reference_same_request(self):
        observations = [
            make_observation(
                observation_id="O1",
                request_id="R1",
                value="ACCEPTED",
            ),
            make_observation(
                observation_id="O2",
                request_id="R1",
                value="RECONSIDERED",
            ),
        ]

        self.assertEqual(
            observations[0]["request_id"],
            observations[1]["request_id"],
        )

    def test_14_shared_request_does_not_make_observations_identical(self):
        observations = [
            make_observation(
                observation_id="O1",
                request_id="R1",
                value="ACCEPTED",
            ),
            make_observation(
                observation_id="O2",
                request_id="R1",
                value="REJECTED",
            ),
        ]

        self.assertNotEqual(
            observations[0]["observation_id"],
            observations[1]["observation_id"],
        )

        self.assertNotEqual(
            observations[0]["value"],
            observations[1]["value"],
        )

    # ---------------------------------------------------------
    # 7. Multiple relationship occurrences may require
    #    additional distinguishing information
    # ---------------------------------------------------------

    def test_15_same_endpoints_are_not_enough_when_occurrences_must_be_distinguished(self):
        relationship_a = make_relationship(
            "O1",
            "request",
            "R1",
        )

        relationship_b = make_relationship(
            "O1",
            "request",
            "R1",
        )

        endpoints_a = (
            relationship_a["observation_id"],
            relationship_a["target_type"],
            relationship_a["target_id"],
        )

        endpoints_b = (
            relationship_b["observation_id"],
            relationship_b["target_type"],
            relationship_b["target_id"],
        )

        self.assertEqual(endpoints_a, endpoints_b)

        # Endpoint references alone cannot distinguish
        # two otherwise identical relationship occurrences.

    def test_16_relationship_id_can_distinguish_same_endpoints(self):
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
            relationship_a["target_id"],
            relationship_b["target_id"],
        )

        self.assertNotEqual(
            relationship_a["relationship_id"],
            relationship_b["relationship_id"],
        )

    def test_17_sequence_can_distinguish_same_relationship_endpoints(self):
        relationship_a = {
            "observation_id": "O1",
            "target_type": "request",
            "target_id": "R1",
            "sequence": 1,
        }

        relationship_b = {
            "observation_id": "O1",
            "target_type": "request",
            "target_id": "R1",
            "sequence": 2,
        }

        self.assertEqual(
            relationship_a["target_id"],
            relationship_b["target_id"],
        )

        self.assertNotEqual(
            relationship_a["sequence"],
            relationship_b["sequence"],
        )

    # ---------------------------------------------------------
    # 8. Relationship distinction does not imply new semantic
    #    concept
    # ---------------------------------------------------------

    def test_18_distinguishing_relationship_occurrence_does_not_create_new_concept(self):
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
            relationship_a["target_type"],
            relationship_b["target_type"],
        )

        self.assertEqual(
            relationship_a["target_id"],
            relationship_b["target_id"],
        )

    # ---------------------------------------------------------
    # 9. Relationship identity is optional in the minimal model
    # ---------------------------------------------------------

    def test_19_minimal_relationship_does_not_require_identity(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
        )

        self.assertIsNone(
            relationship["relationship_id"]
        )

    def test_20_relationship_identity_can_be_added_without_changing_membership(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
        )

        original_membership = (
            relationship["observation_id"],
            relationship["target_type"],
            relationship["target_id"],
        )

        relationship["relationship_id"] = "REL1"

        self.assertEqual(
            (
                relationship["observation_id"],
                relationship["target_type"],
                relationship["target_id"],
            ),
            original_membership,
        )

    # ---------------------------------------------------------
    # 10. Relationship identity does not determine cardinality
    # ---------------------------------------------------------

    def test_21_relationship_identity_does_not_define_cardinality(self):
        relationships = [
            make_relationship(
                "O1",
                "request",
                "R1",
                relationship_id="REL1",
            ),
            make_relationship(
                "O2",
                "request",
                "R1",
                relationship_id="REL2",
            ),
        ]

        self.assertEqual(len(relationships), 2)

        self.assertEqual(
            relationships[0]["target_id"],
            relationships[1]["target_id"],
        )

    def test_22_cardinality_does_not_require_relationship_identity(self):
        relationships = [
            make_relationship("O1", "request", "R1"),
            make_relationship("O2", "request", "R1"),
        ]

        self.assertEqual(len(relationships), 2)

        self.assertTrue(
            all(
                relationship["relationship_id"] is None
                for relationship in relationships
            )
        )

    # ---------------------------------------------------------
    # 11. Relationship identity is not automatically lifecycle
    # ---------------------------------------------------------

    def test_23_relationship_identity_does_not_imply_lifecycle(self):
        relationship = make_relationship(
            "O1",
            "request",
            "R1",
            relationship_id="REL1",
        )

        self.assertEqual(
            relationship["relationship_id"],
            "REL1",
        )

        # Identity alone does not prove that the relationship
        # has lifecycle semantics.

    def test_24_relationship_can_be_distinguished_without_lifecycle_model(self):
        relationships = [
            {
                "observation_id": "O1",
                "target_type": "request",
                "target_id": "R1",
                "sequence": 1,
            },
            {
                "observation_id": "O1",
                "target_type": "request",
                "target_id": "R1",
                "sequence": 2,
            },
        ]

        self.assertNotEqual(
            relationships[0]["sequence"],
            relationships[1]["sequence"],
        )


if __name__ == "__main__":
    unittest.main()