"""Fail-closed controls for the exact singular packet."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CODE = Path(__file__).resolve().parents[1]/"research"/"akn"
sys.path.insert(0, str(CODE))
from atlas_region_count import input_basis
from atlas_strata_check import boundary_of, verify


class SingularCertificateTest(unittest.TestCase):
    def test_pair_cap_records_identical_frontier(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            args = [sys.executable, str(CODE/"atlas_strata_driver.py"),
                    "--max-pairs", "0"]
            for name in ("a", "b"):
                run = subprocess.run([*args, "--out", str(out/name)])
                self.assertEqual(run.returncode, 1)
            a = (out/"a"/"singular-strata.json").read_bytes()
            self.assertEqual(a, (out/"b"/"singular-strata.json").read_bytes())
            packet = json.loads(a)
            self.assertEqual(len(packet["unprocessed_pairs"]), 8505)
            record = json.loads((out/"a"/"singular-run.json").read_text())
            self.assertEqual(record["state"], "frontier_inconclusive")
            with self.assertRaisesRegex(ValueError, "inconclusive"):
                verify(packet)

    def test_empty_full_claim_rejected(self):
        *_, digest = input_basis()
        with self.assertRaisesRegex(ValueError, "incomplete chord"):
            verify({"format": "AKN-SINGULAR-STRATA-1", "basis_sha256": digest,
                    "pair_budget": 8505, "unprocessed_pairs": [],
                    "strata": [], "memberships": []})

    def test_incidence_does_not_cross_transition(self):
        self.assertTrue(boundary_of((4, 0, 6), (5, 0, 5)))
        self.assertFalse(boundary_of((4, 0, 6), (7, 0, 5)))


if __name__ == "__main__":
    unittest.main()
