"""Reproducible finite cover versus single-quotient matching-rule controls.

The synthetic parity rule is deliberately NOT Katz's decoration. It shows
why UNSAT on one periodic quotient is not a global perfect-rule theorem.
"""
import json
import sys
import unittest
from pathlib import Path

AKN = Path(__file__).resolve().parents[1] / "research" / "akn"
sys.path.insert(0, str(AKN))

from decorated_covers import (  # noqa: E402
    cover_graph, integral_period_coordinates, parity_face_grammar,
    solve_cover, verify_cover_assignment,
)
from decorated_quotient import bare_control_grammar  # noqa: E402

CERT = json.loads((AKN / "certificate_3_2.json").read_text())


class CoverControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rule = parity_face_grammar()
        cls.base_edges,cls.base_report = cover_graph(CERT,(1,1,1))
        cls.double_edges,cls.double_report = cover_graph(CERT,(2,1,1))

    def test_period_coordinate_solver_is_exact(self):
        periods = CERT["period_lattice"]
        self.assertEqual(integral_period_coordinates(tuple(periods[0]),periods),
                         (1,0,0))
        self.assertEqual(integral_period_coordinates(tuple(-x for x in periods[1]),
                                                     periods),(0,-1,0))
        with self.assertRaises(ValueError):
            integral_period_coordinates((1,0,0,0,0,0),periods)

    def test_deck_cover_uses_all_oriented_faces(self):
        self.assertEqual(self.base_report["cells"],576)
        self.assertEqual(self.base_report["face_pairs"],1728)
        self.assertEqual(self.base_report["nonzero_base_face_seams"],308)
        self.assertEqual(self.double_report["cells"],1152)
        self.assertEqual(self.double_report["face_pairs"],3456)

    def test_parity_rule_has_explicit_twofold_periodic_witness(self):
        L0 = CERT["period_lattice"][0]
        self.assertEqual(L0[0]%2,1)
        assignment=[]
        for deck in (0,1):
            for base,axes in CERT["cells"]:
                p = (base[0]+deck*L0[0])%2
                assignment.append("I"+"-".join(map(str,axes))+"-p"+str(p))
        self.assertTrue(verify_cover_assignment(CERT,self.rule,(2,1,1),
                                                assignment))
        self.assertFalse(verify_cover_assignment(CERT,self.rule,(1,1,1),
                                                 assignment[:576]))
        damaged = assignment[:]
        damaged[0] = ("I"+"-".join(map(str,CERT["cells"][0][1]))+
                      "-p"+str(1-(CERT["cells"][0][0][0]%2)))
        self.assertFalse(verify_cover_assignment(CERT,self.rule,(2,1,1),
                                                 damaged))

    def test_onefold_unsat_does_not_exclude_twofold_sat(self):
        base=solve_cover(CERT,self.rule,(1,1,1),max_nodes=3)
        doubled=solve_cover(CERT,self.rule,(2,1,1),max_nodes=3)
        self.assertEqual(base["status"],"UNSAT_FINITE_COVER")
        self.assertEqual(doubled["status"],"SAT_PERIODIC_WITNESS")
        self.assertTrue(verify_cover_assignment(
            CERT,self.rule,(2,1,1),doubled["assignment"]))

    def test_caps_and_grammar_limits_are_explicit(self):
        with self.assertRaises(ValueError):
            cover_graph(CERT,(0,1,1))
        with self.assertRaises(ValueError):
            solve_cover(CERT,self.rule,(1,1,1),max_nodes=0)
        self.assertEqual(solve_cover(
            CERT,bare_control_grammar(),(1,1,1),max_nodes=1)["status"],
            "SAT_PERIODIC_WITNESS")
        self.assertEqual(solve_cover(
            CERT,bare_control_grammar(),(2,1,1),max_nodes=1)["status"],
            "SAT_PERIODIC_WITNESS")


if __name__ == "__main__":
    unittest.main()
