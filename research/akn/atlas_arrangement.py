"""Exact candidate arrangement for generic AKN radius-one vertex stars.

The ideal vertex window is Z(W_1,...,W_6). At the origin, each possible
incident 3-cell has axes I, corner orientation S in {0,1}^3, and center
C/2 = (sum_{i in I} (1-2*S_i)*W_i)/2.

For each complementary facet normal N = W_j x W_k, its inclusion changes
only where 2<N,gamma> = <N,C> +/- H, with
H = sum_{l not in I} |<W_l,N>|.

The vertex window itself has boundary planes 2<N,gamma> = +/- H_W.
Thus the arrangement generated below contains ALL possible transitions
of the 160 candidate signed triple cells at a generic central vertex.

This is an exact finite *reduction*, NOT a proof that the 24 sampled
vertex-star classes exhaust the arrangement. The next obligation is to
enumerate every nonempty OPEN chamber within the vertex window, construct
a rational Q(tau) witness, classify its complete star, and verify coverage
including faces/edges/vertices of the arrangement under an explicit
singularity convention.
"""
from __future__ import annotations

import json
from functools import cmp_to_key
from itertools import combinations, product

from radius2_exact import (FACETS, W, WINDOW_WIDTHS, CELL_WIDTHS,
                           ZERO, za, zs, zi, zdot, sign, sumz)


def arrangement() -> list[dict]:
    cuts = []
    for i, j, n in FACETS:
        upper = WINDOW_WIDTHS[(i, j)]
        levels = {upper, zi(upper, -1)}
        candidate_halfspaces = 0
        for I in combinations(range(6), 3):
            if i in I or j in I:
                continue
            width = CELL_WIDTHS[I][(i, j)]
            for bits in product((0, 1), repeat=3):
                twice_center = tuple(
                    sumz(zi(W[axis][k], 1 - 2*bit)
                         for axis, bit in zip(I, bits))
                    for k in range(3)
                )
                threshold = zdot(n, twice_center)
                levels.add(za(threshold, width))
                levels.add(zs(threshold, width))
                candidate_halfspaces += 1
        ordered = sorted(levels, key=cmp_to_key(lambda a, b: sign(zs(a, b))))
        cuts.append({
            "axis_pair": [i, j],
            "candidate_corner_cells": candidate_halfspaces,
            "levels_in_Z_tau_for_twice_normal_projection": [
                list(level) for level in ordered
            ],
        })
    return cuts


def main() -> None:
    cuts = arrangement()
    print(json.dumps({
        "normal_directions": len(cuts),
        "distinct_plane_levels": sum(len(c["levels_in_Z_tau_for_twice_normal_projection"])
                                     for c in cuts),
        "chamber_coverage_verified": False,
        "cuts": cuts,
    }, indent=2))


if __name__ == "__main__":
    main()
