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


def _compact(planes: list[Plane]) -> tuple[list[Plane], Plane | None]:
    """Keep the strongest strict bound in each positive-ray direction.

    No inexact rounding, divisions, or tolerance comparisons are used.
    """
    out: list[Plane] = []
    for p in planes:
        if _zero(p.a):
            if sign(p.b) <= 0:
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


def eliminate(planes: list[Plane]) -> Result:
    """Strict Fourier-Motzkin elimination, yielding exact feasibility.

    Multipliers -n.a[j] and p.a[j] are *positive*, so elimination preserves
    strict inequalities. A derived 0 < b with b <= 0 is a contradiction.
    Each step is reversible by choosing the eliminated variable between its
    strict lower and upper bounds.
    """
    sys, bad = _compact(planes)
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
                derived = Plane(a, b, (p.source, n.source))
                if _zero(a):
                    if sign(b) <= 0:
                        return Result(False, b, derived.source, tuple(stages))
                else:
                    projected.append(derived)
        sys, bad = _compact(projected)
        stages.append(len(sys))
        if bad is not None:
            return Result(False, bad.b, bad.source, tuple(stages))
    return Result(True, None, None, tuple(stages))


# Every nonzero normal to a true perpendicular-space window facet is
# a cross-product W_i x W_j; there are only 15 such axis pairs.
FACETS = tuple((i, j, zcross(W[i], W[j]))
               for i, j in combinations(range(6), 2))
CELL_WIDTHS: dict[tuple[int, int, int], dict[tuple[int, int], Z]] = {}
for I in combinations(range(6), 3):
    rest = tuple(W[k] for k in range(6) if k not in I)
    CELL_WIDTHS[I] = {
        (i, j): sumz(zzabs(zdot(g, n)) for g in rest)
        for i, j, n in FACETS if i not in I and j not in I
    }


def sumz(items) -> Z:
    s = ZERO
    for v in items:
        s = za(s, v)
    return s
