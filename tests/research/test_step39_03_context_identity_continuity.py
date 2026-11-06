import unittest


def make_context(name, rule):
    return {
        "name": name,
        "rule": rule,
    }


def make_entity(identity, value):
    return {
        "identity": identity,
        "value": value,
    }


def observe(context, entity, result):
    return {
        "context": context,
        "entity": entity,
        "result": result,
    }


class TestContextIdentityContinuity(unittest.TestCase):

    def test_01_same_entity_can_be_observed_in_multiple_contexts(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observation_a = observe(
            context_a,
            entity,
            "VALID",
        )

        observation_b = observe(
            context_b,
            entity,
            "INVALID",
        )

        self.assertIs(
            observation_a["entity"],
            observation_b["entity"],
        )

    def test_02_context_change_does_not_change_entity_identity(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observe(context_a, entity, "VALID")

        identity_after_a = entity["identity"]

        observe(context_b, entity, "INVALID")

        identity_after_b = entity["identity"]

        self.assertEqual(
            identity_after_a,
            identity_after_b,
        )

    def test_03_context_change_does_not_change_entity_value(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observe(context_a, entity, "VALID")

        value_after_a = entity["value"]

        observe(context_b, entity, "INVALID")

        value_after_b = entity["value"]

        self.assertEqual(
            value_after_a,
            value_after_b,
        )

    def test_04_different_contexts_can_produce_different_observations(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "allow",
        )

        context_b = make_context(
            "context_b",
            "deny",
        )

        observation_a = observe(
            context_a,
            entity,
            "ACCEPTED",
        )

        observation_b = observe(
            context_b,
            entity,
            "REJECTED",
        )

        self.assertNotEqual(
            observation_a["result"],
            observation_b["result"],
        )

    def test_05_different_observations_do_not_require_different_entity_identity(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observation_a = observe(
            context_a,
            entity,
            "VALID",
        )

        observation_b = observe(
            context_b,
            entity,
            "INVALID",
        )

        self.assertEqual(
            observation_a["entity"]["identity"],
            observation_b["entity"]["identity"],
        )

    def test_06_new_observation_does_not_imply_new_entity(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observation_a = observe(
            context_a,
            entity,
            "VALID",
        )

        observation_b = observe(
            context_b,
            entity,
            "INVALID",
        )

        self.assertIsNot(
            observation_a,
            observation_b,
        )

        self.assertIs(
            observation_a["entity"],
            observation_b["entity"],
        )

    def test_07_context_identity_is_distinct_from_entity_identity(self):
        context_id = "CTX-001"
        entity_id = "REQ-001"

        self.assertNotEqual(
            context_id,
            entity_id,
        )

    def test_08_multiple_contexts_can_reference_same_identity(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        contexts = [
            make_context("context_a", "rule_a"),
            make_context("context_b", "rule_b"),
            make_context("context_c", "rule_c"),
        ]

        observations = [
            observe(
                context,
                entity,
                "VALID",
            )
            for context in contexts
        ]

        identities = [
            observation["entity"]["identity"]
            for observation in observations
        ]

        self.assertEqual(
            identities,
            [
                "REQ-001",
                "REQ-001",
                "REQ-001",
            ],
        )

    def test_09_same_context_can_observe_multiple_entities(self):
        context = make_context(
            "shared_context",
            "rule",
        )

        entity_a = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        entity_b = make_entity(
            "REQ-002",
            "ACTIVE",
        )

        observation_a = observe(
            context,
            entity_a,
            "VALID",
        )

        observation_b = observe(
            context,
            entity_b,
            "VALID",
        )

        self.assertNotEqual(
            observation_a["entity"]["identity"],
            observation_b["entity"]["identity"],
        )

    def test_10_context_does_not_become_entity_identity(self):
        context = make_context(
            "execution_context",
            "rule",
        )

        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        observation = observe(
            context,
            entity,
            "VALID",
        )

        self.assertNotEqual(
            observation["context"]["name"],
            observation["entity"]["identity"],
        )

    def test_11_context_change_can_preserve_identity_continuity(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observe(context_a, entity, "VALID")
        identity_before = entity["identity"]

        observe(context_b, entity, "INVALID")
        identity_after = entity["identity"]

        self.assertEqual(
            identity_before,
            identity_after,
        )

    def test_12_observation_identity_can_be_distinct_from_entity_identity(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context = make_context(
            "context_a",
            "rule_a",
        )

        observation = observe(
            context,
            entity,
            "VALID",
        )

        observation_identity = id(observation)

        self.assertNotEqual(
            observation_identity,
            entity["identity"],
        )

    def test_13_context_change_does_not_mutate_entity(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        before = dict(entity)

        observe(context_a, entity, "VALID")
        observe(context_b, entity, "INVALID")

        self.assertEqual(
            entity,
            before,
        )

    def test_14_same_entity_can_have_multiple_contextual_results(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        contexts = [
            make_context("context_a", "rule_a"),
            make_context("context_b", "rule_b"),
            make_context("context_c", "rule_c"),
        ]

        results = [
            "VALID",
            "INVALID",
            "VALID",
        ]

        observations = [
            observe(
                context,
                entity,
                result,
            )
            for context, result in zip(
                contexts,
                results,
            )
        ]

        self.assertEqual(
            len(observations),
            3,
        )

        self.assertEqual(
            observations[0]["entity"]["identity"],
            "REQ-001",
        )

        self.assertEqual(
            observations[1]["entity"]["identity"],
            "REQ-001",
        )

        self.assertEqual(
            observations[2]["entity"]["identity"],
            "REQ-001",
        )

    def test_15_context_does_not_require_identity_mutation(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context = make_context(
            "context_a",
            "rule_a",
        )

        before = entity["identity"]

        observe(
            context,
            entity,
            "VALID",
        )

        after = entity["identity"]

        self.assertEqual(
            before,
            after,
        )

    def test_16_different_contexts_do_not_require_different_entity_instances(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observation_a = observe(
            context_a,
            entity,
            "VALID",
        )

        observation_b = observe(
            context_b,
            entity,
            "INVALID",
        )

        self.assertIs(
            observation_a["entity"],
            observation_b["entity"],
        )

    def test_17_same_identity_can_appear_in_multiple_observations(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observations = [
            observe(
                context_a,
                entity,
                "VALID",
            ),
            observe(
                context_b,
                entity,
                "INVALID",
            ),
        ]

        self.assertEqual(
            len(
                {
                    observation["entity"]["identity"]
                    for observation in observations
                }
            ),
            1,
        )

    def test_18_observation_difference_can_be_contextual(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "allow",
        )

        context_b = make_context(
            "context_b",
            "deny",
        )

        observation_a = observe(
            context_a,
            entity,
            "VALID",
        )

        observation_b = observe(
            context_b,
            entity,
            "INVALID",
        )

        self.assertNotEqual(
            observation_a["context"],
            observation_b["context"],
        )

        self.assertNotEqual(
            observation_a["result"],
            observation_b["result"],
        )

        self.assertEqual(
            observation_a["entity"],
            observation_b["entity"],
        )

    def test_19_context_change_does_not_create_new_lifecycle_for_entity(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observe(context_a, entity, "VALID")
        observe(context_b, entity, "INVALID")

        self.assertEqual(
            entity["identity"],
            "REQ-001",
        )

    def test_20_context_change_does_not_create_new_state(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observe(context_a, entity, "VALID")
        observe(context_b, entity, "INVALID")

        self.assertEqual(
            entity["value"],
            "ACTIVE",
        )

    def test_21_context_change_does_not_create_new_permission(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observe(context_a, entity, "VALID")
        observe(context_b, entity, "INVALID")

        permission = None

        self.assertIsNone(
            permission,
        )

    def test_22_context_change_does_not_create_new_authority(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observe(context_a, entity, "VALID")
        observe(context_b, entity, "INVALID")

        authority = None

        self.assertIsNone(
            authority,
        )

    def test_23_context_can_change_observation_without_identity_change(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observation_a = observe(
            context_a,
            entity,
            "VALID",
        )

        observation_b = observe(
            context_b,
            entity,
            "INVALID",
        )

        self.assertNotEqual(
            observation_a["result"],
            observation_b["result"],
        )

        self.assertEqual(
            observation_a["entity"]["identity"],
            observation_b["entity"]["identity"],
        )

    def test_24_context_is_not_identity_substitute(self):
        context = make_context(
            "context_a",
            "rule_a",
        )

        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        observation = observe(
            context,
            entity,
            "VALID",
        )

        self.assertNotEqual(
            observation["context"]["name"],
            observation["entity"]["identity"],
        )

    def test_25_identity_continuity_is_possible_across_contexts(self):
        entity = make_entity(
            "REQ-001",
            "ACTIVE",
        )

        contexts = [
            make_context("context_a", "rule_a"),
            make_context("context_b", "rule_b"),
            make_context("context_c", "rule_c"),
        ]

        observations = [
            observe(
                context,
                entity,
                "VALID",
            )
            for context in contexts
        ]

        identities = [
            observation["entity"]["identity"]
            for observation in observations
        ]

        self.assertEqual(
            identities,
            [
                "REQ-001",
                "REQ-001",
                "REQ-001",
            ],
        )


if __name__ == "__main__":
    unittest.main()