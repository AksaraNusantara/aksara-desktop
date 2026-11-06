# -*- coding: utf-8 -*-
"""
AD-TR-01 — Phase 2E-5 — Step 17
Experiment 17-4 — Output Semantic Generalization

Architecture probe only.

This experiment MUST NOT import or modify production code.
"""

import unittest
from dataclasses import dataclass
from enum import Enum, auto


# ============================================================
# Experimental Capability Types
# ============================================================


class ExperimentalCapability(Enum):
    TRANSLITERATION = auto()
    AUDIO_PLAYBACK = auto()
    PROGRESS_PERSISTENCE = auto()
    CHARACTER_LOOKUP = auto()
    CAPABILITY_DISCOVERY = auto()


class ExperimentalExecutionState(Enum):
    SUCCESS = auto()
    FAILED = auto()
    NOT_EXECUTED = auto()


class ExperimentalFailureClassification(Enum):
    EXECUTION_ERROR = auto()


# ============================================================
# Capability-Specific Output Models
# ============================================================


@dataclass(frozen=True)
class TransliterationOutput:
    text: str


@dataclass(frozen=True)
class AudioPlaybackOutput:
    started: bool
    duration_ms: int


@dataclass(frozen=True)
class ProgressPersistenceOutput:
    saved: bool
    record_id: str


@dataclass(frozen=True)
class CharacterLookupOutput:
    glyph: str
    latin: str


@dataclass(frozen=True)
class CapabilityDiscoveryOutput:
    capability_names: tuple[str, ...]


# ============================================================
# Generic Experimental Result
# ============================================================


@dataclass(frozen=True)
class ExperimentalExecutionResult:
    """
    Generic execution-result probe.

    The output is intentionally unconstrained.

    This is NOT a production API.
    """

    capability: ExperimentalCapability
    state: ExperimentalExecutionState
    output: object = None
    failure: ExperimentalFailureClassification = None
    diagnostic: str = None


# ============================================================
# Experiment 17-4
# ============================================================


class TestCapabilityOutputGeneralization(unittest.TestCase):

    def test_transliteration_can_return_text_output(self):
        output = TransliterationOutput(
            text="ꦲꦤꦕꦫꦏ",
        )

        result = ExperimentalExecutionResult(
            capability=ExperimentalCapability.TRANSLITERATION,
            state=ExperimentalExecutionState.SUCCESS,
            output=output,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertIsInstance(
            result.output,
            TransliterationOutput,
        )

        self.assertEqual(
            result.output.text,
            "ꦲꦤꦕꦫꦏ",
        )

    def test_audio_can_return_audio_specific_output(self):
        output = AudioPlaybackOutput(
            started=True,
            duration_ms=2500,
        )

        result = ExperimentalExecutionResult(
            capability=ExperimentalCapability.AUDIO_PLAYBACK,
            state=ExperimentalExecutionState.SUCCESS,
            output=output,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertIsInstance(
            result.output,
            AudioPlaybackOutput,
        )

        self.assertTrue(result.output.started)
        self.assertEqual(result.output.duration_ms, 2500)

    def test_persistence_can_return_persistence_specific_output(self):
        output = ProgressPersistenceOutput(
            saved=True,
            record_id="progress-001",
        )

        result = ExperimentalExecutionResult(
            capability=ExperimentalCapability.PROGRESS_PERSISTENCE,
            state=ExperimentalExecutionState.SUCCESS,
            output=output,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertIsInstance(
            result.output,
            ProgressPersistenceOutput,
        )

        self.assertTrue(result.output.saved)
        self.assertEqual(
            result.output.record_id,
            "progress-001",
        )

    def test_query_can_return_domain_specific_output(self):
        output = CharacterLookupOutput(
            glyph="ꦲ",
            latin="ha",
        )

        result = ExperimentalExecutionResult(
            capability=ExperimentalCapability.CHARACTER_LOOKUP,
            state=ExperimentalExecutionState.SUCCESS,
            output=output,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertIsInstance(
            result.output,
            CharacterLookupOutput,
        )

        self.assertEqual(result.output.glyph, "ꦲ")
        self.assertEqual(result.output.latin, "ha")

    def test_discovery_can_return_collection_output(self):
        output = CapabilityDiscoveryOutput(
            capability_names=(
                "transliteration",
                "audio_playback",
                "progress_persistence",
            ),
        )

        result = ExperimentalExecutionResult(
            capability=ExperimentalCapability.CAPABILITY_DISCOVERY,
            state=ExperimentalExecutionState.SUCCESS,
            output=output,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertIsInstance(
            result.output,
            CapabilityDiscoveryOutput,
        )

        self.assertEqual(
            result.output.capability_names,
            (
                "transliteration",
                "audio_playback",
                "progress_persistence",
            ),
        )

    def test_different_output_types_do_not_change_execution_semantics(self):
        """
        The result container remains semantically identical even
        when output types differ between capabilities.
        """

        results = (
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.TRANSLITERATION,
                state=ExperimentalExecutionState.SUCCESS,
                output=TransliterationOutput(text="ꦲ"),
            ),
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.AUDIO_PLAYBACK,
                state=ExperimentalExecutionState.SUCCESS,
                output=AudioPlaybackOutput(
                    started=True,
                    duration_ms=1000,
                ),
            ),
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.PROGRESS_PERSISTENCE,
                state=ExperimentalExecutionState.SUCCESS,
                output=ProgressPersistenceOutput(
                    saved=True,
                    record_id="001",
                ),
            ),
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.CHARACTER_LOOKUP,
                state=ExperimentalExecutionState.SUCCESS,
                output=CharacterLookupOutput(
                    glyph="ꦲ",
                    latin="ha",
                ),
            ),
            ExperimentalExecutionResult(
                capability=ExperimentalCapability.CAPABILITY_DISCOVERY,
                state=ExperimentalExecutionState.SUCCESS,
                output=CapabilityDiscoveryOutput(
                    capability_names=("transliteration",),
                ),
            ),
        )

        output_types = {
            type(result.output)
            for result in results
        }

        self.assertEqual(len(output_types), 5)

        for result in results:
            with self.subTest(capability=result.capability):
                self.assertEqual(
                    result.state,
                    ExperimentalExecutionState.SUCCESS,
                )

                self.assertIsNotNone(result.output)

    def test_failed_execution_does_not_require_output(self):
        """
        A failed execution does not require a successful output.
        """

        result = ExperimentalExecutionResult(
            capability=ExperimentalCapability.TRANSLITERATION,
            state=ExperimentalExecutionState.FAILED,
            failure=(
                ExperimentalFailureClassification.EXECUTION_ERROR
            ),
            diagnostic="synthetic execution error",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.FAILED,
        )

        self.assertIsNone(result.output)

        self.assertEqual(
            result.failure,
            ExperimentalFailureClassification.EXECUTION_ERROR,
        )

    def test_not_executed_does_not_require_output(self):
        """
        A non-executed operation does not require an output.
        """

        result = ExperimentalExecutionResult(
            capability=ExperimentalCapability.AUDIO_PLAYBACK,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            diagnostic="synthetic capability unavailable",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

        self.assertIsNone(result.output)
        self.assertIsNone(result.failure)


if __name__ == "__main__":
    unittest.main()