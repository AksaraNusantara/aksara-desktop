import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalCapability(Enum):
    TRANSLITERATION = auto()
    AUDIO_PLAYBACK = auto()
    PROGRESS_PERSISTENCE = auto()


class ExperimentalExecutionState(Enum):
    SUCCESS = auto()
    FAILED = auto()
    NOT_EXECUTED = auto()


class ExperimentalFailureClassification(Enum):
    EXECUTION_ERROR = auto()


class ExperimentalNonExecutionReason(Enum):
    CAPABILITY_UNAVAILABLE = auto()
    PRECONDITION_NOT_MET = auto()


# ============================================================
# Model A
# Capability owns execution semantics
# ============================================================

@dataclass(frozen=True)
class CapabilityOwnedExecution:
    state: ExperimentalExecutionState
    failure: ExperimentalFailureClassification | None = None
    non_execution_reason: (
        ExperimentalNonExecutionReason | None
    ) = None


@dataclass(frozen=True)
class CapabilityWithOwnedExecution:
    capability: ExperimentalCapability
    execution: CapabilityOwnedExecution


# ============================================================
# Model B
# Capability contract is independent from execution layer
# ============================================================

@dataclass(frozen=True)
class IndependentCapability:
    capability: ExperimentalCapability


@dataclass(frozen=True)
class GenericExecution:
    capability: ExperimentalCapability
    state: ExperimentalExecutionState
    failure: ExperimentalFailureClassification | None = None
    non_execution_reason: (
        ExperimentalNonExecutionReason | None
    ) = None


class GenericExecutionLayer:

    @staticmethod
    def execute(
        capability: IndependentCapability,
        state: ExperimentalExecutionState,
        failure=None,
        non_execution_reason=None,
    ):
        return GenericExecution(
            capability=capability.capability,
            state=state,
            failure=failure,
            non_execution_reason=non_execution_reason,
        )


