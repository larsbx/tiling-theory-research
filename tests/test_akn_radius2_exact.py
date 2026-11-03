"""Exact radius-2 AKN patch-language regression (no third-party dependencies)."""
import json
import sys
import unittest
from pathlib import Path

AKN = Path(__file__).resolve().parents[1] / "research" / "akn"
sys.path.insert(0, str(AKN))
from radius2_exact import (Plane, audit, check_obstruction, constraints, eliminate,
                           patch_cells, projection, sign, za, zm, _star_map)  # noqa: E402

CERT = json.loads((AKN / "certificate_3_2.json").read_text())


class RingAndSolver(unittest.TestCase):
    def test_exact_integer_ring(self):
        tau = (0, 1)
        self.assertEqual(zm(tau, tau), (1, 1))
        self.assertEqual(za((1, 0), (-1, 0)), (0, 0))
        self.assertEqual(sign((-2, 1)), -1)  # tau - 2 < 0

    def test_open_constraints_distinguish_boundary_from_contradiction(self):
        p = ((1, 0), (0, 0), (0, 0))
        n = ((-1, 0), (0, 0), (0, 0))
        self.assertTrue(eliminate([
            Plane(p, (1, 0)), Plane(n, (1, 0))
        ]).feasible)
        boundary = eliminate([
            Plane(p, (0, 0)), Plane(n, (0, 0))
        ])
        self.assertFalse(boundary.feasible)
        self.assertEqual(sign(boundary.obstruction), 0)
        self.assertTrue(eliminate([
            Plane(p, (0, 0)), Plane(n, (0, 0))
        ], strict=False).feasible)
        impossible = eliminate([
            Plane(p, (-1, 0)), Plane(n, (0, 0))
        ])
        self.assertFalse(impossible.feasible)
        self.assertLess(sign(impossible.obstruction), 0)
        self.assertFalse(eliminate([
            Plane(p, (-1, 0)), Plane(n, (0, 0))
        ], strict=False).feasible)
        proof_planes = [
            Plane(p, (0, 0), ("upper",)),
            Plane(n, (0, 0), ("lower",)),
        ]
        certificate = eliminate(proof_planes)
        self.assertFalse(certificate.feasible)
        self.assertTrue(check_obstruction(certificate, proof_planes))
        self.assertFalse(check_obstruction(certificate, proof_planes,
                                          strict=False))
        self.assertFalse(check_obstruction(certificate, proof_planes[:1]))


class PeriodicPatches(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stars = _star_map(CERT)
        cls.radius1 = audit(CERT, 1)
        cls.radius2 = audit(CERT, 2)

    def test_periodic_quotient_and_relative_lifts(self):
        self.assertEqual(len(self.stars), 576)
        self.assertEqual(
            len({projection(tuple(n)) for n in CERT["vertices"]}), 576
        )
        center = tuple(CERT["vertices"][0])
        small = patch_cells(center, self.stars, 1)
        large = patch_cells(center, self.stars, 2)
        self.assertTrue(set(small) <= set(large))
        self.assertGreater(len(large), len(small))
        self.assertEqual(len(constraints(large)), 30)

    def test_all_central_stars_are_generically_akn_realizable(self):
        self.assertEqual(self.radius1["vertices_checked"], 576)
        self.assertEqual(self.radius1["result_counts"], {"feasible": 576})

    def test_radius_two_generic_feasibility_census(self):
        self.assertEqual(self.radius2["vertices_checked"], 576)
        counts = self.radius2["result_counts"]
        self.assertEqual(sum(counts.values()), 576)
        # Baseline from a separately implemented exact Z[tau] JS elimination.
        self.assertEqual(counts.get("feasible"), 286)
        self.assertEqual(
            counts.get("obstructed_at_boundary", 0) +
            counts.get("obstructed_strict", 0), 290
        )
        self.assertEqual(counts.get("obstructed_at_boundary"), 287)
        self.assertEqual(counts.get("obstructed_strict"), 3)


if __name__ == "__main__":
    unittest.main()
