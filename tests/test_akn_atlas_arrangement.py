"""Finite exact arrangement basis for the still-open atlas completeness proof."""
import json
import sys
import unittest
from pathlib import Path

AKN = Path(__file__).resolve().parents[1] / "research" / "akn"
sys.path.insert(0, str(AKN))

from atlas_arrangement import arrangement  # noqa: E402
from radius2_exact import sign, zs  # noqa: E402


class ExactAtlasArrangement(unittest.TestCase):
    def test_all_160_candidate_cells_are_represented_in_arrangement(self):
        cuts = arrangement()
        fixture = json.loads((AKN / "atlas_hyperplanes.json").read_text())
        self.assertEqual(len(fixture["families"]), len(cuts))
        for cut, expected in zip(cuts, fixture["families"]):
            self.assertEqual(cut["axis_pair"], expected["axis_pair"])
            self.assertEqual(cut["levels_in_Z_tau_for_twice_normal_projection"],
                             expected["levels"])
        self.assertEqual(len(cuts), 15)
        self.assertEqual(sum(len(c["levels_in_Z_tau_for_twice_normal_projection"])
                             for c in cuts), 135)
        for c in cuts:
            self.assertEqual(c["candidate_corner_cells"], 32)
            levels = [tuple(v) for v in
                      c["levels_in_Z_tau_for_twice_normal_projection"]]
            self.assertEqual(len(levels), 9)
            self.assertTrue(all(sign(zs(b, a)) > 0
                                for a, b in zip(levels, levels[1:])))


if __name__ == "__main__":
    unittest.main()
