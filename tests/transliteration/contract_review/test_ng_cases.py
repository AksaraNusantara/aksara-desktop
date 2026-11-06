"""
AD-TR-01 — TR-CR-001
NG Orthographic Resolution — Contract Review Cases

Purpose
-------
This module provides the initial contract-review test foundation for
the contextual Latin sequence ``ng``.

These tests distinguish between:

1. LOCKED contract invariants that can already be verified.
2. OPEN orthographic behaviors that require future implementation
   evidence before they can become regression contracts.

The tests deliberately do not assert unresolved Unicode output.
"""

from dataclasses import dataclass
from enum import Enum
import unittest


class OrthographicRole(str, Enum):
    """Candidate orthographic roles relevant to the ``ng`` token."""

    NGLEGENA = "nglegena"
    PASANGAN = "pasangan"
    PANYIGEG = "panyigeg"


@dataclass(frozen=True)
class NgReviewCase:
    """
    A contextual review scenario for the Latin sequence ``ng``.

    ``candidate_roles`` represents orthographic roles that may be
    investigated during contract review. It is not a production
    expectation until the corresponding behavior is LOCKED.
    """

    case_id: str
    text: str
    review_question: str
    candidate_roles: tuple[OrthographicRole, ...]


NG_REVIEW_CASES = (
    NgReviewCase(
        case_id="TR-CR-001-NG-01",
        text="ng",
        review_question=(
            "How should standalone 'ng' be resolved when surrounding "
            "orthographic context is insufficient?"
        ),
        candidate_roles=(
            OrthographicRole.NGLEGENA,
            OrthographicRole.PANYIGEG,
        ),
    ),
    NgReviewCase(
        case_id="TR-CR-001-NG-02",
        text="nga",
        review_question=(
            "How should 'ng' followed by a vowel be resolved?"
        ),
        candidate_roles=(
            OrthographicRole.NGLEGENA,
        ),
    ),
    NgReviewCase(
        case_id="TR-CR-001-NG-03",
        text="ngka",
        review_question=(
            "How should 'ng' be resolved before a following consonant?"
        ),
        candidate_roles=(
            OrthographicRole.NGLEGENA,
            OrthographicRole.PANYIGEG,
        ),
    ),
    NgReviewCase(
        case_id="TR-CR-001-NG-04",
        text="angka",
        review_question=(
            "How should 'ng' be resolved when embedded within a larger "
            "Latin orthographic sequence?"
        ),
        candidate_roles=(
            OrthographicRole.NGLEGENA,
            OrthographicRole.PANYIGEG,
        ),
    ),
    NgReviewCase(
        case_id="TR-CR-001-NG-05",
        text="kang",
        review_question=(
            "How should terminal 'ng' be resolved?"
        ),
        candidate_roles=(
            OrthographicRole.PANYIGEG,
        ),
    ),
)


class TestNgContractReviewMatrix(unittest.TestCase):
    """
    Contract-review tests for TR-CR-001.

    These tests verify the integrity and completeness of the review
    matrix itself. They do not yet test the production transliteration
    pipeline.
    """

    def test_review_matrix_contains_all_required_contexts(self):
        """
        The initial review matrix must cover the minimum contexts
        identified during AD-TR-01 contract analysis.
        """

        inputs = {case.text for case in NG_REVIEW_CASES}

        required_inputs = {
            "ng",      # standalone
            "nga",     # vowel-following
            "ngka",    # consonant-following
            "angka",   # embedded
            "kang",    # terminal
        }

        self.assertTrue(required_inputs.issubset(inputs))

    def test_each_case_has_a_unique_identifier(self):
        """Every review scenario must have a unique contract-review ID."""

        case_ids = [case.case_id for case in NG_REVIEW_CASES]

        self.assertEqual(
            len(case_ids),
            len(set(case_ids)),
            "NG contract-review case identifiers must be unique.",
        )

    def test_each_case_has_an_explicit_review_question(self):
        """
        An OPEN review case must explicitly state what is being reviewed.
        """

        for case in NG_REVIEW_CASES:
            with self.subTest(case_id=case.case_id):
                self.assertTrue(
                    case.review_question.strip(),
                    "Every contract-review case requires a question.",
                )

    def test_each_case_contains_the_ng_sequence(self):
        """
        Every TR-CR-001 scenario must actually exercise the ``ng``
        sequence.
        """

        for case in NG_REVIEW_CASES:
            with self.subTest(case_id=case.case_id):
                self.assertIn("ng", case.text)

    def test_candidate_roles_are_valid_orthographic_roles(self):
        """
        Candidate roles must come from the controlled orthographic
        role vocabulary.
        """

        for case in NG_REVIEW_CASES:
            with self.subTest(case_id=case.case_id):
                self.assertGreater(
                    len(case.candidate_roles),
                    0,
                    "Each review case requires at least one role to review.",
                )

                for role in case.candidate_roles:
                    self.assertIsInstance(role, OrthographicRole)


if __name__ == "__main__":
    unittest.main()