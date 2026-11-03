"""Small exact singular-stratum checks, without full enumeration or a convention."""
import sys
import unittest
from pathlib import Path

AKN = Path(__file__).resolve().parents[1]/"research"/"akn"
sys.path.insert(0, str(AKN))

from atlas_singular_probe import classify
from atlas_region_count import candidate_cells, input_basis, Z
from geometry import Q5


class SingularResearch(unittest.TestCase):
    def test_origin_boundary_status_agrees_with_independent_cell_equations(self):
        normals, levels, _, _ = input_basis()
        direct_forced, direct_possible = classify((Q5.of(0),)*3)
        cells = candidate_cells(normals, levels)
        independent_forced, independent_possible = [], []
        for signed, requirements in cells:
            strict = all(levels[f][lo] < Z < levels[f][hi]
                         for f, lo, hi in requirements)
            closed = all(levels[f][lo] <= Z <= levels[f][hi]
                         for f, lo, hi in requirements)
            if strict:
                independent_forced.append(signed)
            if closed:
                independent_possible.append(signed)
        self.assertEqual(direct_forced, sorted(independent_forced))
        self.assertEqual(direct_possible, sorted(independent_possible))
        self.assertLessEqual(len(direct_forced), len(direct_possible))


if __name__ == "__main__":
    unittest.main()
