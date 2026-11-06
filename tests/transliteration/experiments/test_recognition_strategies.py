"""
Recognition strategy experiment for Javanese transliteration.

AD-TR-01 — Comparative Study
Step 4 — Recognition Experiment

This module is an experimental test harness.

It does not define production behavior.
It does not define a transliteration contract.
It does not produce Javanese Unicode output.

The purpose is to compare recognition strategies and
collect evidence before making an architectural decision.
"""

import unittest


# ---------------------------------------------------------------------
# Experiment Corpus
# ---------------------------------------------------------------------

CORPUS = [
    "a",
    "ka",
    "nga",
    "nya",
    "dha",
    "tha",
    "ngka",
    "angka",
    "kang",
    "hanacaraka",
]


# ---------------------------------------------------------------------
# Strategy A
# Character-by-character recognition
# ---------------------------------------------------------------------

def recognize_by_character(text):
    """
    Split the input into individual characters.

    This strategy makes no assumptions about
    multi-character recognition patterns.
    """
    return list(text)


# ---------------------------------------------------------------------
# Strategy B
# Fixed pattern recognition
# ---------------------------------------------------------------------

FIXED_PATTERNS = [
    "nga",
    "nya",
    "dha",
    "tha",
    "ka",
]


def recognize_fixed_patterns(text):
    """
    Recognize known patterns from a fixed experiment list.

    Patterns are checked from longest to shortest.
    """

    patterns = sorted(
        FIXED_PATTERNS,
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
# Strategy C
# Longest known pattern
# ---------------------------------------------------------------------

SCRIPT_PACK_PATTERNS = {
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


def recognize_longest_known_pattern(text):
    """
    Recognize the longest available pattern.

    This simulates a data-driven recognition approach
    in which recognition patterns originate from
    known ScriptPack data.
    """

    patterns = sorted(
        SCRIPT_PACK_PATTERNS,
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
# Recognition Experiment
# ---------------------------------------------------------------------

class TestRecognitionStrategies(unittest.TestCase):
    """
    Experimental comparison of recognition strategies.

    The purpose of these tests is observation.

    Each strategy must preserve the original input
    when its recognized units are joined together.
    """

    def test_strategy_a_character_by_character(self):

        for text in CORPUS:

            with self.subTest(text=text):

                units = recognize_by_character(text)

                print(
                    f"\nInput      : {text}"
                )
                print(
                    f"Strategy A : {units}"
                )

                self.assertEqual(
                    "".join(units),
                    text,
                )

    def test_strategy_b_fixed_patterns(self):

        for text in CORPUS:

            with self.subTest(text=text):

                units = recognize_fixed_patterns(text)

                print(
                    f"\nInput      : {text}"
                )
                print(
                    f"Strategy B : {units}"
                )

                self.assertEqual(
                    "".join(units),
                    text,
                )

    def test_strategy_c_longest_known_pattern(self):

        for text in CORPUS:

            with self.subTest(text=text):

                units = recognize_longest_known_pattern(text)

                print(
                    f"\nInput      : {text}"
                )
                print(
                    f"Strategy C : {units}"
                )

                self.assertEqual(
                    "".join(units),
                    text,
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)