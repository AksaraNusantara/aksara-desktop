"""
Recognition-to-Resolution Experiment.

AD-TR-01 — Comparative Study
Step 6 — Recognition-to-Resolution Experiment

This module is an experimental probe.

It does not implement production transliteration.
It does not define orthographic output.
It does not establish a final recognition contract.

The purpose is to observe what information is available
to a hypothetical Orthographic Resolution layer after
different recognition boundaries are applied.
"""

import unittest


# ---------------------------------------------------------------------
# Experiment Corpus
# ---------------------------------------------------------------------

CORPUS = [
    "nga",
    "ngka",
    "angka",
    "kang",
]


# ---------------------------------------------------------------------
# Known Recognition Patterns
#
# These represent experimental knowledge derived from
# currently known ScriptPack-style patterns.
#
# This is NOT production ScriptPack loading.
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
# Recognition Representations
# ---------------------------------------------------------------------

def recognize_longest_known_pattern(text):
    """
    Experimental Strategy C.

    Recognize the longest known pattern.

    Unknown input falls back to a single character.
    """

    patterns = sorted(
        KNOWN_PATTERNS,
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


def recognize_with_ng_candidate(text):
    """
    Experimental alternative strategy.

    'ng' is treated as a candidate recognition pattern.

    Important:
    This does NOT mean 'ng' is a confirmed token.
    The purpose is to compare what information becomes
    available to the next layer.
    """

    patterns = set(KNOWN_PATTERNS)

    patterns.add("ng")

    patterns = sorted(
        patterns,
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
# Resolution Probe
# ---------------------------------------------------------------------

def inspect_resolution_context(units):
    """
    Inspect information available to a hypothetical
    Orthographic Resolution layer.

    No transliteration decision is made here.
    """

    observations = []

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

        observations.append(
            {
                "index": index,
                "unit": unit,
                "known_pattern": unit in KNOWN_PATTERNS,
                "previous": previous_unit,
                "next": next_unit,
            }
        )

    return observations


# ---------------------------------------------------------------------
# Experiment Tests
# ---------------------------------------------------------------------

class TestRecognitionToResolution(unittest.TestCase):
    """
    Compare information available after recognition.

    The tests do not assert that one representation is
    orthographically correct.

    They only verify that each representation preserves
    the original input and allows context inspection.
    """

    def test_longest_known_pattern_representation(self):

        for text in CORPUS:

            with self.subTest(text=text):

                units = recognize_longest_known_pattern(text)

                observations = (
                    inspect_resolution_context(units)
                )

                print()
                print("=" * 60)
                print(
                    f"Input: {text}"
                )
                print(
                    "Strategy: Longest Known Pattern"
                )
                print(
                    f"Units: {units}"
                )
                print(
                    "Resolution Context:"
                )

                for observation in observations:

                    print(
                        "  "
                        f"[{observation['index']}] "
                        f"unit={observation['unit']!r}, "
                        f"known={observation['known_pattern']}, "
                        f"previous={observation['previous']!r}, "
                        f"next={observation['next']!r}"
                    )

                self.assertEqual(
                    "".join(units),
                    text,
                )

                self.assertEqual(
                    len(observations),
                    len(units),
                )

    def test_ng_candidate_representation(self):

        for text in CORPUS:

            with self.subTest(text=text):

                units = recognize_with_ng_candidate(text)

                observations = (
                    inspect_resolution_context(units)
                )

                print()
                print("=" * 60)
                print(
                    f"Input: {text}"
                )
                print(
                    "Strategy: NG Candidate"
                )
                print(
                    f"Units: {units}"
                )
                print(
                    "Resolution Context:"
                )

                for observation in observations:

                    print(
                        "  "
                        f"[{observation['index']}] "
                        f"unit={observation['unit']!r}, "
                        f"known={observation['known_pattern']}, "
                        f"previous={observation['previous']!r}, "
                        f"next={observation['next']!r}"
                    )

                self.assertEqual(
                    "".join(units),
                    text,
                )

                self.assertEqual(
                    len(observations),
                    len(units),
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)