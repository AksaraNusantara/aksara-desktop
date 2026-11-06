import unittest


class TestStep36_02OccurrenceAmbiguity(unittest.TestCase):

    def make_observation(
        self,
        concept="EvaluationResult",
        value="ALLOWED",
        request_id="REQ-1",
        execution_id=None,
        context="CTX-1",
        observation_id=None,
        sequence=None,
        timestamp=None,
    ):
        return {
            "concept": concept,
            "value": value,
            "request_id": request_id,
            "execution_id": execution_id,
            "context": context,
            "observation_id": observation_id,
            "sequence": sequence,
            "timestamp": timestamp,
        }

    # ---------------------------------------------------------
    # 1. Completely equivalent observations
    # ---------------------------------------------------------

    def test_two_equivalent_observations_have_same_semantic_attributes(self):
        first = self.make_observation()
        second = self.make_observation()

        self.assertEqual(
            first["concept"],
            second["concept"],
        )

        self.assertEqual(
            first["value"],
            second["value"],
        )

        self.assertEqual(
            first["request_id"],
            second["request_id"],
        )

        self.assertEqual(
            first["context"],
            second["context"],
        )

    def test_equivalent_observations_have_no_distinguishing_information(self):
        first = self.make_observation()
        second = self.make_observation()

        self.assertIsNone(first["observation_id"])
        self.assertIsNone(second["observation_id"])

        self.assertIsNone(first["sequence"])
        self.assertIsNone(second["sequence"])

        self.assertIsNone(first["timestamp"])
        self.assertIsNone(second["timestamp"])

    # ---------------------------------------------------------
    # 2. Concept/value/request/context are insufficient
    # ---------------------------------------------------------

    def test_equivalent_observations_cannot_be_distinguished_by_semantic_attributes(self):
        first = self.make_observation()
        second = self.make_observation()

        semantic_projection = lambda observation: (
            observation["concept"],
            observation["value"],
            observation["request_id"],
            observation["context"],
        )

        self.assertEqual(
            semantic_projection(first),
            semantic_projection(second),
        )

    def test_same_semantic_projection_does_not_identify_occurrence(self):
        observations = [
            self.make_observation(),
            self.make_observation(),
        ]

        projections = [
            (
                observation["concept"],
                observation["value"],
                observation["request_id"],
                observation["context"],
            )
            for observation in observations
        ]

        self.assertEqual(
            projections[0],
            projections[1],
        )

    # ---------------------------------------------------------
    # 3. Adding identity distinguishes occurrences
    # ---------------------------------------------------------

    def test_identity_can_distinguish_equivalent_occurrences(self):
        first = self.make_observation(
            observation_id="OBS-1",
        )

        second = self.make_observation(
            observation_id="OBS-2",
        )

        self.assertNotEqual(
            first["observation_id"],
            second["observation_id"],
        )

    def test_identity_does_not_change_semantic_value(self):
        first = self.make_observation(
            observation_id="OBS-1",
        )

        second = self.make_observation(
            observation_id="OBS-2",
        )

        self.assertEqual(
            first["concept"],
            second["concept"],
        )

        self.assertEqual(
            first["value"],
            second["value"],
        )

    # ---------------------------------------------------------
    # 4. Ordering can distinguish occurrences
    # ---------------------------------------------------------

    def test_sequence_can_distinguish_equivalent_occurrences(self):
        first = self.make_observation(
            sequence=1,
        )

        second = self.make_observation(
            sequence=2,
        )

        self.assertNotEqual(
            first["sequence"],
            second["sequence"],
        )

    def test_sequence_does_not_change_semantic_value(self):
        first = self.make_observation(
            sequence=1,
        )

        second = self.make_observation(
            sequence=2,
        )

        self.assertEqual(
            first["concept"],
            second["concept"],
        )

        self.assertEqual(
            first["value"],
            second["value"],
        )

    # ---------------------------------------------------------
    # 5. Temporal information can distinguish occurrences
    # ---------------------------------------------------------

    def test_timestamp_can_distinguish_occurrences(self):
        first = self.make_observation(
            timestamp="T1",
        )

        second = self.make_observation(
            timestamp="T2",
        )

        self.assertNotEqual(
            first["timestamp"],
            second["timestamp"],
        )

    def test_timestamp_does_not_change_semantic_value(self):
        first = self.make_observation(
            timestamp="T1",
        )

        second = self.make_observation(
            timestamp="T2",
        )

        self.assertEqual(
            first["concept"],
            second["concept"],
        )

        self.assertEqual(
            first["value"],
            second["value"],
        )

    # ---------------------------------------------------------
    # 6. Context can distinguish observations
    # ---------------------------------------------------------

    def test_context_can_distinguish_occurrences(self):
        first = self.make_observation(
            context="CTX-1",
        )

        second = self.make_observation(
            context="CTX-2",
        )

        self.assertNotEqual(
            first["context"],
            second["context"],
        )

    def test_context_distinction_is_not_identity(self):
        first = self.make_observation(
            context="CTX-1",
        )

        second = self.make_observation(
            context="CTX-2",
        )

        self.assertIsNone(first["observation_id"])
        self.assertIsNone(second["observation_id"])

        self.assertNotEqual(
            first["context"],
            second["context"],
        )

    # ---------------------------------------------------------
    # 7. Distinguishing information is orthogonal to value
    # ---------------------------------------------------------

    def test_same_value_can_have_different_occurrence_identity(self):
        observations = [
            self.make_observation(
                value="ALLOWED",
                observation_id="OBS-1",
            ),
            self.make_observation(
                value="ALLOWED",
                observation_id="OBS-2",
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

    def test_same_value_can_have_different_sequence(self):
        first = self.make_observation(
            value="ALLOWED",
            sequence=1,
        )

        second = self.make_observation(
            value="ALLOWED",
            sequence=2,
        )

        self.assertEqual(
            first["value"],
            second["value"],
        )

        self.assertNotEqual(
            first["sequence"],
            second["sequence"],
        )

    # ---------------------------------------------------------
    # 8. Identity is not the only possible distinction
    # ---------------------------------------------------------

    def test_identity_and_sequence_are_alternative_distinguishers(self):
        first = self.make_observation(
            observation_id="OBS-1",
        )

        second = self.make_observation(
            sequence=2,
        )

        self.assertNotEqual(
            first["observation_id"],
            second["observation_id"],
        )

        self.assertIsNone(first["sequence"])
        self.assertEqual(second["sequence"], 2)

    def test_identity_and_timestamp_are_alternative_distinguishers(self):
        first = self.make_observation(
            observation_id="OBS-1",
        )

        second = self.make_observation(
            timestamp="T2",
        )

        self.assertEqual(
            first["concept"],
            second["concept"],
        )

        self.assertEqual(
            first["value"],
            second["value"],
        )

        self.assertNotEqual(
            first["observation_id"],
            second["observation_id"],
        )

        self.assertNotEqual(
            first["timestamp"],
            second["timestamp"],
        )

    # ---------------------------------------------------------
    # 9. Distinguishing occurrence does not create new concept
    # ---------------------------------------------------------

    def test_occurrence_identity_does_not_create_new_concept(self):
        first = self.make_observation(
            observation_id="OBS-1",
        )

        second = self.make_observation(
            observation_id="OBS-2",
        )

        self.assertEqual(
            first["concept"],
            second["concept"],
        )

    def test_sequence_does_not_create_new_concept(self):
        first = self.make_observation(
            sequence=1,
        )

        second = self.make_observation(
            sequence=2,
        )

        self.assertEqual(
            first["concept"],
            second["concept"],
        )

    # ---------------------------------------------------------
    # 10. Request identity remains stable
    # ---------------------------------------------------------

    def test_multiple_occurrences_can_share_request_identity(self):
        observations = [
            self.make_observation(
                observation_id="OBS-1",
            ),
            self.make_observation(
                observation_id="OBS-2",
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

    def test_occurrence_distinction_does_not_require_new_request(self):
        first = self.make_observation(
            observation_id="OBS-1",
        )

        second = self.make_observation(
            observation_id="OBS-2",
        )

        self.assertEqual(
            first["request_id"],
            second["request_id"],
        )

    # ---------------------------------------------------------
    # 11. Execution identity remains independent
    # ---------------------------------------------------------

    def test_multiple_observations_can_share_execution_identity(self):
        first = self.make_observation(
            execution_id="EXEC-1",
            observation_id="OBS-1",
        )

        second = self.make_observation(
            execution_id="EXEC-1",
            observation_id="OBS-2",
        )

        self.assertEqual(
            first["execution_id"],
            second["execution_id"],
        )

        self.assertNotEqual(
            first["observation_id"],
            second["observation_id"],
        )

    # ---------------------------------------------------------
    # 12. Boundary condition
    # ---------------------------------------------------------

    def test_without_distinguishing_information_occurrences_are_ambiguous(self):
        first = self.make_observation()
        second = self.make_observation()

        self.assertEqual(first, second)

    def test_distinguishing_information_breaks_ambiguity(self):
        first = self.make_observation(
            observation_id="OBS-1",
        )

        second = self.make_observation(
            observation_id="OBS-2",
        )

        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()