import unittest


def make_model(
    entity_id=None,
    request_id=None,
    execution_id=None,
    value=None,
    state=None,
    sequence=None,
    attributes=None,
    relationship=None,
    decision=None,
):
    return {
        "entity_id": entity_id,
        "request_id": request_id,
        "execution_id": execution_id,
        "value": value,
        "state": state,
        "sequence": sequence,
        "attributes": attributes or {},
        "relationship": relationship,
        "decision": decision,
    }


class TestSemanticDimensionCoexistence(unittest.TestCase):

    # ---------------------------------------------------------
    # 1. Multiple dimensions can coexist
    # ---------------------------------------------------------

    def test_01_identity_and_state_can_coexist(self):
        model = make_model(
            entity_id="E1",
            state="ACTIVE",
        )

        self.assertEqual(model["entity_id"], "E1")
        self.assertEqual(model["state"], "ACTIVE")

    def test_02_identity_and_value_can_coexist(self):
        model = make_model(
            entity_id="E1",
            value="A",
        )

        self.assertEqual(model["entity_id"], "E1")
        self.assertEqual(model["value"], "A")

    def test_03_identity_and_ordering_can_coexist(self):
        model = make_model(
            entity_id="E1",
            sequence=1,
        )

        self.assertEqual(model["entity_id"], "E1")
        self.assertEqual(model["sequence"], 1)

    def test_04_identity_and_attributes_can_coexist(self):
        model = make_model(
            entity_id="E1",
            attributes={
                "mode": "direct",
            },
        )

        self.assertEqual(model["entity_id"], "E1")
        self.assertEqual(
            model["attributes"]["mode"],
            "direct",
        )

    # ---------------------------------------------------------
    # 2. Coexistence does not collapse dimensions
    # ---------------------------------------------------------

    def test_05_state_does_not_become_identity(self):
        model = make_model(
            entity_id="E1",
            state="ACTIVE",
        )

        self.assertNotEqual(
            model["entity_id"],
            model["state"],
        )

    def test_06_sequence_does_not_become_identity(self):
        model = make_model(
            entity_id="E1",
            sequence=1,
        )

        self.assertNotEqual(
            model["entity_id"],
            model["sequence"],
        )

    def test_07_attribute_does_not_become_identity(self):
        model = make_model(
            entity_id="E1",
            attributes={
                "mode": "direct",
            },
        )

        self.assertNotEqual(
            model["entity_id"],
            model["attributes"]["mode"],
        )

    def test_08_value_does_not_become_identity(self):
        model = make_model(
            entity_id="E1",
            value="A",
        )

        self.assertNotEqual(
            model["entity_id"],
            model["value"],
        )

    # ---------------------------------------------------------
    # 3. Request and execution dimensions can coexist
    # ---------------------------------------------------------

    def test_09_request_and_execution_identity_can_coexist(self):
        model = make_model(
            request_id="R1",
            execution_id="E1",
        )

        self.assertEqual(model["request_id"], "R1")
        self.assertEqual(model["execution_id"], "E1")

        self.assertNotEqual(
            model["request_id"],
            model["execution_id"],
        )

    def test_10_execution_identity_does_not_replace_request_identity(self):
        model = make_model(
            request_id="R1",
            execution_id="E1",
        )

        self.assertEqual(model["request_id"], "R1")
        self.assertEqual(model["execution_id"], "E1")

    # ---------------------------------------------------------
    # 4. Cardinality can be represented independently
    # ---------------------------------------------------------

    def test_11_multiple_models_can_share_request_identity(self):
        models = [
            make_model(
                entity_id="O1",
                request_id="R1",
            ),
            make_model(
                entity_id="O2",
                request_id="R1",
            ),
        ]

        self.assertEqual(
            len(models),
            2,
        )

        self.assertEqual(
            models[0]["request_id"],
            models[1]["request_id"],
        )

        self.assertNotEqual(
            models[0]["entity_id"],
            models[1]["entity_id"],
        )

    def test_12_cardinality_does_not_collapse_identity(self):
        models = [
            make_model(
                entity_id="O1",
                request_id="R1",
            ),
            make_model(
                entity_id="O2",
                request_id="R1",
            ),
        ]

        self.assertEqual(
            len(models),
            2,
        )

        self.assertNotEqual(
            models[0]["entity_id"],
            models[1]["entity_id"],
        )

    # ---------------------------------------------------------
    # 5. Ordering remains independent
    # ---------------------------------------------------------

    def test_13_same_identity_can_have_multiple_ordered_observations(self):
        observations = [
            make_model(
                entity_id="E1",
                sequence=1,
            ),
            make_model(
                entity_id="E1",
                sequence=2,
            ),
        ]

        self.assertEqual(
            observations[0]["entity_id"],
            observations[1]["entity_id"],
        )

        self.assertNotEqual(
            observations[0]["sequence"],
            observations[1]["sequence"],
        )

    def test_14_sequence_change_does_not_require_identity_change(self):
        model = make_model(
            entity_id="E1",
            sequence=1,
        )

        original_identity = model["entity_id"]

        model["sequence"] = 2

        self.assertEqual(
            model["entity_id"],
            original_identity,
        )

    # ---------------------------------------------------------
    # 6. Relationship can coexist with identity and attributes
    # ---------------------------------------------------------

    def test_15_relationship_can_coexist_with_identity(self):
        model = make_model(
            entity_id="O1",
            relationship={
                "target_type": "request",
                "target_id": "R1",
            },
        )

        self.assertEqual(
            model["entity_id"],
            "O1",
        )

        self.assertEqual(
            model["relationship"]["target_id"],
            "R1",
        )

    def test_16_relationship_can_coexist_with_attributes(self):
        model = make_model(
            entity_id="O1",
            relationship={
                "target_type": "request",
                "target_id": "R1",
            },
            attributes={
                "role": "source",
            },
        )

        self.assertEqual(
            model["relationship"]["target_id"],
            "R1",
        )

        self.assertEqual(
            model["attributes"]["role"],
            "source",
        )

    # ---------------------------------------------------------
    # 7. Decision can coexist with other dimensions
    # ---------------------------------------------------------

    def test_17_decision_can_coexist_with_request_identity(self):
        model = make_model(
            request_id="R1",
            decision="ACCEPT",
        )

        self.assertEqual(model["request_id"], "R1")
        self.assertEqual(model["decision"], "ACCEPT")

    def test_18_decision_does_not_become_request_identity(self):
        model = make_model(
            request_id="R1",
            decision="ACCEPT",
        )

        self.assertNotEqual(
            model["request_id"],
            model["decision"],
        )

    # ---------------------------------------------------------
    # 8. Changing one dimension need not change others
    # ---------------------------------------------------------

    def test_19_state_change_need_not_change_identity(self):
        model = make_model(
            entity_id="E1",
            state="ACTIVE",
            value="A",
        )

        model["state"] = "INACTIVE"

        self.assertEqual(
            model["entity_id"],
            "E1",
        )

        self.assertEqual(
            model["value"],
            "A",
        )

    def test_20_attribute_change_need_not_change_state(self):
        model = make_model(
            entity_id="E1",
            state="ACTIVE",
            attributes={
                "mode": "direct",
            },
        )

        model["attributes"]["mode"] = "queued"

        self.assertEqual(
            model["state"],
            "ACTIVE",
        )

    # ---------------------------------------------------------
    # 9. Composition does not imply composite identity
    # ---------------------------------------------------------

    def test_21_multiple_dimensions_do_not_require_composite_identity(self):
        model = make_model(
            entity_id="E1",
            request_id="R1",
            execution_id="X1",
            state="ACTIVE",
            sequence=1,
            attributes={
                "mode": "direct",
            },
        )

        self.assertEqual(model["entity_id"], "E1")
        self.assertEqual(model["request_id"], "R1")
        self.assertEqual(model["execution_id"], "X1")
        self.assertEqual(model["state"], "ACTIVE")
        self.assertEqual(model["sequence"], 1)

    def test_22_composite_representation_is_not_same_as_composite_identity(self):
        model = make_model(
            entity_id="E1",
            request_id="R1",
            execution_id="X1",
        )

        composite_value = (
            model["entity_id"],
            model["request_id"],
            model["execution_id"],
        )

        self.assertEqual(
            composite_value,
            ("E1", "R1", "X1"),
        )

        self.assertNotEqual(
            composite_value,
            model["entity_id"],
        )

    # ---------------------------------------------------------
    # 10. Dimension composition remains contextual
    # ---------------------------------------------------------

    def test_23_same_identity_can_appear_with_different_contextual_dimensions(self):
        model_a = make_model(
            entity_id="E1",
            state="ACTIVE",
            sequence=1,
        )

        model_b = make_model(
            entity_id="E1",
            state="INACTIVE",
            sequence=2,
        )

        self.assertEqual(
            model_a["entity_id"],
            model_b["entity_id"],
        )

        self.assertNotEqual(
            model_a["state"],
            model_b["state"],
        )

        self.assertNotEqual(
            model_a["sequence"],
            model_b["sequence"],
        )

    def test_24_contextual_difference_does_not_require_new_identity(self):
        model = make_model(
            entity_id="E1",
            state="ACTIVE",
            sequence=1,
        )

        model["state"] = "INACTIVE"
        model["sequence"] = 2

        self.assertEqual(
            model["entity_id"],
            "E1",
        )

    # ---------------------------------------------------------
    # 11. Composition does not imply lifecycle
    # ---------------------------------------------------------

    def test_25_multiple_dimensions_do_not_create_lifecycle_automatically(self):
        model = make_model(
            entity_id="E1",
            state="ACTIVE",
            sequence=1,
            decision="ACCEPT",
        )

        self.assertEqual(model["state"], "ACTIVE")
        self.assertEqual(model["sequence"], 1)
        self.assertEqual(model["decision"], "ACCEPT")

        # Coexistence alone does not establish lifecycle semantics.

    def test_26_decision_and_state_remain_distinct(self):
        model = make_model(
            entity_id="E1",
            state="ACTIVE",
            decision="ACCEPT",
        )

        self.assertNotEqual(
            model["state"],
            model["decision"],
        )

    # ---------------------------------------------------------
    # 12. Final composition boundaries
    # ---------------------------------------------------------

    def test_27_composition_does_not_collapse_identity_and_attribute(self):
        model = make_model(
            entity_id="E1",
            attributes={
                "mode": "direct",
            },
        )

        self.assertNotEqual(
            model["entity_id"],
            model["attributes"]["mode"],
        )

    def test_28_composition_does_not_collapse_identity_and_state(self):
        model = make_model(
            entity_id="E1",
            state="ACTIVE",
        )

        self.assertNotEqual(
            model["entity_id"],
            model["state"],
        )

    def test_29_composition_does_not_collapse_identity_and_ordering(self):
        model = make_model(
            entity_id="E1",
            sequence=1,
        )

        self.assertNotEqual(
            model["entity_id"],
            model["sequence"],
        )

    def test_30_composition_does_not_collapse_relationship_and_identity(self):
        model = make_model(
            entity_id="E1",
            relationship={
                "target_type": "request",
                "target_id": "R1",
            },
        )

        self.assertNotEqual(
            model["entity_id"],
            model["relationship"]["target_id"],
        )

    def test_31_composition_does_not_collapse_decision_and_identity(self):
        model = make_model(
            entity_id="E1",
            decision="ACCEPT",
        )

        self.assertNotEqual(
            model["entity_id"],
            model["decision"],
        )

    def test_32_composition_preserves_dimension_boundaries(self):
        model = make_model(
            entity_id="E1",
            request_id="R1",
            execution_id="X1",
            value="A",
            state="ACTIVE",
            sequence=1,
            attributes={
                "mode": "direct",
            },
            relationship={
                "target_type": "request",
                "target_id": "R1",
            },
            decision="ACCEPT",
        )

        self.assertEqual(model["entity_id"], "E1")
        self.assertEqual(model["request_id"], "R1")
        self.assertEqual(model["execution_id"], "X1")
        self.assertEqual(model["value"], "A")
        self.assertEqual(model["state"], "ACTIVE")
        self.assertEqual(model["sequence"], 1)
        self.assertEqual(
            model["attributes"]["mode"],
            "direct",
        )
        self.assertEqual(
            model["relationship"]["target_id"],
            "R1",
        )
        self.assertEqual(model["decision"], "ACCEPT")


if __name__ == "__main__":
    unittest.main()