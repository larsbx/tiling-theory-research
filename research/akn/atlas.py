"""AKN vertex atlas: Monte Carlo discovery in floats, exact witness per class.

A vertex of the AKN tiling with perp coordinate u (relative to the shift) has a star
determined by u in W.  Sampling u uniformly in W finds the classes; each class is then
re-derived from a rational witness gamma = u in exact Q(sqrt5) arithmetic, so every
recorded class provably occurs.  Completeness (no unseen class) is NOT certified here.

Usage: python atlas.py SAMPLES SEED OUT.json
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from itertools import product

import numpy as np

from geometry import (AXES, PERP_TRUE, TRIPLES, CutProject, Q5, canonical_star, cell_shape,
                      ih_group)

W = np.array([[float(x) for x in v] for v in PERP_TRUE])          # 6 x 3
CANDIDATES = [(I, S) for I in TRIPLES for S in product((0, 1), repeat=3)]


def sample_window(rng, k):
    """Uniform samples of the open window Z(W) via its 6D-cube parametrization's hull."""
    box = np.abs(W).sum(0) / 2
    pts = rng.uniform(-box, box, size=(k, 3))
    coeff_ok = np.ones(k, bool)
    for j in AXES:
        for l in AXES[j + 1:]:
            n = np.cross(W[j], W[l]); h = np.abs(W @ n).sum() / 2
            coeff_ok &= np.abs(pts @ n) < h
    return pts[coeff_ok]


def stars(u, W=W):
    """Signed-axis stars of a vertex at perp offset u (rows) for perp vectors W (6 x 3),
    plus each row's min distance to a selection boundary."""
    k = len(u); cells = [[] for _ in range(k)]; margin = np.full(k, np.inf)
    for I, S in CANDIDATES:
        rest = [l for l in AXES if l not in I]
        centre = np.array([0.5 - S[I.index(i)] if i in I else 0.0 for i in AXES])
        t = np.linalg.solve(W[rest].T, (u - centre @ W).T).T          # coords in W_rest
        margin = np.minimum(margin, np.abs(np.abs(t) - 0.5).min(1))
        for r in np.nonzero((np.abs(t) < 0.5).all(1))[0]:
            cells[r].append(frozenset(-(i + 1) if s else i + 1 for i, s in zip(I, S)))
    return [frozenset(c) for c in cells], margin


def discover(samples, seed, group, batch=20000, eps=1e-9):
    """class -> (hits, best margin, sample with best margin); boundary-near samples dropped."""
    rng = np.random.default_rng(seed); best = {}; left = samples
    while left > 0:
        u = sample_window(rng, min(batch, left)); left -= len(u)
        sts, margin = stars(u)
        for star, m, x in zip(sts, margin, u):
            if m > eps:
                key = canonical_star(star, group)
                hits, m0, x0 = best.get(key, (0, -1.0, None))
                best[key] = (hits + 1, *((m, x) if m > m0 else (m0, x0)))
    return best


def exact_witness(x, key, group):
    """Rationalize a sample and recompute its star exactly; must reproduce `key`."""
    gamma = tuple(Fraction(float(c)).limit_denominator(10 ** 9) for c in x)
    cp = CutProject(PERP_TRUE, tuple(map(Q5.of, gamma)))
    assert cp.vertex((0,) * 6)
    assert canonical_star(cp.star((0,) * 6), group) == key
    return gamma


def main(samples, seed, out):
    group = ih_group(); best = discover(samples, seed, group)
    classes = []
    for key, (hits, m, x) in sorted(best.items(), key=lambda kv: -kv[1][0]):
        shapes = [cell_shape(c) for c in key]
        classes.append({'star': [list(c) for c in key], 'cells': len(key),
                        'P': shapes.count('P'), 'O': shapes.count('O'), 'hits': hits,
                        'witness_gamma': [str(c) for c in exact_witness(x, key, group)]})
    json.dump({'samples': samples, 'seed': seed, 'classes': classes}, open(out, 'w'), indent=1)
    print(len(classes), 'classes;', [(c['P'], c['O']) for c in classes])


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
