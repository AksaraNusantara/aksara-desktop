import unittest


def make_dimension(name, value):
    return {
        "name": name,
        "value": value,
    }


def make_constraint(name, rule):
    return {
        "name": name,
        "rule": rule,
    }


class TestConstraintVsDimension(unittest.TestCase):

    def test_01_constraint_can_coexist_with_identity(self):
        identity = make_dimension("identity", "E1")
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        self.assertEqual(identity["name"], "identity")
        self.assertEqual(identity["value"], "E1")
        self.assertEqual(
            constraint["name"],
            "identity_required",
        )

    def test_02_constraint_can_coexist_with_state(self):
        state = make_dimension("state", "ACTIVE")
        constraint = make_constraint(
            "active_only",
            "state_must_be_active",
        )

        self.assertEqual(state["value"], "ACTIVE")
        self.assertEqual(
            constraint["rule"],
            "state_must_be_active",
        )

    def test_03_constraint_can_coexist_with_value(self):
        value = make_dimension("value", "A")
        constraint = make_constraint(
            "value_required",
            "value_must_exist",
        )

        self.assertEqual(value["value"], "A")
        self.assertEqual(
            constraint["name"],
            "value_required",
        )

    def test_04_constraint_can_coexist_with_ordering(self):
        ordering = make_dimension("sequence", 1)
        constraint = make_constraint(
            "ordered",
            "sequence_must_be_positive",
        )

        self.assertEqual(ordering["value"], 1)
        self.assertEqual(
            constraint["rule"],
            "sequence_must_be_positive",
        )

    def test_05_constraint_can_coexist_with_attributes(self):
        attributes = make_dimension(
            "attributes",
            {"mode": "direct"},
        )
        constraint = make_constraint(
            "mode_required",
            "mode_must_exist",
        )

        self.assertEqual(
            attributes["value"]["mode"],
            "direct",
        )
        self.assertEqual(
            constraint["name"],
            "mode_required",
        )

    def test_06_constraint_is_not_identity(self):
        identity = make_dimension("identity", "E1")
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        self.assertNotEqual(
            identity["value"],
            constraint["name"],
        )

    def test_07_constraint_is_not_state(self):
        state = make_dimension("state", "ACTIVE")
        constraint = make_constraint(
            "active_only",
            "state_must_be_active",
        )

        self.assertNotEqual(
            state["value"],
            constraint["name"],
        )

    def test_08_constraint_is_not_value(self):
        value = make_dimension("value", "A")
        constraint = make_constraint(
            "value_required",
            "value_must_exist",
        )

        self.assertNotEqual(
            value["value"],
            constraint["name"],
        )

    def test_09_constraint_is_not_ordering(self):
        ordering = make_dimension("sequence", 1)
        constraint = make_constraint(
            "ordered",
            "sequence_must_be_positive",
        )

        self.assertNotEqual(
            ordering["value"],
            constraint["name"],
        )

    def test_10_constraint_is_not_attribute(self):
        attributes = make_dimension(
            "attributes",
            {"mode": "direct"},
        )
        constraint = make_constraint(
            "mode_required",
            "mode_must_exist",
        )

        self.assertNotEqual(
            attributes["name"],
            constraint["name"],
        )

    def test_11_constraint_does_not_replace_dimension_identity(self):
        identity = make_dimension("identity", "E1")
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        self.assertEqual(identity["value"], "E1")
        self.assertEqual(
            constraint["name"],
            "identity_required",
        )

    def test_12_constraint_does_not_replace_dimension_state(self):
        state = make_dimension("state", "ACTIVE")
        constraint = make_constraint(
            "active_only",
            "state_must_be_active",
        )

        self.assertEqual(state["value"], "ACTIVE")
        self.assertEqual(
            constraint["rule"],
            "state_must_be_active",
        )

    def test_13_constraint_does_not_create_composite_identity(self):
        identity = make_dimension("identity", "E1")
        state = make_dimension("state", "ACTIVE")

        constraint = make_constraint(
            "active_only",
            "state_must_be_active",
        )

        composite = (
            identity["value"],
            state["value"],
            constraint["name"],
        )

        self.assertNotEqual(
            composite,
            identity["value"],
        )
        self.assertNotEqual(
            composite,
            state["value"],
        )

    def test_14_multiple_constraints_can_coexist(self):
        constraints = [
            make_constraint(
                "identity_required",
                "identity_must_exist",
            ),
            make_constraint(
                "state_required",
                "state_must_exist",
            ),
            make_constraint(
                "value_required",
                "value_must_exist",
            ),
        ]

        self.assertEqual(len(constraints), 3)
        self.assertEqual(
            constraints[0]["name"],
            "identity_required",
        )
        self.assertEqual(
            constraints[1]["name"],
            "state_required",
        )
        self.assertEqual(
            constraints[2]["name"],
            "value_required",
        )

    def test_15_constraint_collection_is_not_dimension(self):
        state = make_dimension("state", "ACTIVE")

        constraints = [
            make_constraint(
                "active_only",
                "state_must_be_active",
            ),
            make_constraint(
                "identity_required",
                "identity_must_exist",
            ),
        ]

        self.assertEqual(state["name"], "state")
        self.assertEqual(len(constraints), 2)
        self.assertNotEqual(
            state["name"],
            constraints[0]["name"],
        )

    def test_16_constraint_can_reference_dimension(self):
        identity = make_dimension("identity", "E1")

        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        self.assertEqual(identity["name"], "identity")
        self.assertEqual(
            constraint["rule"],
            "identity_must_exist",
        )

    def test_17_reference_does_not_make_constraint_dimension(self):
        identity = make_dimension("identity", "E1")

        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        self.assertEqual(
            constraint["rule"],
            "identity_must_exist",
        )
        self.assertNotEqual(
            constraint["name"],
            identity["name"],
        )

    def test_18_constraint_can_reference_multiple_dimensions(self):
        identity = make_dimension("identity", "E1")
        state = make_dimension("state", "ACTIVE")

        constraint = make_constraint(
            "identity_state",
            "identity_exists_and_state_is_active",
        )

        self.assertEqual(identity["name"], "identity")
        self.assertEqual(state["name"], "state")
        self.assertEqual(
            constraint["name"],
            "identity_state",
        )

    def test_19_constraint_can_describe_relationship_between_dimensions(self):
        request = make_dimension("request", "R1")
        decision = make_dimension("decision", "ACCEPT")

        constraint = make_constraint(
            "request_decision",
            "decision_requires_request",
        )

        self.assertEqual(request["name"], "request")
        self.assertEqual(decision["name"], "decision")
        self.assertEqual(
            constraint["rule"],
            "decision_requires_request",
        )

    def test_20_constraint_does_not_become_relationship(self):
        request = make_dimension("request", "R1")
        decision = make_dimension("decision", "ACCEPT")

        constraint = make_constraint(
            "request_decision",
            "decision_requires_request",
        )

        relationship = {
            "source": request["name"],
            "target": decision["name"],
        }

        self.assertEqual(
            relationship["source"],
            "request",
        )
        self.assertEqual(
            relationship["target"],
            "decision",
        )
        self.assertNotEqual(
            constraint["name"],
            relationship["source"],
        )
        self.assertNotEqual(
            constraint["name"],
            relationship["target"],
        )

    def test_21_constraint_does_not_create_lifecycle(self):
        state = make_dimension("state", "ACTIVE")

        constraint = make_constraint(
            "active_only",
            "state_must_be_active",
        )

        self.assertEqual(state["value"], "ACTIVE")
        self.assertEqual(
            constraint["rule"],
            "state_must_be_active",
        )

    def test_22_constraint_does_not_create_ordering(self):
        constraint = make_constraint(
            "ordered",
            "sequence_must_be_positive",
        )

        self.assertNotIn(
            "sequence",
            constraint,
        )

    def test_23_constraint_can_exist_without_evaluation(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        self.assertEqual(
            constraint["name"],
            "identity_required",
        )

    def test_24_constraint_is_not_evaluation_result(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        evaluation_result = "SATISFIED"

        self.assertEqual(
            constraint["name"],
            "identity_required",
        )
        self.assertNotEqual(
            constraint["name"],
            evaluation_result,
        )

    def test_25_constraint_can_coexist_with_relationship(self):
        relationship = {
            "source": "request",
            "target": "decision",
            "relation": "uses_as_input",
        }

        constraint = make_constraint(
            "decision_input",
            "request_must_exist",
        )

        self.assertEqual(
            relationship["relation"],
            "uses_as_input",
        )
        self.assertEqual(
            constraint["rule"],
            "request_must_exist",
        )

    def test_26_constraint_does_not_replace_relationship(self):
        relationship = {
            "source": "request",
            "target": "decision",
            "relation": "uses_as_input",
        }

        constraint = make_constraint(
            "decision_input",
            "request_must_exist",
        )

        self.assertEqual(
            relationship["source"],
            "request",
        )
        self.assertEqual(
            relationship["target"],
            "decision",
        )
        self.assertNotEqual(
            relationship["relation"],
            constraint["name"],
        )

    def test_27_constraint_can_be_contextual(self):
        constraint = make_constraint(
            "strict_request",
            "request_must_exist",
        )

        context = {
            "policy": "STRICT",
            "constraint": constraint,
        }

        self.assertEqual(
            context["policy"],
            "STRICT",
        )
        self.assertEqual(
            context["constraint"],
            constraint,
        )

    def test_28_context_does_not_make_constraint_identity(self):
        constraint = make_constraint(
            "strict_request",
            "request_must_exist",
        )

        context = {
            "policy": "STRICT",
            "constraint": constraint,
        }

        context_id = "CTX-1"

        self.assertEqual(
            context["constraint"],
            constraint,
        )
        self.assertNotEqual(
            context_id,
            constraint["name"],
        )

    def test_29_constraint_can_remain_stable_while_context_changes(self):
        constraint = make_constraint(
            "request_required",
            "request_must_exist",
        )

        context_a = {
            "policy": "STRICT",
            "constraint": constraint,
        }

        context_b = {
            "policy": "LENIENT",
            "constraint": constraint,
        }

        self.assertEqual(
            context_a["constraint"],
            context_b["constraint"],
        )
        self.assertNotEqual(
            context_a["policy"],
            context_b["policy"],
        )

    def test_30_final_boundary_constraint_is_distinct_from_dimension(self):
        identity = make_dimension("identity", "E1")
        state = make_dimension("state", "ACTIVE")

        constraint = make_constraint(
            "identity_state",
            "identity_exists_and_state_is_active",
        )

        self.assertEqual(identity["name"], "identity")
        self.assertEqual(state["name"], "state")
        self.assertEqual(
            constraint["name"],
            "identity_state",
        )

        self.assertNotEqual(
            constraint["name"],
            identity["name"],
        )
        self.assertNotEqual(
            constraint["name"],
            state["name"],
        )


if __name__ == "__main__":
    unittest.main()