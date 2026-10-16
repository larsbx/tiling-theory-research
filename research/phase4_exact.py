"""Exact Q(sqrt(5)) arithmetic; no floating-point ordering or tolerances."""
from dataclasses import dataclass
from fractions import Fraction
from functools import total_ordering


@total_ordering
@dataclass(frozen=True)
class Q5:
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __post_init__(self):
        object.__setattr__(self, 'a', Fraction(self.a))
        object.__setattr__(self, 'b', Fraction(self.b))

    @staticmethod
    def coerce(other):
        return other if isinstance(other, Q5) else Q5(other)

    def __add__(self, other):
        other = self.coerce(other)
        return Q5(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q5(-self.a, -self.b)

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        other = self.coerce(other)
        return Q5(self.a * other.a + 5 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        norm = other.a * other.a - 5 * other.b * other.b
        if not norm:
            raise ZeroDivisionError
        return self * Q5(other.a / norm, -other.b / norm)

    def sign(self):
        a, b = self.a, self.b
        if not b:
            return (a > 0) - (a < 0)
        if not a or (a > 0) == (b > 0):
            return 1 if b > 0 else -1
        # Opposite signs: compare rational squares, not approximations.
        delta = a * a - 5 * b * b
        return ((delta > 0) - (delta < 0)) * (1 if a > 0 else -1)

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def __eq__(self, other):
        if not isinstance(other, (Q5, int, Fraction)):
            return NotImplemented
        other = self.coerce(other)
        return (self.a, self.b) == (other.a, other.b)

    def __hash__(self):
        return hash(self.a) if not self.b else hash((self.a, self.b))

    def __lt__(self, other):
        return (self - other).sign() < 0

    def __abs__(self):
        return -self if self.sign() < 0 else self

    def ceil(self):
        # Rational bracketing from 2 < sqrt(5) < 3, followed by exact bisection.
        lo = self.a + (2 if self.b >= 0 else 3) * self.b
        hi = self.a + (3 if self.b >= 0 else 2) * self.b
        low, high = lo.numerator // lo.denominator, -(-hi.numerator // hi.denominator)
        while low < high:
            middle = (low + high) // 2
            if self <= middle:
                high = middle
            else:
                low = middle + 1
        return low

    def record(self):
        return {'rational': str(self.a), 'sqrt5': str(self.b)}


SQRT5 = Q5(0, 1)
T = (1 + SQRT5) / 2
TP = (1 - SQRT5) / 2
RHO = TP * TP
R = SQRT5 * T
INITIAL_BOUND = 2 * R
LENGTH = {'a': T, 'b': Q5(1)}
CHILD = {
    'a': [('a', (0, 0)), ('a', (1, 0)), ('b', (2, 0))],
    'b': [('b', (0, 0)), ('a', (0, 1))],
}


def E(v):
    return T * v[0] + v[1]


def C(v):
    return TP * v[0] + v[1]


def M(v):
    return 2 * v[0] + v[1], v[0] + v[1]


def sub(u, v):
    return u[0] - v[0], u[1] - v[1]


def overlap(i, j, v):
    return -LENGTH[j] < E(v) < LENGTH[i]


def lattice_box(physical_bound, internal_bound):
    # Invert (E,C): x=(E-C)/sqrt5, y=(tau*C-tau'*E)/sqrt5.
    return ((physical_bound + internal_bound) / SQRT5).ceil(), (
        (T * internal_bound + abs(TP) * physical_bound) / SQRT5).ceil()


def vectors(physical_bound, internal_bound):
    nx, ny = lattice_box(physical_bound, internal_bound)
    return {(x, y) for x in range(-nx, nx + 1) for y in range(-ny, ny + 1)
            if abs(E((x, y))) <= physical_bound and abs(C((x, y))) <= internal_bound}


def potential_states(bound=INITIAL_BOUND):
    return {(i, j, v) for v in vectors(T, bound) for i in LENGTH for j in LENGTH
            if overlap(i, j, v)}


def successors(state):
    i, j, d = state
    md = M(d)
    return {(ip, jp, nd) for ip, p in CHILD[i] for jp, q in CHILD[j]
            if overlap(ip, jp, nd := (md[0] + q[0] - p[0], md[1] + q[1] - p[1]))}


def graph(states):
    """Fail closed: never silently discard an overlapping descendant."""
    adj = {state: successors(state) for state in states}
    escaped = set().union(*adj.values()) - states if adj else set()
    if escaped:
        raise ValueError(f'Nonclosed state universe: {sorted(escaped)}')
    return adj


def coincidence_distances(adj):
    from collections import defaultdict, deque
    back = defaultdict(set)
    for source, targets in adj.items():
        for target in targets:
            back[target].add(source)
    distance = {s: 0 for s in adj if s[0] == s[1] and s[2] == (0, 0)}
    queue = deque(sorted(distance))
    while queue:
        target = queue.popleft()
        for source in sorted(back[target]):
            if source not in distance:
                distance[source] = distance[target] + 1
                queue.append(source)
    return distance
