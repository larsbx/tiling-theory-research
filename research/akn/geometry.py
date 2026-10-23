"""Exact geometry of the AKN (3D Penrose) rhombohedral tiling.

Canonical cut-and-project from Z^6 (Oguey--Duneau--Katz criterion):

* vertex  n          is selected  iff  gamma - pi_perp(n)            in Z(W)
* 3-cell  (n, I)     is selected  iff  gamma - pi_perp(n + 1_I / 2)  in Z(W_{I^c})

where Z(V) = sum_{v in V} [-1/2, 1/2] v is the zonotope of V and W = pi_perp(e_1..e_6).
Selection is evaluated either in the true perp space (tau -> tau' = 1 - tau, exact in
Q(sqrt5)) or in a rational approximant perp space (tau -> x in Q).  Tiles are always
realized with the true parallel vectors, i.e. as exact golden rhombohedra in Z[tau]^3.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations, product

# Six 5-fold axes of the icosahedron, e_i = A_i + tau * B_i.
A = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, 1))
B = ((0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1), (1, 0, 0), (-1, 0, 0))
AXES = range(6)
TRIPLES = tuple(combinations(AXES, 3))


@dataclass(frozen=True, order=True)
class Q5:
    """a + b*sqrt5 with a, b rational; exact ordered field arithmetic."""
    a: Fraction
    b: Fraction = Fraction(0)

    @staticmethod
    def of(x) -> 'Q5':
        return x if isinstance(x, Q5) else Q5(Fraction(x))

    def __add__(s, o): o = Q5.of(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q5(-s.a, -s.b)
    def __sub__(s, o): return s + (-Q5.of(o))
    def __rsub__(s, o): return Q5.of(o) - s
    def __mul__(s, o): o = Q5.of(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__

    def __truediv__(s, o):
        o = Q5.of(o); n = o.a * o.a - 5 * o.b * o.b
        return s * Q5(o.a / n, -o.b / n)

    def sign(s) -> int:
        """Exact sign of a + b sqrt5."""
        sa, sb = (s.a > 0) - (s.a < 0), (s.b > 0) - (s.b < 0)
        if sa == sb or sb == 0: return sa
        if sa == 0: return sb
        return sa * ((s.a * s.a > 5 * s.b * s.b) - (s.a * s.a < 5 * s.b * s.b))

    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def __abs__(s): return -s if s.sign() < 0 else s


SQRT5 = Q5(Fraction(0), Fraction(1))
TAU = Q5(Fraction(1, 2), Fraction(1, 2))
TAU_CONJ = Q5(Fraction(1, 2), Fraction(-1, 2))


def vec(x) -> tuple:
    """The six axis vectors with tau replaced by the scalar x."""
    return tuple(tuple(a + x * b for a, b in zip(Ai, Bi)) for Ai, Bi in zip(A, B))


def dot(u, v): return sum((x * y for x, y in zip(u, v)), Q5.of(0) if isinstance(u[0], Q5) else 0)
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def det(u, v, w): return dot(u, cross(v, w))
def add(u, v): return tuple(x + y for x, y in zip(u, v))
def sub(u, v): return tuple(x - y for x, y in zip(u, v))
def scale(c, u): return tuple(c * x for x in u)
def sgn(x) -> int: return x.sign() if isinstance(x, Q5) else (x > 0) - (x < 0)


def lin(vs, n):
    """sum_i n_i vs_i for integer or half-integer coefficients n."""
    out = scale(0, vs[0])
    for c, v in zip(n, vs):
        if c: out = add(out, scale(c, v))
    return out


PAR = vec(TAU)                       # true parallel vectors, exact in Q(sqrt5)
PERP_TRUE = vec(TAU_CONJ)            # true perp vectors (Galois conjugate)


def zonotope_side(p, gens) -> int:
    """+1 / 0 / -1 as p lies inside / on the boundary of / outside Z(gens), exactly.

    Z(gens) = {x : |<x, n_jk>| <= h_jk} over facet normals n_jk = g_j x g_k with
    h_jk = 1/2 sum_l |<g_l, n_jk>|.
    """
    sides = []
    for gj, gk in combinations(gens, 2):
        n = cross(gj, gk)
        h = sum((abs(dot(g, n)) for g in gens), 0 * n[0]) / 2
        sides.append(sgn(h - abs(dot(p, n))))
    return min(sides)


@dataclass(frozen=True)
class CutProject:
    """Canonical selection in the perp space spanned by `perp` with shift gamma."""
    perp: tuple
    gamma: tuple

    def project(self, n): return lin(self.perp, n)

    def _test(self, centre, gens):
        side = zonotope_side(sub(self.gamma, self.project(centre)), gens)
        if side == 0:
            raise ValueError(f'non-generic shift: {centre} on a window boundary')
        return side > 0

    def vertex(self, n) -> bool:
        return self._test(n, self.perp)

    def cell(self, n, I) -> bool:
        centre = tuple(c + Fraction(1, 2) * (i in I) for i, c in enumerate(n))
        return self._test(centre, tuple(self.perp[l] for l in AXES if l not in I))

    def star(self, n) -> frozenset:
        """Cells at vertex n as frozensets of signed axes (+i+1 / -(i+1)) leaving n."""
        out = set()
        for I in TRIPLES:
            for S in product((0, 1), repeat=3):
                base = list(n)
                for i, s in zip(I, S): base[i] -= s
                if self.cell(tuple(base), I):
                    out.add(frozenset((-(i + 1) if s else i + 1) for i, s in zip(I, S)))
        return frozenset(out)


# --- icosahedral symmetry acting on signed axes --------------------------------

def gram(vs): return tuple(tuple(dot(u, v) for v in vs) for u in vs)


def ih_group() -> tuple:
    """All signed permutations of the six axes preserving the parallel Gram matrix.

    Each element is a tuple g with g[i] = +-(j+1) meaning e_i -> +-e_j.  Preserving
    the Gram matrix of a spanning set is equivalent to extending to an orthogonal map,
    so this is the full point group I_h (order 120) of the axis star.
    """
    G = gram(PAR)
    out = []
    for perm in permutations(AXES):
        for signs in product((1, -1), repeat=6):
            if all(signs[i] * signs[j] * G[perm[i]][perm[j]] == G[i][j]
                   for i in AXES for j in AXES):
                out.append(tuple(s * (p + 1) for s, p in zip(signs, perm)))
    return tuple(out)


def act(g, signed: int) -> int:
    return (1 if signed > 0 else -1) * g[abs(signed) - 1]


def canonical_star(star, group) -> tuple:
    """Lexicographically least image of a star under the group: a class invariant."""
    return min(tuple(sorted(tuple(sorted(act(g, s) for s in cell)) for cell in star))
               for g in group)


def cell_shape(signed_triple) -> str:
    """'P' (prolate) or 'O' (oblate) from the edge vectors at a corner."""
    u, v, w = (scale(1 if s > 0 else -1, PAR[abs(s) - 1]) for s in signed_triple)
    # Sign-flip invariant: a prolate cell has a corner with three acute face angles,
    # an oblate one a corner with three obtuse face angles.
    p = sgn(dot(u, v)) * sgn(dot(v, w)) * sgn(dot(u, w))
    return 'P' if p > 0 else 'O'
