"""Universe of combinatorially possible AKN-rhombohedral vertex configurations.

A corner of a golden rhombohedron at a vertex is a signed axis triple {s_a, s_b, s_c}
(edge vectors +-e_a, +-e_b, +-e_c, distinct axes): 20 triples x 8 signs = 160 corners.
Its link is the spherical triangle on the 12 icosahedral directions.  A vertex
configuration is a set of corners whose link triangles tile S^2: interiors pairwise
disjoint and every arc shared by exactly two triangles on opposite sides.  No geodesic
between two non-antipodal icosahedral directions passes through a third, so this is an
edge-to-edge triangulation, i.e. the cells meet face-to-face around the vertex.

Enumeration: exact-cover backtracking from each I_h-orbit representative corner,
closing the open arc with the fewest candidates first; results are deduplicated by the
least triangle bitmask over I_h.  All geometric predicates are exact in Q(sqrt5).

Usage: python corona.py OUT.json
"""
from __future__ import annotations

import json
import sys
from itertools import combinations, product

from geometry import (PAR, TRIPLES, act, canonical_star, cell_shape, cross, det, dot, ih_group,
                      scale, sgn)

CORNERS = tuple(tuple((-(i + 1) if s else i + 1) for i, s in zip(I, S))
                for I in TRIPLES for S in product((0, 1), repeat=3))
INDEX = {frozenset(c): k for k, c in enumerate(CORNERS)}


def ray(s): return scale(1 if s > 0 else -1, PAR[abs(s) - 1])


def disjoint_interiors(c1, c2) -> bool:
    """Cones over c1, c2 have disjoint interiors iff some plane through 0 separates them.

    For two simplicial cones a separating plane can be taken spanned by two of their
    rays (an edge plane of either, or one ray of each), so finitely many tests suffice.
    """
    A, B = [ray(s) for s in c1], [ray(s) for s in c2]
    for u, v in combinations(A + B, 2):
        n = cross(u, v)
        if all(sgn(x) == 0 for x in n): continue
        sa, sb = [sgn(dot(n, a)) for a in A], [sgn(dot(n, b)) for b in B]
        if (min(sa) >= 0 and max(sb) <= 0) or (max(sa) <= 0 and min(sb) >= 0):
            return True
    return False


def side(a, b, c) -> int:
    """Side of directed arc a->b on which direction c lies."""
    return sgn(det(ray(a), ray(b), ray(c)))


CONFLICT = tuple(sum(1 << j for j, d in enumerate(CORNERS) if j != k and not disjoint_interiors(c, d))
                 for k, c in enumerate(CORNERS))


def arcs(k):
    """Directed boundary arcs (a, b, side of the corner) of corner k."""
    c = CORNERS[k]
    return [((a, b), side(a, b, next(x for x in c if x not in (a, b))))
            for a, b in combinations(c, 2)]


ARCS = tuple(arcs(k) for k in range(len(CORNERS)))
ACROSS = {}                   # (arc, side needed) -> corners containing the arc on that side
for k in range(len(CORNERS)):
    for arc, s in ARCS[k]:
        ACROSS.setdefault((arc, s), []).append(k)


def configurations(root: int):
    """All triangulations of S^2 by corners that contain corner `root` (as bitmasks)."""
    def extend(chosen, conflict, open_arcs):
        if not open_arcs:
            yield chosen; return
        best = None
        for arc, s in open_arcs.items():
            options = [k for k in ACROSS.get((arc, -s), ()) if not conflict >> k & 1]
            if best is None or len(options) < len(best[1]):
                best = (arc, options)
                if not options: return
        for k in best[1]:
            nxt = dict(open_arcs)
            for arc, s in ARCS[k]:
                if arc in nxt: del nxt[arc]           # closes an arc: sides are opposite
                else: nxt[arc] = s
            yield from extend(chosen | 1 << k, conflict | CONFLICT[k] | 1 << k, nxt)
    yield from extend(1 << root, CONFLICT[root] | 1 << root, dict(ARCS[root]))


def corner_perm(g):
    return tuple(INDEX[frozenset(act(g, s) for s in c)] for c in CORNERS)


def orbit(mask: int, perms) -> set:
    bits = [k for k in range(len(CORNERS)) if mask >> k & 1]
    return {sum(1 << p[k] for k in bits) for p in perms}


def enumerate_universe():
    """Corner-orbit roots and the least-bitmask representative of every class."""
    perms = [corner_perm(g) for g in ih_group()]
    roots = sorted({min(p[k] for p in perms) for k in range(len(CORNERS))})
    seen, found = set(), []
    for r in roots:
        for mask in configurations(r):
            if mask not in seen:
                images = orbit(mask, perms); seen |= images; found.append(min(images))
    return roots, sorted(found)


def as_star(mask: int):
    return [list(CORNERS[k]) for k in range(len(CORNERS)) if mask >> k & 1]


def main(out, atlas_path='atlas.json'):
    """Write the universe; `akn` marks classes in the (exactly witnessed) AKN atlas."""
    roots, found = enumerate_universe(); group = ih_group()
    atlas = {tuple(map(tuple, c['star'])) for c in json.load(open(atlas_path))['classes']}
    rows = []
    for m in found:
        star = as_star(m); shapes = [cell_shape(c) for c in star]
        akn = tuple(canonical_star(frozenset(map(frozenset, star)), group)) in atlas
        rows.append({'star': star, 'P': shapes.count('P'), 'O': shapes.count('O'), 'akn': akn})
    json.dump({'corner_orbit_roots': [list(CORNERS[r]) for r in roots], 'configurations': rows},
              open(out, 'w'), separators=(',', ':'))
    print(len(roots), 'corner orbits;', len(rows), 'configurations;',
          sum(r['akn'] for r in rows), 'in the AKN atlas')


if __name__ == '__main__':
    main(sys.argv[1])
