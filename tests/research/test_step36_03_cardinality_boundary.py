import unittest


class TestStep36_03CardinalityBoundary(unittest.TestCase):

    def make_observation(
        self,
        concept,
        value,
        request_id="REQ-1",
        execution_id=None,
        observation_id=None,
    ):
        return {
            "concept": concept,
            "value": value,
            "request_id": request_id,
            "execution_id": execution_id,
            "observation_id": observation_id,
        }

    # ---------------------------------------------------------
    # 1. Zero occurrence is representable
    # ---------------------------------------------------------

    def test_request_can_have_zero_admission_observations(self):
        admissions = []

        self.assertEqual(
            len(admissions),
            0,
        )

    def test_request_can_have_zero_evaluation_observations(self):
        evaluations = []

        self.assertEqual(
            len(evaluations),
            0,
        )

    def test_request_can_have_zero_execution_decisions(self):
        decisions = []

        self.assertEqual(
            len(decisions),
            0,
        )

    def test_request_can_have_zero_executions(self):
        executions = []

        self.assertEqual(
            len(executions),
            0,
        )

    # ---------------------------------------------------------
    # 2. One occurrence is representable
    # ---------------------------------------------------------

    def test_request_can_have_one_admission(self):
        admissions = [
            self.make_observation(
                "AdmissionDecision",
                "ACCEPTED",
            )
        ]

        self.assertEqual(
            len(admissions),
            1,
        )

    def test_request_can_have_one_evaluation(self):
        evaluations = [
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
            )
        ]

        self.assertEqual(
            len(evaluations),
            1,
        )

    def test_request_can_have_one_execution_decision(self):
        decisions = [
            self.make_observation(
                "ExecutionDecision",
                "PROCEED",
            )
        ]

        self.assertEqual(
            len(decisions),
            1,
        )

    # ---------------------------------------------------------
    # 3. Multiple occurrences are representable
    # ---------------------------------------------------------

    def test_request_can_have_multiple_admissions(self):
        admissions = [
            self.make_observation(
                "AdmissionDecision",
                "ACCEPTED",
                observation_id="ADM-1",
            ),
            self.make_observation(
                "AdmissionDecision",
                "REJECTED",
                observation_id="ADM-2",
            ),
        ]

        self.assertEqual(
            len(admissions),
            2,
        )

    def test_request_can_have_multiple_evaluations(self):
        evaluations = [
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
                observation_id="EVAL-1",
            ),
            self.make_observation(
                "EvaluationResult",
                "BLOCKED",
                observation_id="EVAL-2",
            ),
        ]

        self.assertEqual(
            len(evaluations),
            2,
        )

    def test_request_can_have_multiple_execution_decisions(self):
        decisions = [
            self.make_observation(
                "ExecutionDecision",
                "PROCEED",
                observation_id="DEC-1",
            ),
            self.make_observation(
                "ExecutionDecision",
                "DO_NOT_PROCEED",
                observation_id="DEC-2",
            ),
        ]

        self.assertEqual(
            len(decisions),
            2,
        )

    def test_request_can_have_multiple_triggers(self):
        triggers = [
            self.make_observation(
                "ExecutionTrigger",
                "TRIGGERED",
                observation_id="TRG-1",
            ),
            self.make_observation(
                "ExecutionTrigger",
                "TRIGGERED",
                observation_id="TRG-2",
            ),
        ]

        self.assertEqual(
            len(triggers),
            2,
        )

    # ---------------------------------------------------------
    # 4. Multiple occurrences can share Request Identity
    # ---------------------------------------------------------

    def test_multiple_admissions_can_share_request_identity(self):
        admissions = [
            self.make_observation(
                "AdmissionDecision",
                "ACCEPTED",
                observation_id="ADM-1",
            ),
            self.make_observation(
                "AdmissionDecision",
                "REJECTED",
                observation_id="ADM-2",
            ),
        ]

        request_ids = {
            admission["request_id"]
            for admission in admissions
        }

        self.assertEqual(
            request_ids,
            {"REQ-1"},
        )

    def test_multiple_decisions_can_share_request_identity(self):
        decisions = [
            self.make_observation(
                "ExecutionDecision",
                "PROCEED",
                observation_id="DEC-1",
            ),
            self.make_observation(
                "ExecutionDecision",
                "DO_NOT_PROCEED",
                observation_id="DEC-2",
            ),
        ]

        request_ids = {
            decision["request_id"]
            for decision in decisions
        }

        self.assertEqual(
            request_ids,
            {"REQ-1"},
        )

    # ---------------------------------------------------------
    # 5. Cardinality does not imply concept identity
    # ---------------------------------------------------------

    def test_multiple_occurrences_do_not_merge_concepts(self):
        observations = [
            self.make_observation(
                "AdmissionDecision",
                "ACCEPTED",
                observation_id="OBS-1",
            ),
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
                observation_id="OBS-2",
            ),
            self.make_observation(
                "ExecutionDecision",
                "PROCEED",
                observation_id="OBS-3",
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
                "EvaluationResult",
                "ExecutionDecision",
            },
        )

    def test_same_cardinality_does_not_mean_same_semantic_role(self):
        admission = [
            self.make_observation(
                "AdmissionDecision",
                "ACCEPTED",
            )
        ]

        execution = [
            self.make_observation(
                "ExecutionDecision",
                "PROCEED",
            )
        ]

        self.assertEqual(
            len(admission),
            len(execution),
        )

        self.assertNotEqual(
            admission[0]["concept"],
            execution[0]["concept"],
        )

    # ---------------------------------------------------------
    # 6. Multiple executions per Request
    # ---------------------------------------------------------

    def test_request_can_have_multiple_executions(self):
        executions = [
            self.make_observation(
                "Execution",
                "OCCURRED",
                execution_id="EXEC-1",
            ),
            self.make_observation(
                "Execution",
                "OCCURRED",
                execution_id="EXEC-2",
            ),
        ]

        execution_ids = {
            execution["execution_id"]
            for execution in executions
        }

        self.assertEqual(
            execution_ids,
            {
                "EXEC-1",
                "EXEC-2",
            },
        )

    def test_multiple_executions_can_share_request_identity(self):
        executions = [
            self.make_observation(
                "Execution",
                "OCCURRED",
                execution_id="EXEC-1",
            ),
            self.make_observation(
                "Execution",
                "OCCURRED",
                execution_id="EXEC-2",
            ),
        ]

        request_ids = {
            execution["request_id"]
            for execution in executions
        }

        self.assertEqual(
            request_ids,
            {"REQ-1"},
        )

    # ---------------------------------------------------------
    # 7. Observation cardinality vs Execution cardinality
    # ---------------------------------------------------------

    def test_multiple_observations_can_refer_to_one_execution(self):
        observations = [
            self.make_observation(
                "ExecutionState",
                "RUNNING",
                execution_id="EXEC-1",
                observation_id="STATE-1",
            ),
            self.make_observation(
                "ExecutionState",
                "COMPLETED",
                execution_id="EXEC-1",
                observation_id="STATE-2",
            ),
        ]

        execution_ids = {
            observation["execution_id"]
            for observation in observations
        }

        self.assertEqual(
            execution_ids,
            {"EXEC-1"},
        )

        self.assertEqual(
            len(observations),
            2,
        )

    def test_multiple_observations_do_not_require_multiple_executions(self):
        observations = [
            self.make_observation(
                "ExecutionState",
                "RUNNING",
                execution_id="EXEC-1",
                observation_id="STATE-1",
            ),
            self.make_observation(
                "ExecutionState",
                "COMPLETED",
                execution_id="EXEC-1",
                observation_id="STATE-2",
            ),
        ]

        execution_ids = {
            observation["execution_id"]
            for observation in observations
        }

        self.assertEqual(
            len(execution_ids),
            1,
        )

    # ---------------------------------------------------------
    # 8. Cardinality and identity are independent
    # ---------------------------------------------------------

    def test_multiple_occurrences_can_exist_without_dedicated_identity(self):
        observations = [
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
            ),
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
            ),
        ]

        self.assertEqual(
            len(observations),
            2,
        )

        self.assertIsNone(
            observations[0]["observation_id"],
        )

        self.assertIsNone(
            observations[1]["observation_id"],
        )

    def test_identity_can_be_added_when_occurrence_distinction_is_needed(self):
        observations = [
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
                observation_id="EVAL-1",
            ),
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
                observation_id="EVAL-2",
            ),
        ]

        identities = {
            observation["observation_id"]
            for observation in observations
        }

        self.assertEqual(
            identities,
            {
                "EVAL-1",
                "EVAL-2",
            },
        )

    # ---------------------------------------------------------
    # 9. Cardinality does not imply ordering
    # ---------------------------------------------------------

    def test_multiple_occurrences_do_not_automatically_have_order(self):
        observations = [
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
                observation_id="EVAL-A",
            ),
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
                observation_id="EVAL-B",
            ),
        ]

        self.assertEqual(
            len(observations),
            2,
        )

        # No sequence information exists.
        self.assertNotIn(
            "sequence",
            observations[0],
        )

    # ---------------------------------------------------------
    # 10. Cardinality does not imply lifecycle
    # ---------------------------------------------------------

    def test_multiple_decisions_do_not_automatically_mean_multiple_requests(self):
        decisions = [
            self.make_observation(
                "ExecutionDecision",
                "PROCEED",
                observation_id="DEC-1",
            ),
            self.make_observation(
                "ExecutionDecision",
                "DO_NOT_PROCEED",
                observation_id="DEC-2",
            ),
        ]

        request_ids = {
            decision["request_id"]
            for decision in decisions
        }

        self.assertEqual(
            len(request_ids),
            1,
        )

    def test_multiple_admissions_do_not_automatically_mean_multiple_requests(self):
        admissions = [
            self.make_observation(
                "AdmissionDecision",
                "ACCEPTED",
                observation_id="ADM-1",
            ),
            self.make_observation(
                "AdmissionDecision",
                "REJECTED",
                observation_id="ADM-2",
            ),
        ]

        request_ids = {
            admission["request_id"]
            for admission in admissions
        }

        self.assertEqual(
            len(request_ids),
            1,
        )

    # ---------------------------------------------------------
    # 11. Cross-dimension cardinality
    # ---------------------------------------------------------

    def test_one_request_can_have_multiple_semantic_dimensions(self):
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

        self.assertEqual(
            len(observations),
            3,
        )

        self.assertEqual(
            {
                observation["request_id"]
                for observation in observations
            },
            {"REQ-1"},
        )

    def test_cardinality_does_not_require_uniform_occurrence_counts(self):
        admissions = [
            self.make_observation(
                "AdmissionDecision",
                "ACCEPTED",
                observation_id="ADM-1",
            ),
        ]

        evaluations = [
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
                observation_id="EVAL-1",
            ),
            self.make_observation(
                "EvaluationResult",
                "BLOCKED",
                observation_id="EVAL-2",
            ),
        ]

        self.assertNotEqual(
            len(admissions),
            len(evaluations),
        )

        self.assertEqual(
            admissions[0]["request_id"],
            evaluations[0]["request_id"],
        )

    # ---------------------------------------------------------
    # 12. Cardinality does not force production abstraction
    # ---------------------------------------------------------

    def test_cardinality_is_representable_as_collection(self):
        observations = [
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
            ),
            self.make_observation(
                "EvaluationResult",
                "BLOCKED",
            ),
        ]

        self.assertIsInstance(
            observations,
            list,
        )

    def test_collection_represents_cardinality_without_special_object(self):
        observations = []

        self.assertEqual(
            len(observations),
            0,
        )

        observations.append(
            self.make_observation(
                "EvaluationResult",
                "ALLOWED",
            )
        )

        self.assertEqual(
            len(observations),
            1,
        )


if __name__ == "__main__":
    unittest.main()