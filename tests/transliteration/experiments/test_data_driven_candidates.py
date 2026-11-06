"""
Data-Driven Recognition Candidate Experiment.

AD-TR-01 — Comparative Study
Step 10 — Data-Driven Recognition Candidate Experiment

This module is an experimental probe.

It does not implement production transliteration.
It does not produce Javanese Unicode.
It does not define the final ScriptPack contract.

The purpose is to verify whether recognition candidates
can be represented as data and processed by generic logic,
without hard-coded knowledge of a specific candidate such
as "ng".
"""

import unittest


# ---------------------------------------------------------------------
# Experimental Recognition Knowledge
# ---------------------------------------------------------------------

KNOWN_PATTERNS = {
    "ha",
    "na",
    "ca",
    "ra",
    "ka",
    "da",
    "ta",
    "sa",
    "wa",
    "la",
    "pa",
    "dha",
    "ja",
    "ya",
    "nya",
    "ma",
    "ga",
    "ba",
    "tha",
    "nga",
}


RECOGNITION_CANDIDATES = {
    "ng",
}


# ---------------------------------------------------------------------
# Experimental Corpus
# ---------------------------------------------------------------------

CORPUS = [
    "nga",
    "ngka",
    "angka",
    "kang",
]


# ---------------------------------------------------------------------
# Recognition
# ---------------------------------------------------------------------

def recognize_patterns(text):
    """
    Recognize the longest available pattern.

    Both known patterns and recognition candidates
    participate in recognition.

    Recognition priority is determined by longest match.
    Unknown input falls back to individual characters.
    """

    available_patterns = (
        KNOWN_PATTERNS
        | RECOGNITION_CANDIDATES
    )

    patterns = sorted(
        available_patterns,
        key=len,
        reverse=True,
    )

    units = []
    position = 0

    while position < len(text):

        matched_pattern = None

        for pattern in patterns:

            if text.startswith(pattern, position):
                matched_pattern = pattern
                break

        if matched_pattern is not None:

            units.append(matched_pattern)
            position += len(matched_pattern)

        else:

            units.append(text[position])
            position += 1

    return units


# ---------------------------------------------------------------------
# Generic Unit Classification
# ---------------------------------------------------------------------

def classify_unit(unit):
    """
    Classify one recognition unit.

    Generic logic does not contain knowledge of
    any specific candidate string.
    """

    if unit in KNOWN_PATTERNS:

        return "KNOWN_COMPLETE_PATTERN"

    if unit in RECOGNITION_CANDIDATES:

        return "RECOGNITION_CANDIDATE"

    return "UNKNOWN_FALLBACK"


# ---------------------------------------------------------------------
# Context Classification
# ---------------------------------------------------------------------

def classify_context(units):
    """
    Inspect contextual information available after
    data-driven recognition.

    No orthographic output is produced.
    """

    decisions = []

    for index, unit in enumerate(units):

        previous_unit = (
            units[index - 1]
            if index > 0
            else None
        )

        next_unit = (
            units[index + 1]
            if index < len(units) - 1
            else None
        )

        unit_type = classify_unit(unit)

        # -------------------------------------------------------------
        # Generic contextual classification
        # -------------------------------------------------------------

        if (
            unit_type == "RECOGNITION_CANDIDATE"
            and next_unit in KNOWN_PATTERNS
        ):

            context = "CANDIDATE_BEFORE_KNOWN"

        elif (
            unit_type == "RECOGNITION_CANDIDATE"
            and next_unit is None
        ):

            context = "FINAL_CANDIDATE"

        else:

            context = unit_type

        decisions.append(
            {
                "index": index,
                "unit": unit,
                "unit_type": unit_type,
                "context": context,
                "previous": previous_unit,
                "next": next_unit,
            }
        )

    return decisions


# ---------------------------------------------------------------------
# Experiment Tests
# ---------------------------------------------------------------------

class TestDataDrivenCandidates(unittest.TestCase):
    """
    Verify that candidate recognition can be handled
    through data rather than hard-coded unit identity.
    """

    def test_data_driven_recognition(self):

        for text in CORPUS:

            with self.subTest(text=text):

                units = recognize_patterns(text)

                print()
                print("=" * 65)
                print(f"Input: {text}")
                print(f"Units: {units}")

                self.assertEqual(
                    "".join(units),
                    text,
                )

    def test_data_driven_context_classification(self):

        for text in CORPUS:

            with self.subTest(text=text):

                units = recognize_patterns(text)
                decisions = classify_context(units)

                print()
                print("=" * 65)
                print(f"Input: {text}")
                print(f"Units: {units}")
                print("Classification:")

                for decision in decisions:

                    print(
                        f"  [{decision['index']}] "
                        f"unit={decision['unit']!r}, "
                        f"type={decision['unit_type']}, "
                        f"context={decision['context']}, "
                        f"previous={decision['previous']!r}, "
                        f"next={decision['next']!r}"
                    )

                self.assertEqual(
                    len(decisions),
                    len(units),
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)