"""Independent replay checker for partial or exhaustive AKN chamber packets.

Does NOT import atlas_chambers or trust its clipping, claimed coverage,
classification, search-exhaustion flag, or conjugacy data. Uses exact strict
Fourier--Motzkin elimination on every missing/present prefix branch, an
independently implemented decision path from the enumerator's polytope split.
A complete packet with zero frontier leaves certifies OPEN chamber coverage
relative to the exact 135-plane basis; no singular-boundary conclusion follows.

Run: python research/akn/atlas_chamber_check.py /tmp/akn.json
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

from atlas_arrangement import arrangement
from geometry import (CutProject, PERP_TRUE, Q5, act, canonical_star,
                      dot, ih_group, sgn)
from radius2_exact import (FACETS, WINDOW_WIDTHS, Plane, check_obstruction,
                           eliminate, sign, zi, zn, zs)

HERE = Path(__file__).resolve().parent


def q(z):
    a, b = z
    return Q5(Fraction(2*a+b, 2), Fraction(b, 2))


def parse_witness(data):
    assert isinstance(data, list) and len(data) == 3
    assert all(isinstance(z, list) and len(z) == 2
               and all(isinstance(x, str) for x in z) for z in data)
    return tuple(Q5(Fraction(a), Fraction(b)) for a, b in data)


def source():
    """Cross-check registered fixture from the 160 possible signed cells."""
    fixture = json.loads((HERE/"atlas_hyperplanes.json").read_text())
    computed = arrangement()
    assert len(computed) == len(fixture["families"]) == 15
    normals = []
    levels = []
    for fam, generated in zip(fixture["families"], computed):
        pair = tuple(fam["axis_pair"])
        assert fam["levels"] == generated["levels_in_Z_tau_for_twice_normal_projection"]
        assert tuple(generated["axis_pair"]) == pair
        n = next(n for i, j, n in FACETS if (i, j) == pair)
        cuts = [tuple(x) for x in fam["levels"]]
        assert len(cuts) == 9 and all(sign(zs(b, a)) > 0
                                     for a, b in zip(cuts, cuts[1:]))
        assert cuts[0] == zn(WINDOW_WIDTHS[pair])
        assert cuts[-1] == WINDOW_WIDTHS[pair]
        normals.append(n)
        levels.append(cuts)
    digest = sha256(json.dumps(fixture, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    return normals, levels, digest


def strict_feasible(prefix, normals, levels):
    """Independent strict FM test of every proposed and omitted slab."""
    assert len(prefix) <= len(normals)
    halfspaces = []
    for j, (normal, cuts) in enumerate(zip(normals, levels)):
        if j < len(prefix):
            i = prefix[j]
            assert isinstance(i, int) and 0 <= i < 8
            lower, upper = cuts[i], cuts[i+1]
        else:
            lower, upper = cuts[0], cuts[-1]
        halfspaces.append(Plane(normal, upper, (j, "upper")))
        halfspaces.append(Plane(tuple(zn(v) for v in normal),
                                zn(lower), (j, "lower")))
    res = eliminate(halfspaces, strict=True)
    if not res.feasible:
        assert check_obstruction(res, halfspaces), "invalid FM contradiction"
    return res.feasible


def compose(g, h):
    return tuple((1 if v > 0 else -1)*g[abs(v)-1] for v in h)


def inverse(g):
    result = [0]*6
    for i, x in enumerate(g):
        result[abs(x)-1] = (1 if x > 0 else -1)*(i+1)
    return tuple(result)


def stabilizer_type(star, group):
    stab = [g for g in group if frozenset(
        frozenset(act(g, e) for e in cell) for cell in star) == star]
    idx = {g: i for i, g in enumerate(group)}
    minimum = min(tuple(sorted(idx[compose(compose(g, h), inverse(g))]
                               for h in stab)) for g in group)
    digest = sha256(json.dumps(minimum, separators=(",", ":")).encode()).hexdigest()
    return len(stab), digest


def verify_packet(packet):
    normals, levels, digest = source()
    assert packet["format"] == "AKN-ATLAS-CHAMBERS-1"
    assert packet["plane_fixture_sha256"] == digest
    assert packet["scope"] == "open generic chambers only; singular boundaries excluded"
    leaves = packet["leaves"]
    assert isinstance(leaves, list) and len(leaves) > 0
    assert leaves == sorted(leaves, key=lambda x: x["prefix"]), (
        "leaf order is not canonical"
    )
    group = ih_group()
    atlas = json.loads((HERE/"atlas.json").read_text())
    known = {tuple(map(tuple, entry["star"])): i
             for i, entry in enumerate(atlas["classes"])}
    assert len(known) == len(atlas["classes"]) == 24

    trie = {}
    classes = set()
    type_to_orbits = {}
    frontier = 0
    classified = 0
    for leaf in leaves:
        prefix = leaf["prefix"]
        assert isinstance(prefix, list) and len(prefix) <= 15
        assert all(type(n) is int and 0 <= n < 8 for n in prefix)
        assert leaf["kind"] in ("frontier", "classified")
        if leaf["kind"] == "classified":
            assert len(prefix) == 15, "classification requires all 15 families"
        else:
            assert len(prefix) < 15, "full sign vector cannot be frontier"
        point = parse_witness(leaf["witness_y"])
        # Exact, strict witness in every selected slab and in every
        # remaining vertex-window direction.
        for j, (n, cuts) in enumerate(zip(normals, levels)):
            lo, hi = ((cuts[prefix[j]], cuts[prefix[j]+1])
                      if j < len(prefix) else (cuts[0], cuts[-1]))
            height = dot(tuple(q(z) for z in n), point)
            assert sgn(height-q(lo)) > 0 and sgn(q(hi)-height) > 0, (
                "invalid open interior witness", prefix, j
            )

        if leaf["kind"] == "frontier":
            frontier += 1
        else:
            classified += 1
            cp = CutProject(PERP_TRUE, tuple(y/2 for y in point))
            star = cp.star((0,)*6)
            key = canonical_star(star, group)
            expected = known.get(key, -1)
            assert leaf["orbit_class"] == expected
            order, type_digest = stabilizer_type(star, group)
            assert leaf["stabilizer_order"] == order
            assert leaf["stabilizer_conjugacy_sha256"] == type_digest
            if expected == -1:
                assert leaf.get("counterexample_star") == [list(c) for c in key]
            else:
                assert "counterexample_star" not in leaf
            classes.add(expected)
            type_to_orbits.setdefault(type_digest, set()).add(expected)

        node = trie
        for part in prefix:
            assert "_leaf" not in node, "prefix overlap"
            node = node.setdefault(part, {})
        assert "_leaf" not in node and not node, "duplicate or prefix overlap"
        node["_leaf"] = leaf["kind"]

    assert frontier == packet["frontier_count"]
    assert classified == packet["classified_count"]
    assert (frontier == 0) == packet["search_exhausted"]
    assert sorted(classes) == packet["observed_orbit_class_ids"]

    # This is the coverage proof: an independent exact FM solver verifies
    # the trie contains EVERY nonempty open slab of each visited prefix.
    # No omitted feasible child is allowed. A frontier node is explicitly
    # an unresolved finite subtree, never a negative result.
    verified_internal_nodes = 0
    def verify_node(node, prefix):
        nonlocal verified_internal_nodes
        assert strict_feasible(prefix, normals, levels)
        if "_leaf" in node:
            assert len(node) == 1
            return
        assert len(prefix) < 15
        verified_internal_nodes += 1
        for k in range(8):
            feasible = strict_feasible(prefix+(k,), normals, levels)
            assert (k in node) == feasible, (
                "missing or invented open subchamber", prefix, k
            )
            if feasible:
                verify_node(node[k], prefix+(k,))
        assert all(type(k) is int and 0 <= k < 8 for k in node)

    verify_node(trie, ())
    assert packet["expanded_prefixes"] == verified_internal_nodes
    return {
        "verified_partition_prefixes": verified_internal_nodes,
        "verified_leaves": len(leaves),
        "classified_chambers": classified,
        "unresolved_frontier": frontier,
        "observed_icosahedral_orbits": sorted(classes),
        "stabilizer_conjugacy_types": len(type_to_orbits),
        "complete_generic_coverage": frontier == 0,
        "exactly_24_known_orbits": frontier == 0 and classes == set(range(24)),
        "counterexample_found": -1 in classes,
        "singular_boundaries_verified": False,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("packet", type=Path)
    args = p.parse_args()
    record = json.loads(args.packet.read_text())
    print(json.dumps(verify_packet(record), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
