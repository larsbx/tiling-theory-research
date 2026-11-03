"""State-machine tests: automated math never promotes from a capped run."""
import copy
import json
from pathlib import Path
import sys
import unittest

AKN = Path(__file__).resolve().parents[1]/"research"/"akn"
sys.path.insert(0, str(AKN))

from atlas_research_driver import assess


class AutonomousResearchGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = json.loads(
            (AKN/"atlas_chamber_full_manifest.json").read_text())

    def test_bounded_run_is_inconclusive(self):
        packet = {
            "leaves": [{"kind": "frontier", "prefix": []}],
            "frontier_count": 1, "search_exhausted": False
        }
        status, next_step = assess(packet, {"complete_generic_coverage": False},
                                   self.baseline)
        self.assertEqual(status, "frontier_inconclusive")
        self.assertIn("frontier", next_step)

    def test_unrecognized_star_is_counterexample_not_a_crash(self):
        packet = {
            "leaves": [{"kind": "classified", "orbit_class": -1,
                        "counterexample_star": [[1, 2, 3]]}],
            "frontier_count": 0, "search_exhausted": True
        }
        status, next_step = assess(packet, {"coverage_verified_generic": True},
                                   self.baseline)
        self.assertEqual(status, "counterexample_candidate")
        self.assertIn("witness", next_step)

    def test_complete_independent_agreement_remains_candidate(self):
        baseline = self.baseline
        packet = {
            "leaves": [{"kind": "classified", "orbit_class": 0}],
            "frontier_count": 0, "search_exhausted": True,
        }
        replay = {
            "coverage_verified_generic": True,
            "independently_counted_regions": baseline[
                "independent_exact_2d_slice_arrangement_region_count"],
            "exact_witnessed_distinct_chambers": baseline[
                "enumerated_full_dimensional_chambers"],
            "slice_region_counts_sha256": baseline[
                "independent_105_slice_region_counts_sha256"],
            "exactly_existing_24_orbits": True,
            "stabilizer_subgroup_conjugacy_types": baseline[
                "stabilizer_subgroup_conjugacy_types"],
        }
        status, next_step = assess(packet, replay, baseline)
        self.assertEqual(status, "generic_candidate_verified")
        self.assertIn("singular", next_step)
        altered = copy.deepcopy(replay)
        altered["independently_counted_regions"] += 1
        changed, _ = assess(packet, altered, baseline)
        self.assertEqual(changed, "baseline_disagreement")

    def test_false_coverage_is_not_accepted(self):
        state, _ = assess({"leaves": [], "frontier_count": 0,
                           "search_exhausted": False},
                          {"coverage_verified_generic": False}, self.baseline)
        self.assertEqual(state, "verification_failed")


if __name__ == "__main__":
    unittest.main()
