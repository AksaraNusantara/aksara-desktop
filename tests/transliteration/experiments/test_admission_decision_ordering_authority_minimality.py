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
    observation_id: str
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


class TestAdmissionDecisionOrderingAuthorityMinimality(unittest.TestCase):

    def test_minimal_context_can_hold_authority_scope_and_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.001",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        context = {
            "authority": "authority-a",
            "scope": "scope-a",
            "observation": observation,
        }

        self.assertEqual(
            context["authority"],
            "authority-a",
        )

        self.assertEqual(
            context["scope"],
            "scope-a",
        )

        self.assertIs(
            context["observation"],
            observation,
        )

    def test_minimal_context_preserves_observation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.002",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        context = {
            "authority": "authority-a",
            "scope": "scope-a",
            "observation": observation,
        }

        self.assertEqual(
            context["observation"].observation_id,
            "obs.002",
        )

    def test_minimal_context_preserves_decision_value(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.003",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        context = {
            "authority": "authority-a",
            "scope": "scope-a",
            "observation": observation,
        }

        self.assertEqual(
            context["observation"].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_minimal_context_preserves_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.004",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        context = {
            "authority": "authority-a",
            "scope": "scope-a",
            "observation": observation,
        }

        self.assertEqual(
            context["observation"].request.request_id,
            "req.004",
        )

    def test_minimal_context_does_not_require_authority_object(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.005",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        context = {
            "authority": "external-policy",
            "scope": "scope-a",
            "observation": observation,
        }

        self.assertEqual(
            context["authority"],
            "external-policy",
        )

    def test_minimal_context_does_not_require_scope_object(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.006",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        context = {
            "authority": "authority-a",
            "scope": "ordering-scope",
            "observation": observation,
        }

        self.assertEqual(
            context["scope"],
            "ordering-scope",
        )

    def test_minimal_context_does_not_require_context_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.007",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        context = {
            "authority": "authority-a",
            "scope": "scope-a",
            "observation": observation,
        }

        self.assertNotIn(
            "context_id",
            context,
        )

    def test_minimal_context_supports_multiple_observations(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request_a = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        request_b = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="carakan",
        )

        observation_a = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.008",
            request=request_a,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        observation_b = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.009",
            request=request_b,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        context = {
            "authority": "authority-a",
            "scope": "scope-a",
            "observations": (
                observation_a,
                observation_b,
            ),
        }

        self.assertEqual(
            len(context["observations"]),
            2,
        )

    def test_minimal_context_supports_same_observation_in_multiple_contexts(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.010",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        context_a = {
            "authority": "authority-a",
            "scope": "scope-a",
            "observation": observation,
        }

        context_b = {
            "authority": "authority-b",
            "scope": "scope-b",
            "observation": observation,
        }

        self.assertIs(
            context_a["observation"],
            context_b["observation"],
        )

    def test_minimal_context_supports_authority_change(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.011",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        context_a = {
            "authority": "authority-a",
            "scope": "scope-a",
            "observation": observation,
        }

        context_b = {
            "authority": "authority-b",
            "scope": "scope-a",
            "observation": observation,
        }

        self.assertNotEqual(
            context_a["authority"],
            context_b["authority"],
        )

        self.assertEqual(
            context_a["scope"],
            context_b["scope"],
        )

        self.assertIs(
            context_a["observation"],
            context_b["observation"],
        )

    def test_minimal_context_supports_scope_change(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.012",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        context_a = {
            "authority": "authority-a",
            "scope": "scope-a",
            "observation": observation,
        }

        context_b = {
            "authority": "authority-a",
            "scope": "scope-b",
            "observation": observation,
        }

        self.assertEqual(
            context_a["authority"],
            context_b["authority"],
        )

        self.assertNotEqual(
            context_a["scope"],
            context_b["scope"],
        )

        self.assertIs(
            context_a["observation"],
            context_b["observation"],
        )


if __name__ == "__main__":
    unittest.main()