import unittest


class AdmissionDecision:
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class ExecutionPermission:
    GRANTED = "GRANTED"
    NOT_GRANTED = "NOT_GRANTED"


class ExecutionEligibility:
    ALLOWED = "ALLOWED"
    BLOCKED = "BLOCKED"


class Policy:
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules


def evaluate_eligibility(admission, permission, policy):
    return policy.rules.get(
        (admission, permission),
        ExecutionEligibility.BLOCKED,
    )


class TestAdmissionPermissionRelationship(unittest.TestCase):

    def test_admission_and_permission_can_be_combined_for_evaluation(self):
        policy = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.ALLOWED,
            },
        )

        result = evaluate_eligibility(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            policy,
        )

        self.assertEqual(
            result,
            ExecutionEligibility.ALLOWED,
        )

    def test_accepted_not_granted_can_be_blocked(self):
        policy = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.NOT_GRANTED,
                ): ExecutionEligibility.BLOCKED,
            },
        )

        result = evaluate_eligibility(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
            policy,
        )

        self.assertEqual(
            result,
            ExecutionEligibility.BLOCKED,
        )

    def test_rejected_granted_can_be_blocked(self):
        policy = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.REJECTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.BLOCKED,
            },
        )

        result = evaluate_eligibility(
            AdmissionDecision.REJECTED,
            ExecutionPermission.GRANTED,
            policy,
        )

        self.assertEqual(
            result,
            ExecutionEligibility.BLOCKED,
        )

    def test_rejected_not_granted_can_be_blocked(self):
        policy = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.REJECTED,
                    ExecutionPermission.NOT_GRANTED,
                ): ExecutionEligibility.BLOCKED,
            },
        )

        result = evaluate_eligibility(
            AdmissionDecision.REJECTED,
            ExecutionPermission.NOT_GRANTED,
            policy,
        )

        self.assertEqual(
            result,
            ExecutionEligibility.BLOCKED,
        )

    def test_same_admission_and_permission_can_have_different_results_under_different_policies(self):
        policy_a = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.ALLOWED,
            },
        )

        policy_b = Policy(
            "policy_b",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.BLOCKED,
            },
        )

        result_a = evaluate_eligibility(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            policy_a,
        )

        result_b = evaluate_eligibility(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            policy_b,
        )

        self.assertNotEqual(result_a, result_b)

    def test_permission_does_not_alone_determine_execution_eligibility(self):
        policy = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.ALLOWED,
                (
                    AdmissionDecision.REJECTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.BLOCKED,
            },
        )

        granted_accepted = evaluate_eligibility(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            policy,
        )

        granted_rejected = evaluate_eligibility(
            AdmissionDecision.REJECTED,
            ExecutionPermission.GRANTED,
            policy,
        )

        self.assertNotEqual(
            granted_accepted,
            granted_rejected,
        )

    def test_admission_does_not_alone_determine_execution_eligibility(self):
        policy = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.ALLOWED,
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.NOT_GRANTED,
                ): ExecutionEligibility.BLOCKED,
            },
        )

        accepted_granted = evaluate_eligibility(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            policy,
        )

        accepted_not_granted = evaluate_eligibility(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
            policy,
        )

        self.assertNotEqual(
            accepted_granted,
            accepted_not_granted,
        )

    def test_execution_eligibility_is_distinct_from_admission(self):
        policy = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.ALLOWED,
            },
        )

        result = evaluate_eligibility(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            policy,
        )

        self.assertNotEqual(
            result,
            AdmissionDecision.ACCEPTED,
        )

    def test_execution_eligibility_is_distinct_from_permission(self):
        policy = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.ALLOWED,
            },
        )

        result = evaluate_eligibility(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            policy,
        )

        self.assertNotEqual(
            result,
            ExecutionPermission.GRANTED,
        )

    def test_eligibility_is_not_execution_occurrence(self):
        policy = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.ALLOWED,
            },
        )

        result = evaluate_eligibility(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            policy,
        )

        execution_id = None

        self.assertEqual(
            result,
            ExecutionEligibility.ALLOWED,
        )
        self.assertIsNone(execution_id)

    def test_policy_is_an_external_semantic_input(self):
        policy = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.ALLOWED,
            },
        )

        result = evaluate_eligibility(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            policy,
        )

        self.assertIsNotNone(policy)
        self.assertIsNotNone(result)

    def test_permission_and_admission_remain_identifiable_after_evaluation(self):
        policy = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.ALLOWED,
            },
        )

        admission = AdmissionDecision.ACCEPTED
        permission = ExecutionPermission.GRANTED

        result = evaluate_eligibility(
            admission,
            permission,
            policy,
        )

        self.assertEqual(admission, AdmissionDecision.ACCEPTED)
        self.assertEqual(permission, ExecutionPermission.GRANTED)
        self.assertEqual(result, ExecutionEligibility.ALLOWED)

    def test_policy_change_does_not_require_admission_change(self):
        policy_a = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.ALLOWED,
            },
        )

        policy_b = Policy(
            "policy_b",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.BLOCKED,
            },
        )

        admission = AdmissionDecision.ACCEPTED
        permission = ExecutionPermission.GRANTED

        result_a = evaluate_eligibility(admission, permission, policy_a)
        result_b = evaluate_eligibility(admission, permission, policy_b)

        self.assertEqual(admission, AdmissionDecision.ACCEPTED)
        self.assertEqual(result_a, ExecutionEligibility.ALLOWED)
        self.assertEqual(result_b, ExecutionEligibility.BLOCKED)

    def test_policy_change_does_not_require_permission_change(self):
        policy_a = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.ALLOWED,
            },
        )

        policy_b = Policy(
            "policy_b",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.BLOCKED,
            },
        )

        admission = AdmissionDecision.ACCEPTED
        permission = ExecutionPermission.GRANTED

        result_a = evaluate_eligibility(admission, permission, policy_a)
        result_b = evaluate_eligibility(admission, permission, policy_b)

        self.assertEqual(permission, ExecutionPermission.GRANTED)
        self.assertNotEqual(result_a, result_b)

    def test_admission_and_permission_do_not_have_intrinsic_execution_order(self):
        policy = Policy(
            "policy_a",
            {
                (
                    AdmissionDecision.ACCEPTED,
                    ExecutionPermission.GRANTED,
                ): ExecutionEligibility.ALLOWED,
            },
        )

        result_1 = evaluate_eligibility(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            policy,
        )

        result_2 = evaluate_eligibility(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            policy,
        )

        self.assertEqual(result_1, result_2)


if __name__ == "__main__":
    unittest.main()