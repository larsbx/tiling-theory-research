"""Replay the singular certificate by chord coverage and planar Euler counts.

The checker derives its own plane and cell equations. It clips each pair
intersection in planar coordinates, then checks that the witnessed intervals
partition the entire chord. It does not regenerate faces by perturbing edges.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path

from atlas_region_count import (HERE, K, ONE, Z, act, candidate_cells, cross,
                                dot, input_basis, point_group, section_basis,
                                subgroup_conjugacy)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def active(key):
    return tuple((f, code//2) for f, code in enumerate(key) if code % 2 == 0)


def boundary_of(lower, upper):
    return all(a == b or (b % 2 == 1 and abs(a-b) == 1)
               for a, b in zip(lower, upper))


def decode(point):
    require(len(point) == 3 and all(len(c) == 2 for c in point),
            "invalid witness shape")
    return tuple(K(*c) for c in point)


def clipped_chord(section, other, levels, widths):
    """Clip a planar line by the window strips, including singleton chords."""
    projected, free = section
    f, k = other
    a, b, c = projected[f]
    c = levels[f][k]-c
    if b != Z:
        axis = free[0]
        s, t, ds, dt = Z, c/b, ONE, -a/b
    else:
        axis = free[1]
        s, t, ds, dt = c/a, Z, Z, ONE
    lo = hi = None
    for (u, v, w), width in zip(projected, widths):
        value, slope = u*s+v*t+w, u*ds+v*dt
        if slope == Z:
            if not -width <= value <= width:
                return axis, None
            continue
        bounds = sorted(((-width-value)/slope, (width-value)/slope))
        lo = bounds[0] if lo is None else max(lo, bounds[0])
        hi = bounds[1] if hi is None else min(hi, bounds[1])
        if hi < lo:
            return axis, None
    return axis, (lo, hi)


def verify(packet):
    ns, levels, widths, digest = input_basis()
    require(packet["format"] == "AKN-SINGULAR-STRATA-1" and
            packet["basis_sha256"] == digest, "wrong packet or plane basis")
    require(packet["unprocessed_pairs"] == [] and packet["pair_budget"] >= 8505,
            "pair budget exhausted: singular coverage inconclusive")

    @lru_cache(maxsize=None)
    def rank(families):
        if len(families) < 2:
            return len(families)
        f, g, *rest = families
        direction = cross(ns[f], ns[g])
        return 3 if any(dot(direction, ns[h]) != Z for h in rest) else 2

    # For each family/code, mask out cells violating a strict or closed bound.
    catalog = sorted(candidate_cells(ns, levels))
    all_cells = (1 << len(catalog))-1
    masks = [[[all_cells, all_cells] for _ in range(17)] for _ in ns]
    for index, (_, conditions) in enumerate(catalog):
        bit = 1 << index
        for f, lo, hi in conditions:
            for code, mask in enumerate(masks[f]):
                if not 2*lo < code < 2*hi:
                    mask[0] ^= bit
                if not 2*lo <= code <= 2*hi:
                    mask[1] ^= bit

    @lru_cache(maxsize=None)
    def cells_from_mask(mask):
        return tuple(cell for i, (cell, _) in enumerate(catalog) if mask >> i & 1)

    memberships = [tuple(tuple(map(tuple, cells)) for cells in entry)
                   for entry in packet["memberships"]]
    require(len(set(memberships)) == len(memberships), "duplicate membership")
    used_memberships = set()
    vertices, edges, faces = {}, {}, {}
    on_plane = defaultdict(Counter)
    vertices_by_pair = defaultdict(set)
    edges_by_pair = defaultdict(list)
    edge_faces = Counter()
    examples = {}
    prior = (-1, ())
    for row in packet["strata"]:
        dim, key = row["dimension"], tuple(row["key"])
        require((dim, key) > prior, "duplicate or unordered stratum")
        prior = dim, key
        require(len(key) == 15 and all(type(c) is int and 0 <= c <= 16 for c in key),
                "invalid sign key")
        point = decode(row["witness"])
        planes = active(key)
        require(dim in (0, 1, 2) and rank(tuple(f for f, _ in planes)) == 3-dim,
                "incorrect stratum dimension")
        forced = closed = all_cells
        for f, code in enumerate(key):
            value = dot(ns[f], point)
            k = code//2
            inside = (value == levels[f][k] if code % 2 == 0 else
                      levels[f][k] < value < levels[f][k+1])
            require(inside, "incorrect exact relative-interior witness")
            strict_mask, closed_mask = masks[f][code]
            forced &= strict_mask
            closed &= closed_mask
        index = row["membership"]
        require(type(index) is int and 0 <= index < len(memberships),
                "invalid membership reference")
        require(memberships[index] == (cells_from_mask(forced),
                                      cells_from_mask(closed ^ forced)),
                "incorrect incident-cell membership")
        used_memberships.add(index)
        location = "window_boundary" if 0 in key or 16 in key else "window_interior"
        examples.setdefault((index, location), row)
        for plane in planes:
            on_plane[plane][dim] += 1
        if dim == 0:
            vertices[key] = point
            for pair in combinations(planes, 2):
                vertices_by_pair[pair].add(point)
        else:
            boundary = list(map(tuple, row["boundary"]))
            require(boundary == sorted(set(boundary)), "noncanonical boundary")
            source = vertices if dim == 1 else edges
            require(all(k in source and boundary_of(k, key) for k in boundary),
                    "incorrect incidence")
            if dim == 1:
                require(len(boundary) == 2, "edge must have two distinct ends")
                ends = tuple(vertices[k] for k in boundary)
                edges[key] = ends
                for pair in combinations(planes, 2):
                    edges_by_pair[pair].append(ends)
            else:
                require(len(boundary) >= 3, "face must have a polygonal boundary")
                faces[key] = boundary
                for edge in boundary:
                    edge_faces[edge, planes[0]] += 1

    require(used_memberships == set(range(len(memberships))), "unused membership")
    all_planes = [(f, k) for f in range(15) for k in range(9)]
    for plane in all_planes:
        f, k = plane
        pivot = next(i for i, v in enumerate(ns[f]) if v != Z)
        free = [i for i in range(3) if i != pivot]
        p, u, v = section_basis(ns[f], levels[f][k])
        projected = [(dot(n, u), dot(n, v), dot(n, p)) for n in ns]
        section = projected, free
        for other in all_planes:
            if other <= plane or other[0] == f:
                continue
            axis, chord = clipped_chord(section, other, levels, widths)
            pair = plane, other
            intervals = edges_by_pair.get(pair, ())
            points = {p[axis] for p in vertices_by_pair.get(pair, ())}
            if chord is None:
                require(not intervals and not points, "strata on empty chord")
                continue
            lo, hi = chord
            segments = sorted(tuple(sorted((a[axis], b[axis]))) for a, b in intervals)
            current = lo
            for start, end in segments:
                require(start == current and start < end, "chord gap or overlap")
                current = end
            require(current == hi and points == {lo, hi, *(b for _, b in segments)},
                    "incomplete chord or missing singleton")
        counts = on_plane[plane]
        require(counts[2] == 1+counts[1]-counts[0],
                "missing or extra section faces by planar Euler count")
    for key in edges:
        planes = active(key)
        for plane in planes:
            on_section_boundary = any(other != plane and other[1] in (0, 8)
                                      for other in planes)
            require(edge_faces[key, plane] == (1 if on_section_boundary else 2),
                    "missing or extra edge-to-face incidence")

    group = point_group()
    known = {tuple(map(tuple, row["star"])) for row in
             json.loads((HERE/"atlas.json").read_text())["classes"]}
    require(len(known) == 24, "unexpected generic comparison atlas")
    orbit_cache, stabilizers = {}, {}
    by_convention = defaultdict(set)
    counterexamples = {}
    for (index, location), example in examples.items():
        forced, optional = memberships[index]
        for convention, raw in (("strict", forced),
                                ("closed", tuple(sorted(forced+optional)))):
            if raw not in orbit_cache:
                orbit = {tuple(sorted(tuple(sorted(act(g, s) for s in cell))
                                      for cell in raw)) for g in group}
                representative = min(orbit)
                orbit_cache.update(dict.fromkeys(orbit, representative))
                stabilizers[representative] = subgroup_conjugacy(representative, group)
            representative = orbit_cache[raw]
            center_included = convention == "closed" or location == "window_interior"
            category = f"{convention}/{location}"
            by_convention[category].add(representative)
            if representative not in known:
                order, conjugacy = stabilizers[representative]
                counterexamples.setdefault((category, representative), {
                    "convention": convention, "stratum": example,
                    "location": location, "center_included": center_included,
                    "forced": forced, "boundary_dependent": optional,
                    "canonical_star": representative,
                    "stabilizer_order": order,
                    "stabilizer_conjugacy_sha256": conjugacy,
                })

    return {
        "all_singular_strata_covered": True,
        "basis_sha256": digest,
        "boundary_convention_decided": False,
        "scope": "finite local cell patterns under strict and closed threshold rules",
        "strict_window_boundary_has_center": False,
        "strata_counts": [len(vertices), len(edges), len(faces)],
        "window_boundary_counts": [sum(0 in key or 16 in key for key in rows)
                                   for rows in (vertices, edges, faces)],
        "orbits": {c: len(stars) for c, stars in by_convention.items()},
        "stabilizer_conjugacy_types": {
            c: len({stabilizers[s][1] for s in stars})
            for c, stars in by_convention.items()},
        "counterexamples_to_generic_orbit_coverage": list(counterexamples.values()),
        "next_obligation": "Determine which coherent singular tiling conventions "
                           "are realizable and classify their local stars.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = verify(json.loads(args.packet.read_text()))
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")


if __name__ == "__main__":
    main()
