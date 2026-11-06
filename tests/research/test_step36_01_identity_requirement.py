import unittest


class TestStep36_01IdentityRequirement(unittest.TestCase):

    # ---------------------------------------------------------
    # Conceptual observation model
    # ---------------------------------------------------------

    def make_observation(
        self,
        concept,
        value,
        request_id="REQ-1",
        execution_id=None,
        context="CTX-1",
        observation_id=None,
    ):
        return {
            "concept": concept,
            "value": value,
            "request_id": request_id,
            "execution_id": execution_id,
            "context": context,
            "observation_id": observation_id,
        }

    # ---------------------------------------------------------
    # 1. Semantic distinction without identity
    # ---------------------------------------------------------

    def test_different_concepts_remain_distinct_without_identity(self):
        admission = self.make_observation(
            "AdmissionDecision",
            "ACCEPTED",
        )

        execution_decision = self.make_observation(
            "ExecutionDecision",
            "ACCEPTED",
        )

        self.assertEqual(
            admission["value"],
            execution_decision["value"],
        )

        self.assertNotEqual(
            admission["concept"],
            execution_decision["concept"],
        )

        self.assertIsNone(admission["observation_id"])
        self.assertIsNone(execution_decision["observation_id"])

    def test_same_value_does_not_merge_different_concepts(self):
        observations = [
            self.make_observation(
                "AdmissionDecision",
                "ACCEPTED",
            ),
            self.make_observation(
                "ExecutionDecision",
                "ACCEPTED",
            ),
        ]

        concepts = {
            observation["concept"]
            for observation in observations
        }

        self.assertEqual(
            concepts,
            {
                "AdmissionDecision",
                "ExecutionDecision",
            },
        )

    # ---------------------------------------------------------
    # 2. Different values within same concept
    # ---------------------------------------------------------

    def test_same_concept_different_values_are_distinguishable(self):
        first = self.make_observation(
            "ExecutionDecision",
            "PROCEED",
        )

        second = self.make_observation(
            "ExecutionDecision",
            "DO_NOT_PROCEED",
        )

        self.assertEqual(
            first["concept"],
            second["concept"],
        )

        self.assertNotEqual(
            first["value"],
            second["value"],
        )

    def test_value_difference_does_not_require_identity(self):
        first = self.make_observation(
            "ExecutionDecision",
            "PROCEED",
        )

        second = self.make_observation(
            "ExecutionDecision",
            "DO_NOT_PROCEED",
        )

        self.assertIsNone(first["observation_id"])
        self.assertIsNone(second["observation_id"])

        self.assertNotEqual(
            first["value"],
            second["value"],
        )

    # ---------------------------------------------------------
    # 3. Same concept + same value
    # ---------------------------------------------------------

    def test_same_concept_same_value_can_exist_without_identity(self):
        first = self.make_observation(
            "AdmissionDecision",
            "ACCEPTED",
        )

        second = self.make_observation(
            "AdmissionDecision",
            "ACCEPTED",
        )

        self.assertEqual(
            first["concept"],
            second["concept"],
        )

        self.assertEqual(
            first["value"],
            second["value"],
        )

        self.assertIsNone(first["observation_id"])
        self.assertIsNone(second["observation_id"])

    def test_same_concept_same_value_does_not_prove_identity_requirement(self):
        first = self.make_observation(
            "EvaluationResult",
            "ALLOWED",
        )

        second = self.make_observation(
            "EvaluationResult",
            "ALLOWED",
        )

        self.assertEqual(first["concept"], second["concept"])
        self.assertEqual(first["value"], second["value"])

        # Identity remains optional in this conceptual model.
        self.assertIsNone(first["observation_id"])
        self.assertIsNone(second["observation_id"])

    # ---------------------------------------------------------
    # 4. Request identity vs observation identity
    # ---------------------------------------------------------

    def test_same_request_can_have_multiple_concepts(self):
        observations = [
            self.make_observation(
                "AdmissionDecision",
                "ACCEPTED",
            ),
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
            ),
            self.make_observation(
                "ExecutionDecision",
                "PROCEED",
            ),
        ]

        request_ids = {
            observation["request_id"]
            for observation in observations
        }

        self.assertEqual(
            request_ids,
            {"REQ-1"},
        )

    def test_same_request_does_not_require_same_concept(self):
        observations = [
            self.make_observation(
                "AdmissionDecision",
                "ACCEPTED",
            ),
            self.make_observation(
                "ExecutionDecision",
                "PROCEED",
            ),
        ]

        concepts = {
            observation["concept"]
            for observation in observations
        }

        self.assertEqual(len(concepts), 2)

    # ---------------------------------------------------------
    # 5. Context identity
    # ---------------------------------------------------------

    def test_same_authority_can_exist_across_contexts(self):
        first = self.make_observation(
            "Authority",
            "AUTH-A",
            context="CTX-1",
        )

        second = self.make_observation(
            "Authority",
            "AUTH-A",
            context="CTX-2",
        )

        self.assertEqual(
            first["value"],
            second["value"],
        )

        self.assertNotEqual(
            first["context"],
            second["context"],
        )

        self.assertIsNone(first["observation_id"])
        self.assertIsNone(second["observation_id"])

    def test_context_change_does_not_prove_new_authority_identity(self):
        first = self.make_observation(
            "Authority",
            "AUTH-A",
            context="CTX-1",
        )

        second = self.make_observation(
            "Authority",
            "AUTH-A",
            context="CTX-2",
        )

        self.assertEqual(
            first["value"],
            second["value"],
        )

    # ---------------------------------------------------------
    # 6. Execution identity vs state
    # ---------------------------------------------------------

    def test_execution_state_can_reference_execution_without_state_identity(self):
        state = self.make_observation(
            "ExecutionState",
            "NOT_STARTED",
            execution_id="EXEC-1",
        )

        self.assertEqual(
            state["execution_id"],
            "EXEC-1",
        )

        self.assertIsNone(
            state["observation_id"],
        )

    def test_state_is_distinct_from_execution_identity(self):
        state = self.make_observation(
            "ExecutionState",
            "RUNNING",
            execution_id="EXEC-1",
        )

        self.assertEqual(
            state["execution_id"],
            "EXEC-1",
        )

        self.assertNotEqual(
            state["concept"],
            "Execution",
        )

    # ---------------------------------------------------------
    # 7. Concept identity vs occurrence identity
    # ---------------------------------------------------------

    def test_concept_identity_is_not_observation_identity(self):
        first = self.make_observation(
            "ExecutionDecision",
            "PROCEED",
            observation_id="OBS-1",
        )

        second = self.make_observation(
            "ExecutionDecision",
            "PROCEED",
            observation_id="OBS-2",
        )

        self.assertEqual(
            first["concept"],
            second["concept"],
        )

        self.assertNotEqual(
            first["observation_id"],
            second["observation_id"],
        )

    def test_same_value_can_have_multiple_occurrences(self):
        observations = [
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
                observation_id="OBS-1",
            ),
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
                observation_id="OBS-2",
            ),
        ]

        identities = {
            observation["observation_id"]
            for observation in observations
        }

        self.assertEqual(
            identities,
            {"OBS-1", "OBS-2"},
        )

    # ---------------------------------------------------------
    # 8. Identity is contextual, not automatically universal
    # ---------------------------------------------------------

    def test_observation_identity_can_be_added_without_changing_concept(self):
        observation = self.make_observation(
            "AdmissionDecision",
            "ACCEPTED",
        )

        self.assertIsNone(
            observation["observation_id"],
        )

        observation["observation_id"] = "OBS-1"

        self.assertEqual(
            observation["concept"],
            "AdmissionDecision",
        )

        self.assertEqual(
            observation["observation_id"],
            "OBS-1",
        )

    def test_adding_identity_does_not_change_semantic_value(self):
        observation = self.make_observation(
            "ExecutionDecision",
            "PROCEED",
        )

        original_value = observation["value"]

        observation["observation_id"] = "OBS-1"

        self.assertEqual(
            observation["value"],
            original_value,
        )

    # ---------------------------------------------------------
    # 9. Request identity and execution identity remain distinct
    # ---------------------------------------------------------

    def test_request_identity_is_not_execution_identity(self):
        observation = self.make_observation(
            "ExecutionState",
            "RUNNING",
            request_id="REQ-1",
            execution_id="EXEC-1",
        )

        self.assertNotEqual(
            observation["request_id"],
            observation["execution_id"],
        )

    def test_execution_identity_does_not_replace_request_identity(self):
        observation = self.make_observation(
            "ExecutionDecision",
            "PROCEED",
            request_id="REQ-1",
            execution_id="EXEC-1",
        )

        self.assertEqual(
            observation["request_id"],
            "REQ-1",
        )

        self.assertEqual(
            observation["execution_id"],
            "EXEC-1",
        )

    # ---------------------------------------------------------
    # 10. No automatic identity proliferation
    # ---------------------------------------------------------

    def test_semantic_distinction_does_not_require_dedicated_identity(self):
        concepts = [
            "AdmissionDecision",
            "EvaluationResult",
            "ExecutionDecision",
            "Authority",
            "Permission",
            "ExecutionTrigger",
        ]

        observations = [
            self.make_observation(
                concept,
                "VALUE",
            )
            for concept in concepts
        ]

        for observation in observations:
            self.assertIsNone(
                observation["observation_id"],
            )

    def test_identity_is_an_optional_dimension_in_this_model(self):
        observation = self.make_observation(
            "ExecutionDecision",
            "PROCEED",
        )

        self.assertIn(
            "observation_id",
            observation,
        )

        self.assertIsNone(
            observation["observation_id"],
        )


if __name__ == "__main__":
    unittest.main()