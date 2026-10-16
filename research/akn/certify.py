"""Independent exact check that a periodic certificate is an AKN-vertex-atlas tiling.

Uses no window/selection test.  From the certificate (period lattice L, vertex and cell
representatives in Z^6) it checks, in exact Q(sqrt5) arithmetic on the true golden
rhombohedra:

  1. L is the full integer kernel of the quotient map q = pi_perp_x (rank 3, saturated),
     so q(n) faithfully labels n mod L.
  2. cell corners are listed vertices; labels are unique.
  3. every 2-face lies in exactly two cells, on opposite sides;
  4. dihedral angles around every edge sum to 2 pi;
  5. corner solid angles around every vertex sum to 4 pi;
  6. total cell volume equals the covolume of pi_par(L).

(3)-(5) make the glued cell complex a closed 3-manifold mapping to R^3 / pi_par(L) by a
local homeomorphism, hence a covering; (6) makes it one-sheeted.  So the cells lift to
a face-to-face periodic tiling of R^3.  Finally every vertex star is looked up in the
atlas, whose classes each carry an exact AKN witness.

Usage: python certify.py CERT.json ATLAS.json
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import gcd

from geometry import PAR, TAU, Q5, canonical_star, det, dot, ih_group, lin, scale, sgn, sub, vec

COS2 = {1: TAU * TAU / 4, 2: (TAU - 1) * (TAU - 1) / 4}       # cos^2(pi/5), cos^2(2pi/5)


def signed(s): return scale(1 if s > 0 else -1, PAR[abs(s) - 1])


def dihedral(e, u, w) -> int:
    """Dihedral angle along edge e between faces (e,u), (e,w), in units of pi/5."""
    E, U, Wv = signed(e), signed(u), signed(w)
    U, Wv = (sub(V, scale(dot(V, E) / dot(E, E), E)) for V in (U, Wv))
    c, c2 = dot(U, Wv), dot(U, Wv) * dot(U, Wv) / (dot(U, U) * dot(Wv, Wv))
    k = next(k for k, v in COS2.items() if c2 == v)
    return k if sgn(c) > 0 else 5 - k


def corners(n, I):
    """(vertex, signed edge triple at it) for the 8 corners of cell (n, I)."""
    for S in product((0, 1), repeat=3):
        v = tuple(c + sum(s for i, s in zip(I, S) if i == j) for j, c in enumerate(n))
        yield v, tuple(-(i + 1) if s else i + 1 for i, s in zip(I, S))


def minors_gcd(L) -> int:
    g = 0
    for cols in combinations(range(6), 3):
        M = [[L[r][c] for c in cols] for r in range(3)]
        g = gcd(g, M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
                - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    return g


def check(cert: dict, atlas: dict) -> dict:
    x = Fraction(cert['x']); Pq = vec(x); L = cert['period_lattice']
    key = lambda n: lin(Pq, n)
    # 1. quotient map
    assert all(key(b) == (0, 0, 0) for b in L), 'period not in kernel'
    assert det(*(lin(Pq, u) for u in ((1, 0, 0, 0, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 1, 0)))) != 0
    assert minors_gcd(L) == 1, 'period lattice not saturated'
    # 2. labels
    verts = {key(n): tuple(n) for n in cert['vertices']}
    assert len(verts) == len(cert['vertices']), 'duplicate vertex'
    cells = {(key(n), tuple(I)): tuple(n) for n, I in cert['cells']}
    assert len(cells) == len(cert['cells']), 'duplicate cell'
    faces, edges, solid, star = defaultdict(list), Counter(), Counter(), defaultdict(set)
    for (_, I), n in cells.items():
        for v, triple in corners(n, I):
            assert key(v) in verts, 'cell corner is not a vertex'
            star[key(v)].add(frozenset(triple))
            dh = [dihedral(e, *(t for t in triple if t != e)) for e in triple]
            solid[key(v)] += sum(dh) - 5
            for e, d in zip(triple, dh):
                if e > 0: edges[(key(v), e)] += d             # count each edge once, at its base
        for k in I:                                           # 3. faces
            J = tuple(i for i in I if i != k); o = sgn(det(PAR[J[0]], PAR[J[1]], PAR[k]))
            top = tuple(c + (j == k) for j, c in enumerate(n))
            faces[(key(n), J)].append(o); faces[(key(top), J)].append(-o)
    assert all(sorted(s) == [-1, 1] for s in faces.values()), 'face not shared by two opposite cells'
    assert set(edges.values()) == {10}, 'dihedral sum != 2 pi'          # 4.
    assert set(solid.values()) == {20} and len(solid) == len(verts), 'solid angle != 4 pi'  # 5.
    vol = sum((abs(det(*(PAR[i] for i in I))) for _, I in cells), Q5.of(0))
    cov = abs(det(*(lin(PAR, b) for b in L)))
    assert vol == cov, 'volume != covolume'                   # 6.
    group = ih_group(); known = {tuple(map(tuple, c['star'])): i for i, c in enumerate(atlas['classes'])}
    classes = Counter(known.get(canonical_star(frozenset(s), group), -1) for s in star.values())
    shapes = Counter('P' if sgn(dot(PAR[I[0]], PAR[I[1]]) * dot(PAR[I[1]], PAR[I[2]])
                               * dot(PAR[I[0]], PAR[I[2]])) > 0 else 'O' for _, I in cells)
    return {'vertices': len(verts), 'prolate': shapes['P'], 'oblate': shapes['O'],
            'faces': len(faces), 'edges': len(edges), 'covolume': [str(cov.a), str(cov.b)],
            'non_atlas_vertices': classes.pop(-1, 0),
            'atlas_classes_used': len(classes), 'class_counts': dict(sorted(classes.items()))}


if __name__ == '__main__':
    report = check(json.load(open(sys.argv[1])), json.load(open(sys.argv[2])))
    print(json.dumps(report, indent=1))
    sys.exit(report['non_atlas_vertices'] != 0)
