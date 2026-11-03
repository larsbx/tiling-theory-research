"""Reproducible finite cover versus single-quotient matching-rule controls.

The synthetic parity rule is deliberately NOT Katz's decoration. It shows
why UNSAT on one periodic quotient is not a global perfect-rule theorem.
"""
import copy
import itertools
import json
import sys
import unittest
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

AKN = Path(__file__).resolve().parents[1] / "research" / "akn"
sys.path.insert(0, str(AKN))

from decorated_covers import (  # noqa: E402
    cover_graph, integral_period_coordinates, parity_face_grammar,
    solve_cover, verify_cover_assignment,
)
from decorated_quotient import bare_control_grammar  # noqa: E402

CERT = json.loads((AKN / "certificate_3_2.json").read_text())


def direct_integer_face_audit(grammar, dims, assignment):
    """Replay by reducing actual 6D corners, with no cover/solver helpers.

    For this fixed certificate, the first three coordinates give period
    coefficients a=(n0+n1)/6, b=(n0-n1)/4, c=(n2-2a)/3. Removing
    floor(a/m0), etc. times each cover generator gives a canonical corner.
    In-face axes distinguish faces at the same corner. Parity labels use
    equality, so this independent control needs no oriented-glue machinery.
    """
    variants = {v['id']: v for v in grammar['variants']}
    faces = defaultdict(list)
    periods = CERT['period_lattice']
    n = len(CERT['cells'])
    for k, deck in enumerate(itertools.product(*(range(m) for m in dims))):
        for i, (base, axes) in enumerate(CERT['cells']):
            variant = variants[assignment[k*n+i]]
            for position, axis in enumerate(axes):
                for side in (0, 1):
                    corner = [base[j] + sum(deck[t]*periods[t][j] for t in range(3))
                              + (side if j == axis else 0) for j in range(6)]
                    a = Fraction(corner[0]+corner[1], 6)
                    b = Fraction(corner[0]-corner[1], 4)
                    c = (corner[2]-2*a)/3
                    shifts = [v//m for v, m in zip((a,b,c), dims)]
                    reduced = tuple(corner[j] - sum(shifts[t]*dims[t]*periods[t][j]
                                                   for t in range(3))
                                    for j in range(6))
                    key = reduced, tuple(a for a in axes if a != axis)
                    faces[key].append(variant['faces'][position][side])
    if any(len(labels) != 2 for labels in faces.values()):
        raise AssertionError('direct cover has incomplete face pairing')
    mismatches = sum(labels[0] != labels[1] for labels in faces.values())
    return len(faces), mismatches


class CoverControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rule = parity_face_grammar()
        cls.base_edges,cls.base_report = cover_graph(CERT,(1,1,1))
        cls.double_edges,cls.double_report = cover_graph(CERT,(2,1,1))

    def test_period_coordinate_solver_is_exact(self):
        periods = CERT["period_lattice"]
        self.assertEqual(integral_period_coordinates(tuple(periods[0]),periods),
                         (1,0,0))
        self.assertEqual(integral_period_coordinates(tuple(-x for x in periods[1]),
                                                     periods),(0,-1,0))
        with self.assertRaises(ValueError):
            integral_period_coordinates((1,0,0,0,0,0),periods)

    def test_deck_cover_uses_all_oriented_faces(self):
        self.assertEqual(self.base_report["cells"],576)
        self.assertEqual(self.base_report["face_pairs"],1728)
        self.assertEqual(self.base_report["nonzero_base_face_seams"],308)
        self.assertEqual(self.double_report["cells"],1152)
        self.assertEqual(self.double_report["face_pairs"],3456)
        for dims in ((1,1,1), (2,1,1), (1,2,1), (2,2,1)):
            with self.subTest(dims=dims):
                edges, report = cover_graph(CERT, dims)
                cells = 576*dims[0]*dims[1]*dims[2]
                endpoints = [(f.cell, f.position, f.side)
                             for e in edges for f in (e.positive, e.negative)]
                self.assertEqual(report['cells'], cells)
                self.assertEqual(len(edges), 3*cells)
                self.assertEqual(len(endpoints), 6*cells)
                self.assertEqual(len(set(endpoints)), 6*cells)

    def test_parity_rule_has_explicit_twofold_periodic_witness(self):
        L0 = CERT["period_lattice"][0]
        self.assertEqual(L0[0]%2,1)
        assignment=[]
        for deck in (0,1):
            for base,axes in CERT["cells"]:
                p = (base[0]+deck*L0[0])%2
                assignment.append("I"+"-".join(map(str,axes))+"-p"+str(p))
        self.assertTrue(verify_cover_assignment(CERT,self.rule,(2,1,1),
                                                assignment))
        self.assertEqual(direct_integer_face_audit(self.rule, (2,1,1), assignment),
                         (3456, 0))
        self.assertFalse(verify_cover_assignment(CERT,self.rule,(1,1,1),
                                                 assignment[:576]))
        damaged = assignment[:]
        damaged[0] = ("I"+"-".join(map(str,CERT["cells"][0][1]))+
                      "-p"+str(1-(CERT["cells"][0][0][0]%2)))
        self.assertFalse(verify_cover_assignment(CERT,self.rule,(2,1,1),
                                                 damaged))
        self.assertGreater(direct_integer_face_audit(self.rule, (2,1,1), damaged)[1], 0)

    def test_onefold_unsat_does_not_exclude_twofold_sat(self):
        base=solve_cover(CERT,self.rule,(1,1,1),max_nodes=3)
        doubled=solve_cover(CERT,self.rule,(2,1,1),max_nodes=3)
        self.assertEqual(base["status"],"UNSAT_FINITE_COVER")
        self.assertEqual(doubled["status"],"SAT_PERIODIC_WITNESS")
        self.assertTrue(verify_cover_assignment(
            CERT,self.rule,(2,1,1),doubled["assignment"]))

    def test_deep_ambiguous_cover_is_stack_safe_and_budgeted(self):
        grammar = bare_control_grammar()
        for variant in list(grammar['variants']):
            duplicate = copy.deepcopy(variant)
            duplicate['id'] += '-duplicate'
            grammar['variants'].append(duplicate)
        result = solve_cover(CERT, grammar, (2,1,1), max_nodes=1200)
        self.assertEqual(result['status'], 'SAT_PERIODIC_WITNESS')
        self.assertEqual(result['explored_nodes'], 1153)
        self.assertTrue(verify_cover_assignment(CERT, grammar, (2,1,1),
                                                result['assignment']))
        capped = solve_cover(CERT, grammar, (2,1,1), max_nodes=1000)
        self.assertEqual(capped['status'], 'INCONCLUSIVE')
        self.assertEqual(capped['termination_reason'], 'node_cap')
        self.assertEqual(capped['explored_nodes'], 1000)
        self.assertIsNone(capped['assignment'])

    def test_partial_unsat_search_cannot_certify_unsat(self):
        # The base parity contradiction requires both root choices to fail.
        for cap in (1, 2):
            result = solve_cover(CERT, self.rule, (1,1,1), max_nodes=cap)
            self.assertEqual(result['status'], 'INCONCLUSIVE')
            self.assertEqual(result['termination_reason'], 'node_cap')
            self.assertIsNone(result['assignment'])
        complete = solve_cover(CERT, self.rule, (1,1,1), max_nodes=3)
        self.assertEqual(complete['status'], 'UNSAT_FINITE_COVER')
        self.assertEqual(complete['termination_reason'], 'exhaustive_search')
        self.assertEqual(complete['explored_nodes'], 3)

    def test_search_memory_exhaustion_is_inconclusive(self):
        with patch('decorated_covers._propagate', side_effect=MemoryError):
            result = solve_cover(CERT, self.rule, (2,1,1), max_nodes=3)
        self.assertEqual(result['status'], 'INCONCLUSIVE')
        self.assertEqual(result['termination_reason'], 'memory_exhaustion')
        self.assertIsNone(result['assignment'])

    def test_caps_and_grammar_limits_are_explicit(self):
        with self.assertRaises(ValueError):
            cover_graph(CERT,(0,1,1))
        with self.assertRaises(ValueError):
            solve_cover(CERT,self.rule,(1,1,1),max_nodes=0)
        self.assertEqual(solve_cover(
            CERT,bare_control_grammar(),(1,1,1),max_nodes=1)["status"],
            "SAT_PERIODIC_WITNESS")
        self.assertEqual(solve_cover(
            CERT,bare_control_grammar(),(2,1,1),max_nodes=1)["status"],
            "SAT_PERIODIC_WITNESS")


if __name__ == "__main__":
    unittest.main()
