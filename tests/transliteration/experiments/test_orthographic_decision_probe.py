"""
Minimal Orthographic Decision Probe.

AD-TR-01 — Comparative Study
Step 8 — Minimal Orthographic Decision Probe

This module is an experimental probe.

It does not produce Javanese Unicode.
It does not implement production transliteration.
It does not define the final orthographic contract.

The purpose is to compare how different recognition
representations expose contextual information to a
hypothetical Orthographic Resolution layer.
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
# Experimental Corpus
# ---------------------------------------------------------------------

CORPUS = [
    "nga",
    "ngka",
    "angka",
    "kang",
]


# ---------------------------------------------------------------------
# Recognition Strategies
# ---------------------------------------------------------------------

def recognize_longest_known_pattern(text):
    """
    Recognize the longest known ScriptPack-style pattern.

    Unknown input falls back to individual characters.
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
    Experimental alternative recognition strategy.

    'ng' is added as a recognition candidate.

    This does not define 'ng' as a known script character.
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
# Minimal Decision Probe
# ---------------------------------------------------------------------

def classify_units(units):
    """
    Classify contextual information exposed by recognition.

    The classification is experimental and descriptive.
    It does not determine orthographic output.
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

        # -------------------------------------------------------------
        # 1. Known complete pattern
        # -------------------------------------------------------------

        if unit in KNOWN_PATTERNS:

            classification = "KNOWN_COMPLETE_PATTERN"

        # -------------------------------------------------------------
        # 2. Candidate 'ng' before known pattern
        # -------------------------------------------------------------

        elif (
            unit == "ng"
            and next_unit in KNOWN_PATTERNS
        ):

            classification = "CANDIDATE_BEFORE_KNOWN"

        # -------------------------------------------------------------
        # 3. Candidate 'ng' in final position
        # -------------------------------------------------------------

        elif (
            unit == "ng"
            and next_unit is None
        ):

            classification = "FINAL_CANDIDATE"

        # -------------------------------------------------------------
        # 4. Unknown fallback
        # -------------------------------------------------------------

        else:

            classification = "UNKNOWN_FALLBACK"

        decisions.append(
            {
                "index": index,
                "unit": unit,
                "classification": classification,
                "previous": previous_unit,
                "next": next_unit,
            }
        )

    return decisions


# ---------------------------------------------------------------------
# Experiment Tests
# ---------------------------------------------------------------------

class TestOrthographicDecisionProbe(unittest.TestCase):
    """
    Compare contextual information exposed by two
    recognition representations.

    The experiment does not assert that either strategy
    is orthographically correct.
    """

    def test_longest_known_pattern_context(self):

        for text in CORPUS:

            with self.subTest(text=text):

                units = recognize_longest_known_pattern(text)
                decisions = classify_units(units)

                print()
                print("=" * 65)
                print(f"Input: {text}")
                print("Strategy: Longest Known Pattern")
                print(f"Units: {units}")
                print("Decision Context:")

                for decision in decisions:

                    print(
                        f"  [{decision['index']}] "
                        f"unit={decision['unit']!r}, "
                        f"classification="
                        f"{decision['classification']}, "
                        f"previous={decision['previous']!r}, "
                        f"next={decision['next']!r}"
                    )

                # Invariant:
                # recognition must preserve the input.
                self.assertEqual(
                    "".join(units),
                    text,
                )

                # Probe must inspect every unit.
                self.assertEqual(
                    len(decisions),
                    len(units),
                )

    def test_ng_candidate_context(self):

        for text in CORPUS:

            with self.subTest(text=text):

                units = recognize_with_ng_candidate(text)
                decisions = classify_units(units)

                print()
                print("=" * 65)
                print(f"Input: {text}")
                print("Strategy: NG Candidate")
                print(f"Units: {units}")
                print("Decision Context:")

                for decision in decisions:

                    print(
                        f"  [{decision['index']}] "
                        f"unit={decision['unit']!r}, "
                        f"classification="
                        f"{decision['classification']}, "
                        f"previous={decision['previous']!r}, "
                        f"next={decision['next']!r}"
                    )

                # Invariant:
                # recognition must preserve the input.
                self.assertEqual(
                    "".join(units),
                    text,
                )

                # Probe must inspect every unit.
                self.assertEqual(
                    len(decisions),
                    len(units),
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)