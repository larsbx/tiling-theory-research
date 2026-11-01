"""Independent algebraic arrangement and conjugacy-type regression checks."""
import json
import sys
import unittest
from collections import Counter
from pathlib import Path

AKN = Path(__file__).resolve().parents[1]/"research"/"akn"
sys.path.insert(0, str(AKN))

from atlas_region_count import (candidate_cells, input_basis, point_group,
                                slice_region_count, subgroup_conjugacy)
from atlas_region_count import Z as ZERO


class ExactRegionCountMethod(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.normals, cls.levels, cls.widths, cls.digest = input_basis()

    def test_independently_rebuilt_135_planes(self):
        self.assertEqual(len(self.normals), 15)
        self.assertEqual(sum(map(len, self.levels)), 135)
        self.assertEqual(len({w for w in self.widths}), 1)
        self.assertEqual(self.digest, json.loads(
            (AKN/"atlas_chamber_full_manifest.json").read_text()
        )["plane_fixture_sha256"])

    def test_initial_exact_2d_slice_region_counts(self):
        # First seven planes are parallel. The first transverse
        # section meets three earlier planes in distinct open lines.
        planes = [(f, levels[k]) for f, levels in
                  enumerate(self.levels) for k in range(1, 8)]
        self.assertEqual(slice_region_count(
            0, planes, self.normals, self.widths), 1)
        self.assertEqual(slice_region_count(
            7, planes, self.normals, self.widths), 4)

    def test_160_cell_conditions_rebuilt_independently(self):
        cells = candidate_cells(self.normals, self.levels)
        self.assertEqual(len(cells), 160)
        self.assertEqual(len({cell for cell, _ in cells}), 160)
        self.assertTrue(all(len(cond) == 3 for _, cond in cells))

    def test_stabilizer_subgroup_conjugacy_not_orbit_count(self):
        group = point_group()
        atlas = json.loads((AKN/"atlas.json").read_text())
        values = [subgroup_conjugacy(
            row["star"], group) for row in atlas["classes"]]
        self.assertEqual(len(values), 24)
        self.assertEqual(Counter(order for order, _ in values),
                         {1: 8, 2: 9, 4: 4, 6: 1, 10: 1, 120: 1})
        self.assertEqual(len({signature for _, signature in values}), 6)


if __name__ == "__main__":
    unittest.main()
