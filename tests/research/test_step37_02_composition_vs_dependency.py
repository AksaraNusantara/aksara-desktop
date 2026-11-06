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


class TestCompositionVsDependency(unittest.TestCase):

    def test_01_identity_and_state_coexist_without_intrinsic_dependency(self):
        model_a = make_model(entity_id="E1", state="ACTIVE")
        model_b = make_model(entity_id="E1", state="INACTIVE")

        self.assertEqual(model_a["entity_id"], model_b["entity_id"])
        self.assertNotEqual(model_a["state"], model_b["state"])

    def test_02_state_does_not_determine_identity(self):
        model_a = make_model(entity_id="E1", state="ACTIVE")
        model_b = make_model(entity_id="E2", state="ACTIVE")

        self.assertNotEqual(model_a["entity_id"], model_b["entity_id"])
        self.assertEqual(model_a["state"], model_b["state"])

    def test_03_identity_does_not_determine_state(self):
        model_a = make_model(entity_id="E1", state="ACTIVE")
        model_b = make_model(entity_id="E1", state="INACTIVE")

        self.assertEqual(model_a["entity_id"], model_b["entity_id"])
        self.assertNotEqual(model_a["state"], model_b["state"])

    def test_04_identity_and_value_can_vary_independently(self):
        model_a = make_model(entity_id="E1", value="A")
        model_b = make_model(entity_id="E1", value="B")

        self.assertEqual(model_a["entity_id"], model_b["entity_id"])
        self.assertNotEqual(model_a["value"], model_b["value"])

    def test_05_same_value_can_exist_with_different_identity(self):
        model_a = make_model(entity_id="E1", value="A")
        model_b = make_model(entity_id="E2", value="A")

        self.assertNotEqual(model_a["entity_id"], model_b["entity_id"])
        self.assertEqual(model_a["value"], model_b["value"])

    def test_06_identity_and_sequence_can_vary_independently(self):
        model_a = make_model(entity_id="E1", sequence=1)
        model_b = make_model(entity_id="E1", sequence=2)

        self.assertEqual(model_a["entity_id"], model_b["entity_id"])
        self.assertNotEqual(model_a["sequence"], model_b["sequence"])

    def test_07_same_sequence_can_exist_with_different_identity(self):
        model_a = make_model(entity_id="E1", sequence=1)
        model_b = make_model(entity_id="E2", sequence=1)

        self.assertNotEqual(model_a["entity_id"], model_b["entity_id"])
        self.assertEqual(model_a["sequence"], model_b["sequence"])

    def test_08_identity_and_attributes_can_vary_independently(self):
        model_a = make_model(
            entity_id="E1",
            attributes={"mode": "direct"},
        )
        model_b = make_model(
            entity_id="E1",
            attributes={"mode": "queued"},
        )

        self.assertEqual(model_a["entity_id"], model_b["entity_id"])
        self.assertNotEqual(
            model_a["attributes"],
            model_b["attributes"],
        )

    def test_09_same_attributes_can_exist_with_different_identity(self):
        attributes = {"mode": "direct"}

        model_a = make_model(
            entity_id="E1",
            attributes=attributes,
        )
        model_b = make_model(
            entity_id="E2",
            attributes=attributes,
        )

        self.assertNotEqual(model_a["entity_id"], model_b["entity_id"])
        self.assertEqual(model_a["attributes"], model_b["attributes"])

    def test_10_request_identity_and_decision_can_vary_independently(self):
        model_a = make_model(
            request_id="R1",
            decision="ACCEPT",
        )
        model_b = make_model(
            request_id="R1",
            decision="REJECT",
        )

        self.assertEqual(model_a["request_id"], model_b["request_id"])
        self.assertNotEqual(model_a["decision"], model_b["decision"])

    def test_11_same_decision_can_exist_for_different_requests(self):
        model_a = make_model(
            request_id="R1",
            decision="ACCEPT",
        )
        model_b = make_model(
            request_id="R2",
            decision="ACCEPT",
        )

        self.assertNotEqual(model_a["request_id"], model_b["request_id"])
        self.assertEqual(model_a["decision"], model_b["decision"])

    def test_12_relationship_and_attributes_can_vary_independently(self):
        model_a = make_model(
            relationship={"target_id": "R1"},
            attributes={"role": "source"},
        )
        model_b = make_model(
            relationship={"target_id": "R1"},
            attributes={"role": "target"},
        )

        self.assertEqual(
            model_a["relationship"],
            model_b["relationship"],
        )
        self.assertNotEqual(
            model_a["attributes"],
            model_b["attributes"],
        )

    def test_13_same_attributes_can_exist_with_different_relationship(self):
        attributes = {"role": "source"}

        model_a = make_model(
            relationship={"target_id": "R1"},
            attributes=attributes,
        )
        model_b = make_model(
            relationship={"target_id": "R2"},
            attributes=attributes,
        )

        self.assertNotEqual(
            model_a["relationship"],
            model_b["relationship"],
        )
        self.assertEqual(
            model_a["attributes"],
            model_b["attributes"],
        )

    def test_14_state_and_decision_can_vary_independently(self):
        model_a = make_model(
            state="ACTIVE",
            decision="ACCEPT",
        )
        model_b = make_model(
            state="INACTIVE",
            decision="ACCEPT",
        )

        self.assertNotEqual(model_a["state"], model_b["state"])
        self.assertEqual(model_a["decision"], model_b["decision"])

    def test_15_same_state_can_exist_with_different_decision(self):
        model_a = make_model(
            state="ACTIVE",
            decision="ACCEPT",
        )
        model_b = make_model(
            state="ACTIVE",
            decision="REJECT",
        )

        self.assertEqual(model_a["state"], model_b["state"])
        self.assertNotEqual(model_a["decision"], model_b["decision"])

    def test_16_cardinality_does_not_determine_identity(self):
        models_a = [
            make_model(entity_id="E1"),
        ]

        models_b = [
            make_model(entity_id="E1"),
            make_model(entity_id="E2"),
        ]

        self.assertEqual(len(models_a), 1)
        self.assertEqual(len(models_b), 2)
        self.assertEqual(models_a[0]["entity_id"], "E1")
        self.assertEqual(models_b[0]["entity_id"], "E1")

    def test_17_identity_does_not_determine_cardinality(self):
        models_a = [
            make_model(entity_id="E1"),
        ]

        models_b = [
            make_model(entity_id="E1"),
            make_model(entity_id="E1"),
        ]

        self.assertEqual(len(models_a), 1)
        self.assertEqual(len(models_b), 2)

    def test_18_ordering_does_not_determine_identity(self):
        model_a = make_model(entity_id="E1", sequence=1)
        model_b = make_model(entity_id="E2", sequence=1)

        self.assertNotEqual(model_a["entity_id"], model_b["entity_id"])
        self.assertEqual(model_a["sequence"], model_b["sequence"])

    def test_19_identity_does_not_determine_ordering(self):
        model_a = make_model(entity_id="E1", sequence=1)
        model_b = make_model(entity_id="E1", sequence=2)

        self.assertEqual(model_a["entity_id"], model_b["entity_id"])
        self.assertNotEqual(model_a["sequence"], model_b["sequence"])

    def test_20_composition_does_not_imply_dependency(self):
        model = make_model(
            entity_id="E1",
            state="ACTIVE",
            value="A",
            sequence=1,
            attributes={"mode": "direct"},
            decision="ACCEPT",
        )

        self.assertEqual(model["entity_id"], "E1")
        self.assertEqual(model["state"], "ACTIVE")
        self.assertEqual(model["value"], "A")
        self.assertEqual(model["sequence"], 1)
        self.assertEqual(model["attributes"]["mode"], "direct")
        self.assertEqual(model["decision"], "ACCEPT")

    def test_21_dependency_requires_semantic_rule(self):
        model = make_model(
            entity_id="E1",
            state="ACTIVE",
        )

        # Coexistence alone does not establish:
        # entity_id -> state
        self.assertEqual(model["entity_id"], "E1")
        self.assertEqual(model["state"], "ACTIVE")

    def test_22_context_can_define_dependency_without_identity_collapse(self):
        model = make_model(
            entity_id="E1",
            state="ACTIVE",
        )

        context_rule = {
            "state_depends_on_identity": True,
        }

        self.assertTrue(context_rule["state_depends_on_identity"])
        self.assertEqual(model["entity_id"], "E1")
        self.assertEqual(model["state"], "ACTIVE")

    def test_23_contextual_dependency_is_not_intrinsic_dependency(self):
        model = make_model(
            entity_id="E1",
            decision="ACCEPT",
        )

        contextual_rule = {
            "decision_uses_request_identity": True,
        }

        self.assertTrue(contextual_rule["decision_uses_request_identity"])
        self.assertEqual(model["request_id"], None)
        self.assertEqual(model["decision"], "ACCEPT")

    def test_24_dependency_does_not_require_identity_fusion(self):
        model = make_model(
            entity_id="E1",
            request_id="R1",
            decision="ACCEPT",
        )

        self.assertEqual(model["entity_id"], "E1")
        self.assertEqual(model["request_id"], "R1")
        self.assertEqual(model["decision"], "ACCEPT")
        self.assertNotEqual(model["entity_id"], model["request_id"])

    def test_25_dependency_does_not_require_composite_identity(self):
        model = make_model(
            entity_id="E1",
            request_id="R1",
            decision="ACCEPT",
        )

        composite_value = (
            model["entity_id"],
            model["request_id"],
            model["decision"],
        )

        self.assertEqual(
            composite_value,
            ("E1", "R1", "ACCEPT"),
        )
        self.assertNotEqual(
            composite_value,
            model["entity_id"],
        )

    def test_26_dependency_does_not_create_lifecycle_automatically(self):
        model = make_model(
            entity_id="E1",
            state="ACTIVE",
            decision="ACCEPT",
        )

        self.assertEqual(model["state"], "ACTIVE")
        self.assertEqual(model["decision"], "ACCEPT")

    def test_27_composition_dependency_and_identity_remain_distinct(self):
        model = make_model(
            entity_id="E1",
            request_id="R1",
            state="ACTIVE",
            decision="ACCEPT",
        )

        self.assertEqual(model["entity_id"], "E1")
        self.assertEqual(model["request_id"], "R1")
        self.assertEqual(model["state"], "ACTIVE")
        self.assertEqual(model["decision"], "ACCEPT")

        self.assertNotEqual(model["entity_id"], model["request_id"])
        self.assertNotEqual(model["state"], model["decision"])

    def test_28_final_boundary_composition_is_not_dependency(self):
        model = make_model(
            entity_id="E1",
            request_id="R1",
            execution_id="X1",
            value="A",
            state="ACTIVE",
            sequence=1,
            attributes={"mode": "direct"},
            relationship={"target_id": "R1"},
            decision="ACCEPT",
        )

        self.assertEqual(model["entity_id"], "E1")
        self.assertEqual(model["request_id"], "R1")
        self.assertEqual(model["execution_id"], "X1")
        self.assertEqual(model["value"], "A")
        self.assertEqual(model["state"], "ACTIVE")
        self.assertEqual(model["sequence"], 1)
        self.assertEqual(model["attributes"]["mode"], "direct")
        self.assertEqual(
            model["relationship"]["target_id"],
            "R1",
        )
        self.assertEqual(model["decision"], "ACCEPT")