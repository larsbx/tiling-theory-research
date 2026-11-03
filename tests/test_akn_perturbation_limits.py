import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"research"/"akn"))
from atlas_perturbation_limits import chamber_trie, classify, neighbors


class TranslationLimits(unittest.TestCase):
    def test_boundary_and_internal_signs(self):
        trie = chamber_trie([(0, 0), (0, 1), (1, 1)])
        self.assertEqual(list(neighbors(trie, (2, 2))), [0, 1, 2])
        self.assertEqual(list(neighbors(trie, (0, 2))), [0, 1])
        self.assertEqual(list(neighbors(trie, (3, 4))), [2])

    def test_optional_cells_cannot_be_chosen_independently(self):
        a, b = (-1, 2, 3), (1, 2, 3)
        catalog = [(a, [(0, 0, 1)]), (b, [(0, 1, 2)])]
        generic = {"leaves": [{"prefix": [0]}, {"prefix": [1]}]}
        singular = {"strata": [{"key": [2], "dimension": 0, "membership": 0}],
                    "memberships": [[[], [a, b]]]}
        result = classify(generic, singular, catalog)["strata"][0]
        self.assertEqual(result["chamber_indices"], [0, 1])
        self.assertEqual(result["distinct_stars"], 2)
        self.assertFalse(result["strict_limit"])
        self.assertFalse(result["closed_limit"])

    def test_missing_chamber_or_invalid_membership_rejected(self):
        a = (-1, 2, 3)
        generic = {"leaves": [{"prefix": [1]}]}
        singular = {"strata": [{"key": [0], "dimension": 0, "membership": 0}],
                    "memberships": [[[a], []]]}
        with self.assertRaisesRegex(ValueError, "chamber incidence"):
            classify(generic, singular, [])
        singular["strata"][0]["key"] = [2]
        with self.assertRaisesRegex(ValueError, "contradicts singular membership"):
            classify(generic, singular, [])


if __name__ == "__main__":
    unittest.main()
