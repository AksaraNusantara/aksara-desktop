import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalAdmissionDecision(Enum):
    ACCEPTED = auto()
    REJECTED = auto()


@dataclass(frozen=True)
class ExperimentalOperation:
    operation_id: str


@dataclass(frozen=True)
class ExperimentalExecutionRequest:
    request_id: str
    operation: ExperimentalOperation
    input_data: object


@dataclass(frozen=True)
class ExperimentalAdmissionDecisionObservation:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


class TestAdmissionDecisionOrderingAuthorityTransfer(unittest.TestCase):

    def test_same_observation_can_be_used_in_context_a(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        context_a = {
            "authority": "context-a",
            "observation": observation,
        }

        self.assertIs(
            context_a["observation"],
            observation,
        )

        self.assertEqual(
            context_a["authority"],
            "context-a",
        )

    def test_same_observation_can_be_used_in_context_b(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        context_b = {
            "authority": "context-b",
            "observation": observation,
        }

        self.assertIs(
            context_b["observation"],
            observation,
        )

        self.assertEqual(
            context_b["authority"],
            "context-b",
        )

    def test_same_observation_can_be_associated_with_two_contexts(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        context_a = {
            "authority": "context-a",
            "observation": observation,
        }

        context_b = {
            "authority": "context-b",
            "observation": observation,
        }

        self.assertIs(
            context_a["observation"],
            context_b["observation"],
        )

    def test_context_authority_can_change_without_mutating_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        context_a = {
            "authority": "context-a",
            "observation": observation,
        }

        context_b = {
            "authority": "context-b",
            "observation": observation,
        }

        self.assertNotEqual(
            context_a["authority"],
            context_b["authority"],
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_observation_identity_remains_stable_across_context_transfer(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        context_a = {"observation": observation}
        context_b = {"observation": observation}

        self.assertIs(
            context_a["observation"],
            context_b["observation"],
        )

    def test_decision_value_remains_stable_across_context_transfer(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        context_a = {
            "authority": "context-a",
            "observation": observation,
        }

        context_b = {
            "authority": "context-b",
            "observation": observation,
        }

        self.assertEqual(
            context_a["observation"].decision,
            context_b["observation"].decision,
        )

    def test_request_identity_remains_stable_across_context_transfer(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        context_a = {"observation": observation}
        context_b = {"observation": observation}

        self.assertEqual(
            context_a["observation"].request.request_id,
            "req.007",
        )

        self.assertEqual(
            context_b["observation"].request.request_id,
            "req.007",
        )

    def test_authority_is_not_part_of_observation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        context_a = {
            "authority": "context-a",
            "observation": observation,
        }

        context_b = {
            "authority": "context-b",
            "observation": observation,
        }

        self.assertIs(
            context_a["observation"],
            context_b["observation"],
        )

        self.assertNotEqual(
            context_a["authority"],
            context_b["authority"],
        )

    def test_authority_transfer_does_not_require_new_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        context_a = {
            "authority": "context-a",
            "observation": observation,
        }

        context_b = {
            "authority": "context-b",
            "observation": observation,
        }

        self.assertIs(
            context_a["observation"],
            context_b["observation"],
        )

    def test_authority_transfer_does_not_require_decision_mutation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        context_a = {
            "authority": "context-a",
            "observation": observation,
        }

        context_b = {
            "authority": "context-b",
            "observation": observation,
        }

        self.assertEqual(
            context_a["observation"].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            context_b["observation"].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_context_can_supply_authority_without_becoming_observation_property(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        context = {
            "authority": "external-policy",
            "observation": observation,
        }

        self.assertEqual(
            context["authority"],
            "external-policy",
        )

        self.assertEqual(
            context["observation"].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_minimal_model_can_transfer_authority_without_authority_field(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        context_a = {
            "authority": "context-a",
            "observation": observation,
        }

        context_b = {
            "authority": "context-b",
            "observation": observation,
        }

        self.assertNotIn(
            "ordering_authority",
            observation.__dict__,
        )

        self.assertIs(
            context_a["observation"],
            context_b["observation"],
        )


if __name__ == "__main__":
    unittest.main()