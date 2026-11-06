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


class ExperimentalNonExecutionReason(Enum):
    CAPABILITY_UNAVAILABLE = auto()
    PRECONDITION_NOT_MET = auto()


class ExperimentalFailureClassification(Enum):
    EXECUTION_ERROR = auto()


@dataclass(frozen=True)
class GenericCapabilityContract:
    capability: ExperimentalCapability


@dataclass(frozen=True)
class TransliterationContract:
    source_text: str
    target_script: str


@dataclass(frozen=True)
class AudioPlaybackContract:
    audio_asset: str
    volume: float


@dataclass(frozen=True)
class ProgressPersistenceContract:
    learner_id: str
    progress_data: dict


@dataclass(frozen=True)
class ExperimentalExecutionResult:
    capability: ExperimentalCapability
    state: ExperimentalExecutionState
    output: object = None
    non_execution_reason: (
        ExperimentalNonExecutionReason | None
    ) = None
    failure: (
        ExperimentalFailureClassification | None
    ) = None
    diagnostic: str | None = None


def generic_execution_projection(result):
    """
    Extract only semantics that Step 17 identified
    as potentially capability-generic.
    """
    return (
        result.state,
        result.non_execution_reason,
        result.failure,
        result.diagnostic,
    )


class TestCapabilityContractBoundary(unittest.TestCase):

    def test_generic_contract_contains_capability_identity(self):
        contract = GenericCapabilityContract(
            capability=ExperimentalCapability.TRANSLITERATION
        )

        self.assertEqual(
            contract.capability,
            ExperimentalCapability.TRANSLITERATION,
        )

    def test_specific_contract_contains_domain_input(self):
        contract = TransliterationContract(
            source_text="hanacaraka",
            target_script="javanese",
        )

        self.assertEqual(contract.source_text, "hanacaraka")
        self.assertEqual(contract.target_script, "javanese")

    def test_different_capabilities_have_different_specific_inputs(self):
        transliteration = TransliterationContract(
            source_text="hanacaraka",
            target_script="javanese",
        )

        audio = AudioPlaybackContract(
            audio_asset="lesson_01.wav",
            volume=0.8,
        )

        persistence = ProgressPersistenceContract(
            learner_id="learner-001",
            progress_data={"lesson": 3},
        )

        self.assertNotEqual(
            transliteration,
            audio,
        )

        self.assertNotEqual(
            audio,
            persistence,
        )

        self.assertNotEqual(
            transliteration,
            persistence,
        )

    def test_execution_result_is_independent_of_specific_input_shape(self):
        result = ExperimentalExecutionResult(
            capability=ExperimentalCapability.TRANSLITERATION,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤꦕꦫꦏ",
        )

        transliteration_input = TransliterationContract(
            source_text="hanacaraka",
            target_script="javanese",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            result.output,
            "ꦲꦤꦕꦫꦏ",
        )

        self.assertEqual(
            transliteration_input.target_script,
            "javanese",
        )

    def test_generic_execution_semantics_apply_to_multiple_capabilities(self):
        results = (
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.TRANSLITERATION,
                state=ExperimentalExecutionState.SUCCESS,
                output="ꦲ",
            ),
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.AUDIO_PLAYBACK,
                state=ExperimentalExecutionState.SUCCESS,
                output={"started": True},
            ),
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.PROGRESS_PERSISTENCE,
                state=ExperimentalExecutionState.SUCCESS,
                output={"saved": True},
            ),
        )

        for result in results:
            self.assertEqual(
                result.state,
                ExperimentalExecutionState.SUCCESS,
            )

    def test_failure_semantics_remain_generic(self):
        results = (
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.TRANSLITERATION,
                state=ExperimentalExecutionState.FAILED,
                failure=ExperimentalFailureClassification.EXECUTION_ERROR,
            ),
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.AUDIO_PLAYBACK,
                state=ExperimentalExecutionState.FAILED,
                failure=ExperimentalFailureClassification.EXECUTION_ERROR,
            ),
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.PROGRESS_PERSISTENCE,
                state=ExperimentalExecutionState.FAILED,
                failure=ExperimentalFailureClassification.EXECUTION_ERROR,
            ),
        )

        for result in results:
            self.assertEqual(
                result.state,
                ExperimentalExecutionState.FAILED,
            )

            self.assertEqual(
                result.failure,
                ExperimentalFailureClassification.EXECUTION_ERROR,
            )

    def test_non_execution_semantics_remain_generic(self):
        results = (
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.TRANSLITERATION,
                state=ExperimentalExecutionState.NOT_EXECUTED,
                non_execution_reason=(
                    ExperimentalNonExecutionReason.PRECONDITION_NOT_MET
                ),
            ),
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.AUDIO_PLAYBACK,
                state=ExperimentalExecutionState.NOT_EXECUTED,
                non_execution_reason=(
                    ExperimentalNonExecutionReason.CAPABILITY_UNAVAILABLE
                ),
            ),
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.PROGRESS_PERSISTENCE,
                state=ExperimentalExecutionState.NOT_EXECUTED,
                non_execution_reason=(
                    ExperimentalNonExecutionReason.PRECONDITION_NOT_MET
                ),
            ),
        )

        for result in results:
            self.assertEqual(
                result.state,
                ExperimentalExecutionState.NOT_EXECUTED,
            )

            self.assertIsNotNone(
                result.non_execution_reason,
            )

    def test_output_remains_capability_specific(self):
        transliteration_result = ExperimentalExecutionResult(
            capability=ExperimentalCapability.TRANSLITERATION,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤ",
        )

        audio_result = ExperimentalExecutionResult(
            capability=ExperimentalCapability.AUDIO_PLAYBACK,
            state=ExperimentalExecutionState.SUCCESS,
            output={
                "started": True,
                "duration_ms": 1200,
            },
        )

        persistence_result = ExperimentalExecutionResult(
            capability=ExperimentalCapability.PROGRESS_PERSISTENCE,
            state=ExperimentalExecutionState.SUCCESS,
            output={
                "saved": True,
                "record_id": "progress-001",
            },
        )

        self.assertIsInstance(
            transliteration_result.output,
            str,
        )

        self.assertIsInstance(
            audio_result.output,
            dict,
        )

        self.assertIsInstance(
            persistence_result.output,
            dict,
        )

    def test_generic_projection_ignores_capability_specific_output(self):
        transliteration = ExperimentalExecutionResult(
            capability=ExperimentalCapability.TRANSLITERATION,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲ",
        )

        audio = ExperimentalExecutionResult(
            capability=ExperimentalCapability.AUDIO_PLAYBACK,
            state=ExperimentalExecutionState.SUCCESS,
            output={
                "started": True,
            },
        )

        persistence = ExperimentalExecutionResult(
            capability=ExperimentalCapability.PROGRESS_PERSISTENCE,
            state=ExperimentalExecutionState.SUCCESS,
            output={
                "saved": True,
            },
        )

        projections = (
            generic_execution_projection(transliteration),
            generic_execution_projection(audio),
            generic_execution_projection(persistence),
        )

        for projection in projections:
            self.assertEqual(
                projection[0],
                ExperimentalExecutionState.SUCCESS,
            )

    def test_generic_contract_does_not_define_domain_specific_fields(self):
        generic = GenericCapabilityContract(
            capability=ExperimentalCapability.TRANSLITERATION
        )

        self.assertTrue(
            hasattr(generic, "capability")
        )

        self.assertFalse(
            hasattr(generic, "source_text")
        )

        self.assertFalse(
            hasattr(generic, "target_script")
        )

        self.assertFalse(
            hasattr(generic, "audio_asset")
        )

        self.assertFalse(
            hasattr(generic, "volume")
        )

        self.assertFalse(
            hasattr(generic, "learner_id")
        )

    def test_specific_contracts_do_not_need_to_share_input_shape(self):
        transliteration = TransliterationContract(
            source_text="abc",
            target_script="javanese",
        )

        audio = AudioPlaybackContract(
            audio_asset="lesson.wav",
            volume=1.0,
        )

        persistence = ProgressPersistenceContract(
            learner_id="learner-001",
            progress_data={"score": 95},
        )

        self.assertTrue(
            hasattr(transliteration, "source_text")
        )

        self.assertTrue(
            hasattr(audio, "audio_asset")
        )

        self.assertTrue(
            hasattr(persistence, "learner_id")
        )

        self.assertFalse(
            hasattr(transliteration, "audio_asset")
        )

        self.assertFalse(
            hasattr(audio, "learner_id")
        )

        self.assertFalse(
            hasattr(persistence, "source_text")
        )


if __name__ == "__main__":
    unittest.main()