"""
Recognition Candidate Abstraction Boundary Stress Test.

AD-TR-01 — Comparative Study
Step 12 — Abstraction Boundary Stress Test

This experiment intentionally tests the boundaries of the
Recognition Candidate abstraction.

The purpose is not to define production transliteration rules.

The experiment attempts to identify conditions where:

- candidate overlap becomes ambiguous
- candidate priority becomes unclear
- standalone candidates lack sufficient context
- consecutive candidates expose limitations in the current
  context model

No production architecture decision is made here.
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
    "n",
    "ng",
    "ny",
}


# ---------------------------------------------------------------------
# Recognition
# ---------------------------------------------------------------------

def recognize_patterns(text):
    """
    Recognize the longest available pattern.

    Known patterns and recognition candidates participate
    in the same recognition process.

    The function intentionally contains no special handling
    for individual candidate identities.
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
    Classify units using the current generic context model.

    The current model only distinguishes:

    - candidate before known pattern
    - final candidate
    - ordinary unit classification

    This intentionally allows the experiment to reveal
    situations that cannot be sufficiently represented.
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
# Diagnostic Helper
# ---------------------------------------------------------------------

def print_decisions(title, text):

    units = recognize_patterns(text)
    decisions = classify_context(units)

    print()
    print("=" * 70)
    print(f"Boundary: {title}")
    print(f"Input   : {text}")
    print(f"Units   : {units}")
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

    return units, decisions


# ---------------------------------------------------------------------
# Boundary Tests
# ---------------------------------------------------------------------

class TestCandidateBoundaries(unittest.TestCase):

    def test_candidate_vs_candidate_overlap(self):
        """
        Test overlapping candidates.

        Candidate set:
            n
            ng

        Expected recognition should prefer the longest match.
        """

        units, _ = print_decisions(
            "Candidate vs Candidate Overlap",
            "ngka",
        )

        self.assertEqual(
            units,
            ["ng", "ka"],
        )

    def test_candidate_vs_known_overlap(self):
        """
        Test candidate and known pattern overlap.

        Candidate:
            ng

        Known pattern:
            nga

        The longer known pattern must remain intact.
        """

        units, _ = print_decisions(
            "Candidate vs Known Pattern Overlap",
            "nga",
        )

        self.assertEqual(
            units,
            ["nga"],
        )

    def test_standalone_candidate(self):
        """
        Test a candidate without surrounding context.

        The purpose is diagnostic.

        We are not asserting that FINAL_CANDIDATE is
        necessarily the final production interpretation.
        """

        units, decisions = print_decisions(
            "Standalone Candidate",
            "ng",
        )

        self.assertEqual(
            units,
            ["ng"],
        )

        self.assertEqual(
            decisions[0]["unit_type"],
            "RECOGNITION_CANDIDATE",
        )

    def test_consecutive_candidates(self):
        """
        Test consecutive recognition candidates.

        This boundary probes whether the current context model
        provides sufficient information when one candidate is
        followed by another candidate.
        """

        units, decisions = print_decisions(
            "Consecutive Candidates",
            "ngnyka",
        )

        self.assertEqual(
            units,
            ["ng", "ny", "ka"],
        )

        self.assertEqual(
            decisions[-1]["unit_type"],
            "KNOWN_COMPLETE_PATTERN",
        )

    def test_candidate_followed_by_candidate_only(self):
        """
        Test a sequence containing only candidates.

        This deliberately removes the known-pattern context.
        """

        units, decisions = print_decisions(
            "Candidate Sequence Without Known Pattern",
            "ngny",
        )

        self.assertEqual(
            units,
            ["ng", "ny"],
        )

        self.assertTrue(
            all(
                decision["unit_type"]
                == "RECOGNITION_CANDIDATE"
                for decision in decisions
            )
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)