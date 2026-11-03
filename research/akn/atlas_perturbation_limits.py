"""Classify common-translation limits at every certified singular stratum."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import file_digest
import json
from pathlib import Path

from atlas_region_count import candidate_cells, input_basis


def digest(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def read_checked(path, expected):
    if digest(path) != expected:
        raise ValueError(f"evidence digest mismatch: {path.name}")
    return json.loads(path.read_text())


def closure_codes(slab):
    return 2*slab, 2*slab+1, 2*slab+2


def chamber_trie(prefixes):
    root = {}
    for index, prefix in enumerate(prefixes):
        node = root
        for slab in prefix:
            node = node.setdefault(slab, {})
        if node:
            raise ValueError("duplicate generic chamber")
        node[None] = index
    return root


def neighbors(node, key, depth=0):
    if depth == len(key):
        yield node[None]
        return
    code = key[depth]
    lower = (code-1)//2
    upper = code//2
    for slab in range(lower, upper+1):
        if slab in node:
            yield from neighbors(node[slab], key, depth+1)


def classify(generic, singular, catalog):
    prefixes = [tuple(leaf["prefix"]) for leaf in generic["leaves"]]
    trie = chamber_trie(prefixes)

    # Independently replay adjacency by intersecting inverted closure postings.
    postings = defaultdict(int)
    stars = []
    for index, prefix in enumerate(prefixes):
        for f, slab in enumerate(prefix):
            for code in closure_codes(slab):
                postings[f, code] |= 1 << index
        stars.append(frozenset(cell for cell, conditions in catalog
                               if all(lo <= prefix[f] < hi
                                      for f, lo, hi in conditions)))

    memberships = [(frozenset(map(tuple, forced)), frozenset(map(tuple, optional)))
                   for forced, optional in singular["memberships"]]
    counts = defaultdict(Counter)
    output = []
    for row in singular["strata"]:
        key = row["key"]
        matches = list(neighbors(trie, key))
        replay = (1 << len(prefixes))-1
        for f, code in enumerate(key):
            replay &= postings[f, code]
        if not matches or sum(1 << i for i in matches) != replay:
            raise ValueError("incomplete or inconsistent chamber incidence")
        forced, optional = memberships[row["membership"]]
        closed = forced | optional
        choices = {stars[i] for i in matches}
        if any(not forced <= star <= closed for star in choices):
            raise ValueError("adjacent chamber contradicts singular membership")
        boundary = 0 in key or 16 in key
        # At a supporting face the strict rule excludes the central vertex.
        strict = not boundary and forced in choices
        closed_limit = closed in choices
        group = counts[f'{row["dimension"]}/{"boundary" if boundary else "interior"}']
        group["strata"] += 1
        group["strict_limit"] += strict
        group["closed_limit"] += closed_limit
        group["both_limits"] += strict and closed_limit
        group["boundary_dependent_strata"] += bool(optional)
        group["strict_limit_with_boundary_dependent_cells"] += strict and bool(optional)
        group["closed_limit_with_boundary_dependent_cells"] += closed_limit and bool(optional)
        group["chamber_incidences"] += len(matches)
        group["max_distinct_stars"] = max(group["max_distinct_stars"], len(choices))
        output.append({
            "key": key, "chamber_indices": matches,
            "distinct_stars": len(choices),
            "strict_limit": strict, "closed_limit": closed_limit,
        })
    return {"counts": counts, "strata": output}


def run(generic_dir, singular_dir):
    generic_run = json.loads((generic_dir/"research-run.json").read_text())
    singular_run = json.loads((singular_dir/"singular-run.json").read_text())
    if (generic_run["state"] != "generic_candidate_verified" or
            singular_run["state"] != "verified_finite_singular_atlas"):
        raise ValueError("both independently verified complete atlases are required")
    g_hash = generic_run["evidence"]["packet_sha256"]
    s_hash = singular_run["packet_sha256"]
    generic = read_checked(generic_dir/"chambers.json", g_hash)
    singular = read_checked(singular_dir/"singular-strata.json", s_hash)
    generic_replay = read_checked(
        generic_dir/"independent-replay.json",
        generic_run["evidence"]["independent_replay_sha256"])
    singular_replay = read_checked(
        singular_dir/"singular-replay.json", singular_run["replay_sha256"])
    ns, levels, _, basis = input_basis()
    if (generic["plane_fixture_sha256"] != basis or singular["basis_sha256"] != basis or
            generic_replay["coverage_verified_generic"] is not True or
            singular_replay["all_singular_strata_covered"] is not True):
        raise ValueError("atlas verification or plane basis mismatch")
    return {
        "scope": "centered stars from one common translation into generic chambers",
        "generic_packet_sha256": g_hash,
        "singular_packet_sha256": s_hash,
        **classify(generic, singular, candidate_cells(ns, levels)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generic", type=Path, required=True)
    parser.add_argument("--singular", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.generic, args.singular)
    with args.out.open("w") as stream:
        json.dump(result, stream, sort_keys=True, separators=(",", ":"))
        stream.write("\n")
    print(json.dumps(result["counts"], sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
