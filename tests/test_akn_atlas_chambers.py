"""Regression gates for the AKN chamber prefix cover and independent checker."""
import copy
import json
import sys
import unittest
from pathlib import Path

AKN = Path(__file__).resolve().parents[1]/"research"/"akn"
sys.path.insert(0, str(AKN))

from atlas_chambers import (basis, children, enumerate_partition, initial_poly,
                            stabilizer_conjugacy, witness)
from atlas_chamber_check import verify_packet
from geometry import ih_group, act


class ChamberCertificate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = enumerate_partition(max_depth=1, max_nodes=1)

    def test_first_exact_sweep_covers_open_window(self):
        p = self.packet
        self.assertEqual(p["expanded_prefixes"], 1)
        self.assertEqual(p["frontier_count"], 8)
        self.assertEqual(p["classified_count"], 0)
        self.assertFalse(p["search_exhausted"])
        self.assertEqual([x["prefix"] for x in p["leaves"]],
                         [[i] for i in range(8)])
        verified = verify_packet(p)
        self.assertEqual(verified["unresolved_frontier"], 8)
        self.assertFalse(verified["complete_generic_coverage"])

    def test_committed_independent_depth_one_fixture(self):
        # These witnesses were constructed along a zonotope support vector,
        # independently of the enumerator's polytope barycenters.
        packet = json.loads((AKN/"atlas_chamber_depth1_exact.json").read_text())
        self.assertEqual(packet["frontier_count"], 8)
        checked = verify_packet(packet)
        self.assertEqual(checked["verified_partition_prefixes"], 1)
        self.assertFalse(checked["complete_generic_coverage"])

    def test_reproduction_is_byte_deterministic(self):
        another = enumerate_partition(max_depth=1, max_nodes=1)
        self.assertEqual(json.dumps(self.packet, sort_keys=True),
                         json.dumps(another, sort_keys=True))

    def test_checker_rejects_dropped_feasible_chamber(self):
        p = copy.deepcopy(self.packet)
        p["leaves"].pop(3)
        p["frontier_count"] -= 1
        with self.assertRaises(AssertionError):
            verify_packet(p)

    def test_checker_rejects_fabricated_interior_witness(self):
        p = copy.deepcopy(self.packet)
        p["leaves"][0]["witness_y"] = [["0", "0"]]*3
        with self.assertRaises(AssertionError):
            verify_packet(p)

    def test_no_depth_limit_is_misreported_as_exhaustive(self):
        p = enumerate_partition(max_depth=0, max_nodes=0)
        self.assertEqual(p["frontier_count"], 1)
        self.assertEqual(p["leaves"][0]["prefix"], [])
        self.assertFalse(verify_packet(p)["complete_generic_coverage"])

    def test_exact_window_clipping(self):
        n, levels, _ = basis()
        poly = initial_poly(n, levels)
        self.assertGreaterEqual(len(poly), 4)
        splits = list(children(poly, n, levels, 0))
        self.assertEqual([i for i, _ in splits], list(range(8)))
        for _, child in splits:
            self.assertEqual(len(witness(child)), 3)

    def test_stabilizer_conjugacy_independent_of_group_action(self):
        group = ih_group()
        star = frozenset((frozenset((1, 2, 3)),
                          frozenset((-1, 4, 5))))
        conjugate = frozenset(frozenset(act(group[17], s) for s in cell)
                             for cell in star)
        self.assertEqual(stabilizer_conjugacy(star, group),
                         stabilizer_conjugacy(conjugate, group))


if __name__ == "__main__":
    unittest.main()
