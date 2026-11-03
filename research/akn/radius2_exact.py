"""Exact finite-patch feasibility audit for the 3/2 AKN periodic certificate.

Uses an independent Z[tau] arithmetic implementation (tau**2 = tau + 1),
integer projection keys, and strict Fourier-Motzkin elimination. It does NOT
import geometry.py, certify.py, atlas.py, numpy, or an LP solver.

Radius 2 means the full cells of the central vertex star and the full stars
of all edge-neighbor vertices. It is NOT Euclidean radius 2, an arbitrary
two-cell shell, or a proof about every possible radius-2 patch.

Every required cell is demanded in a *single* regular (non-boundary) AKN
cut-and-project realization. The resulting open halfspaces are jointly
feasible if and only if a generic AKN shift can contain those required cells.
An infeasible OPEN system does not settle all possible singular conventions.

Usage:
    python research/akn/radius2_exact.py
    python research/akn/radius2_exact.py --json
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

Z = tuple[int, int]
V = tuple[Z, Z, Z]
ZERO: Z = (0, 0)
A = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
     (0, 0, 1), (0, 0, 1))
B = ((0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1),
     (1, 0, 0), (-1, 0, 0))
# tau'=1-tau; physical directions are not needed for this patch-language test.
W: tuple[V, ...] = tuple(
    tuple((a + b, -b) for a, b in zip(ax, bx))  # type: ignore[misc]
    for ax, bx in zip(A, B)
)
# 3*pi_x with x=-2/3, a faithful integer coordinate on Z^6 / L.
Q = tuple(tuple(3*a - 2*b for a, b in zip(ax, bx))
          for ax, bx in zip(A, B))


def za(x: Z, y: Z) -> Z:
    return x[0] + y[0], x[1] + y[1]


def zn(x: Z) -> Z:
    return -x[0], -x[1]


def zs(x: Z, y: Z) -> Z:
    return za(x, zn(y))


def zm(x: Z, y: Z) -> Z:
    return (x[0]*y[0] + x[1]*y[1],
            x[0]*y[1] + x[1]*y[0] + x[1]*y[1])


def zi(x: Z, n: int) -> Z:
    return x[0]*n, x[1]*n


def sign(x: Z) -> int:
    """Exact sign via 2(a+b*tau) = (2a+b)+b*sqrt(5)."""
    a, b = 2*x[0] + x[1], x[1]
    if a == 0:
        return (b > 0) - (b < 0)
    if b == 0 or (a > 0) == (b > 0):
        return (a > 0) - (a < 0)
    d = a*a - 5*b*b
    assert d != 0  # sqrt(5) is irrational
    return ((a > 0) - (a < 0)) * ((d > 0) - (d < 0))


def zzabs(x: Z) -> Z:
    return zn(x) if sign(x) < 0 else x


def zdot(x: V, y: V) -> Z:
    out = ZERO
    for u, v in zip(x, y):
        out = za(out, zm(u, v))
    return out


def zcross(u: V, v: V) -> V:
    return (zs(zm(u[1], v[2]), zm(u[2], v[1])),
            zs(zm(u[2], v[0]), zm(u[0], v[2])),
            zs(zm(u[0], v[1]), zm(u[1], v[0])))


def projection(n: tuple[int, ...]) -> tuple[int, int, int]:
    return tuple(sum(n[i]*Q[i][j] for i in range(6))
                 for j in range(3))  # type: ignore[return-value]


def triple_volume_sign(I: tuple[int, ...]) -> int:
    return sign(zdot(W[I[0]], zcross(W[I[1]], W[I[2]])))


@dataclass(frozen=True)
class Plane:
    a: V
    b: Z
    source: object = None  # identifying data, or a derivation pair


@dataclass(frozen=True)
class Result:
    feasible: bool
    obstruction: Z | None
    source: object = None
    stages: tuple[int, ...] = ()


def _zero(a: V) -> bool:
    return all(sign(x) == 0 for x in a)


def _compact(planes: list[Plane], strict: bool = True) -> tuple[list[Plane], Plane | None]:
    """Keep the strongest strict bound in each positive-ray direction.

    No inexact rounding, divisions, or tolerance comparisons are used.
    """
    out: list[Plane] = []
    for p in planes:
        if _zero(p.a):
            if sign(p.b) < 0 or (strict and sign(p.b) == 0):
                return [], p
            continue
        for k, old in enumerate(out):
            pivot = next(j for j in range(3) if sign(old.a[j]) != 0)
            if sign(old.a[pivot]) != sign(p.a[pivot]):
                continue
            if any(zm(p.a[j], old.a[pivot]) !=
                   zm(old.a[j], p.a[pivot]) for j in range(3)):
                continue
            # Compare bounds after scaling both normals to equal magnitude.
            cmp = zs(zm(p.b, zzabs(old.a[pivot])),
                     zm(old.b, zzabs(p.a[pivot])))
            if sign(cmp) < 0:
                out[k] = p
            break
        else:
            out.append(p)
    return out, None


def eliminate(planes: list[Plane], strict: bool = True) -> Result:
    """Strict Fourier-Motzkin elimination, yielding exact feasibility.

    Multipliers -n.a[j] and p.a[j] are *positive*. They preserve
    either strict inequalities (default) or non-strict closed inequalities.
    For strict systems, 0 < b fails when b <= 0; for closed, 0 <= b
    fails only when b < 0.
    Each step is reversible by choosing the eliminated variable between its
    strict lower and upper bounds.
    """
    sys, bad = _compact(planes, strict=strict)
    stages = [len(sys)]
    if bad is not None:
        return Result(False, bad.b, bad.source, tuple(stages))
    for j in (2, 1, 0):
        pos, neg, flat = [], [], []
        for p in sys:
            d = sign(p.a[j])
            (pos if d > 0 else neg if d < 0 else flat).append(p)
        projected = list(flat)
        for p in pos:
            for n in neg:
                v, w = zn(n.a[j]), p.a[j]  # both strictly positive
                a: V = tuple(za(zm(v, p.a[i]), zm(w, n.a[i]))
                             for i in range(3))  # type: ignore[assignment]
                b = za(zm(v, p.b), zm(w, n.b))
                derived = Plane(a, b, ("combine", v, w, p.source, n.source))
                if _zero(a):
                    if sign(b) < 0 or (strict and sign(b) == 0):
                        return Result(False, b, derived.source, tuple(stages))
                else:
                    projected.append(derived)
        sys, bad = _compact(projected, strict=strict)
        stages.append(len(sys))
        if bad is not None:
            return Result(False, bad.b, bad.source, tuple(stages))
    return Result(True, None, None, tuple(stages))


def check_obstruction(result: Result, originals: list[Plane], strict: bool = True) -> bool:
    """Replay a strict-infeasibility proof over the ORIGINAL inequalities.

    The derivation tree stores strictly positive Z[tau] multipliers for
    each Fourier-Motzkin pair. Equality 0<0 is a valid obstruction to an
    *open* common-shift solution, but not to singular boundary selection.
    """
    if result.feasible or result.source is None:
        return False
    known = {p.source: p for p in originals}

    def replay(node: object) -> Plane:
        if isinstance(node, tuple) and node and node[0] == "combine":
            _, v, w, p, n = node
            if sign(v) <= 0 or sign(w) <= 0:
                raise AssertionError("nonpositive elimination multiplier")
            left, right = replay(p), replay(n)
            a = tuple(za(zm(v, left.a[i]), zm(w, right.a[i]))
                      for i in range(3))
            b = za(zm(v, left.b), zm(w, right.b))
            return Plane(a, b)
        if node not in known:
            raise AssertionError("proof leaf not among input halfspaces")
        return known[node]

    try:
        final = replay(result.source)
    except (AssertionError, KeyError, TypeError):
        return False
    return (_zero(final.a) and final.b == result.obstruction
            and (sign(final.b) < 0 or (strict and sign(final.b) == 0)))


# Every nonzero normal to a true perpendicular-space window facet is
# a cross-product W_i x W_j; there are only 15 such axis pairs.
FACETS = tuple((i, j, zcross(W[i], W[j]))
               for i, j in combinations(range(6), 2))
def sumz(items) -> Z:
    s = ZERO
    for v in items:
        s = za(s, v)
    return s


CELL_WIDTHS: dict[tuple[int, int, int], dict[tuple[int, int], Z]] = {}
for I in combinations(range(6), 3):
    rest = tuple(W[k] for k in range(6) if k not in I)
    CELL_WIDTHS[I] = {
        (i, j): sumz(zzabs(zdot(g, n)) for g in rest)
        for i, j, n in FACETS if i not in I and j not in I
    }
WINDOW_WIDTHS = {
    (i, j): sumz(zzabs(zdot(g, n)) for g in W)
    for i, j, n in FACETS
}


def _star_map(cert: dict) -> dict[tuple[int, int, int], set[tuple[int, ...]]]:
    stars: dict[tuple[int, int, int], set[tuple[int, ...]]] = {}
    for base, I in cert["cells"]:
        for mask in range(8):
            vertex = list(base)
            signed = []
            for k, axis in enumerate(I):
                high = (mask >> k) & 1
                vertex[axis] += high
                signed.append(-(axis + 1) if high else axis + 1)
            stars.setdefault(projection(tuple(vertex)), set()).add(
                tuple(sorted(signed))
            )
    return stars


def patch_cells(
    center: tuple[int, ...],
    stars: dict[tuple[int, int, int], set[tuple[int, ...]]],
    radius: int,
) -> tuple[tuple[tuple[int, ...], tuple[int, int, int]], ...]:
    """Return relative lifted cell bases and axis triples.

    Radius 1: all cells incident at center.
    Radius 2: also all cells incident to edge-neighbors of center.
    Lift each neighboring star relative to the SAME central Z^6 anchor, so
    cell incidences crossing the periodic quotient are accounted for.
    """
    if radius not in (1, 2):
        raise ValueError("implemented radii: 1, 2 (edge-neighbor-star convention)")
    neighboring = {tuple(center)}
    if radius == 2:
        for tri in stars[projection(center)]:
            for signed in tri:
                v = list(center)
                v[abs(signed) - 1] += 1 if signed > 0 else -1
                neighboring.add(tuple(v))

    out = set()
    for v in neighboring:
        for tri in stars[projection(v)]:
            base = list(v)
            I = tuple(sorted(abs(s) - 1 for s in tri))
            for signed in tri:
                if signed < 0:
                    base[-signed - 1] -= 1
            relative = tuple(base[i] - center[i] for i in range(6))
            out.add((relative, I))
    return tuple(sorted(out))


def constraints(
    cells: tuple[tuple[tuple[int, ...], tuple[int, int, int]], ...],
) -> list[Plane]:
    """Necessary and sufficient strict cell-inclusion halfspaces.

    For N = W_i x W_j and a cell based at n with axes I, let
        C = 2*pi_perp(n) + sum_{k in I} W_k
        H = sum_{k not in I} |<W_k,N>|.
    Cell inclusion is exactly
        2<N,gamma> < <N,C> + H
       -2<N,gamma> < H - <N,C>.
    The central vertex's full 6-generator window is included as well.
    Since every listed cell must appear, intersection of these convex open
    regions is equivalent to existence of a generic common shift.
    """
    tight: dict[tuple[int, int, int], Plane] = {}

    def record(base: tuple[int, ...], I: tuple[int, ...] | None) -> None:
        twice_center = tuple(
            sumz(zi(W[k][j], 2*base[k] + (int(k in I) if I else 0))
                 for k in range(6))
            for j in range(3)
        )
        widths = CELL_WIDTHS[I] if I is not None else WINDOW_WIDTHS
        for f, (i, j, normal) in enumerate(FACETS):
            width = widths.get((i, j))
            if width is None:
                continue
            shift = zdot(normal, twice_center)
            for side in (1, -1):
                a: V = tuple(zi(x, 2*side) for x in normal)  # type: ignore[assignment]
                b = za(width, zi(shift, side))
                info = ("vertex" if I is None else "cell",
                        tuple(base), I, (i, j), side)
                item = Plane(a, b, info)
                key = (f, side, 0)
                prior = tight.get(key)
                if prior is None or sign(zs(b, prior.b)) < 0:
                    tight[key] = item

    record((0, 0, 0, 0, 0, 0), None)
    for relative, I in cells:
        record(relative, I)
    assert len(tight) == 30, "unexpected missing facet bound"
    return list(tight.values())


def audit(cert: dict, radius: int) -> dict:
    stars = _star_map(cert)
    vertices = [tuple(v) for v in cert["vertices"]]
    assert len(vertices) == len(stars) == 576
    results = Counter()
    patch_sizes = Counter()
    examples = {}
    for index, center in enumerate(vertices):
        patch = patch_cells(center, stars, radius)
        planes = constraints(patch)
        result = eliminate(planes)
        if not result.feasible:
            assert check_obstruction(result, planes), "invalid strict-infeasibility proof"
        if result.feasible:
            name = "feasible"
        else:
            # Strict open infeasibility alone CANNOT distinguish equality
            # obstruction from a genuinely empty closed intersection.
            closed = eliminate(planes, strict=False)
            if closed.feasible:
                name = "obstructed_at_boundary"
            else:
                assert check_obstruction(closed, planes, strict=False), (
                    "invalid closed-infeasibility proof"
                )
                name = "obstructed_strict"
        results[name] += 1
        patch_sizes[len(patch)] += 1
        if name not in examples:
            examples[name] = {
                "vertex_index": index,
                "vertex": list(center),
                "patch_cells": len(patch),
                "elimination_stages": list(result.stages),
                "obstruction": (
                    list(result.obstruction) if result.obstruction is not None
                    else None
                ),
            }
    return {
        "radius_convention": "central full star and full edge-neighbor stars"
        if radius == 2 else "central full star",
        "arithmetic": "exact Z[tau] strict Fourier-Motzkin",
        "radius": radius,
        "vertices_checked": len(vertices),
        "result_counts": dict(sorted(results.items())),
        "patch_cell_counts": dict(sorted(patch_sizes.items())),
        "examples": examples,
        "caveat": ("Strict feasibility is generic AKN patch-language membership. "
                   "Boundary obstruction does not decide singular shifts."),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args()
    path = Path(__file__).resolve().parent / "certificate_3_2.json"
    cert = json.loads(path.read_text())
    result = {"radius_1": audit(cert, 1), "radius_2": audit(cert, 2)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
