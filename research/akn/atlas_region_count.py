"""Independent exact count of ALL generic AKN 135-plane window chambers.

This checker does not import the chamber enumerator or use its clipping,
witness-generation, or region-coverage conclusions. It independently
derives the 160 candidate cell thresholds, then uses the incremental
hyperplane-arrangement formula:

    regions_3D = 1 + sum_{H} regions_2D(H intersect open window),

where, for the distinct lines cut on a convex planar slice,

    regions_2D = 1 + number_of_intersecting_lines
                   + sum_{interior_concurrency_points p}(multiplicity(p)-1).

All counts, line deduplication, intersections, and window tests use
rational arithmetic in Q(tau). Coincident lines and concurrent triples
are handled exactly. The 30 window supporting planes do NOT divide
the open window; only the 105 interior planes are inserted.

A full witness packet is exhaustive if and only if its distinct strict
sign vectors number the independently counted regions. Star assignments
and stabilizer-subgroup conjugacy classes are independently replayed.

This is a finite generic-configuration certificate only; faces and
singular boundary selection conventions are entirely separate.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from geometry import A, B

HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class K:
    """Ordered exact field Q[tau] with tau**2=tau+1."""
    a: Fraction
    b: Fraction = Fraction(0)

    def __post_init__(self):
        object.__setattr__(self, "a", Fraction(self.a))
        object.__setattr__(self, "b", Fraction(self.b))

    @staticmethod
    def of(x):
        return x if isinstance(x, K) else K(Fraction(x))

    def __add__(self, other):
        z = K.of(other)
        return K(self.a+z.a, self.b+z.b)
    __radd__ = __add__

    def __neg__(self):
        return K(-self.a, -self.b)

    def __sub__(self, other):
        return self+-K.of(other)

    def __rsub__(self, other):
        return K.of(other)+-self

    def __mul__(self, other):
        z = K.of(other)
        return K(self.a*z.a+self.b*z.b,
                 self.a*z.b+self.b*z.a+self.b*z.b)
    __rmul__ = __mul__

    def __truediv__(self, other):
        z = K.of(other)
        norm = z.a*z.a+z.a*z.b-z.b*z.b
        if not norm:
            raise ZeroDivisionError("zero norm in Q(tau)")
        return self*K((z.a+z.b)/norm, -z.b/norm)

    def sign(self):
        """Sign of 2(a+b*tau)=(2a+b)+b*sqrt5, no approximations."""
        x, y = 2*self.a+self.b, self.b
        if x == 0:
            return (y > 0)-(y < 0)
        if y == 0 or (x > 0) == (y > 0):
            return (x > 0)-(x < 0)
        delta = x*x-5*y*y
        assert delta != 0
        return ((x > 0)-(x < 0))*((delta > 0)-(delta < 0))

    def __lt__(self, other):
        return (self-K.of(other)).sign() < 0

    def __le__(self, other):
        return (self-K.of(other)).sign() <= 0


Z = K(0)
ONE = K(1)
W = tuple(tuple(K(a+b, -b) for a, b in zip(x, y))
          for x, y in zip(A, B))
PAR = tuple(tuple(K(a, b) for a, b in zip(x, y))
            for x, y in zip(A, B))
PAIRS = tuple(combinations(range(6), 2))


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), Z)


def cross(u, v):
    return (u[1]*v[2]-u[2]*v[1],
            u[2]*v[0]-u[0]*v[2],
            u[0]*v[1]-u[1]*v[0])


def magnitude(x):
    return -x if x.sign() < 0 else x


def normals():
    return tuple(cross(W[i], W[j]) for i, j in PAIRS)


def input_basis():
    """Reconstruct all candidate transition levels without atlas_arrangement."""
    fixture = json.loads((HERE/"atlas_hyperplanes.json").read_text())
    assert fixture["tau_relation"] == "tau^2=tau+1"
    assert fixture["perp_slope"] == "tau'=1-tau"
    assert len(fixture["families"]) == 15
    ns = normals()
    all_levels = []
    widths = []
    for f, ((i, j), n) in enumerate(zip(PAIRS, ns)):
        width = sum((magnitude(dot(g, n)) for g in W), Z)
        calculated = {-width, width}
        for axes in combinations(range(6), 3):
            if i in axes or j in axes:
                continue
            rest = [k for k in range(6) if k not in axes]
            cell_width = sum((magnitude(dot(W[k], n)) for k in rest), Z)
            for signs in product((-1, 1), repeat=3):
                center = tuple(sum((s*W[axis][d] for s, axis in
                                    zip(signs, axes)), Z) for d in range(3))
                shift = dot(center, n)
                calculated.update((shift-cell_width, shift+cell_width))
        expected = sorted(calculated)
        saved = [K(*pair) for pair in fixture["families"][f]["levels"]]
        assert fixture["families"][f]["axis_pair"] == [i, j]
        assert len(expected) == len(saved) == 9 and expected == saved
        assert saved[0] == -width and saved[-1] == width
        assert all(saved[k] < saved[k+1] for k in range(8))
        widths.append(width)
        all_levels.append(tuple(saved))
    digest = sha256(json.dumps(fixture, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    return ns, tuple(all_levels), tuple(widths), digest


def section_basis(normal, level):
    pivot = next(k for k, x in enumerate(normal) if x.sign())
    other = [k for k in range(3) if k != pivot]
    p, u, v = [Z]*3, [Z]*3, [Z]*3
    p[pivot] = level/normal[pivot]
    u[pivot] = -normal[other[0]]/normal[pivot]
    u[other[0]] = ONE
    v[pivot] = -normal[other[1]]/normal[pivot]
    v[other[1]] = ONE
    return tuple(p), tuple(u), tuple(v)


def line_in_section(section, other, ns):
    fi, li = section
    fj, lj = other
    p, u, v = section_basis(ns[fi], li)
    a, b, c = dot(ns[fj], u), dot(ns[fj], v), lj-dot(ns[fj], p)
    if a == Z and b == Z:
        assert c != Z, "duplicate planes in 135-plane input"
        return None  # parallel 3D planes: no intersection line
    factor = a if a != Z else b
    return a/factor, b/factor, c/factor


def section_window(section, ns):
    p, u, v = section_basis(ns[section[0]], section[1])
    return tuple((dot(n, u), dot(n, v), dot(n, p)) for n in ns)


def line_crosses_open_window(line, window, widths):
    a, b, c = line
    if b != Z:
        s0, t0, ds, dt = Z, c/b, ONE, -a/b
    else:
        s0, t0, ds, dt = c/a, Z, Z, ONE
    lower = upper = None
    for (a0, b0, c0), width in zip(window, widths):
        origin = a0*s0+b0*t0+c0
        slope = a0*ds+b0*dt
        if slope == Z:
            if not -width < origin < width:
                return False
        else:
            lo, hi = (-width-origin)/slope, (width-origin)/slope
            if hi < lo:
                lo, hi = hi, lo
            if lower is None or lower < lo:
                lower = lo
            if upper is None or hi < upper:
                upper = hi
            if not lower < upper:
                return False
    return True


def interior(s, t, window, widths):
    return all(-width < a*s+b*t+c < width
               for (a, b, c), width in zip(window, widths))


def slice_region_count(at, planes, ns, widths):
    current = planes[at]
    window = section_window(current, ns)
    lines = {}
    for j in range(at):
        line = line_in_section(current, planes[j], ns)
        if line is not None and line not in lines and (
                line_crosses_open_window(line, window, widths)):
            lines[line] = len(lines)
    unique = list(lines)
    points = defaultdict(set)
    for i, (a, b, c) in enumerate(unique):
        for j in range(i+1, len(unique)):
            d, e, f = unique[j]
            delta = a*e-b*d
            if delta == Z:
                continue  # distinct parallel lines
            s, t = (c*e-b*f)/delta, (a*f-c*d)/delta
            if interior(s, t, window, widths):
                points[(s, t)].update((i, j))
    return 1+len(unique)+sum(len(hits)-1 for hits in points.values())


def count_regions(ns, levels, widths):
    """Zaslavsky-style incremental count, restricted to the OPEN window."""
    active = [(f, cuts[k]) for f, cuts in enumerate(levels) for k in range(1, 8)]
    assert len(active) == 105
    assert all(-widths[f] < lev < widths[f] for f, lev in active)
    by_slice = [slice_region_count(i, active, ns, widths)
                for i in range(len(active))]
    return 1+sum(by_slice), by_slice


def candidate_cells(ns, levels):
    index = {pair: f for f, pair in enumerate(PAIRS)}
    cells = []
    for axes in combinations(range(6), 3):
        rest = [j for j in range(6) if j not in axes]
        for signs in product((1, -1), repeat=3):
            center = tuple(sum((s*W[axis][d] for s, axis in zip(signs, axes)), Z)
                           for d in range(3))
            conditions = []
            for pair in combinations(rest, 2):
                f = index[pair]
                width = sum((magnitude(dot(W[j], ns[f])) for j in rest), Z)
                shift = dot(ns[f], center)
                lo, hi = shift-width, shift+width
                assert lo in levels[f] and hi in levels[f]
                conditions.append((f, levels[f].index(lo), levels[f].index(hi)))
            signed = tuple(sorted(s*(axis+1) for s, axis in zip(signs, axes)))
            cells.append((signed, tuple(conditions)))
    assert len(cells) == 160
    return cells


def point_group():
    gram = tuple(tuple(dot(u, v) for v in PAR) for u in PAR)
    group = []
    for perm in permutations(range(6)):
        for signs in product((1, -1), repeat=6):
            if all(signs[i]*signs[j]*gram[perm[i]][perm[j]] == gram[i][j]
                   for i in range(6) for j in range(i+1, 6)):
                group.append(tuple(s*(p+1) for s, p in zip(signs, perm)))
    assert len(group) == 120
    return tuple(group)


def act(g, value):
    return (1 if value > 0 else -1)*g[abs(value)-1]


def canonical(star, group):
    return min(tuple(sorted(tuple(sorted(act(g, s) for s in cell))
                            for cell in star)) for g in group)


def compose(g, h):
    return tuple((1 if x > 0 else -1)*g[abs(x)-1] for x in h)


def inverse(g):
    output = [0]*6
    for i, x in enumerate(g):
        output[abs(x)-1] = (1 if x > 0 else -1)*(i+1)
    return tuple(output)


def subgroup_conjugacy(star, group):
    raw = frozenset(frozenset(cell) for cell in star)
    stab = [g for g in group if frozenset(
        frozenset(act(g, s) for s in cell) for cell in raw) == raw]
    index = {g: i for i, g in enumerate(group)}
    sig = min(tuple(sorted(index[compose(compose(g, h), inverse(g))]
                           for h in stab)) for g in group)
    return len(stab), sha256(json.dumps(sig, separators=(",", ":")).encode()).hexdigest()


def witness_in_tau(data):
    """Convert [a,b] for a+b*sqrt5 to Q(tau): (a-b)+2b*tau."""
    assert isinstance(data, list) and len(data) == 3
    out = []
    for pair in data:
        assert isinstance(pair, list) and len(pair) == 2
        assert all(isinstance(v, str) for v in pair)
        a, b = Fraction(pair[0]), Fraction(pair[1])
        out.append(K(a-b, 2*b))
    return tuple(out)


def verify_complete_packet(packet):
    """Full-coverage criterion by independent region count, NOT prefix FM."""
    ns, levels, widths, digest = input_basis()
    assert packet["format"] == "AKN-ATLAS-CHAMBERS-1"
    assert packet["plane_fixture_sha256"] == digest
    assert packet["scope"] == "open generic chambers only; singular boundaries excluded"
    assert packet["search_exhausted"] is True
    assert packet["frontier_count"] == 0
    assert packet["classified_count"] == len(packet["leaves"])
    n_regions, per_slice = count_regions(ns, levels, widths)
    leaves = packet["leaves"]
    assert len(leaves) == n_regions, "missing or extra open chambers"
    cells = candidate_cells(ns, levels)
    group = point_group()
    atlas = json.loads((HERE/"atlas.json").read_text())
    known = {tuple(map(tuple, row["star"])): i
             for i, row in enumerate(atlas["classes"])}
    assert len(known) == len(atlas["classes"]) == 24
    prior = None
    prefixes_by_depth = [set() for _ in range(15)]
    raw_cache = {}
    orbits = Counter()
    types = set()
    for leaf in leaves:
        prefix = leaf["prefix"]
        assert leaf["kind"] == "classified"
        assert isinstance(prefix, list) and len(prefix) == 15
        assert all(type(k) is int and 0 <= k < 8 for k in prefix)
        prefix = tuple(prefix)
        assert prior is None or prior < prefix, "duplicate or unordered chamber"
        prior = prefix
        for depth in range(15):
            prefixes_by_depth[depth].add(prefix[:depth])
        y = witness_in_tau(leaf["witness_y"])
        assert all(levels[f][k] < dot(ns[f], y) < levels[f][k+1]
                   for f, k in enumerate(prefix)), "invalid exact chamber witness"
        raw = tuple(cell for cell, requirements in cells
                    if all(low <= prefix[f] < high
                           for f, low, high in requirements))
        if raw not in raw_cache:
            key = canonical(raw, group)
            idx = known.get(key, -1)
            order, stabilizer = subgroup_conjugacy(raw, group)
            raw_cache[raw] = (idx, order, stabilizer, key)
        idx, order, stabilizer, key = raw_cache[raw]
        assert leaf["orbit_class"] == idx
        assert leaf["stabilizer_order"] == order
        assert leaf["stabilizer_conjugacy_sha256"] == stabilizer
        if idx < 0:
            assert leaf.get("counterexample_star") == [list(x) for x in key]
        else:
            assert "counterexample_star" not in leaf
        orbits[idx] += 1
        types.add(stabilizer)
    assert sum(map(len, prefixes_by_depth)) == packet["expanded_prefixes"]
    assert sorted(orbits) == packet["observed_orbit_class_ids"]
    return {
        "independently_counted_regions": n_regions,
        "exact_witnessed_distinct_chambers": len(leaves),
        "classified_orbits": dict(sorted(orbits.items())),
        "icosahedral_star_orbits": len(orbits),
        "stabilizer_subgroup_conjugacy_types": len(types),
        "concurrent_line_slices_counted": len(per_slice),
        "slice_region_counts_sha256": sha256(
            json.dumps(per_slice, separators=(",", ":")).encode()).hexdigest(),
        "coverage_verified_generic": True,
        "exactly_existing_24_orbits": set(orbits) == set(range(24)),
        "counterexample_to_24_orbits": -1 in orbits,
        "singular_boundary_membership_verified": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path,
                        help="check an exhaustive 15-family witness packet")
    args = parser.parse_args()
    if args.packet:
        record = verify_complete_packet(json.loads(args.packet.read_text()))
    else:
        ns, cuts, widths, basis_sha = input_basis()
        count, slices = count_regions(ns, cuts, widths)
        record = {"generic_open_chambers": count,
                  "basis_sha256": basis_sha,
                  "active_internal_hyperplanes": len(slices),
                  "slice_region_counts_sha256": sha256(
                      json.dumps(slices, separators=(",", ":")).encode()).hexdigest(),
                  "boundary_supporting_planes": 30,
                  "singular_boundary_membership_verified": False}
    print(json.dumps(record, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
