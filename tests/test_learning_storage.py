"""
Tests for Learning Engine storage implementations.

Architecture references:
    AD-LE-009 — Learning Engine SHALL NOT depend on a specific
                storage technology.
"""

from pathlib import Path
import shutil
import sys
import tempfile
import unittest


# ---------------------------------------------------------------------------
# Project path
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ---------------------------------------------------------------------------
# Learning Engine imports
# ---------------------------------------------------------------------------

from core.learning.storage.json_storage import JSONStorage
from core.learning.storage.storage_adapter import StorageAdapter


class TestJSONStorage(unittest.TestCase):
    """Test JSONStorage against the StorageAdapter contract."""

    def setUp(self) -> None:
        """Create an isolated temporary storage directory."""

        self.temp_dir = Path(tempfile.mkdtemp())
        self.storage = JSONStorage(self.temp_dir)

    def tearDown(self) -> None:
        """Remove the temporary storage directory."""

        shutil.rmtree(
            self.temp_dir,
            ignore_errors=True,
        )

    def test_is_storage_adapter(self):
        """JSONStorage satisfies the StorageAdapter contract."""

        self.assertIsInstance(
            self.storage,
            StorageAdapter,
        )

    def test_save_and_load(self):
        """Saved data can be loaded again."""

        data = {
            "name": "Aksara Nusantara",
            "value": 42,
        }

        self.storage.save(
            "test",
            data,
        )

        loaded = self.storage.load("test")

        self.assertEqual(
            loaded,
            data,
        )

    def test_exists_after_save(self):
        """A saved key is reported as existing."""

        self.storage.save(
            "test",
            {"value": 1},
        )

        self.assertTrue(
            self.storage.exists("test"),
        )

    def test_missing_key_returns_none(self):
        """Loading a missing key returns None."""

        loaded = self.storage.load("missing")

        self.assertIsNone(
            loaded,
        )

    def test_missing_key_does_not_exist(self):
        """A missing key is reported as absent."""

        self.assertFalse(
            self.storage.exists("missing"),
        )

    def test_delete(self):
        """A saved key can be deleted."""

        self.storage.save(
            "test",
            {"value": 1},
        )

        self.assertTrue(
            self.storage.exists("test"),
        )

        self.storage.delete("test")

        self.assertFalse(
            self.storage.exists("test"),
        )

        self.assertIsNone(
            self.storage.load("test"),
        )

    def test_nested_data(self):
        """Nested JSON-compatible data is preserved."""

        data = {
            "profile": {
                "total_sessions": 3,
                "statistics": {
                    "correct": 24,
                    "incorrect": 6,
                },
            },
            "sessions": [
                {
                    "id": "session-001",
                    "type": "quiz",
                },
                {
                    "id": "session-002",
                    "type": "quiz",
                },
            ],
        }

        self.storage.save(
            "nested",
            data,
        )

        loaded = self.storage.load("nested")

        self.assertEqual(
            loaded,
            data,
        )

    def test_unicode_data(self):
        """Unicode data is preserved correctly."""

        data = {
            "script": "Javanese",
            "glyph": "ꦲꦤꦕꦫꦏ",
            "description": "Aksara Jawa",
        }

        self.storage.save(
            "unicode",
            data,
        )

        loaded = self.storage.load("unicode")

        self.assertEqual(
            loaded,
            data,
        )

    def test_storage_file_is_created(self):
        """Saving data creates the expected JSON file."""

        self.storage.save(
            "profile",
            {"learner_id": "learner-001"},
        )

        expected_path = self.temp_dir / "profile.json"

        self.assertTrue(
            expected_path.exists(),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)