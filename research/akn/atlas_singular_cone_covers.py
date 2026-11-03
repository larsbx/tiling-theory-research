"""Enumerate boundary selections whose physical tangent cones tile space."""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path

from atlas_perturbation_limits import digest
from atlas_region_count import candidate_cells, input_basis
from geometry import PAR, act, cross, dot, ih_group, scale


def physical_chambers(normals):
    """Exact sign vectors using the first nonzero coefficient along a flag."""
    signs = set()
    earlier_lines = [set() for _ in normals]
    for i, j in combinations(range(len(normals)), 2):
        a, b = normals[i], normals[j]
        ray = cross(a, b)
        along = tuple(dot(n, ray).sign() for n in normals)
        if not any(along):
            continue
        earlier_lines[j].add(tuple(f for f, sign in enumerate(along) if not sign))
        for index, plane in enumerate(normals):
            if along[index]:
                continue
            tangent = cross(plane, ray)
            across = tuple(dot(n, tangent).sign() for n in normals)
            normal = tuple(dot(n, plane).sign() for n in normals)
            for r, t, s in product((-1, 1), repeat=3):
                key = tuple(r*x or t*y or s*z
                            for x, y, z in zip(along, across, normal))
                if 0 in key:
                    raise ValueError("non-generic physical chamber flag")
                signs.add(key)
    # Inserting a central plane cut by k distinct lines adds 2k chambers.
    if len(signs) != 2+2*sum(map(len, earlier_lines)):
        raise ValueError("physical chamber flags disagree with arrangement count")
    return sorted(signs)


def cone_masks(catalog):
    pairs = tuple(combinations(range(6), 2))
    normals = tuple(cross(PAR[i], PAR[j]) for i, j in pairs)
    chambers = physical_chambers(normals)
    masks = {}
    for cell, _ in catalog:
        requirements = []
        for u, v in combinations(cell, 2):
            w, = set(cell)-{u, v}
            f = pairs.index(tuple(sorted((abs(u)-1, abs(v)-1))))
            required = dot(normals[f], scale(1 if w > 0 else -1,
                                             PAR[abs(w)-1])).sign()
            if not required:
                raise ValueError("degenerate physical cone")
            requirements.append((f, required))
        masks[cell] = sum(1 << i for i, key in enumerate(chambers)
                          if all(key[f] == sign for f, sign in requirements))
        if not masks[cell]:
            raise ValueError("cone has no witnessed interior")
    return chambers, masks


def covers(forced, optional, masks, full):
    """Choose a cell covering the least-supported uncovered chamber."""
    remaining = full
    for cell in forced:
        mask = masks[cell]
        if mask & remaining != mask:
            return set()
        remaining ^= mask

    def search(uncovered, candidates):
        if not uncovered:
            yield frozenset()
            return
        available = [(cell, masks[cell]) for cell in candidates
                     if masks[cell] & uncovered == masks[cell]]
        possible = 0
        for _, mask in available:
            possible |= mask
        if possible != uncovered:
            return
        pivot = uncovered
        choices = available
        while pivot:
            bit = pivot & -pivot
            covering = [(cell, mask) for cell, mask in available if mask & bit]
            if len(covering) < len(choices):
                choices = covering
                if len(choices) == 1:
                    break
            pivot ^= bit
        for cell, mask in choices:
            for rest in search(uncovered ^ mask, [c for c, _ in available if c != cell]):
                yield rest | {cell}

    return {frozenset(forced) | choice for choice in search(remaining, optional)}


def classify(generic, singular, limits):
    ns, levels, _, _ = input_basis()
    catalog = candidate_cells(ns, levels)
    physical, masks = cone_masks(catalog)
    full = (1 << len(physical))-1
    generic_stars = []
    for leaf in generic["leaves"]:
        prefix = leaf["prefix"]
        generic_stars.append(frozenset(cell for cell, tests in catalog
                                       if all(lo <= prefix[f] < hi
                                              for f, lo, hi in tests)))
    all_covers = [covers(tuple(map(tuple, forced)), tuple(map(tuple, optional)),
                         masks, full) for forced, optional in singular["memberships"]]
    counts = Counter()
    examples = {}
    orbit_cache = {}
    group = ih_group()
    atlas = json.loads(Path(__file__).with_name("atlas.json").read_text())
    known = {tuple(map(tuple, row["star"])) for row in atlas["classes"]}
    extra_orbits = set()
    outside_examples = {}

    def orbit(star):
        if star not in orbit_cache:
            images = {tuple(sorted(tuple(sorted(act(g, axis) for axis in cell))
                                   for cell in star)) for g in group}
            representative = min(images)
            orbit_cache.update((frozenset(image), representative) for image in images)
        return orbit_cache[star]
    for row, incidence in zip(singular["strata"], limits["strata"], strict=True):
        if row["key"] != incidence["key"]:
            raise ValueError("translation incidence keys disagree")
        translated = {generic_stars[i] for i in incidence["chamber_indices"]}
        physical_covers = all_covers[row["membership"]]
        if not translated or not translated <= physical_covers:
            raise ValueError("a generic limit failed the physical cover test")
        extra = physical_covers-translated
        counts["strata"] += 1
        counts["local_covers"] += len(physical_covers)
        counts["translation_covers"] += len(translated)
        counts["strata_with_extra_covers"] += bool(extra)
        counts["extra_covers"] += len(extra)
        outside = 0
        for star in sorted(extra, key=lambda cells: tuple(sorted(cells))):
            representative = orbit(star)
            extra_orbits.add(representative)
            if representative not in known:
                outside += 1
                outside_examples.setdefault(representative, {
                    "stratum": row, "star": sorted(star),
                    "canonical_star": representative,
                    "translation_chamber_indices": incidence["chamber_indices"],
                })
        counts["extra_covers_outside_generic_orbits"] += outside
        counts["strata_with_outside_orbits"] += bool(outside)
        if extra:
            choices = sorted(tuple(sorted(star)) for star in extra)
            examples.setdefault(row["membership"], {
                "stratum": row, "extra_stars": choices,
                "translation_chamber_indices": incidence["chamber_indices"],
            })
    return {"physical_direction_chambers": len(physical),
            "membership_patterns": len(all_covers), "counts": counts,
            "extra_orbits": len(extra_orbits),
            "extra_orbits_outside_generic_atlas": len(outside_examples),
            "outside_orbit_witnesses": [outside_examples[key]
                                        for key in sorted(outside_examples)],
            "examples_by_membership": examples}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("generic", "singular", "limits", "out"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    limits = json.loads(args.limits.read_text())
    for path, field in ((args.generic, "generic_packet_sha256"),
                        (args.singular, "singular_packet_sha256")):
        if digest(path) != limits[field]:
            raise ValueError(f"translation input digest mismatch: {path.name}")
    result = classify(json.loads(args.generic.read_text()),
                      json.loads(args.singular.read_text()), limits)
    result["translation_packet_sha256"] = digest(args.limits)
    args.out.write_text(json.dumps(result, sort_keys=True, separators=(",", ":"))+"\n")
    print(json.dumps(result["counts"], sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
