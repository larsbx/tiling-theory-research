"""Independent exact replay of bounded AKN singular-plane probe packet.

Uses the separate Q[tau] arithmetic and 160 cell-threshold equations from
atlas_region_count, not the geometry selector used by the probe generator.
Verifies every one of 105 target planes is present and every reported cell
has correct strict/closed window status. It explicitly DOES NOT certify
all 2D/1D/0D strata or choose a singular tiling convention.
"""
from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

from atlas_region_count import (candidate_cells, dot, input_basis,
                                witness_in_tau)


def verify(packet):
    normals, levels, widths, digest = input_basis()
    assert packet["format"] == "AKN-SINGULAR-PLANE-PROBES-1"
    assert packet["input_plane_fixture_sha256"] == digest
    assert packet["boundary_convention_selected"] is False
    assert packet["all_singular_memberships_classified"] is False
    assert packet["scope"] == "one exact interior witness per interior plane; NOT all strata"
    targets = [(f, i) for f in range(15) for i in range(1, 8)]
    assert packet["candidate_plane_count"] == len(targets) == 105
    rows = packet["probes"]
    assert len(rows) == 105
    assert [tuple(row["target_plane"]) for row in rows] == targets
    cells = candidate_cells(normals, levels)

    ambiguous_points = 0
    multi_plane = 0
    boundary_incident_cells = 0
    for (family, index), row in zip(targets, rows):
        y = witness_in_tau(row["witness_y"])
        distances = [dot(n, y) for n in normals]
        assert all(-w < d < w for d, w in zip(distances, widths)), (
            "singular probe is not strictly inside vertex window"
        )
        assert distances[family] == levels[family][index]
        active = [[f, j] for f, d in enumerate(distances)
                  for j in range(1, 8) if d == levels[f][j]]
        assert active == row["active_internal_hyperplanes"]
        must = []
        may = []
        for signed, conditions in cells:
            strong = all(levels[f][lo] < distances[f] < levels[f][hi]
                         for f, lo, hi in conditions)
            weak = all(levels[f][lo] <= distances[f] <= levels[f][hi]
                       for f, lo, hi in conditions)
            assert not strong or weak
            if strong:
                must.append(signed)
            if weak:
                may.append(signed)
        must.sort()
        may.sort()
        assert row["forced_signed_cells"] == [list(s) for s in must]
        assert row["closed_possible_signed_cells"] == [list(s) for s in may]
        assert row["boundary_dependent_cell_count"] == len(may)-len(must)
        if len(may) != len(must):
            ambiguous_points += 1
        if len(active) > 1:
            multi_plane += 1
        boundary_incident_cells += len(may)-len(must)

    return {
        "exact_interior_plane_probes_verified": len(rows),
        "independent_cell_thresholds_verified": len(rows)*160,
        "probes_with_open_closed_cell_ambiguity": ambiguous_points,
        "probes_on_multiple_internal_planes": multi_plane,
        "total_probe_boundary_cell_occurrences": boundary_incident_cells,
        "all_singular_strata_covered": False,
        "boundary_convention_decided": False,
        "next_obligation": (
            "Enumerate exact lower-dimensional strata and specify a "
            "consistent singular-boundary cell-selection convention."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = verify(json.loads(args.packet.read_text()))
    text = json.dumps(report, sort_keys=True, indent=2)+"\n"
    if args.out:
        args.out.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
