import unittest


def make_relationship(
    observation_id,
    target_type,
    target_id,
    attributes=None,
    relationship_id=None,
):
    return {
        "relationship_id": relationship_id,
        "observation_id": observation_id,
        "target_type": target_type,
        "target_id": target_id,
        "attributes": attributes or {},
    }


class TestRelationshipAttributesIdentity(unittest.TestCase):

    # ---------------------------------------------------------
    # 1. Relationship attributes can exist without identity
    # ---------------------------------------------------------

    def test_01_relationship_can_have_attributes_without_identity(self):
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

    def test_02_multiple_attributes_can_exist_without_identity(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
                "priority": "high",
                "origin": "context-a",
            },
        )

        self.assertEqual(
            len(relationship["attributes"]),
            3,
        )

        self.assertIsNone(
            relationship["relationship_id"]
        )

    # ---------------------------------------------------------
    # 2. Attributes are distinct from endpoint identity
    # ---------------------------------------------------------

    def test_03_attribute_does_not_replace_observation_identity(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
            },
        )

        self.assertEqual(
            relationship["observation_id"],
            "O1",
        )

        self.assertEqual(
            relationship["attributes"]["role"],
            "source",
        )

    def test_04_attribute_does_not_replace_target_identity(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
            },
        )

        self.assertEqual(
            relationship["target_id"],
            "R1",
        )

        self.assertNotEqual(
            relationship["attributes"]["role"],
            relationship["target_id"],
        )

    # ---------------------------------------------------------
    # 3. Changing attributes does not inherently create
    #    relationship identity
    # ---------------------------------------------------------

    def test_05_attribute_change_can_preserve_same_endpoints(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
            },
        )

        original_endpoints = (
            relationship["observation_id"],
            relationship["target_type"],
            relationship["target_id"],
        )

        relationship["attributes"]["role"] = "target"

        new_endpoints = (
            relationship["observation_id"],
            relationship["target_type"],
            relationship["target_id"],
        )

        self.assertEqual(
            original_endpoints,
            new_endpoints,
        )

    def test_06_attribute_change_does_not_require_new_relationship_id(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
            },
        )

        relationship["attributes"]["role"] = "target"

        self.assertIsNone(
            relationship["relationship_id"]
        )

    # ---------------------------------------------------------
    # 4. Different attributes do not necessarily mean
    #    different relationships
    # ---------------------------------------------------------

    def test_07_same_endpoints_can_have_different_attribute_values(self):
        relationship_a = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
            },
        )

        relationship_b = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "target",
            },
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
            relationship_a["attributes"]["role"],
            relationship_b["attributes"]["role"],
        )

    def test_08_attribute_difference_does_not_prove_identity_difference(self):
        relationship_a = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "mode": "direct",
            },
        )

        relationship_b = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "mode": "queued",
            },
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

    # ---------------------------------------------------------
    # 5. Attributes may become distinguishing information
    # ---------------------------------------------------------

    def test_09_attribute_can_distinguish_relationship_occurrences(self):
        relationship_a = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "occurrence": 1,
            },
        )

        relationship_b = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "occurrence": 2,
            },
        )

        self.assertNotEqual(
            relationship_a["attributes"]["occurrence"],
            relationship_b["attributes"]["occurrence"],
        )

    def test_10_distinguishing_attribute_does_not_require_relationship_id(self):
        relationship_a = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "sequence": 1,
            },
        )

        relationship_b = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "sequence": 2,
            },
        )

        self.assertIsNone(
            relationship_a["relationship_id"]
        )

        self.assertIsNone(
            relationship_b["relationship_id"]
        )

    # ---------------------------------------------------------
    # 6. Relationship identity can be added independently
    # ---------------------------------------------------------

    def test_11_identity_can_be_added_without_changing_attributes(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
            },
        )

        original_attributes = dict(
            relationship["attributes"]
        )

        relationship["relationship_id"] = "REL1"

        self.assertEqual(
            relationship["attributes"],
            original_attributes,
        )

    def test_12_identity_can_be_added_without_changing_endpoints(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
        )

        original_endpoints = (
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
            original_endpoints,
        )

    # ---------------------------------------------------------
    # 7. Relationship identity and attributes are independent
    # ---------------------------------------------------------

    def test_13_relationship_identity_and_attributes_are_distinct_dimensions(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
            },
            relationship_id="REL1",
        )

        self.assertEqual(
            relationship["relationship_id"],
            "REL1",
        )

        self.assertEqual(
            relationship["attributes"]["role"],
            "source",
        )

        self.assertNotEqual(
            relationship["relationship_id"],
            relationship["attributes"]["role"],
        )

    def test_14_same_identity_can_have_multiple_attributes(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
                "mode": "direct",
            },
            relationship_id="REL1",
        )

        self.assertEqual(
            relationship["relationship_id"],
            "REL1",
        )

        self.assertEqual(
            len(relationship["attributes"]),
            2,
        )

    # ---------------------------------------------------------
    # 8. Attribute presence does not imply lifecycle
    # ---------------------------------------------------------

    def test_15_attributes_do_not_imply_relationship_lifecycle(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "status": "active",
            },
        )

        self.assertEqual(
            relationship["attributes"]["status"],
            "active",
        )

        self.assertIsNone(
            relationship["relationship_id"]
        )

    def test_16_attribute_named_status_does_not_prove_lifecycle(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "status": "active",
            },
        )

        self.assertIn(
            "status",
            relationship["attributes"],
        )

        # Attribute naming alone does not establish
        # lifecycle semantics.

    # ---------------------------------------------------------
    # 9. Attribute multiplicity does not imply identity
    # ---------------------------------------------------------

    def test_17_multiple_relationships_can_have_same_attribute_without_identity(self):
        relationships = [
            make_relationship(
                "O1",
                "request",
                "R1",
                attributes={"role": "source"},
            ),
            make_relationship(
                "O2",
                "request",
                "R1",
                attributes={"role": "source"},
            ),
        ]

        self.assertEqual(
            relationships[0]["attributes"],
            relationships[1]["attributes"],
        )

        self.assertIsNone(
            relationships[0]["relationship_id"]
        )

        self.assertIsNone(
            relationships[1]["relationship_id"]
        )

    def test_18_multiple_attributes_do_not_define_relationship_cardinality(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
                "mode": "direct",
                "priority": "high",
            },
        )

        self.assertEqual(
            len(relationship["attributes"]),
            3,
        )

        # Attribute count is not relationship cardinality.

    # ---------------------------------------------------------
    # 10. Independent relationship occurrences may require
    #     distinguishing information
    # ---------------------------------------------------------

    def test_19_same_endpoints_and_different_attributes_can_distinguish_occurrences(self):
        relationship_a = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={
                "sequence": 1,
            },
        )

        relationship_b = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={
                "sequence": 2,
            },
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
            relationship_a["attributes"]["sequence"],
            relationship_b["attributes"]["sequence"],
        )

    def test_20_identity_is_one_possible_distinguishing_mechanism(self):
        relationship_a = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"sequence": 1},
        )

        relationship_b = make_relationship(
            "O1",
            "request",
            "R1",
            attributes={"sequence": 2},
        )

        self.assertNotEqual(
            relationship_a["attributes"]["sequence"],
            relationship_b["attributes"]["sequence"],
        )

        relationship_a["relationship_id"] = "REL1"
        relationship_b["relationship_id"] = "REL2"

        self.assertNotEqual(
            relationship_a["relationship_id"],
            relationship_b["relationship_id"],
        )

    # ---------------------------------------------------------
    # 11. Attribute semantics do not automatically become
    #     identity semantics
    # ---------------------------------------------------------

    def test_21_attribute_value_does_not_automatically_become_identity(self):
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

    def test_22_attribute_change_does_not_automatically_create_new_identity(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
            },
        )

        relationship["attributes"]["role"] = "target"

        self.assertIsNone(
            relationship["relationship_id"]
        )

    # ---------------------------------------------------------
    # 12. Minimal relationship model remains possible
    # ---------------------------------------------------------

    def test_23_minimal_relationship_can_contain_endpoints_only(self):
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

        self.assertEqual(
            relationship["attributes"],
            {},
        )

        self.assertIsNone(
            relationship["relationship_id"]
        )

    def test_24_attributes_are_optional_in_minimal_model(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
        )

        self.assertEqual(
            relationship["attributes"],
            {},
        )

    def test_25_relationship_identity_is_optional_even_when_attributes_exist(self):
        relationship = make_relationship(
            observation_id="O1",
            target_type="request",
            target_id="R1",
            attributes={
                "role": "source",
                "mode": "direct",
            },
        )

        self.assertIsNone(
            relationship["relationship_id"]
        )

        self.assertEqual(
            relationship["attributes"]["role"],
            "source",
        )

        self.assertEqual(
            relationship["attributes"]["mode"],
            "direct",
        )


if __name__ == "__main__":
    unittest.main()