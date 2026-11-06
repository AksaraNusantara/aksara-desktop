"""
Generic Candidate Extensibility Experiment.

AD-TR-01 — Comparative Study
Step 11 — Generic Candidate Extensibility Experiment

This experiment verifies whether the Recognition Candidate
abstraction remains generic when additional candidates are
introduced through data alone.

The additional candidate "ny" is experimental.

It does not define a production transliteration rule.
It does not modify the ScriptPack contract.
It exists only to test abstraction extensibility.
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


# ---------------------------------------------------------------------
# Experimental Recognition Candidates
# ---------------------------------------------------------------------

RECOGNITION_CANDIDATES = {
    "ng",
    "ny",
}


# ---------------------------------------------------------------------
# Experimental Corpus
# ---------------------------------------------------------------------

CORPUS = [
    "nga",
    "ngka",
    "angka",
    "kang",
    "nya",
    "nyka",
    "kany",
]


# ---------------------------------------------------------------------
# Recognition
# ---------------------------------------------------------------------

def recognize_patterns(text):
    """
    Recognize the longest available pattern.

    Known patterns and recognition candidates participate
    in the same recognition process.

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
    Classify a recognition unit.

    The logic must not contain candidate-specific identity checks.
    """

    if unit in KNOWN_PATTERNS:

        return "KNOWN_COMPLETE_PATTERN"

    if unit in RECOGNITION_CANDIDATES:

        return "RECOGNITION_CANDIDATE"

    return "UNKNOWN_FALLBACK"


# ---------------------------------------------------------------------
# Generic Context Classification
# ---------------------------------------------------------------------

def classify_context(units):
    """
    Inspect generic contextual information.

    This function does not know the identity of individual
    recognition candidates.
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
# Tests
# ---------------------------------------------------------------------

class TestCandidateExtensibility(unittest.TestCase):
    """
    Verify that multiple recognition candidates can be
    introduced without modifying generic logic.
    """

    def test_multiple_candidate_recognition(self):

        for text in CORPUS:

            with self.subTest(text=text):

                units = recognize_patterns(text)

                print()
                print("=" * 65)
                print(f"Input: {text}")
                print(f"Units: {units}")

                # Recognition must preserve the original input.
                self.assertEqual(
                    "".join(units),
                    text,
                )

    def test_multiple_candidate_classification(self):

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

                # Every recognition unit must receive
                # exactly one contextual classification.
                self.assertEqual(
                    len(decisions),
                    len(units),
                )

    def test_candidate_set_is_data_driven(self):
        """
        Verify that multiple candidates are represented
        through the candidate data set.
        """

        self.assertIn(
            "ng",
            RECOGNITION_CANDIDATES,
        )

        self.assertIn(
            "ny",
            RECOGNITION_CANDIDATES,
        )

        # Both candidates must be classified generically.
        self.assertEqual(
            classify_unit("ng"),
            "RECOGNITION_CANDIDATE",
        )

        self.assertEqual(
            classify_unit("ny"),
            "RECOGNITION_CANDIDATE",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)