class TestCapabilityExecutionOwnership(unittest.TestCase):

    # --------------------------------------------------------
    # Model A
    # --------------------------------------------------------

    def test_model_a_capability_can_contain_execution(self):
        capability = CapabilityWithOwnedExecution(
            capability=ExperimentalCapability.TRANSLITERATION,
            execution=CapabilityOwnedExecution(
                state=ExperimentalExecutionState.SUCCESS,
            ),
        )

        self.assertEqual(
            capability.capability,
            ExperimentalCapability.TRANSLITERATION,
        )

        self.assertEqual(
            capability.execution.state,
            ExperimentalExecutionState.SUCCESS,
        )

    def test_model_a_execution_is_structurally_bound_to_capability(self):
        capability = CapabilityWithOwnedExecution(
            capability=ExperimentalCapability.AUDIO_PLAYBACK,
            execution=CapabilityOwnedExecution(
                state=ExperimentalExecutionState.FAILED,
                failure=(
                    ExperimentalFailureClassification.EXECUTION_ERROR
                ),
            ),
        )

        self.assertIsNotNone(capability.execution)
        self.assertEqual(
            capability.execution.failure,
            ExperimentalFailureClassification.EXECUTION_ERROR,
        )

    # --------------------------------------------------------
    # Model B
    # --------------------------------------------------------

    def test_model_b_capability_can_exist_without_execution(self):
        capability = IndependentCapability(
            capability=ExperimentalCapability.TRANSLITERATION,
        )

        self.assertEqual(
            capability.capability,
            ExperimentalCapability.TRANSLITERATION,
        )

    def test_model_b_execution_layer_can_execute_capability(self):
        capability = IndependentCapability(
            capability=ExperimentalCapability.TRANSLITERATION,
        )

        execution = GenericExecutionLayer.execute(
            capability,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            execution.capability,
            capability.capability,
        )

        self.assertEqual(
            execution.state,
            ExperimentalExecutionState.SUCCESS,
        )

    def test_model_b_execution_layer_is_reusable_across_capabilities(self):
        capabilities = (
            IndependentCapability(
                ExperimentalCapability.TRANSLITERATION
            ),
            IndependentCapability(
                ExperimentalCapability.AUDIO_PLAYBACK
            ),
            IndependentCapability(
                ExperimentalCapability.PROGRESS_PERSISTENCE
            ),
        )

        for capability in capabilities:
            execution = GenericExecutionLayer.execute(
                capability,
                ExperimentalExecutionState.SUCCESS,
            )

            self.assertEqual(
                execution.capability,
                capability.capability,
            )

            self.assertEqual(
                execution.state,
                ExperimentalExecutionState.SUCCESS,
            )

    # --------------------------------------------------------
    # Ownership independence probes
    # --------------------------------------------------------

    def test_model_b_execution_can_be_created_without_mutating_capability(self):
        capability = IndependentCapability(
            ExperimentalCapability.AUDIO_PLAYBACK
        )

        original_capability = capability

        execution = GenericExecutionLayer.execute(
            capability,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            capability,
            original_capability,
        )

        self.assertEqual(
            execution.capability,
            capability.capability,
        )

    def test_model_b_same_capability_can_have_multiple_execution_results(self):
        capability = IndependentCapability(
            ExperimentalCapability.PROGRESS_PERSISTENCE
        )

        success = GenericExecutionLayer.execute(
            capability,
            ExperimentalExecutionState.SUCCESS,
        )

        failure = GenericExecutionLayer.execute(
            capability,
            ExperimentalExecutionState.FAILED,
            failure=(
                ExperimentalFailureClassification.EXECUTION_ERROR
            ),
        )

        not_executed = GenericExecutionLayer.execute(
            capability,
            ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.PRECONDITION_NOT_MET
            ),
        )

        self.assertEqual(
            success.capability,
            capability.capability,
        )

        self.assertEqual(
            failure.capability,
            capability.capability,
        )

        self.assertEqual(
            not_executed.capability,
            capability.capability,
        )

        self.assertEqual(
            success.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            failure.state,
            ExperimentalExecutionState.FAILED,
        )

        self.assertEqual(
            not_executed.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    def test_model_b_execution_layer_does_not_need_domain_specific_input_shape(self):
        capability = IndependentCapability(
            ExperimentalCapability.TRANSLITERATION
        )

        execution = GenericExecutionLayer.execute(
            capability,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            execution.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertFalse(
            hasattr(execution, "source_text")
        )

        self.assertFalse(
            hasattr(execution, "target_script")
        )

    def test_model_b_execution_semantics_remain_same_for_different_capabilities(self):
        capabilities = (
            ExperimentalCapability.TRANSLITERATION,
            ExperimentalCapability.AUDIO_PLAYBACK,
            ExperimentalCapability.PROGRESS_PERSISTENCE,
        )

        for capability_type in capabilities:
            capability = IndependentCapability(capability_type)

            execution = GenericExecutionLayer.execute(
                capability,
                ExperimentalExecutionState.NOT_EXECUTED,
                non_execution_reason=(
                    ExperimentalNonExecutionReason.CAPABILITY_UNAVAILABLE
                ),
            )

            self.assertEqual(
                execution.state,
                ExperimentalExecutionState.NOT_EXECUTED,
            )

            self.assertEqual(
                execution.non_execution_reason,
                ExperimentalNonExecutionReason.CAPABILITY_UNAVAILABLE,
            )

    # --------------------------------------------------------
    # Comparison probes
    # --------------------------------------------------------

    def test_both_models_can_represent_same_execution_semantics(self):
        model_a = CapabilityWithOwnedExecution(
            capability=ExperimentalCapability.TRANSLITERATION,
            execution=CapabilityOwnedExecution(
                state=ExperimentalExecutionState.SUCCESS,
            ),
        )

        capability_b = IndependentCapability(
            ExperimentalCapability.TRANSLITERATION
        )

        model_b = GenericExecutionLayer.execute(
            capability_b,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            model_a.capability,
            model_b.capability,
        )

        self.assertEqual(
            model_a.execution.state,
            model_b.state,
        )

    def test_model_b_preserves_separation_of_concerns(self):
        capability = IndependentCapability(
            ExperimentalCapability.TRANSLITERATION
        )

        execution = GenericExecutionLayer.execute(
            capability,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertTrue(
            hasattr(capability, "capability")
        )

        self.assertFalse(
            hasattr(capability, "state")
        )

        self.assertTrue(
            hasattr(execution, "state")
        )

        self.assertTrue(
            hasattr(execution, "capability")
        )


if __name__ == "__main__":
    unittest.main()