"""Periodic cubic approximants of the AKN tiling and their exact certificate data.

Selection uses the rational perp space tau -> x, where x = -q/p approximates the Galois
conjugate tau' = -1/tau for tau ~ p/q; tiles are the true golden rhombohedra.  Kernel(pi_perp_x) cap
Z^6 = L is the period lattice, and n mod L is identified by pi_perp_x(n), so a period's
vertices are the finitely many points of pi_perp_x(Z^6) in the shifted window.

Usage: python approximant.py P Q TRIALS SEED [OUT.json]
  screens TRIALS random rational shifts in floats and writes the exact cell data of the
  first one whose vertex stars all lie in atlas.json to OUT.json (checked by certify.py).
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, product

import numpy as np

from atlas import stars
from geometry import AXES, TRIPLES, CutProject, act, canonical_star, ih_group, lin, vec, zonotope_side

UNIT = tuple(tuple(int(i == j) for j in AXES) for i in AXES)


def period_lattice(x: Fraction, K: int = 6) -> list:
    """Three shortest independent integer kernel vectors of n -> sum n_i e_i(x).

    Saturation (= they generate all of ker cap Z^6) is certified by certify.py.
    """
    P = np.array([[float(c) for c in v] for v in vec(x)])           # 6 x 3, exact on ints
    grid = np.array(np.meshgrid(*[np.arange(-K, K + 1)] * 6, indexing='ij')).reshape(6, -1).T
    ker = grid[np.abs(grid @ P).max(1) < 1e-9]
    ker = sorted((n for n in ker if n.any()), key=lambda n: (n @ n, tuple(-n)))
    basis = []
    for n in ker:
        if np.linalg.matrix_rank(np.array(basis + [n])) > len(basis):
            basis.append(n)
        if len(basis) == 3: break
    assert all(lin(vec(x), b) == (0, 0, 0) for b in map(tuple, map(lambda v: map(int, v), basis)))
    return [list(map(int, b)) for b in basis]


def vertex_classes(cp: CutProject) -> dict:
    """BFS over +-e_i steps from vertex 0; returns key(=pi_perp_x(n)) -> representative n."""
    assert cp.vertex((0,) * 6)
    seen = {cp.project((0,) * 6): (0,) * 6}; frontier = [(0,) * 6]
    while frontier:
        nxt = []
        for n in frontier:
            for i, s in product(AXES, (1, -1)):
                m = tuple(c + s * (j == i) for j, c in enumerate(n))
                k = cp.project(m)
                if k not in seen and cp.vertex(m):
                    seen[k] = m; nxt.append(m)
        frontier = nxt
    return seen


def build(x: Fraction, gamma: tuple, group) -> dict:
    cp = CutProject(vec(x), gamma)
    verts = vertex_classes(cp)
    cells = {}
    for n in verts.values():
        for I in TRIPLES:
            for S in product((0, 1), repeat=3):
                base = tuple(c - sum(s for i, s in zip(I, S) if i == j) for j, c in enumerate(n))
                if cp.cell(base, I):
                    cells[(cp.project(base), I)] = base
    stars = [canonical_star(cp.star(n), group) for n in verts.values()]
    return {'x': str(x), 'gamma': [str(g) for g in gamma], 'period_lattice': period_lattice(x),
            'vertices': [list(n) for n in verts.values()],
            'cells': [[list(b), list(I)] for (_, I), b in cells.items()], 'stars': stars}


def random_gamma(x: Fraction, rng: random.Random, den: int = 10007) -> tuple:
    """A random rational point of the approximant window (rejection sampling)."""
    W = vec(x); box = [sum(abs(v[k]) for v in W) / 2 for k in range(3)]
    while True:
        g = tuple(Fraction(rng.randrange(-den, den + 1), den) * b for b in box)
        if zonotope_side(g, W) > 0: return g


def lattice_points(x: Fraction, radius: float) -> np.ndarray:
    """All points of pi_perp_x(Z^6) within sup-norm `radius`, in floats."""
    P = np.array([[float(c) for c in v] for v in vec(x)]); scale = 6 * 3 * x.denominator
    seen = {(0, 0, 0)}; frontier = [np.zeros(3)]
    while frontier:
        nxt = []
        for p in frontier:
            for m in np.concatenate([p + P, p - P]):
                k = tuple(np.rint(m * scale).astype(int))
                if k not in seen and np.abs(m).max() <= radius:
                    seen.add(k); nxt.append(m)
        frontier = nxt
    return np.array(sorted(seen)) / scale


def screen(x: Fraction, gammas: np.ndarray, atlas_images: set) -> list:
    """Float pre-screen: number of non-atlas vertex stars per period for each shift."""
    W = np.array([[float(c) for c in v] for v in vec(x)])
    pts = lattice_points(x, 2 * np.abs(W).sum(0).max())
    out = []
    for g in gammas:
        u = g - pts
        inside = np.ones(len(u), bool)
        for j, l in combinations(AXES, 2):
            n = np.cross(W[j], W[l]); inside &= np.abs(u @ n) < np.abs(W @ n).sum() / 2
        sts, margin = stars(u[inside], W)
        out.append(sum(s not in atlas_images for s in sts) if margin.min() > 1e-9 else -1)
    return out


def atlas_images(atlas: dict, group) -> set:
    """Every I_h image of every atlas star, as frozensets of signed triples."""
    return {frozenset(frozenset(act(g, s) for s in cell) for cell in c['star'])
            for c in atlas['classes'] for g in group}


def main(p, q, trials, seed, out=None):
    """Float-screen `trials` rational shifts; exactly rebuild the first clean one."""
    x = -Fraction(q, p); group = ih_group(); rng = random.Random(seed)
    gammas = [random_gamma(x, rng) for _ in range(trials)]
    defects = screen(x, np.array([[float(c) for c in g] for g in gammas]),
                     atlas_images(json.load(open('atlas.json')), group))
    clean = [i for i, d in enumerate(defects) if d == 0]
    print(f'{p}/{q}: {len(clean)}/{trials} shifts clean in float screen; defects {sorted(defects)}')
    if clean and out:
        cert = build(x, gammas[clean[0]], group)
        cert.update(approximant=f'{p}/{q}', seed=seed, trial=clean[0]); del cert['stars']
        json.dump(cert, open(out, 'w'), separators=(',', ':'))


if __name__ == '__main__':
    main(*map(int, sys.argv[1:5]), *sys.argv[5:])
