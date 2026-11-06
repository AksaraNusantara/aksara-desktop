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
#
# Capability → Execution
#
# No explicit Operation abstraction.
# ============================================================

@dataclass(frozen=True)
class CapabilityA:
    capability: ExperimentalCapability


@dataclass(frozen=True)
class ExecutionA:
    capability: ExperimentalCapability
    state: ExperimentalExecutionState
    output: object = None


def execute_capability_a(
    capability: CapabilityA,
    state: ExperimentalExecutionState,
    output=None,
):
    return ExecutionA(
        capability=capability.capability,
        state=state,
        output=output,
    )


# ============================================================
# Model B
#
# Capability → Operation → Execution
#
# Operation is an explicit intermediate abstraction.
# ============================================================

@dataclass(frozen=True)
class CapabilityB:
    capability: ExperimentalCapability


@dataclass(frozen=True)
class OperationB:
    capability: CapabilityB
    operation_name: str
    input_data: object = None


@dataclass(frozen=True)
class ExecutionB:
    operation: OperationB
    state: ExperimentalExecutionState
    output: object = None


def execute_operation_b(
    operation: OperationB,
    state: ExperimentalExecutionState,
    output=None,
):
    return ExecutionB(
        operation=operation,
        state=state,
        output=output,
    )


# ============================================================
# Model C
#
# Capability
# ├── Operation Definition
# └── Execution Instance
#
# Operation describes what can be invoked.
# Execution represents one occurrence.
# ============================================================

@dataclass(frozen=True)
class CapabilityC:
    capability: ExperimentalCapability


@dataclass(frozen=True)
class OperationDefinitionC:
    capability: CapabilityC
    operation_name: str


@dataclass(frozen=True)
class ExecutionC:
    operation: OperationDefinitionC
    state: ExperimentalExecutionState
    input_data: object = None
    output: object = None


def execute_operation_c(
    operation: OperationDefinitionC,
    state: ExperimentalExecutionState,
    input_data=None,
    output=None,
):
    return ExecutionC(
        operation=operation,
        state=state,
        input_data=input_data,
        output=output,
    )


