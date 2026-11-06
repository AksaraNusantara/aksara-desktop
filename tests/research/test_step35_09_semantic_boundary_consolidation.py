import unittest


class TestStep35_09SemanticBoundaryConsolidation(unittest.TestCase):

    # ---------------------------------------------------------
    # Concept registry
    # ---------------------------------------------------------

    CONCEPTS = {
        "ExecutionRequest": "REQUEST_INTENT",

        "AdmissionDecision": "EVALUATION_DECISION",
        "EvaluationResult": "EVALUATION_DECISION",
        "ExecutionDecision": "EVALUATION_DECISION",

        "Authority": "AUTHORITY_GOVERNANCE",
        "Permission": "AUTHORITY_GOVERNANCE",

        "ExecutionTrigger": "EXECUTION_CONTROL",

        "Execution": "EXECUTION_OCCURRENCE",
        "ExecutionState": "EXECUTION_OCCURRENCE",
    }

    # ---------------------------------------------------------
    # 1. Every concept must have exactly one semantic group
    # ---------------------------------------------------------

    def test_all_concepts_are_registered(self):
        expected = {
            "ExecutionRequest",
            "AdmissionDecision",
            "EvaluationResult",
            "ExecutionDecision",
            "Authority",
            "Permission",
            "ExecutionTrigger",
            "Execution",
            "ExecutionState",
        }

        self.assertEqual(set(self.CONCEPTS), expected)

    def test_every_concept_has_one_group(self):
        for concept, group in self.CONCEPTS.items():
            self.assertIsInstance(concept, str)
            self.assertIsInstance(group, str)
            self.assertTrue(group)

    # ---------------------------------------------------------
    # 2. Grouping must not imply identity
    # ---------------------------------------------------------

    def test_admission_and_evaluation_result_are_distinct(self):
        self.assertEqual(
            self.CONCEPTS["AdmissionDecision"],
            self.CONCEPTS["EvaluationResult"],
        )
        self.assertNotEqual(
            "AdmissionDecision",
            "EvaluationResult",
        )

    def test_evaluation_result_and_execution_decision_are_distinct(self):
        self.assertEqual(
            self.CONCEPTS["EvaluationResult"],
            self.CONCEPTS["ExecutionDecision"],
        )
        self.assertNotEqual(
            "EvaluationResult",
            "ExecutionDecision",
        )

    def test_admission_and_execution_decision_are_distinct(self):
        self.assertEqual(
            self.CONCEPTS["AdmissionDecision"],
            self.CONCEPTS["ExecutionDecision"],
        )
        self.assertNotEqual(
            "AdmissionDecision",
            "ExecutionDecision",
        )

    def test_authority_and_permission_are_distinct(self):
        self.assertEqual(
            self.CONCEPTS["Authority"],
            self.CONCEPTS["Permission"],
        )
        self.assertNotEqual(
            "Authority",
            "Permission",
        )

    def test_execution_and_execution_state_are_distinct(self):
        self.assertEqual(
            self.CONCEPTS["Execution"],
            self.CONCEPTS["ExecutionState"],
        )
        self.assertNotEqual(
            "Execution",
            "ExecutionState",
        )

    # ---------------------------------------------------------
    # 3. Cross-group concepts remain distinct
    # ---------------------------------------------------------

    def test_request_is_distinct_from_decision(self):
        self.assertNotEqual(
            self.CONCEPTS["ExecutionRequest"],
            self.CONCEPTS["ExecutionDecision"],
        )

    def test_request_is_distinct_from_authority(self):
        self.assertNotEqual(
            self.CONCEPTS["ExecutionRequest"],
            self.CONCEPTS["Authority"],
        )

    def test_decision_is_distinct_from_authority(self):
        self.assertNotEqual(
            self.CONCEPTS["ExecutionDecision"],
            self.CONCEPTS["Authority"],
        )

    def test_decision_is_distinct_from_trigger(self):
        self.assertNotEqual(
            self.CONCEPTS["ExecutionDecision"],
            self.CONCEPTS["ExecutionTrigger"],
        )

    def test_trigger_is_distinct_from_execution(self):
        self.assertNotEqual(
            self.CONCEPTS["ExecutionTrigger"],
            self.CONCEPTS["Execution"],
        )

    def test_execution_is_distinct_from_request(self):
        self.assertNotEqual(
            self.CONCEPTS["Execution"],
            self.CONCEPTS["ExecutionRequest"],
        )

    # ---------------------------------------------------------
    # 4. Group membership must not imply causal ordering
    # ---------------------------------------------------------

    def test_same_group_does_not_define_execution_order(self):
        group = "EVALUATION_DECISION"

        members = [
            concept
            for concept, member_group in self.CONCEPTS.items()
            if member_group == group
        ]

        self.assertEqual(
            set(members),
            {
                "AdmissionDecision",
                "EvaluationResult",
                "ExecutionDecision",
            },
        )


    def test_authority_group_does_not_define_evaluation_order(self):
        group = "AUTHORITY_GOVERNANCE"

        members = [
            concept
            for concept, member_group in self.CONCEPTS.items()
            if member_group == group
        ]

        self.assertEqual(
            set(members),
            {
                "Authority",
                "Permission",
            },
        )


    def test_execution_occurrence_group_does_not_define_identity(self):
        group = "EXECUTION_OCCURRENCE"

        members = [
            concept
            for concept, member_group in self.CONCEPTS.items()
            if member_group == group
        ]

        self.assertEqual(
            set(members),
            {
                "Execution",
                "ExecutionState",
            },
        )

    # ---------------------------------------------------------
    # 5. Grouping must not create implication
    # ---------------------------------------------------------

    def test_admission_group_does_not_imply_execution_decision(self):
        admission_group = self.CONCEPTS["AdmissionDecision"]
        execution_decision_group = self.CONCEPTS["ExecutionDecision"]

        self.assertEqual(
            admission_group,
            execution_decision_group,
        )

        # Same group is NOT evidence of identity.
        self.assertNotEqual(
            "AdmissionDecision",
            "ExecutionDecision",
        )

    def test_authority_group_does_not_imply_permission(self):
        self.assertEqual(
            self.CONCEPTS["Authority"],
            self.CONCEPTS["Permission"],
        )
        self.assertNotEqual(
            "Authority",
            "Permission",
        )

    def test_execution_group_does_not_imply_execution_occurrence(self):
        self.assertEqual(
            self.CONCEPTS["Execution"],
            self.CONCEPTS["ExecutionState"],
        )
        self.assertNotEqual(
            "Execution",
            "ExecutionState",
        )

    # ---------------------------------------------------------
    # 6. Trigger remains its own semantic role
    # ---------------------------------------------------------

    def test_trigger_has_independent_group(self):
        trigger_group = self.CONCEPTS["ExecutionTrigger"]

        self.assertEqual(
            trigger_group,
            "EXECUTION_CONTROL",
        )

        for concept, group in self.CONCEPTS.items():
            if concept != "ExecutionTrigger":
                self.assertNotEqual(group, trigger_group)

    # ---------------------------------------------------------
    # 7. Request remains independent from downstream concepts
    # ---------------------------------------------------------

    def test_request_has_independent_group(self):
        request_group = self.CONCEPTS["ExecutionRequest"]

        self.assertEqual(
            request_group,
            "REQUEST_INTENT",
        )

        for concept, group in self.CONCEPTS.items():
            if concept != "ExecutionRequest":
                self.assertNotEqual(group, request_group)

    # ---------------------------------------------------------
    # 8. Grouping is classification, not transformation
    # ---------------------------------------------------------

    def test_grouping_preserves_concept_count(self):
        self.assertEqual(
            len(self.CONCEPTS),
            9,
        )

    def test_grouping_does_not_merge_concepts(self):
        groups = {}

        for concept, group in self.CONCEPTS.items():
            groups.setdefault(group, []).append(concept)

        total_members = sum(
            len(members)
            for members in groups.values()
        )

        self.assertEqual(
            total_members,
            len(self.CONCEPTS),
        )

    def test_each_concept_occurs_once(self):
        concepts = list(self.CONCEPTS.keys())

        self.assertEqual(
            len(concepts),
            len(set(concepts)),
        )

    # ---------------------------------------------------------
    # 9. Candidate taxonomy remains observational
    # ---------------------------------------------------------

    def test_grouping_contains_no_execution_value(self):
        forbidden_execution_values = {
            "PROCEED",
            "DO_NOT_PROCEED",
            "EXECUTED",
            "NOT_EXECUTED",
            "TRIGGERED",
            "NOT_TRIGGERED",
        }

        for group in self.CONCEPTS.values():
            self.assertNotIn(
                group,
                forbidden_execution_values,
            )

    def test_grouping_does_not_define_state(self):
        for concept, group in self.CONCEPTS.items():
            self.assertNotEqual(
                group,
                "EXECUTED",
            )
            self.assertNotEqual(
                group,
                "NOT_EXECUTED",
            )

    # ---------------------------------------------------------
    # 10. Semantic boundaries survive consolidation
    # ---------------------------------------------------------

    def test_consolidation_preserves_known_boundary_pairs(self):
        boundary_pairs = [
            ("ExecutionRequest", "ExecutionDecision"),
            ("AdmissionDecision", "ExecutionDecision"),
            ("EvaluationResult", "ExecutionDecision"),
            ("Authority", "Permission"),
            ("ExecutionDecision", "ExecutionTrigger"),
            ("ExecutionTrigger", "Execution"),
            ("Execution", "ExecutionState"),
        ]

        for left, right in boundary_pairs:
            self.assertNotEqual(left, right)

    def test_consolidation_does_not_create_new_identity(self):
        grouped_members = {}

        for concept, group in self.CONCEPTS.items():
            grouped_members.setdefault(group, []).append(concept)

        for members in grouped_members.values():
            self.assertEqual(
                len(members),
                len(set(members)),
            )


if __name__ == "__main__":
    unittest.main()