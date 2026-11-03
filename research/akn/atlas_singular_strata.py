"""Enumerate the closed-window stratification by exact line sweeps."""
from __future__ import annotations

import argparse
from bisect import bisect_left
from collections import defaultdict
from itertools import combinations
import json
from pathlib import Path

from atlas_chambers import basis, incident_cell_intervals
from atlas_region_count import K, Z, cross, dot


def signature(values, levels):
    result = []
    for value, cuts in zip(values, levels):
        index = bisect_left(cuts, value)
        result.append(2*index if index < len(cuts) and cuts[index] == value
                      else 2*index-1)
    return tuple(result)


def window_contains(key):
    return all(0 <= code <= 16 for code in key)


def encode(point):
    return [[str(x.a), str(x.b)] for x in point]


def sweep(ns, levels, digest, max_pairs):
    planes = [(f, k) for f, cuts in enumerate(levels) for k in range(len(cuts))]
    pairs = [(a, b) for a, b in combinations(planes, 2) if a[0] != b[0]]
    vertices, edges = {}, {}
    faces = defaultdict(set)
    for (f, i), (g, j) in pairs[:max_pairs]:
        n, m = ns[f], ns[g]
        direction = cross(n, m)
        pivot = next(k for k, x in enumerate(direction) if x != Z)
        a, b = (pivot+1) % 3, (pivot+2) % 3
        origin = [Z]*3
        origin[a] = (levels[f][i]*m[b]-n[b]*levels[g][j])/direction[pivot]
        origin[b] = (n[a]*levels[g][j]-levels[f][i]*m[a])/direction[pivot]
        values = [dot(u, origin) for u in ns]
        slopes = [dot(u, direction) for u in ns]
        fixed = signature(values, levels)
        active = [(h, code//2) for h, (code, slope) in
                  enumerate(zip(fixed, slopes)) if slope == Z and code % 2 == 0]
        if active[:2] != [(f, i), (g, j)]:
            continue
        if any(slope == Z and not 0 <= code <= 16
               for slope, code in zip(slopes, fixed)):
            continue

        events = defaultdict(list)
        lower, upper = [], []
        for h, (value, slope, cuts) in enumerate(zip(values, slopes, levels)):
            if slope == Z:
                continue
            times = [(cut-value)/slope for cut in cuts]
            lower.append(min(times[0], times[-1]))
            upper.append(max(times[0], times[-1]))
            for k, t in enumerate(times):
                events[t].append((h, 2*k))
        lo, hi = max(lower), min(upper)
        if hi < lo:
            continue
        side_steps = []
        if lo < hi:
            for h, _ in active:
                transverse = cross(ns[h], direction)
                side_steps.append([(r, dot(ns[r], transverse).sign())
                                   for r, _ in active if r != h])
        previous = None
        for t in sorted(t for t in events if lo <= t <= hi):
            point = tuple(x+t*d for x, d in zip(origin, direction))
            key = signature([x+t*d for x, d in zip(values, slopes)], levels)
            vertices[key] = point
            if previous is not None:
                old, left = previous
                middle = tuple((x+y)/2 for x, y in zip(left, point))
                edge = tuple(x if x == y else min(x, y) | 1 for x, y in zip(old, key))
                edges[edge] = middle, sorted((old, key))
                for steps in side_steps:
                    for side in (-1, 1):
                        face = list(edge)
                        for r, step in steps:
                            face[r] += side*step
                        if window_contains(face):
                            faces[tuple(face)].add(edge)
            previous = key, point

    complete = len(pairs) <= max_pairs
    rows = [{"dimension": 0, "key": key, "witness": encode(point)}
            for key, point in sorted(vertices.items())]
    rows.extend({"dimension": 1, "key": key, "witness": encode(point),
                 "boundary": ends} for key, (point, ends) in sorted(edges.items()))
    if complete:
        for key, boundary in sorted(faces.items()):
            corners = {v for e in boundary for v in edges[e][1]}
            center = [sum((vertices[v][d] for v in corners), Z)/len(corners)
                      for d in range(3)]
            rows.append({"dimension": 2, "key": key, "witness": encode(center),
                         "boundary": sorted(boundary)})
    return {"format": "AKN-SINGULAR-STRATA-1", "basis_sha256": digest,
            "pair_budget": max_pairs, "unprocessed_pairs": pairs[max_pairs:],
            "strata": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-pairs", type=int, default=8505)
    args = parser.parse_args()
    if args.max_pairs < 0:
        parser.error("--max-pairs must be nonnegative")
    normals, cuts, digest = basis()
    cells = incident_cell_intervals(normals, cuts)

    def in_tau(vector):
        return tuple(K(x.a-x.b, 2*x.b) for x in vector)

    packet = sweep(list(map(in_tau, normals)), list(map(in_tau, cuts)),
                   digest, args.max_pairs)
    memberships = {}
    for row in packet["strata"]:
        key = row["key"]
        forced, optional = [], []
        for cell, conditions in cells:
            if all(2*lo <= key[f] <= 2*hi for f, lo, hi in conditions):
                target = forced if all(2*lo < key[f] < 2*hi
                                       for f, lo, hi in conditions) else optional
                target.append(tuple(sorted(cell)))
        membership = tuple(sorted(forced)), tuple(sorted(optional))
        row["membership"] = memberships.setdefault(membership, len(memberships))
    packet["memberships"] = list(memberships)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as stream:
        json.dump(packet, stream, separators=(",", ":"))
        stream.write("\n")


if __name__ == "__main__":
    main()