class TestCapabilityOperationBoundary(unittest.TestCase):

    # --------------------------------------------------------
    # Model A
    # --------------------------------------------------------

    def test_model_a_capability_can_execute_directly(self):
        capability = CapabilityA(
            ExperimentalCapability.TRANSLITERATION
        )

        execution = execute_capability_a(
            capability,
            ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤ",
        )

        self.assertEqual(
            execution.capability,
            ExperimentalCapability.TRANSLITERATION,
        )

        self.assertEqual(
            execution.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            execution.output,
            "ꦲꦤ",
        )

    def test_model_a_does_not_require_explicit_operation_object(self):
        capability = CapabilityA(
            ExperimentalCapability.AUDIO_PLAYBACK
        )

        execution = execute_capability_a(
            capability,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertFalse(
            hasattr(execution, "operation")
        )

    # --------------------------------------------------------
    # Model B
    # --------------------------------------------------------

    def test_model_b_explicit_operation_can_exist(self):
        capability = CapabilityB(
            ExperimentalCapability.TRANSLITERATION
        )

        operation = OperationB(
            capability=capability,
            operation_name="transliterate",
            input_data={
                "source_text": "hanacaraka",
                "target_script": "javanese",
            },
        )

        self.assertEqual(
            operation.capability,
            capability,
        )

        self.assertEqual(
            operation.operation_name,
            "transliterate",
        )

    def test_model_b_execution_belongs_to_operation(self):
        capability = CapabilityB(
            ExperimentalCapability.TRANSLITERATION
        )

        operation = OperationB(
            capability=capability,
            operation_name="transliterate",
        )

        execution = execute_operation_b(
            operation,
            ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤ",
        )

        self.assertEqual(
            execution.operation,
            operation,
        )

        self.assertEqual(
            execution.state,
            ExperimentalExecutionState.SUCCESS,
        )

    def test_model_b_operation_can_carry_domain_input(self):
        capability = CapabilityB(
            ExperimentalCapability.TRANSLITERATION
        )

        operation = OperationB(
            capability=capability,
            operation_name="transliterate",
            input_data={
                "source_text": "abc",
                "target_script": "javanese",
            },
        )

        self.assertEqual(
            operation.input_data["source_text"],
            "abc",
        )

    # --------------------------------------------------------
    # Model C
    # --------------------------------------------------------

    def test_model_c_operation_definition_can_exist_without_execution(self):
        capability = CapabilityC(
            ExperimentalCapability.TRANSLITERATION
        )

        operation = OperationDefinitionC(
            capability=capability,
            operation_name="transliterate",
        )

        self.assertEqual(
            operation.capability,
            capability,
        )

        self.assertEqual(
            operation.operation_name,
            "transliterate",
        )

    def test_model_c_execution_represents_one_operation_occurrence(self):
        capability = CapabilityC(
            ExperimentalCapability.TRANSLITERATION
        )

        operation = OperationDefinitionC(
            capability=capability,
            operation_name="transliterate",
        )

        execution = execute_operation_c(
            operation,
            ExperimentalExecutionState.SUCCESS,
            input_data="hanacaraka",
            output="ꦲꦤꦕꦫꦏ",
        )

        self.assertEqual(
            execution.operation,
            operation,
        )

        self.assertEqual(
            execution.input_data,
            "hanacaraka",
        )

        self.assertEqual(
            execution.output,
            "ꦲꦤꦕꦫꦏ",
        )

    def test_model_c_same_operation_can_have_multiple_executions(self):
        capability = CapabilityC(
            ExperimentalCapability.TRANSLITERATION
        )

        operation = OperationDefinitionC(
            capability=capability,
            operation_name="transliterate",
        )

        execution_1 = execute_operation_c(
            operation,
            ExperimentalExecutionState.SUCCESS,
            input_data="abc",
            output="ꦲ",
        )

        execution_2 = execute_operation_c(
            operation,
            ExperimentalExecutionState.FAILED,
            input_data="invalid",
        )

        execution_3 = execute_operation_c(
            operation,
            ExperimentalExecutionState.NOT_EXECUTED,
            input_data="blocked",
        )

        self.assertEqual(
            execution_1.operation,
            operation,
        )

        self.assertEqual(
            execution_2.operation,
            operation,
        )

        self.assertEqual(
            execution_3.operation,
            operation,
        )

        self.assertEqual(
            execution_1.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            execution_2.state,
            ExperimentalExecutionState.FAILED,
        )

        self.assertEqual(
            execution_3.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    # --------------------------------------------------------
    # Cross-model semantic comparison
    # --------------------------------------------------------

    def test_model_a_and_model_c_can_represent_same_success(self):
        capability_a = CapabilityA(
            ExperimentalCapability.AUDIO_PLAYBACK
        )

        execution_a = execute_capability_a(
            capability_a,
            ExperimentalExecutionState.SUCCESS,
            output={
                "started": True,
            },
        )

        capability_c = CapabilityC(
            ExperimentalCapability.AUDIO_PLAYBACK
        )

        operation_c = OperationDefinitionC(
            capability=capability_c,
            operation_name="play",
        )

        execution_c = execute_operation_c(
            operation_c,
            ExperimentalExecutionState.SUCCESS,
            output={
                "started": True,
            },
        )

        self.assertEqual(
            execution_a.capability,
            execution_c.operation.capability.capability,
        )

        self.assertEqual(
            execution_a.state,
            execution_c.state,
        )

        self.assertEqual(
            execution_a.output,
            execution_c.output,
        )

    def test_operation_identity_can_be_distinct_from_capability_identity(self):
        capability = CapabilityC(
            ExperimentalCapability.TRANSLITERATION
        )

        transliterate = OperationDefinitionC(
            capability=capability,
            operation_name="transliterate",
        )

        normalize = OperationDefinitionC(
            capability=capability,
            operation_name="normalize",
        )

        self.assertEqual(
            transliterate.capability,
            normalize.capability,
        )

        self.assertNotEqual(
            transliterate.operation_name,
            normalize.operation_name,
        )

    def test_same_capability_can_expose_multiple_operations(self):
        capability = CapabilityC(
            ExperimentalCapability.TRANSLITERATION
        )

        operations = (
            OperationDefinitionC(
                capability=capability,
                operation_name="transliterate",
            ),
            OperationDefinitionC(
                capability=capability,
                operation_name="validate",
            ),
            OperationDefinitionC(
                capability=capability,
                operation_name="normalize",
            ),
        )

        self.assertEqual(
            len(operations),
            3,
        )

        for operation in operations:
            self.assertEqual(
                operation.capability,
                capability,
            )

    def test_operation_can_be_stable_while_execution_is_ephemeral(self):
        capability = CapabilityC(
            ExperimentalCapability.PROGRESS_PERSISTENCE
        )

        operation = OperationDefinitionC(
            capability=capability,
            operation_name="save_progress",
        )

        execution_1 = execute_operation_c(
            operation,
            ExperimentalExecutionState.SUCCESS,
            input_data={"score": 90},
            output={"saved": True},
        )

        execution_2 = execute_operation_c(
            operation,
            ExperimentalExecutionState.SUCCESS,
            input_data={"score": 95},
            output={"saved": True},
        )

        self.assertEqual(
            execution_1.operation,
            execution_2.operation,
        )

        self.assertNotEqual(
            execution_1.input_data,
            execution_2.input_data,
        )

        self.assertEqual(
            execution_1.state,
            execution_2.state,
        )


if __name__ == "__main__":
    unittest.main()