"""Exact global-rule negative controls. No third-party dependencies."""
import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path

AKN = Path(__file__).resolve().parents[1] / "research" / "akn"
sys.path.insert(0, str(AKN))
from global_rule_obstruction import (  # noqa: E402
    A, B, determinant, physical, perpendicular, qmul, qsign,
    rational_perp_zero, report, saturated_rank_three,
    separating_periodic_cells,
)

PERIODS = ((3, 3, 2, -2, 0, 0),
           (2, -2, 0, 0, 3, -3),
           (0, 0, 3, 3, 2, 2))


class GlobalMatchingRuleSpike(unittest.TestCase):
    def test_height_injectivity_and_singular_control(self):
        self.assertEqual(determinant([list(row) for row in A+B]), 8)
        self.assertEqual(determinant([[0,1],[1,0]]), -1)
        self.assertEqual(determinant([[1,2],[2,4]]), 0)

    def test_undecorated_cocycle_closure_does_not_imply_perfection(self):
        # +e0, +e1, -e0, -e1 has zero integer and physical sum.
        # This property also holds inside the globally periodic witness.
        walk = ((0,1),(1,1),(0,-1),(1,-1))
        total = tuple(sum(s for axis,s in walk if axis==j)
                      for j in range(6))
        self.assertEqual(total, (0,)*6)
        self.assertEqual(physical(total), ((0,0),)*3)
        self.assertEqual(perpendicular(total), ((0,0),)*3)

    def test_exact_period_drift(self):
        self.assertTrue(saturated_rank_three(PERIODS))
        for row in PERIODS:
            self.assertTrue(rational_perp_zero(row,Fraction(-2,3)))
            self.assertNotEqual(perpendicular(row), ((0,0),)*3)
        self.assertEqual(physical(PERIODS[0]),
                         ((0,0),(4,6),(0,0)))
        self.assertEqual(perpendicular(PERIODS[0]),
                         ((0,0),(10,-6),(0,0)))

    def test_remote_two_cell_closed_window_separation(self):
        self.assertEqual(qmul((0,1),(0,1)),(1,1))
        self.assertEqual(qsign((6,-4)),-1)
        fixture = {
            "cells":[[[0,0,-1,0,0,0],[1,2,4]]],
            "period_lattice":[list(row) for row in PERIODS],
        }
        result = separating_periodic_cells(fixture)
        self.assertTrue(result["strict_disjointness"])
        self.assertEqual(result["period_multiple"],3)
        self.assertEqual(result["dot_perp_period_normal_z_tau"],[-10,6])
        self.assertEqual(result["full_window_width_z_tau"],[4,-2])
        with self.assertRaises(ValueError):
            separating_periodic_cells(dict(fixture,cells=[]))

    def test_certificate_replay_and_adversarial_mutations(self):
        cert = json.loads((AKN/"certificate_3_2.json").read_text())
        result = report(cert)
        self.assertEqual(result["stacked_integer_projection_determinant"],8)
        self.assertEqual(len(result["periods"]),3)
        self.assertTrue(result["remote_two_cell_obstruction"]["strict_disjointness"])
        with self.assertRaises(ValueError):
            report(dict(cert,x="-3/5"))
        nonsaturated = [list(row) for row in PERIODS]
        nonsaturated[0] = [2*v for v in nonsaturated[0]]
        with self.assertRaises(ValueError):
            report(dict(cert,period_lattice=nonsaturated))
        notkernel = [list(row) for row in PERIODS]
        notkernel[0][0] += 1
        with self.assertRaises(ValueError):
            report(dict(cert,period_lattice=notkernel))


if __name__ == "__main__":
    unittest.main()
