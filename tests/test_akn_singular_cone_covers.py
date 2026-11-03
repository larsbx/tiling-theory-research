from itertools import combinations
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"research"/"akn"))
from atlas_singular_cone_covers import covers, physical_chambers
from geometry import Q5


class ConeCoverTests(unittest.TestCase):
    def test_three_coordinate_planes_give_eight_chambers(self):
        normals = tuple(tuple(Q5.of(i == j) for i in range(3)) for j in range(3))
        self.assertEqual(len(physical_chambers(normals)), 8)

    def test_search_matches_brute_force_with_and_without_forced_cells(self):
        masks = {"a": 0b001, "b": 0b010, "c": 0b100,
                 "d": 0b011, "e": 0b110, "f": 0b111}
        for forced in ((), ("a",), ("a", "d")):
            optional = tuple(c for c in masks if c not in forced)
            expected = set()
            for size in range(len(optional)+1):
                for subset in combinations(optional, size):
                    star = forced+subset
                    if all(sum(bool(masks[c] & bit) for c in star) == 1
                           for bit in (1, 2, 4)):
                        expected.add(frozenset(star))
            self.assertEqual(covers(forced, optional, masks, 0b111), expected)


if __name__ == "__main__":
    unittest.main()
