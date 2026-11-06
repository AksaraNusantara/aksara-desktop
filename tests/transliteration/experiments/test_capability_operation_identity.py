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
# Capability Identity
#
# Represents an available capability/domain.
# ============================================================

@dataclass(frozen=True)
class Capability:
    capability_id: str
    capability_type: ExperimentalCapability


# ============================================================
# Operation Identity
#
# Represents a distinct operation provided by a capability.
# ============================================================

@dataclass(frozen=True)
class Operation:
    operation_id: str
    capability: Capability
    operation_name: str


# ============================================================
# Execution Identity
#
# Represents one occurrence of an operation being executed.
# ============================================================

@dataclass(frozen=True)
class Execution:
    execution_id: str
    operation: Operation
    state: ExperimentalExecutionState
    output: object = None
    failure: ExperimentalFailureClassification | None = None
    non_execution_reason: (
        ExperimentalNonExecutionReason | None
    ) = None


class TestCapabilityOperationIdentity(unittest.TestCase):

    # --------------------------------------------------------
    # Capability identity
    # --------------------------------------------------------

    def test_capability_has_its_own_identity(self):
        capability = Capability(
            capability_id="cap.transliteration",
            capability_type=ExperimentalCapability.TRANSLITERATION,
        )

        self.assertEqual(
            capability.capability_id,
            "cap.transliteration",
        )

        self.assertEqual(
            capability.capability_type,
            ExperimentalCapability.TRANSLITERATION,
        )

    def test_same_capability_identity_can_be_shared_by_multiple_operations(self):
        capability = Capability(
            capability_id="cap.transliteration",
            capability_type=ExperimentalCapability.TRANSLITERATION,
        )

        transliterate = Operation(
            operation_id="op.transliterate",
            capability=capability,
            operation_name="transliterate",
        )

        validate = Operation(
            operation_id="op.validate",
            capability=capability,
            operation_name="validate",
        )

        self.assertEqual(
            transliterate.capability,
            capability,
        )

        self.assertEqual(
            validate.capability,
            capability,
        )

        self.assertEqual(
            transliterate.capability.capability_id,
            validate.capability.capability_id,
        )

    # --------------------------------------------------------
    # Operation identity
    # --------------------------------------------------------

    def test_operations_have_distinct_identity(self):
        capability = Capability(
            capability_id="cap.transliteration",
            capability_type=ExperimentalCapability.TRANSLITERATION,
        )

        transliterate = Operation(
            operation_id="op.transliterate",
            capability=capability,
            operation_name="transliterate",
        )

        validate = Operation(
            operation_id="op.validate",
            capability=capability,
            operation_name="validate",
        )

        self.assertNotEqual(
            transliterate.operation_id,
            validate.operation_id,
        )

        self.assertNotEqual(
            transliterate.operation_name,
            validate.operation_name,
        )

    def test_operation_identity_does_not_replace_capability_identity(self):
        capability = Capability(
            capability_id="cap.audio",
            capability_type=ExperimentalCapability.AUDIO_PLAYBACK,
        )

        play = Operation(
            operation_id="op.play",
            capability=capability,
            operation_name="play",
        )

        self.assertEqual(
            play.capability.capability_id,
            "cap.audio",
        )

        self.assertNotEqual(
            play.operation_id,
            play.capability.capability_id,
        )

    # --------------------------------------------------------
    # Execution identity
    # --------------------------------------------------------

    def test_execution_has_distinct_identity(self):
        capability = Capability(
            capability_id="cap.transliteration",
            capability_type=ExperimentalCapability.TRANSLITERATION,
        )

        operation = Operation(
            operation_id="op.transliterate",
            capability=capability,
            operation_name="transliterate",
        )

        execution = Execution(
            execution_id="exec.001",
            operation=operation,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤ",
        )

        self.assertEqual(
            execution.execution_id,
            "exec.001",
        )

        self.assertNotEqual(
            execution.execution_id,
            operation.operation_id,
        )

        self.assertNotEqual(
            execution.execution_id,
            capability.capability_id,
        )

    def test_same_operation_can_have_multiple_execution_identities(self):
        capability = Capability(
            capability_id="cap.transliteration",
            capability_type=ExperimentalCapability.TRANSLITERATION,
        )

        operation = Operation(
            operation_id="op.transliterate",
            capability=capability,
            operation_name="transliterate",
        )

        execution_1 = Execution(
            execution_id="exec.001",
            operation=operation,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲ",
        )

        execution_2 = Execution(
            execution_id="exec.002",
            operation=operation,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦤ",
        )

        self.assertEqual(
            execution_1.operation,
            operation,
        )

        self.assertEqual(
            execution_2.operation,
            operation,
        )

        self.assertNotEqual(
            execution_1.execution_id,
            execution_2.execution_id,
        )

    # --------------------------------------------------------
    # Identity chain
    # --------------------------------------------------------

    def test_identity_chain_is_capability_to_operation_to_execution(self):
        capability = Capability(
            capability_id="cap.persistence",
            capability_type=ExperimentalCapability.PROGRESS_PERSISTENCE,
        )

        operation = Operation(
            operation_id="op.save_progress",
            capability=capability,
            operation_name="save_progress",
        )

        execution = Execution(
            execution_id="exec.001",
            operation=operation,
            state=ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            execution.operation.capability,
            capability,
        )

        self.assertEqual(
            execution.operation.operation_id,
            "op.save_progress",
        )

        self.assertEqual(
            execution.execution_id,
            "exec.001",
        )

    # --------------------------------------------------------
    # Same capability, different operations
    # --------------------------------------------------------

    def test_same_capability_can_expose_multiple_operations(self):
        capability = Capability(
            capability_id="cap.audio",
            capability_type=ExperimentalCapability.AUDIO_PLAYBACK,
        )

        play = Operation(
            operation_id="op.play",
            capability=capability,
            operation_name="play",
        )

        pause = Operation(
            operation_id="op.pause",
            capability=capability,
            operation_name="pause",
        )

        stop = Operation(
            operation_id="op.stop",
            capability=capability,
            operation_name="stop",
        )

        operations = (play, pause, stop)

        self.assertEqual(
            len(operations),
            3,
        )

        for operation in operations:
            self.assertEqual(
                operation.capability,
                capability,
            )

    # --------------------------------------------------------
    # Different capabilities, same operation name
    # --------------------------------------------------------

    def test_same_operation_name_does_not_imply_same_operation_identity(self):
        transliteration_capability = Capability(
            capability_id="cap.transliteration",
            capability_type=ExperimentalCapability.TRANSLITERATION,
        )

        persistence_capability = Capability(
            capability_id="cap.persistence",
            capability_type=ExperimentalCapability.PROGRESS_PERSISTENCE,
        )

        operation_a = Operation(
            operation_id="op.validate.transliteration",
            capability=transliteration_capability,
            operation_name="validate",
        )

        operation_b = Operation(
            operation_id="op.validate.progress",
            capability=persistence_capability,
            operation_name="validate",
        )

        self.assertEqual(
            operation_a.operation_name,
            operation_b.operation_name,
        )

        self.assertNotEqual(
            operation_a.operation_id,
            operation_b.operation_id,
        )

        self.assertNotEqual(
            operation_a.capability,
            operation_b.capability,
        )

    # --------------------------------------------------------
    # Execution state belongs to execution occurrence
    # --------------------------------------------------------

    def test_same_operation_can_have_different_execution_states(self):
        capability = Capability(
            capability_id="cap.transliteration",
            capability_type=ExperimentalCapability.TRANSLITERATION,
        )

        operation = Operation(
            operation_id="op.transliterate",
            capability=capability,
            operation_name="transliterate",
        )

        success = Execution(
            execution_id="exec.success",
            operation=operation,
            state=ExperimentalExecutionState.SUCCESS,
        )

        failed = Execution(
            execution_id="exec.failed",
            operation=operation,
            state=ExperimentalExecutionState.FAILED,
            failure=ExperimentalFailureClassification.EXECUTION_ERROR,
        )

        not_executed = Execution(
            execution_id="exec.skipped",
            operation=operation,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.PRECONDITION_NOT_MET
            ),
        )

        self.assertEqual(
            success.operation,
            failed.operation,
        )

        self.assertEqual(
            failed.operation,
            not_executed.operation,
        )

        self.assertEqual(
            success.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            failed.state,
            ExperimentalExecutionState.FAILED,
        )

        self.assertEqual(
            not_executed.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    # --------------------------------------------------------
    # Identity independence
    # --------------------------------------------------------

    def test_changing_execution_does_not_change_operation_identity(self):
        capability = Capability(
            capability_id="cap.transliteration",
            capability_type=ExperimentalCapability.TRANSLITERATION,
        )

        operation = Operation(
            operation_id="op.transliterate",
            capability=capability,
            operation_name="transliterate",
        )

        execution_a = Execution(
            execution_id="exec.001",
            operation=operation,
            state=ExperimentalExecutionState.SUCCESS,
        )

        execution_b = Execution(
            execution_id="exec.002",
            operation=operation,
            state=ExperimentalExecutionState.FAILED,
            failure=ExperimentalFailureClassification.EXECUTION_ERROR,
        )

        self.assertEqual(
            execution_a.operation.operation_id,
            execution_b.operation.operation_id,
        )

        self.assertEqual(
            execution_a.operation.operation_name,
            execution_b.operation.operation_name,
        )

    def test_identity_levels_are_distinct(self):
        capability = Capability(
            capability_id="cap.transliteration",
            capability_type=ExperimentalCapability.TRANSLITERATION,
        )

        operation = Operation(
            operation_id="op.transliterate",
            capability=capability,
            operation_name="transliterate",
        )

        execution = Execution(
            execution_id="exec.001",
            operation=operation,
            state=ExperimentalExecutionState.SUCCESS,
        )

        identities = (
            capability.capability_id,
            operation.operation_id,
            execution.execution_id,
        )

        self.assertEqual(
            len(set(identities)),
            3,
        )


if __name__ == "__main__":
    unittest.main()