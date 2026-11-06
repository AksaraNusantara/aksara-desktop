import unittest


def make_dimension(name, value):
    return {
        "name": name,
        "value": value,
    }


def make_dependency(source, target, relation="depends_on"):
    return {
        "source": source,
        "target": target,
        "relation": relation,
    }


class TestDependencyAsRelationship(unittest.TestCase):

    def test_01_dependency_can_be_represented_as_relationship(self):
        identity = make_dimension("identity", "E1")
        state = make_dimension("state", "ACTIVE")

        dependency = make_dependency(
            source="identity",
            target="state",
        )

        self.assertEqual(dependency["source"], identity["name"])
        self.assertEqual(dependency["target"], state["name"])

    def test_02_dependency_is_distinct_from_source_dimension(self):
        identity = make_dimension("identity", "E1")

        dependency = make_dependency(
            source="identity",
            target="state",
        )

        self.assertNotEqual(
            dependency["relation"],
            identity["value"],
        )

    def test_03_dependency_is_distinct_from_target_dimension(self):
        state = make_dimension("state", "ACTIVE")

        dependency = make_dependency(
            source="identity",
            target="state",
        )

        self.assertNotEqual(
            dependency["relation"],
            state["value"],
        )

    def test_04_dependency_does_not_replace_dimension_identity(self):
        identity = make_dimension("identity", "E1")
        state = make_dimension("state", "ACTIVE")

        dependency = make_dependency(
            source="identity",
            target="state",
        )

        self.assertEqual(identity["value"], "E1")
        self.assertEqual(state["value"], "ACTIVE")
        self.assertEqual(dependency["source"], "identity")
        self.assertEqual(dependency["target"], "state")

    def test_05_dependency_can_exist_without_identity_fusion(self):
        identity = make_dimension("identity", "E1")
        state = make_dimension("state", "ACTIVE")

        dependency = make_dependency(
            source="identity",
            target="state",
        )

        self.assertNotEqual(identity["value"], state["value"])
        self.assertEqual(dependency["relation"], "depends_on")

    def test_06_dependency_relationship_can_change_without_identity_change(self):
        identity = make_dimension("identity", "E1")
        state = make_dimension("state", "ACTIVE")

        dependency_a = make_dependency(
            source="identity",
            target="state",
            relation="depends_on",
        )

        dependency_b = make_dependency(
            source="identity",
            target="state",
            relation="conditionally_depends_on",
        )

        self.assertEqual(identity["value"], "E1")
        self.assertEqual(state["value"], "ACTIVE")
        self.assertNotEqual(
            dependency_a["relation"],
            dependency_b["relation"],
        )

    def test_07_same_dimensions_can_have_different_dependency_contexts(self):
        identity = make_dimension("identity", "E1")
        state = make_dimension("state", "ACTIVE")

        dependency_a = make_dependency(
            source="identity",
            target="state",
            relation="depends_on",
        )

        dependency_b = make_dependency(
            source="identity",
            target="state",
            relation="conditionally_depends_on",
        )

        self.assertEqual(dependency_a["source"], dependency_b["source"])
        self.assertEqual(dependency_a["target"], dependency_b["target"])
        self.assertNotEqual(
            dependency_a["relation"],
            dependency_b["relation"],
        )

    def test_08_dependency_is_not_intrinsic_property_of_identity(self):
        identity = make_dimension("identity", "E1")

        dependency = make_dependency(
            source="identity",
            target="state",
        )

        self.assertEqual(identity["name"], "identity")
        self.assertEqual(dependency["source"], "identity")
        self.assertNotEqual(
            dependency["relation"],
            identity["name"],
        )

    def test_09_dependency_is_not_intrinsic_property_of_state(self):
        state = make_dimension("state", "ACTIVE")

        dependency = make_dependency(
            source="identity",
            target="state",
        )

        self.assertEqual(state["name"], "state")
        self.assertEqual(dependency["target"], "state")
        self.assertNotEqual(
            dependency["relation"],
            state["name"],
        )

    def test_10_dependency_relationship_has_two_distinct_endpoints(self):
        dependency = make_dependency(
            source="identity",
            target="state",
        )

        self.assertNotEqual(
            dependency["source"],
            dependency["target"],
        )

    def test_11_dependency_direction_is_part_of_relationship_semantics(self):
        dependency_a = make_dependency(
            source="identity",
            target="state",
        )

        dependency_b = make_dependency(
            source="state",
            target="identity",
        )

        self.assertNotEqual(
            dependency_a["source"],
            dependency_b["source"],
        )

        self.assertNotEqual(
            dependency_a["target"],
            dependency_b["target"],
        )

    def test_12_reverse_dependency_is_not_same_relationship(self):
        dependency_a = make_dependency(
            source="identity",
            target="state",
        )

        dependency_b = make_dependency(
            source="state",
            target="identity",
        )

        self.assertNotEqual(dependency_a, dependency_b)

    def test_13_dependency_relationship_does_not_create_composite_identity(self):
        identity = make_dimension("identity", "E1")
        state = make_dimension("state", "ACTIVE")

        dependency = make_dependency(
            source="identity",
            target="state",
        )

        composite = (
            identity["value"],
            state["value"],
            dependency["relation"],
        )

        self.assertNotEqual(composite, identity["value"])
        self.assertNotEqual(composite, state["value"])

    def test_14_dependency_can_be_contextual(self):
        dependency = make_dependency(
            source="request",
            target="decision",
            relation="uses_as_input",
        )

        context = {
            "dependency_active": True,
        }

        self.assertTrue(context["dependency_active"])
        self.assertEqual(dependency["source"], "request")
        self.assertEqual(dependency["target"], "decision")

    def test_15_contextual_dependency_does_not_mutate_dimensions(self):
        request = make_dimension("request", "R1")
        decision = make_dimension("decision", "ACCEPT")

        dependency = make_dependency(
            source="request",
            target="decision",
            relation="uses_as_input",
        )

        self.assertEqual(request["value"], "R1")
        self.assertEqual(decision["value"], "ACCEPT")
        self.assertEqual(dependency["relation"], "uses_as_input")

    def test_16_dependency_is_not_state(self):
        dependency = make_dependency(
            source="request",
            target="decision",
        )

        self.assertNotIn(
            dependency["relation"],
            {"ACTIVE", "INACTIVE"},
        )

    def test_17_dependency_is_not_ordering(self):
        dependency_a = make_dependency(
            source="request",
            target="decision",
        )

        dependency_b = make_dependency(
            source="request",
            target="decision",
        )

        self.assertEqual(dependency_a["source"], dependency_b["source"])
        self.assertEqual(dependency_a["target"], dependency_b["target"])

    def test_18_dependency_is_not_cardinality(self):
        dependency = make_dependency(
            source="request",
            target="decision",
        )

        collection = [dependency]

        self.assertEqual(len(collection), 1)
        self.assertEqual(collection[0], dependency)

    def test_19_dependency_relationship_can_be_reused(self):
        dependency = make_dependency(
            source="request",
            target="decision",
            relation="uses_as_input",
        )

        context_a = {"dependency": dependency}
        context_b = {"dependency": dependency}

        self.assertIs(
            context_a["dependency"],
            context_b["dependency"],
        )

    def test_20_same_dependency_can_participate_in_multiple_contexts(self):
        dependency = make_dependency(
            source="request",
            target="decision",
            relation="uses_as_input",
        )

        contexts = [
            {"name": "context_a", "dependency": dependency},
            {"name": "context_b", "dependency": dependency},
        ]

        self.assertEqual(
            contexts[0]["dependency"],
            contexts[1]["dependency"],
        )

    def test_21_dependency_relationship_does_not_require_lifecycle(self):
        dependency = make_dependency(
            source="request",
            target="decision",
        )

        self.assertEqual(dependency["source"], "request")
        self.assertEqual(dependency["target"], "decision")

    def test_22_dependency_relationship_can_coexist_with_identity(self):
        dependency = make_dependency(
            source="request",
            target="decision",
        )

        identity = "REL-1"

        self.assertEqual(identity, "REL-1")
        self.assertEqual(dependency["source"], "request")
        self.assertEqual(dependency["target"], "decision")

    def test_23_relationship_identity_is_not_endpoint_identity(self):
        dependency = make_dependency(
            source="request",
            target="decision",
        )

        relationship_id = "REL-1"

        self.assertNotEqual(
            relationship_id,
            dependency["source"],
        )

        self.assertNotEqual(
            relationship_id,
            dependency["target"],
        )

    def test_24_dependency_change_does_not_require_endpoint_identity_change(self):
        request = make_dimension("request", "R1")
        decision = make_dimension("decision", "ACCEPT")

        dependency_a = make_dependency(
            source="request",
            target="decision",
            relation="uses_as_input",
        )

        dependency_b = make_dependency(
            source="request",
            target="decision",
            relation="conditionally_uses",
        )

        self.assertEqual(request["value"], "R1")
        self.assertEqual(decision["value"], "ACCEPT")
        self.assertNotEqual(
            dependency_a["relation"],
            dependency_b["relation"],
        )

    def test_25_dependency_does_not_determine_endpoint_identity(self):
        dependency = make_dependency(
            source="request",
            target="decision",
        )

        request_id = "R1"
        decision_id = "D1"

        self.assertEqual(dependency["source"], "request")
        self.assertEqual(dependency["target"], "decision")
        self.assertNotEqual(request_id, decision_id)

    def test_26_dependency_relationship_is_semantically_distinct(self):
        dependency = make_dependency(
            source="request",
            target="decision",
            relation="uses_as_input",
        )

        self.assertEqual(dependency["relation"], "uses_as_input")
        self.assertNotEqual(
            dependency["relation"],
            dependency["source"],
        )
        self.assertNotEqual(
            dependency["relation"],
            dependency["target"],
        )

    def test_27_final_boundary_dependency_is_relationship_not_dimension_collapse(self):
        request = make_dimension("request", "R1")
        decision = make_dimension("decision", "ACCEPT")

        dependency = make_dependency(
            source="request",
            target="decision",
            relation="uses_as_input",
        )

        self.assertEqual(request["name"], "request")
        self.assertEqual(decision["name"], "decision")
        self.assertEqual(dependency["source"], "request")
        self.assertEqual(dependency["target"], "decision")
        self.assertEqual(dependency["relation"], "uses_as_input")