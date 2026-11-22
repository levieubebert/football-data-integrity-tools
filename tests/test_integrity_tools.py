"""Unit tests use only synthetic, non-sensitive data."""
import tempfile
import unittest
from pathlib import Path

from integrity_tools import inspect_csv, sha256_file


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "sample.csv"

    def test_known_hash(self):
        self.path.write_bytes(b"abc")
        self.assertEqual(
            sha256_file(self.path),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        )

    def test_duplicate_and_blank_keys(self):
        self.path.write_text(
            "match_id,home,away\n"
            "M1,Alpha,Beta\n"
            "M1,Alpha,Beta\n"
            ",Gamma,Delta\n"
            "M2,Epsilon,Zeta\n",
            encoding="utf-8",
        )
        result = inspect_csv(self.path, required_columns=["match_id"], key_columns=["match_id"])
        self.assertEqual(result["rows"], 4)
        self.assertEqual(result["duplicate_keys"], 1)
        self.assertEqual(result["blank_keys"], 1)
        self.assertEqual(result["malformed_rows"], 0)

    def test_missing_column(self):
        self.path.write_text("home,away\nAlpha,Beta\n", encoding="utf-8")
        result = inspect_csv(self.path, required_columns=["match_id"])
        self.assertEqual(result["missing_columns"], ["match_id"])
        self.assertIsNone(result["rows"])

    def test_malformed_row(self):
        self.path.write_text("id,home\nM1\nM2,Alpha,Extra\n", encoding="utf-8")
        result = inspect_csv(self.path, key_columns=["id"])
        self.assertEqual(result["malformed_rows"], 2)

    def test_duplicate_headers_rejected(self):
        self.path.write_text("id,id\nM1,M2\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            inspect_csv(self.path)


if __name__ == "__main__":
    unittest.main()
