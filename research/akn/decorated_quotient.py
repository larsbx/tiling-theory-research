"""Finite *counterexample* search for candidate oriented facet decorations.

A concrete periodic decorated witness refutes PERFECT matching for the
supplied D, because the committed underlying 3/2 tiling is periodic.

This is NOT a transcription of Katz's facet rule: the demo grammar is
purposefully a bare/plain-label negative control. Exhausted UNSAT over
one periodic quotient does NOT prove perfection or exclude aperiodic
decorations of the underlying periodic tiling.

Exactly reproduce face gluings from the 6D certificate, including period
boundary crossings, and check ordered +normal/-normal face-label pairs.
No NumPy / SAT dependency. Search budgets return INCONCLUSIVE, never UNSAT.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from geometry import A, B, PAR, cell_shape, det, sgn


def quotient(n: tuple[int, ...]) -> tuple[int, int, int]:
    if len(n) != 6:
        raise ValueError("expected 6D lift")
    return tuple(sum(n[i] * (3*A[i][j] - 2*B[i][j]) for i in range(6))
                 for j in range(3))  # type: ignore[return-value]


@dataclass(frozen=True)
class Face:
    cell: int
    position: int         # sorted tile-axis index, 0,1,2
    side: int             # 0=low, 1=high
    orientation: int      # +1 or -1 for canonical oriented face


@dataclass(frozen=True)
class Glue:
    positive: Face
    negative: Face


def glue_graph(certificate: dict) -> list[Glue]:
    """Construct every 2-face incidence; reject incomplete/misoriented cells."""
    cells = certificate["cells"]
    by_face: dict[tuple, list[Face]] = defaultdict(list)
    unique_cells = set()
    for cid, (base, axes) in enumerate(cells):
        if len(base) != 6 or len(axes) != 3 or sorted(set(axes)) != axes:
            raise ValueError("cell axes must be three distinct sorted 0-based indices")
        I = tuple(axes)
        kcell = (quotient(tuple(base)), I)
        if kcell in unique_cells:
            raise ValueError("duplicate quotient cell")
        unique_cells.add(kcell)
        for position, axis in enumerate(I):
            J = tuple(i for i in I if i != axis)
            o = sgn(det(PAR[J[0]], PAR[J[1]], PAR[axis]))
            if o not in (-1, 1):
                raise ValueError("degenerate face orientation")
            for side in (0, 1):
                corner = tuple(int(v + (side if j == axis else 0))
                               for j, v in enumerate(base))
                f = Face(cid, position, side, o if side == 0 else -o)
                by_face[(quotient(corner), J)].append(f)
    pairs = []
    for occurrences in by_face.values():
        if len(occurrences) != 2:
            raise ValueError("not exactly two cells incident to face")
        plus = [f for f in occurrences if f.orientation == 1]
        minus = [f for f in occurrences if f.orientation == -1]
        if len(plus) != 1 or len(minus) != 1:
            raise ValueError("face glue not oppositely oriented")
        pairs.append(Glue(plus[0], minus[0]))
    if len(pairs) != 3 * len(cells):
        raise ValueError("face incidence count mismatch")
    return sorted(pairs, key=lambda g: (
        g.positive.cell, g.positive.position, g.positive.side,
        g.negative.cell, g.negative.position, g.negative.side))


def _parse_grammar(grammar: dict) -> tuple[dict, frozenset[tuple[str, str]]]:
    """Each variant is an EXPLICIT oriented tile state.

    faces[j][s] is the face label on axis-position j, side s.
    allowed_pairs contains ordered (positive normal, negative normal)
    labels. allowed_axes if supplied restricts the three physical axes
    to explicitly listed orientations; otherwise all axes of the shape.
    """
    variants = {}
    for entry in grammar["variants"]:
        ident = entry["id"]
        shape = entry["shape"]
        faces = entry["faces"]
        if not isinstance(ident, str) or not ident or ident in variants:
            raise ValueError("duplicate or invalid variant identifier")
        if shape not in ("P", "O") or len(faces) != 3 or any(
            not isinstance(pair, list) or len(pair) != 2 or
            not all(isinstance(s, str) for s in pair) for pair in faces
        ):
            raise ValueError("invalid variant shape or six oriented face labels")
        allowed_axes = entry.get("allowed_axes")
        if allowed_axes is not None and any(
            len(I) != 3 or sorted(set(I)) != I for I in allowed_axes
        ):
            raise ValueError("invalid allowed_axes")
        variants[ident] = {
            "shape": shape,
            "faces": faces,
            "axes": None if allowed_axes is None else {
                tuple(I) for I in allowed_axes
            },
        }
    if not variants:
        raise ValueError("at least one tile variant required")
    allowed_pairs = set()
    for pair in grammar["allowed_pairs"]:
        if not isinstance(pair, list) or len(pair) != 2 or not all(
            isinstance(s, str) for s in pair
        ):
            raise ValueError("ordered face pair must be two strings")
        allowed_pairs.add(tuple(pair))
    return variants, frozenset(allowed_pairs)


def _domains(certificate: dict, variants: dict) -> list[set[str]]:
    out = []
    for _base, axes in certificate["cells"]:
        shape = cell_shape(tuple(i + 1 for i in axes))
        I = tuple(axes)
        out.append({ident for ident, record in variants.items()
                    if record["shape"] == shape and
                    (record["axes"] is None or I in record["axes"])})
    return out


def _compatible(p: str, m: str, glue: Glue,
                variants: dict, pairs: frozenset) -> bool:
    fplus = glue.positive
    fminus = glue.negative
    left = variants[p]["faces"][fplus.position][fplus.side]
    right = variants[m]["faces"][fminus.position][fminus.side]
    return (left, right) in pairs


def _propagate(domains: list[set[str]], edges: list[Glue], variants: dict,
               allowed: frozenset) -> bool:
    """Arc consistency: never infer UNSAT from a search cap."""
    if any(not d for d in domains):
        return False
    changed = True
    while changed:
        changed = False
        for edge in edges:
            p, m = edge.positive.cell, edge.negative.cell
            dp, dm = domains[p], domains[m]
            if p == m:
                keep = {v for v in dp if _compatible(v, v, edge,
                                                      variants, allowed)}
                if not keep:
                    return False
                if keep != dp:
                    domains[p] = keep
                    changed = True
                continue
            pairs = [(x, y) for x in dp for y in dm
                     if _compatible(x, y, edge, variants, allowed)]
            if not pairs:
                return False
            newp = {x for x, _ in pairs}
            newm = {y for _, y in pairs}
            if dp != newp:
                domains[p] = newp
                changed = True
            if dm != newm:
                domains[m] = newm
                changed = True
    return True


def verify_assignment(certificate: dict, grammar: dict,
                      assignment: list[str]) -> bool:
    """Independent certificate checker: no solver state or pruning reused."""
    variants, allowed = _parse_grammar(grammar)
    if len(assignment) != len(certificate["cells"]):
        return False
    for (base, axes), label in zip(certificate["cells"], assignment):
        if label not in variants:
            return False
        variant = variants[label]
        if variant["shape"] != cell_shape(tuple(i + 1 for i in axes)):
            return False
        if variant["axes"] is not None and tuple(axes) not in variant["axes"]:
            return False
    for edge in glue_graph(certificate):
        p, m = edge.positive, edge.negative
        plus = variants[assignment[p.cell]]["faces"][p.position][p.side]
        minus = variants[assignment[m.cell]]["faces"][m.position][m.side]
        if (plus, minus) not in allowed:
            return False
    return True


def solve(certificate: dict, grammar: dict,
          max_nodes: int = 10000) -> dict:
    if max_nodes < 1:
        raise ValueError("positive explicit node budget required")
    graph = glue_graph(certificate)
    variants, allowed = _parse_grammar(grammar)
    start = _domains(certificate, variants)
    explored = 0

    def search(domains: list[set[str]]) -> tuple[str, list[str] | None]:
        nonlocal explored
        if explored >= max_nodes:
            return "INCONCLUSIVE", None
        explored += 1
        if not _propagate(domains, graph, variants, allowed):
            return "UNSAT_FINITE_QUOTIENT", None
        unresolved = [i for i, d in enumerate(domains) if len(d) > 1]
        if not unresolved:
            assignment = [next(iter(d)) for d in domains]
            if not verify_assignment(certificate, grammar, assignment):
                raise AssertionError("produced assignment failed independent replay")
            return "SAT_PERIODIC_WITNESS", assignment
        index = min(unresolved, key=lambda i: (len(domains[i]), i))
        inconclusive = False
        for variant in sorted(domains[index]):
            child = [set(d) for d in domains]
            child[index] = {variant}
            status, witness = search(child)
            if status == "SAT_PERIODIC_WITNESS":
                return status, witness
            if status == "INCONCLUSIVE":
                inconclusive = True
        return ("INCONCLUSIVE" if inconclusive else "UNSAT_FINITE_QUOTIENT"), None

    status, assignment = search(start)
    return {
        "status": status,
        "scope": ("SAT is a falsifying periodic decorated tiling for the supplied "
                  "specific grammar; finite-quotient UNSAT is NOT global perfection"),
        "cells": len(certificate["cells"]),
        "face_pairs": len(graph),
        "explored_search_nodes": explored,
        "node_budget": max_nodes,
        "assignment": assignment,
    }


def bare_control_grammar() -> dict:
    """Intentionally permissive and NOT Katz's rule."""
    return {
        "name": "undecorated-bare-negative-control-NOT-KATZ",
        "variants": [
            {"id": "bare_P", "shape": "P",
             "faces": [["plain","plain"]]*3},
            {"id": "bare_O", "shape": "O",
             "faces": [["plain","plain"]]*3},
        ],
        "allowed_pairs": [["plain", "plain"]],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate",
                        default=str(Path(__file__).resolve().parent /
                                    "certificate_3_2.json"))
    parser.add_argument("--grammar", help="explicit source-derived grammar JSON")
    parser.add_argument("--max-nodes",type=int,default=10000)
    args = parser.parse_args()
    cert = json.loads(Path(args.certificate).read_text())
    grammar = (json.loads(Path(args.grammar).read_text())
               if args.grammar else bare_control_grammar())
    print(json.dumps(solve(cert, grammar, args.max_nodes), indent=2))


if __name__ == "__main__":
    main()
