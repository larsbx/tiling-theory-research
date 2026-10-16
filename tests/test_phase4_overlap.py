"""Exact arithmetic, provenance, coverage graph, and negative controls."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
import unittest

from research.phase4_exact import (Q5, SQRT5, T, TP, R, INITIAL_BOUND, E, C, sub,
                                   overlap, vectors, potential_states, graph,
                                   coincidence_distances, lattice_box)
from research.phase4_overlap_coverage import (certificate, legal_sources, word_prefix,
                                             witness, validate_witness)

ROOT = Path(__file__).resolve().parents[1]


class QuadraticArithmetic(unittest.TestCase):
    def test_field_and_order(self):
        self.assertEqual(T * T, T + 1)
        self.assertEqual(T * TP, -1)
        self.assertEqual(T / T, 1)
        self.assertEqual(Q5(Fraction(1, 3)) + Q5(Fraction(2, 3)), 1)
        self.assertEqual(hash(Q5(1)), hash(1))
        with self.assertRaises(ZeroDivisionError):
            T / 0
        # Pell units: (9+4sqrt5)^k has conjugate positive, arbitrarily close to zero.
        a, b = 9, 4
        for _ in range(12):
            self.assertGreater(Q5(a, -b), 0)
            self.assertLess(Q5(-a, b), 0)
            self.assertEqual(a*a - 5*b*b, 1)
            a, b = 9*a + 20*b, 4*a + 9*b
        self.assertLess(2 - SQRT5, 0)
        self.assertGreater(2 + SQRT5, R)
        for z, expected in [(T, 2), (-T, -1), (Q5(-2), -2), (Q5(), 0), (Q5(3), 3)]:
            self.assertEqual(z.ceil(), expected)

    def test_open_geometric_endpoints(self):
        self.assertFalse(overlap('a', 'b', (1, 0)))
        self.assertFalse(overlap('a', 'b', (0, -1)))
        self.assertTrue(overlap('a', 'b', (0, 0)))
        self.assertTrue(overlap('b', 'a', (-2, 3)))


class LegalSources(unittest.TestCase):
    def test_indexed_search_against_exhaustive_pairs(self):
        for root in ('a', 'b'):
            word, prefix = word_prefix(root, 2)
            returns = {sub(prefix[s], prefix[r]) for r in range(len(word))
                       for s in range(len(word)) if word[r] == word[s]}
            brute = {(word[i], word[j], d) for y in returns
                     for i in range(len(word)) for j in range(len(word))
                     if overlap(word[i], word[j], d := sub(sub(prefix[j], prefix[i]), y))}
            actual, count = legal_sources(root, 2)
            self.assertEqual(set(actual), brute)
            self.assertEqual(count, len(returns))
            for record in actual.values():
                validate_witness(record)

    def test_original_witness_and_corruptions(self):
        record = witness('a', 4, (17, 25), (34, 43))
        self.assertEqual(record['return_vector'], [6, 2])
        self.assertEqual(record['state'], ['b', 'a', [-2, 3]])
        self.assertEqual(record['prefixes'], [[10, 7], [16, 9], [22, 12], [26, 17]])
        validate_witness(record)
        for field, wrong in [('return_vector', [6, 3]), ('state', ['b', 'a', [-2, 2]]),
                             ('prefixes', [[0, 0]]*4), ('word_length', 54)]:
            bad = deepcopy(record)
            bad[field] = wrong
            with self.assertRaises(ValueError):
                validate_witness(bad)
        for rs, ij in [((17, 34), (34, 43)), ((17, 55), (34, 43)),
                       ((17, 25), (0, 54)), ((-1, 25), (34, 43))]:
            with self.assertRaises(ValueError):
                witness('a', 4, rs, ij)


class CoverageCertificate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = certificate()
        cls.states = potential_states()
        cls.adj = graph(cls.states)

    def test_packet_recomputation_and_graph_paths(self):
        committed = json.loads((ROOT / 'research/phase4_overlap_certificate.json').read_text())
        self.assertEqual(self.report, committed)
        self.assertEqual(len(self.states), 64)
        self.assertEqual(sum(map(len, self.adj.values())), 142)
        self.assertEqual(lattice_box(T, INITIAL_BOUND), (4, 6))
        # Independent walk of every stored decreasing-distance certificate.
        rows = committed['states']
        for index, row in enumerate(rows):
            cursor = index
            for _ in range(row['coincidence_distance']):
                target = rows[cursor]['next_to_coincidence']
                self.assertIn(target, rows[cursor]['successors'])
                self.assertEqual(rows[target]['coincidence_distance'],
                                 rows[cursor]['coincidence_distance'] - 1)
                cursor = target
            a, b, d = rows[cursor]['state']
            self.assertEqual(a, b)
            self.assertEqual(d, [0, 0])
        for run in committed['finite_word_enumerations']:
            for record in run['witnesses']:
                validate_witness(record)
        corrupted = deepcopy(committed)
        corrupted['states'][0]['successors'] = []
        self.assertNotEqual(self.report, corrupted)

    def test_historical_domain_is_incomplete(self):
        old = potential_states(R)
        self.assertEqual(len(vectors(2, R)), 15)
        self.assertEqual(len(old), 32)
        self.assertEqual(Counter(coincidence_distances(graph(old)).values()),
                         {0: 2, 1: 6, 2: 12, 3: 6, 4: 6})
        omitted = ('b', 'a', (-2, 3))
        self.assertNotIn(omitted, old)
        self.assertIn(omitted, self.states)
        # Equal cardinality of a witnessed set and the old ball is not coverage.
        run = self.report['finite_word_enumerations'][0]
        legal = {(r['state'][0], r['state'][1], tuple(r['state'][2])) for r in run['witnesses']}
        self.assertEqual(len(legal), len(old))
        self.assertNotEqual(legal, old)
        self.assertIn(omitted, legal)

    def test_nonclosure_and_missing_coincidence_are_rejected(self):
        with self.assertRaises(ValueError):
            graph(self.states - {('a', 'a', (0, 0))})
        # A recurrent noncoincidence is not a negative certificate when it has an exit.
        s, t = ('a', 'b', (0, 0)), ('a', 'a', (0, 0))
        self.assertEqual(coincidence_distances({s: {s, t}, t: {t}})[s], 1)
        self.assertNotIn(s, coincidence_distances({s: {s}, t: {t}}))


if __name__ == '__main__':
    unittest.main()
