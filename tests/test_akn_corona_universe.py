"""Regression tests for the AKN vertex-configuration universe (stdlib only)."""
import json
import sys
import unittest
from collections import Counter
from functools import lru_cache
from pathlib import Path

AKN = Path(__file__).resolve().parents[1] / 'research' / 'akn'
sys.path.insert(0, str(AKN))

from certify import dihedral, signed  # noqa: E402
from geometry import canonical_star, det, ih_group, sgn  # noqa: E402

UNIVERSE = json.loads((AKN / 'corona_universe.json').read_text())['configurations']
ATLAS = json.loads((AKN / 'atlas.json').read_text())['classes']


@lru_cache(maxsize=None)
def solid_angle(corner):
    """Corner solid angle in units of pi/5: sum of its three dihedral angles minus pi."""
    return sum(dihedral(e, *(x for x in corner if x != e)) for e in corner) - 5


def tiles_link_sphere(corners) -> bool:
    """Closed edge-to-edge link (each arc in two corners, on opposite sides) with total
    solid angle 4 pi: a one-sheeted cover of S^2, hence pairwise disjoint interiors.
    Independent of the enumerator's conflict table."""
    sides = {}
    for c in corners:
        for i in range(3):
            a, b, x = c[i], c[(i + 1) % 3], c[(i + 2) % 3]
            arc = (a, b) if (abs(a), a) < (abs(b), b) else (b, a)
            sides.setdefault(arc, []).append(sgn(det(signed(arc[0]), signed(arc[1]), signed(x))))
    return (all(sorted(s) == [-1, 1] for s in sides.values())
            and sum(solid_angle(tuple(c)) for c in corners) == 20)


class Universe(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(len(UNIVERSE), 5450)
        self.assertEqual(sum(u['akn'] for u in UNIVERSE), 24)
        self.assertEqual(sum(not u['akn'] for u in UNIVERSE), 5426)
        self.assertEqual(sorted(Counter(len(u['star']) for u in UNIVERSE).items()),
                         [(4, 1), (6, 3), (8, 20), (10, 71), (12, 277), (14, 742),
                          (16, 1531), (18, 1735), (20, 1070)])

    def test_every_configuration_tiles_the_link_sphere(self):
        for u in UNIVERSE:
            self.assertTrue(tiles_link_sphere(u['star']), u['star'])

    def test_sphere_check_rejects_corruption(self):
        star = UNIVERSE[-1]['star']
        self.assertFalse(tiles_link_sphere(star[1:]))                    # hole
        self.assertFalse(tiles_link_sphere(star + [star[0]]))            # doubled corner

    def test_classes_are_distinct_and_akn_flags_match_the_atlas(self):
        group = ih_group()
        canon = [tuple(canonical_star(frozenset(map(frozenset, u['star'])), group)) for u in UNIVERSE]
        self.assertEqual(len(set(canon)), len(UNIVERSE))
        atlas = {tuple(map(tuple, a['star'])) for a in ATLAS}
        self.assertEqual({c for c, u in zip(canon, UNIVERSE) if u['akn']}, atlas)


class Completeness(unittest.TestCase):
    def test_enumeration_reproduces_the_committed_universe(self):
        import corona
        _, found = corona.enumerate_universe()
        self.assertEqual([corona.as_star(m) for m in found], [u['star'] for u in UNIVERSE])


if __name__ == '__main__':
    unittest.main()
