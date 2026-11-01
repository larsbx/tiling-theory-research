"""Deterministic exact 3D AKN chamber partition (research evidence, not a theorem).

Coordinates y = 2*gamma are in Q(tau)^3. All comparisons are exact.
The 135 planes are grouped into 15 parallel families, nine levels each.
A leaf prefix chooses consecutive open slabs for the first len(prefix) families.
Unexpanded prefixes MUST be retained: a capped search is explicitly incomplete.

Run: python research/akn/atlas_chambers.py --max-depth 2 --out /tmp/akn.json
Verify separately: python research/akn/atlas_chamber_check.py /tmp/akn.json
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from atlas_arrangement import arrangement
from geometry import (CutProject, PERP_TRUE, Q5, act, canonical_star, cross,
                      det, dot, ih_group, sgn)
from radius2_exact import FACETS

HERE = Path(__file__).resolve().parent
ZERO = Q5.of(0)


def as_q(z):
    """Convert a+b*tau into (a+b/2)+(b/2)*sqrt(5)."""
    a, b = z
    return Q5(Fraction(2*a+b, 2), Fraction(b, 2))


def encode(y):
    return [[str(c.a), str(c.b)] for c in y]


def decode(data):
    if len(data) != 3:
        raise ValueError("witness must have three coordinates")
    return tuple(Q5(Fraction(c[0]), Fraction(c[1])) for c in data)


def basis():
    fixture = json.loads((HERE / "atlas_hyperplanes.json").read_text())
    computed = arrangement()
    assert [(f["axis_pair"], f["levels"]) for f in fixture["families"]] == [
        (c["axis_pair"], c["levels_in_Z_tau_for_twice_normal_projection"])
        for c in computed
    ], "exact 135-plane input differs from independently recorded fixture"
    normals_by_pair = {(i, j): tuple(as_q(c) for c in n)
                       for i, j, n in FACETS}
    normals = [normals_by_pair[tuple(f["axis_pair"])]
               for f in fixture["families"]]
    levels = [[as_q(tuple(l)) for l in f["levels"]]
              for f in fixture["families"]]
    assert len(normals) == 15 and all(len(ls) == 9 for ls in levels)
    assert all(sgn(dot(n, PERP_TRUE[0])) in (-1, 0, 1) for n in normals)
    digest = sha256(json.dumps(fixture, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    return normals, levels, digest


@dataclass(frozen=True)
class Vertex:
    point: tuple[Q5, Q5, Q5]
    active: frozenset[int]


def _vkey(v):
    return tuple((c.a, c.b) for c in v.point)


def _rank_two(a, b):
    return any(sgn(x) for x in cross(a, b))


def _rank_three(vectors):
    return any(sgn(det(a, b, c)) for a, b, c in combinations(vectors, 3))


def _full(vertices):
    """A closed polytope has nonempty 3D interior iff 4 points span 3D."""
    if len(vertices) < 4:
        return False
    p = vertices[0].point
    diff = [tuple(x-y for x, y in zip(v.point, p))
            for v in vertices[1:]]
    return _rank_three(diff)


def _vertex_list(found):
    return tuple(Vertex(p, frozenset(s)) for p, s in
                 sorted(found.items(), key=lambda kv:
                        tuple((c.a, c.b) for c in kv[0])))


def initial_poly(normals, levels):
    # All vertices of a zonotope are among its 2^6 generator-sign sums.
    # Keep only extreme points: at least three independent tight facets.
    found = {}
    for signs in product((-1, 1), repeat=6):
        p = tuple(sum((s*w[k] for s, w in zip(signs, PERP_TRUE)), ZERO)
                  for k in range(3))
        tight = []
        for i, (n, cuts) in enumerate(zip(normals, levels)):
            d = dot(n, p)
            assert sgn(d-cuts[0]) >= 0 and sgn(cuts[-1]-d) >= 0
            if d == cuts[0]:
                tight.append(i*9)
            if d == cuts[-1]:
                tight.append(i*9+8)
        if _rank_three([normals[t//9] for t in tight]):
            found[p] = set(tight)
    result = _vertex_list(found)
    assert _full(result), "window must have three-dimensional interior"
    return result


def _edge(a, b, normals):
    # Two distinct vertices are adjacent iff they share two independent
    # supporting planes of the current convex 3D polytope.
    shared = sorted(a.active & b.active)
    return any(_rank_two(normals[u//9], normals[v//9])
               for u, v in combinations(shared, 2))


def clip(vertices, normals, levels, family, index, upper):
    """Intersect with n.y <= L (upper) or >= L (lower), retaining exact vertices."""
    n, level = normals[family], levels[family][index]
    plane_id = family*9+index
    values = [dot(n, v.point)-level for v in vertices]
    signs = [sgn(v) for v in values]
    found = {}

    def add(p, supports):
        found.setdefault(p, set()).update(supports)

    for v, side in zip(vertices, signs):
        if side == 0 or (side < 0 if upper else side > 0):
            add(v.point, v.active | ({plane_id} if side == 0 else set()))
    for i, j in combinations(range(len(vertices)), 2):
        if signs[i]*signs[j] >= 0 or not _edge(vertices[i], vertices[j], normals):
            continue
        a, b = vertices[i].point, vertices[j].point
        t = values[i] / (values[i]-values[j])  # in Q(tau), nonzero denominator
        p = tuple(x + t*(y-x) for x, y in zip(a, b))
        add(p, (vertices[i].active & vertices[j].active) | {plane_id})
    return _vertex_list(found)


def children(vertices, normals, levels, family):
    """Disjoint open slab children, in increasing level order."""
    remaining = vertices
    for k in range(1, 9):
        inside = clip(remaining, normals, levels, family, k, upper=True)
        if _full(inside):
            yield k-1, inside
        remaining = clip(remaining, normals, levels, family, k, upper=False)
        if not _full(remaining):
            break


def witness(vertices):
    if not _full(vertices):
        raise ValueError("no full-dimensional interior")
    count = len(vertices)
    return tuple(sum((v.point[j] for v in vertices), ZERO)/count
                 for j in range(3))


def _act_star(g, star):
    return frozenset(frozenset(act(g, s) for s in cell) for cell in star)


def _compose(g, h):
    """Composition g after h of signed permutations."""
    return tuple((1 if x > 0 else -1)*g[abs(x)-1] for x in h)


def _inverse(g):
    result = [0]*6
    for i, x in enumerate(g):
        result[abs(x)-1] = (1 if x > 0 else -1)*(i+1)
    return tuple(result)


def stabilizer_conjugacy(star, group):
    """Conjugacy of stabilizer SUBGROUPS, not an orbit of vertex stars."""
    stab = [h for h in group if _act_star(h, star) == star]
    index = {g: i for i, g in enumerate(group)}
    conjugates = []
    for g in group:
        inverse = _inverse(g)
        conjugates.append(tuple(sorted(index[_compose(_compose(g, h), inverse)]
                                       for h in stab)))
    signature = min(conjugates)
    digest = sha256(json.dumps(signature, separators=(",", ":")).encode()).hexdigest()
    return len(stab), digest


def star_record(y, group, known):
    cp = CutProject(PERP_TRUE, tuple(x/2 for x in y))
    star = cp.star((0,)*6)
    key = canonical_star(star, group)
    return {"orbit_class": known.get(key, -1),
            "stabilizer_order": stabilizer_conjugacy(star, group)[0],
            "stabilizer_conjugacy_sha256": stabilizer_conjugacy(star, group)[1]}


def enumerate_partition(*, max_nodes=50, max_depth=15):
    if max_depth < 0 or max_depth > 15 or max_nodes < 0:
        raise ValueError("max_depth in [0,15] and max_nodes >= 0 required")
    normals, levels, digest = basis()
    group = ih_group()
    atlas = json.loads((HERE / "atlas.json").read_text())
    known = {tuple(map(tuple, row["star"])): i
             for i, row in enumerate(atlas["classes"])}
    stack = [((), initial_poly(normals, levels))]
    leaves = []
    expanded = 0
    while stack:
        prefix, poly = stack.pop()
        result = {"prefix": list(prefix), "witness_y": encode(witness(poly))}
        if len(prefix) == 15:
            result.update(star_record(witness(poly), group, known))
            result["kind"] = "classified"
            leaves.append(result)
        elif len(prefix) >= max_depth or expanded >= max_nodes:
            result["kind"] = "frontier"
            leaves.append(result)
        else:
            expanded += 1
            new = [(prefix+(i,), p) for i, p in
                   children(poly, normals, levels, len(prefix))]
            stack.extend(reversed(new))
    leaves.sort(key=lambda row: row["prefix"])
    classes = sorted({leaf["orbit_class"] for leaf in leaves
                      if leaf["kind"] == "classified"})
    return {
        "format": "AKN-ATLAS-CHAMBERS-1",
        "plane_fixture_sha256": digest,
        "coordinates": "y=2gamma in Q(sqrt5), entries [rational_a, rational_b]",
        "expanded_prefixes": expanded,
        "classified_count": sum(x["kind"] == "classified" for x in leaves),
        "frontier_count": sum(x["kind"] == "frontier" for x in leaves),
        "search_exhausted": all(x["kind"] == "classified" for x in leaves),
        "observed_orbit_class_ids": classes,
        "leaves": leaves,
        "scope": "open generic chambers only; singular boundaries excluded",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-nodes", type=int, default=50)
    parser.add_argument("--max-depth", type=int, default=15)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    packet = enumerate_partition(max_nodes=args.max_nodes,
                                 max_depth=args.max_depth)
    payload = json.dumps(packet, sort_keys=True, indent=2)+"\n"
    if args.out:
        args.out.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
