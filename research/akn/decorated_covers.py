"""Exact finite covers of the certified 3/2 periodic decorated face quotient.

A periodic witness on ANY cover is an actual periodic decorated tiling of
the infinite golden-rhombohedral geometry, provided the supplied rule is
fully described by per-tile admissibility and ordered face-pair constraints.
UNSAT on a particular cover is only finite evidence; a solver cap is
INCONCLUSIVE. The included parity grammar is a synthetic NON-KATZ control.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from fractions import Fraction

from decorated_quotient import (
    Face, Glue, _compatible, _domains, _parse_grammar, _propagate, glue_graph
)
from geometry import cell_shape


def det3(m: list[list[int]]) -> int:
    a,b,c = m
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            -a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))


def integral_period_coordinates(delta: tuple[int, ...],
                                periods: list[list[int]]) -> tuple[int, int, int]:
    """Solve delta=sum a_i L_i exactly; reject any non-period displacement."""
    if len(delta) != 6 or len(periods) != 3 or any(len(p)!=6 for p in periods):
        raise ValueError("require three six-dimensional lattice generators")
    cols = next((idx for idx in itertools.combinations(range(6), 3)
                 if det3([[periods[k][j] for k in range(3)] for j in idx])),
                None)
    if cols is None:
        raise ValueError("period rank is less than three")
    mat = [[periods[k][j] for k in range(3)] for j in cols]
    d = det3(mat)
    coords = []
    for i in range(3):
        trial = [[delta[cols[j]] if k==i else mat[j][k]
                  for k in range(3)] for j in range(3)]
        f = Fraction(det3(trial), d)
        if f.denominator != 1:
            raise ValueError("relative face origins not separated by period lattice")
        coords.append(int(f))
    if any(sum(coords[k]*periods[k][j] for k in range(3)) != delta[j]
           for j in range(6)):
        raise ValueError("non-period face translation")
    return tuple(coords)  # type: ignore[return-value]


def _face_origin(cert: dict, face: Face) -> tuple[int, ...]:
    base, axes = cert["cells"][face.cell]
    n = list(base)
    n[axes[face.position]] += face.side
    return tuple(n)


def deck_indices(dims: tuple[int,int,int]) -> list[tuple[int,int,int]]:
    if len(dims) != 3 or any(not isinstance(n,int) or n<1 for n in dims):
        raise ValueError("three positive integer cover indices required")
    return list(itertools.product(*(range(n) for n in dims)))


def cover_graph(cert: dict, dims: tuple[int,int,int]) -> tuple[list[Glue], dict]:
    """Lift exactly every face pair through the finite deck group."""
    periods = cert["period_lattice"]
    base_graph = glue_graph(cert)
    group = deck_indices(dims)
    index = {d:i for i,d in enumerate(group)}
    n = len(cert["cells"])
    edges = []
    seam_histogram = {}
    for edge in base_graph:
        plus, minus = edge.positive, edge.negative
        a = _face_origin(cert,plus)
        b = _face_origin(cert,minus)
        lift = integral_period_coordinates(tuple(x-y for x,y in zip(a,b)),
                                           periods)
        key = ",".join(map(str,lift))
        seam_histogram[key] = seam_histogram.get(key,0)+1
        for deck in group:
            target = tuple((deck[k]+lift[k])%dims[k] for k in range(3))
            p = Face(index[deck]*n+plus.cell,plus.position,
                     plus.side,plus.orientation)
            q = Face(index[target]*n+minus.cell,minus.position,
                     minus.side,minus.orientation)
            edges.append(Glue(p,q))
    if len(edges) != len(group)*3*n:
        raise AssertionError("lifted face count mismatch")
    # Every one of six oriented faces of each lifted tile is used once.
    endpoints = [(f.cell,f.position,f.side)
                 for edge in edges for f in (edge.positive,edge.negative)]
    if len(set(endpoints)) != 6*n*len(group):
        raise AssertionError("lifted face incidence not unique")
    return edges,{
        "deck_dimensions":list(dims),
        "deck_size":len(group),
        "cells":len(group)*n,
        "face_pairs":len(edges),
        "nonzero_base_face_seams":sum(
            v for k,v in seam_histogram.items() if k!="0,0,0"),
        "period_coordinate_histogram":seam_histogram
    }


def verify_cover_assignment(cert: dict, grammar: dict,
                            dims: tuple[int,int,int],
                            assignment: list[str]) -> bool:
    """Independent checker of every tile and face on the expanded cover."""
    variants,allowed = _parse_grammar(grammar)
    original = cert["cells"]
    deck = deck_indices(dims)
    if len(assignment)!=len(deck)*len(original):
        return False
    for k,_ in enumerate(deck):
        for i,(_,axes) in enumerate(original):
            name = assignment[k*len(original)+i]
            if name not in variants:
                return False
            entry=variants[name]
            if (entry["shape"]!=cell_shape(tuple(a+1 for a in axes)) or
                entry["axes"] is not None and tuple(axes) not in entry["axes"]):
                return False
    edges,_ = cover_graph(cert,dims)
    for edge in edges:
        p,m=edge.positive,edge.negative
        lp=variants[assignment[p.cell]]["faces"][p.position][p.side]
        lm=variants[assignment[m.cell]]["faces"][m.position][m.side]
        if (lp,lm) not in allowed:
            return False
    return True


def solve_cover(cert: dict, grammar: dict, dims: tuple[int,int,int],
                max_nodes: int=10000) -> dict:
    if max_nodes<1:
        raise ValueError("positive node cap required")
    edges,stats=cover_graph(cert,dims)
    variants,allowed=_parse_grammar(grammar)
    base=_domains(cert,variants)
    domains=[set(d) for _ in deck_indices(dims) for d in base]
    explored=0

    def walk(state):
        nonlocal explored
        if explored>=max_nodes:
            return "INCONCLUSIVE",None
        explored+=1
        if not _propagate(state,edges,variants,allowed):
            return "UNSAT_FINITE_COVER",None
        ambiguous=[i for i,d in enumerate(state) if len(d)>1]
        if not ambiguous:
            assignment=[next(iter(d)) for d in state]
            if not verify_cover_assignment(cert,grammar,dims,assignment):
                raise AssertionError("SAT witness failed independent replay")
            return "SAT_PERIODIC_WITNESS",assignment
        cell=min(ambiguous,key=lambda i:(len(state[i]),i))
        capped=False
        for name in sorted(state[cell]):
            child=[set(d) for d in state]
            child[cell]={name}
            result,proof=walk(child)
            if result=="SAT_PERIODIC_WITNESS":
                return result,proof
            if result=="INCONCLUSIVE":
                capped=True
        return ("INCONCLUSIVE" if capped else "UNSAT_FINITE_COVER"),None

    status,assignment=walk(domains)
    return {
        "status":status,**stats,"explored_nodes":explored,
        "node_cap":max_nodes,"assignment":assignment,
        "claim_limit":"SAT is a finite-cover counterexample to the COMPLETE grammar; "
                      "UNSAT of a specific cover is never a global matching theorem."
    }


def parity_face_grammar() -> dict:
    """Synthetic face rule encoding parity of the first 6D cell-base coordinate.

    Each tile of shape P/O and 0-based axis triple I has states for p in Z/2.
    A face's label is the parity of its canonical 6D lower corner n+side*e_i
    on that face. Equality of the two labels forces parity transport.
    L_1[0]=3 (odd), L_2[0]=2, L_3[0]=0, hence a twofold cover along
    L_1 admits the actual periodic tiling but the single quotient does not.
    This is NOT a historical Katz/Ammann matching-rule reconstruction.
    """
    from geometry import TRIPLES
    variants=[]
    for axes in TRIPLES:
        shape=cell_shape(tuple(i+1 for i in axes))
        for parity in (0,1):
            faces=[]
            for axis in axes:
                faces.append([
                    "p"+str(parity),
                    "p"+str((parity+(1 if axis==0 else 0))%2)
                ])
            variants.append({
                "id":"I"+"-".join(map(str,axes))+"-p"+str(parity),
                "shape":shape,
                "allowed_axes":[list(axes)],
                "faces":faces
            })
    return {
        "name":"synthetic-6D-base-parity-finite-cover-negative-control-NOT-KATZ",
        "source_status":"synthetic finite-cover counterexample only",
        "variants":variants,
        "allowed_pairs":[["p0","p0"],["p1","p1"]]
    }
