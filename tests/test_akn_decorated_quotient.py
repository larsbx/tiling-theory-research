"""Periodic decorated-quotient falsification, without claiming Katz labels."""
import copy
import json
import sys
import unittest
from pathlib import Path

AKN = Path(__file__).resolve().parents[1] / "research" / "akn"
sys.path.insert(0, str(AKN))
from decorated_quotient import (  # noqa: E402
    bare_control_grammar, glue_graph, solve, verify_assignment,
)

CERT = json.loads((AKN / "certificate_3_2.json").read_text())


class DecoratedPeriodicQuotient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = glue_graph(CERT)
        cls.bare = bare_control_grammar()
        cls.sat = solve(CERT, cls.bare, max_nodes=2)

    def test_all_1728_faces_pair_oppositely(self):
        self.assertEqual(len(self.graph), 1728)
        self.assertEqual(len(CERT["cells"]), 576)
        self.assertTrue(all(
            g.positive.orientation == 1 and
            g.negative.orientation == -1 for g in self.graph
        ))

    def test_periodic_plain_label_rule_is_not_perfect(self):
        self.assertEqual(self.sat["status"], "SAT_PERIODIC_WITNESS")
        self.assertEqual(self.sat["face_pairs"], 1728)
        self.assertTrue(verify_assignment(
            CERT, self.bare, self.sat["assignment"]
        ))

    def test_verifier_rejects_incomplete_and_wrong_shape(self):
        assignment = self.sat["assignment"]
        self.assertFalse(verify_assignment(
            CERT, self.bare, assignment[:-1]
        ))
        damaged = list(assignment)
        damaged[0] = "bare_O" if damaged[0] == "bare_P" else "bare_P"
        self.assertFalse(verify_assignment(CERT, self.bare, damaged))
        damaged = list(assignment)
        damaged[0] = "undefined"
        self.assertFalse(verify_assignment(CERT, self.bare, damaged))

    def test_wrong_ordered_face_pairs_are_unacceptable(self):
        wrong = copy.deepcopy(self.bare)
        wrong["allowed_pairs"] = [["plain", "different"]]
        self.assertEqual(solve(CERT, wrong, max_nodes=2)["status"],
                         "UNSAT_FINITE_QUOTIENT")
        self.assertFalse(verify_assignment(
            CERT, wrong, self.sat["assignment"]
        ))

    def test_search_budget_is_inconclusive_not_unsat(self):
        more = copy.deepcopy(self.bare)
        more["variants"].extend([
            {"id": "second_P", "shape": "P",
             "faces": [["plain", "plain"]]*3},
            {"id": "second_O", "shape": "O",
             "faces": [["plain", "plain"]]*3},
        ])
        self.assertEqual(solve(CERT, more, max_nodes=1)["status"],
                         "INCONCLUSIVE")
        with self.assertRaises(ValueError):
            solve(CERT, more, max_nodes=0)

    def test_corrupt_face_data_and_duplicate_cells_rejected(self):
        missing = dict(CERT, cells=CERT["cells"][1:])
        with self.assertRaises(ValueError):
            glue_graph(missing)
        duplicated = dict(CERT, cells=CERT["cells"] +
                          [CERT["cells"][0]])
        with self.assertRaises(ValueError):
            glue_graph(duplicated)

    def test_grammar_orientation_and_duplicate_guards(self):
        invalid = copy.deepcopy(self.bare)
        invalid["variants"].append(copy.deepcopy(invalid["variants"][0]))
        with self.assertRaises(ValueError):
            solve(CERT, invalid)
        invalid = copy.deepcopy(self.bare)
        invalid["variants"][0]["faces"] = [["plain", "plain"]]
        with self.assertRaises(ValueError):
            solve(CERT, invalid)
        invalid = copy.deepcopy(self.bare)
        invalid["variants"][0]["allowed_axes"] = [[1, 0, 2]]
        with self.assertRaises(ValueError):
            solve(CERT, invalid)


if __name__ == "__main__":
    unittest.main()
