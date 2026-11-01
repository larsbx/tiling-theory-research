"""Exact necessary-condition tests for the global AKN matching-rule spike.

No floating-point or third-party imports. This replays a periodic obstruction
to a bare vertex-star rule, NOT a proof about any decorated Katz rule.
The 6x6 integer matrix [A;B] has determinant 8. This makes the golden
physical and conjugate projections individually injective on Z^6.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import combinations
from math import gcd
from pathlib import Path

A = ((1, -1, 0, 0, 0, 0),
     (0, 0, 1, -1, 0, 0),
     (0, 0, 0, 0, 1, 1))
B = ((0, 0, 0, 0, 1, -1),
     (1, 1, 0, 0, 0, 0),
     (0, 0, 1, 1, 0, 0))


def determinant(matrix: list[list[int]]) -> int:
    """Integer fraction-free Bareiss determinant, with row pivoting."""
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("nonempty square matrix required")
    m = [list(map(int, r)) for r in matrix]
    denominator, orientation = 1, 1
    for k in range(n - 1):
        pivot = next((i for i in range(k, n) if m[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
            orientation *= -1
        x = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = m[i][j]*x - m[i][k]*m[k][j]
                quotient, remainder = divmod(numerator, denominator)
                assert remainder == 0, "Bareiss invariant failed"
                m[i][j] = quotient
            m[i][k] = 0
        denominator = x
    return orientation * m[n-1][n-1]


def project_parts(n: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if len(n) != 6:
        raise ValueError("six integer lift coordinates required")
    return (tuple(sum(c*v for c,v in zip(row,n)) for row in A),
            tuple(sum(c*v for c,v in zip(row,n)) for row in B))


def physical(n: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    """Coefficients (a,b) of a+b*tau."""
    a,b = project_parts(n)
    return tuple(zip(a,b))


def perpendicular(n: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    """Coefficients (a,b) of a+b*tau, with tau'=1-tau."""
    a,b = project_parts(n)
    return tuple((a[i]+b[i], -b[i]) for i in range(3))


def rational_perp_zero(n: tuple[int, ...], x: Fraction) -> bool:
    a,b = project_parts(n)
    return all(a[i] + x*b[i] == 0 for i in range(3))


def saturated_rank_three(rows: tuple[tuple[int, ...], ...]) -> bool:
    if len(rows) != 3 or any(len(r)!=6 for r in rows):
        return False
    value = 0
    for cols in combinations(range(6),3):
        value = gcd(value, determinant(
            [[rows[i][j] for j in cols] for i in range(3)]))
    return value == 1


def qadd(x: tuple[int,int], y: tuple[int,int]) -> tuple[int,int]:
    return x[0]+y[0], x[1]+y[1]


def qneg(x: tuple[int,int]) -> tuple[int,int]:
    return -x[0], -x[1]


def qmul(x: tuple[int,int], y: tuple[int,int]) -> tuple[int,int]:
    """Exact multiplication modulo tau^2-tau-1."""
    return (x[0]*y[0]+x[1]*y[1],
            x[0]*y[1]+x[1]*y[0]+x[1]*y[1])


def qsign(x: tuple[int,int]) -> int:
    """Exact sign in ordered Z[tau], using integer sqrt(5) comparison."""
    a,b = 2*x[0]+x[1], x[1]
    if a == 0:
        return (b>0)-(b<0)
    if b == 0 or (a>0)==(b>0):
        return (a>0)-(a<0)
    d = a*a - 5*b*b
    assert d != 0
    return ((a>0)-(a<0))*((d>0)-(d<0))


def qabs(x: tuple[int,int]) -> tuple[int,int]:
    return qneg(x) if qsign(x)<0 else x


def qdot(u,v) -> tuple[int,int]:
    result = (0,0)
    for x,y in zip(u,v):
        result = qadd(result,qmul(x,y))
    return result


def qcross(u,v):
    def sub(x,y):
        return qadd(x,qneg(y))
    return (sub(qmul(u[1],v[2]),qmul(u[2],v[1])),
            sub(qmul(u[2],v[0]),qmul(u[0],v[2])),
            sub(qmul(u[0],v[1]),qmul(u[1],v[0])))


def separating_periodic_cells(cert: dict) -> dict:
    """Exact two-cell CLOSED-window obstruction, three periods apart.

    Pick a committed cell (axes 1,2,4) and its translate by 3 L0.
    In the true internal projection, the complementary facet (0,5)
    separates the two closed phase sets. There is no bounded-radius
    implication: the two cells are physically separated.
    """
    I = (1,2,4)
    base = (0,0,-1,0,0,0)
    if not any(tuple(n)==base and tuple(axes)==I
               for n,axes in cert.get("cells",[])):
        raise ValueError("periodic certificate cell anchor absent")
    period = tuple(cert["period_lattice"][0])
    W = tuple(tuple((A[j][i]+B[j][i],-B[j][i])
                    for j in range(3)) for i in range(6))
    normal = qcross(W[0],W[5])
    drift = qdot(perpendicular(period),normal)
    width = (0,0)
    for i in range(6):
        if i not in I:
            width = qadd(width,qabs(qdot(W[i],normal)))
    two = qabs((2*drift[0],2*drift[1]))
    three = qabs((3*drift[0],3*drift[1]))
    if qsign(qadd(two,qneg(width)))>0 or qsign(qadd(three,qneg(width)))<=0:
        raise AssertionError("expected three-period separation fails")
    return {"cell_base":list(base),
            "axes_zero_based":list(I),
            "period_multiple":3,
            "separating_facet_zero_based":[0,5],
            "dot_perp_period_normal_z_tau":list(drift),
            "full_window_width_z_tau":list(width),
            "strict_disjointness":True,
            "meaning":"two remote required cells have disjoint CLOSED shift domains, not a finite-radius forbidden pattern"}


def report(cert: dict) -> dict:
    if cert.get("x") != "-2/3":
        raise ValueError("expected certified 3/2 rational quotient")
    rows = tuple(tuple(row) for row in cert["period_lattice"])
    if not saturated_rank_three(rows):
        raise ValueError("period lattice must be rank-three saturated")
    if not all(rational_perp_zero(row,Fraction(-2,3)) for row in rows):
        raise ValueError("period lattice is not in rational kernel")
    split = determinant([list(row) for row in A+B])
    assert split == 8
    periods = []
    for row in rows:
        phys,perp = physical(row),perpendicular(row)
        if not any(v!=(0,0) for v in phys):
            raise ValueError("degenerate physical period")
        if not any(v!=(0,0) for v in perp):
            raise ValueError("missing irrational perpendicular drift")
        periods.append({"lift":list(row),
                        "physical_z_tau":[list(v) for v in phys],
                        "perp_z_tau":[list(v) for v in perp]})
    return {
        "claim":"fixed periodic certificate obstructs bare radius-one atlas weak/perfect rules",
        "scope":"exact period-lattice necessary-condition check, conditional on original geometric certificate",
        "stacked_integer_projection_determinant":split,
        "periods":periods,
        "remote_two_cell_obstruction":(
            separating_periodic_cells(cert) if "cells" in cert else None),
        "drift_statement":"perp displacement after k periods equals k times a nonzero Z[tau] vector",
        "not_proved":["decorated-rule perfection","any radius-two global result",
                      "reproduction of Katz 1988 global proof","weak implies perfect"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate",nargs="?",default=str(
        Path(__file__).resolve().parent/"certificate_3_2.json"))
    args = parser.parse_args()
    print(json.dumps(report(json.loads(Path(args.certificate).read_text())),indent=2))


if __name__ == "__main__":
    main()
