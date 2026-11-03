"""Automatically generate exact *partial* AKN singular-boundary experiments.

For each of the 105 interior hyperplanes, select one deterministic pair
of generic chamber witnesses on opposite sides, interpolate an exact
point on that hyperplane, then distinguish cells strictly present,
possibly present under a CLOSED-window convention, and absent.

This samples every interior transition plane once. It DOES NOT enumerate
all lower-dimensional strata or choose a singular inclusion convention.
Run only after a full generic packet is independently accepted.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

from geometry import (PERP_TRUE, Q5, zonotope_side, dot)
from atlas_chambers import basis, decode, encode

HERE = Path(__file__).resolve().parent
ZERO = Q5.of(0)


def classify(y):
    """Original exact selection geometry, keeping boundary ambiguity explicit."""
    gamma = tuple(x/2 for x in y)
    assert zonotope_side(gamma, PERP_TRUE) > 0
    forced, possible = [], []
    for axes in combinations(range(6), 3):
        rest = tuple(PERP_TRUE[j] for j in range(6) if j not in axes)
        for bits in product((0, 1), repeat=3):
            center = tuple(sum(((Fraction(1, 2)-bit)*PERP_TRUE[axis][d]
                                for axis, bit in zip(axes, bits)), ZERO)
                           for d in range(3))
            offset = tuple(g-c for g, c in zip(gamma, center))
            side = zonotope_side(offset, rest)
            signed = tuple(sorted((-(axis+1) if bit else axis+1)
                                  for axis, bit in zip(axes, bits)))
            if side > 0:
                forced.append(signed)
            if side >= 0:
                possible.append(signed)
    return sorted(forced), sorted(possible)


def probe(packet):
    assert packet["search_exhausted"] is True
    assert packet["frontier_count"] == 0
    normals, levels, digest = basis()
    assert packet["plane_fixture_sha256"] == digest
    # One stable strict witness for each of 8 slabs x 15 normal families.
    representatives = {}
    for leaf in packet["leaves"]:
        if leaf["kind"] != "classified":
            raise ValueError("partial packet is not a full generic enumeration")
        for family, slab in enumerate(leaf["prefix"]):
            representatives.setdefault((family, slab), leaf["witness_y"])
        if len(representatives) == 120:
            break
    assert len(representatives) == 120
    rows = []
    for family, normal in enumerate(normals):
        for k in range(1, 8):
            lower = decode(representatives[(family, k-1)])
            upper = decode(representatives[(family, k)])
            level = levels[family][k]
            below = dot(normal, lower)-level
            above = dot(normal, upper)-level
            assert below.sign() < 0 < above.sign()
            t = -below/(above-below)
            assert 0 < t.sign() and (1-t).sign() > 0
            point = tuple(a+t*(b-a) for a, b in zip(lower, upper))
            forced, possible = classify(point)
            active = [[f, j] for f, n in enumerate(normals)
                      for j in range(1, 8)
                      if dot(n, point) == levels[f][j]]
            assert [family, k] in active
            rows.append({
                "target_plane": [family, k],
                "witness_y": encode(point),
                "active_internal_hyperplanes": active,
                "forced_signed_cells": [list(cell) for cell in forced],
                "closed_possible_signed_cells": [list(cell) for cell in possible],
                "boundary_dependent_cell_count": len(possible)-len(forced),
            })
    return {
        "format": "AKN-SINGULAR-PLANE-PROBES-1",
        "input_plane_fixture_sha256": digest,
        "scope": "one exact interior witness per interior plane; NOT all strata",
        "boundary_convention_selected": False,
        "all_singular_memberships_classified": False,
        "candidate_plane_count": 105,
        "probes": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    result = probe(json.loads(args.packet.read_text()))
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")


if __name__ == "__main__":
    main()
