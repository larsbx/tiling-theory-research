"""Regression tests for the AKN vertex-atlas approximant certificate (stdlib only)."""
import json
import sys
import unittest
from collections import Counter
from fractions import Fraction
from pathlib import Path

AKN = Path(__file__).resolve().parents[1] / 'research' / 'akn'
sys.path.insert(0, str(AKN))

from certify import check  # noqa: E402
from geometry import (PERP_TRUE, TAU, TRIPLES, CutProject, Q5, canonical_star,  # noqa: E402
                      cell_shape, ih_group)

ATLAS = json.loads((AKN / 'atlas.json').read_text())
CERT = json.loads((AKN / 'certificate_3_2.json').read_text())


class Geometry(unittest.TestCase):
    def test_point_group_and_shapes(self):
        self.assertEqual(len(ih_group()), 120)
        self.assertEqual(Counter(cell_shape([i + 1 for i in I]) for I in TRIPLES),
                         {'P': 10, 'O': 10})

    def test_exact_sign(self):
        self.assertEqual((TAU * TAU - TAU - 1), Q5.of(0))
        self.assertEqual((Q5(Fraction(-2), Fraction(1))).sign(), 1)      # sqrt5 > 2
        self.assertEqual((Q5(Fraction(9, 4), Fraction(-1))).sign(), 1)   # 9/4 > sqrt5


class Atlas(unittest.TestCase):
    def test_classes(self):
        content = Counter((c['P'], c['O']) for c in ATLAS['classes'])
        self.assertEqual(len(ATLAS['classes']), 24)
        self.assertEqual(content[(20, 0)], 1)
        self.assertEqual(content[(10, 10)], 3)
        self.assertTrue(all(c['P'] + c['O'] == c['cells'] for c in ATLAS['classes']))

    def test_every_class_has_an_exact_akn_witness(self):
        group = ih_group()
        for c in ATLAS['classes']:
            with self.subTest(star=c['star'][:2]):
                cp = CutProject(PERP_TRUE, tuple(Q5.of(Fraction(g)) for g in c['witness_gamma']))
                self.assertTrue(cp.vertex((0,) * 6))
                star = canonical_star(cp.star((0,) * 6), group)
                self.assertEqual([list(s) for s in star], c['star'])


class Certificate(unittest.TestCase):
    def test_3_2_approximant_is_an_atlas_tiling(self):
        report = check(CERT, ATLAS)
        self.assertEqual((report['vertices'], report['prolate'], report['oblate']), (576, 356, 220))
        self.assertEqual(report['non_atlas_vertices'], 0)
        side = 2 * TAU * TAU * TAU * TAU                                  # simple cubic, 2 tau^4
        cube = side * side * side
        self.assertEqual(report['covolume'], [str(cube.a), str(cube.b)])

    def test_checker_rejects_a_missing_cell(self):
        broken = dict(CERT, cells=CERT['cells'][1:])
        with self.assertRaises(AssertionError):
            check(broken, ATLAS)

    def test_checker_rejects_a_non_saturated_period_lattice(self):
        L = CERT['period_lattice']
        broken = dict(CERT, period_lattice=[[2 * c for c in L[0]], L[1], L[2]])
        with self.assertRaises(AssertionError):
            check(broken, ATLAS)

    def test_checker_flags_stars_outside_the_atlas(self):
        report = check(CERT, dict(ATLAS, classes=ATLAS['classes'][1:]))
        self.assertGreater(report['non_atlas_vertices'], 0)


if __name__ == '__main__':
    unittest.main()
