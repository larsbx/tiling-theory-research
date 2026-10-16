#!/usr/bin/env python3
"""Exact finite supergraph plus witnessed legal sources for a->aab, b->ba.

The 64-state universe is a coverage *superset*, not an exact legality oracle.
The independent prefix/return bound is proved in the accompanying research note.
"""
import argparse
from bisect import bisect_left, bisect_right
from collections import Counter
import json
from pathlib import Path

try:
    from .phase4_exact import (T, TP, R, RHO, SQRT5, INITIAL_BOUND, CHILD, E, C,
                              sub, overlap, potential_states, graph,
                              coincidence_distances, lattice_box)
except ImportError:
    from phase4_exact import (T, TP, R, RHO, SQRT5, INITIAL_BOUND, CHILD, E, C,
                             sub, overlap, potential_states, graph,
                             coincidence_distances, lattice_box)


def word_prefix(root, depth):
    if root not in ('a', 'b') or not isinstance(depth, int) or depth < 0:
        raise ValueError('Expected root a/b and nonnegative integer depth')
    word = root
    for _ in range(depth):
        word = ''.join('aab' if z == 'a' else 'ba' for z in word)
    prefix = [(0, 0)]
    for z in word:
        x, y = prefix[-1]
        prefix.append((x + (z == 'a'), y + (z == 'b')))
    return word, prefix


def state_record(state):
    return [state[0], state[1], list(state[2])]


def witness(root, depth, return_positions, overlap_positions):
    word, prefix = word_prefix(root, depth)
    r, s = return_positions
    i, j = overlap_positions
    if any(not isinstance(k, int) or not 0 <= k < len(word) for k in (r, s, i, j)):
        raise ValueError('Tile index outside witness word')
    if word[r] != word[s]:
        raise ValueError('Return endpoints must have the same tile type')
    y = sub(prefix[s], prefix[r])
    d = sub(sub(prefix[j], prefix[i]), y)
    state = (word[i], word[j], d)
    if not overlap(*state):
        raise ValueError('Tiles do not overlap in their interiors')
    return {'root': root, 'depth': depth, 'word_length': len(word),
            'return_positions': [r, s], 'return_type': word[r], 'return_vector': list(y),
            'overlap_positions': [i, j],
            'prefixes': [list(prefix[k]) for k in (r, s, i, j)],
            'state': state_record(state)}


def validate_witness(record):
    expected = witness(record['root'], record['depth'], record['return_positions'],
                       record['overlap_positions'])
    if record != expected:
        raise ValueError('Witness data disagree with the legal substitution word')
    return expected


def legal_sources(root, depth):
    """All overlap states witnessed by two pairs in this one finite word.

    Retain one return pair per vector and one full provenance record per state.
    Signed and zero return vectors are included. A missing state is NOT illegal.
    """
    word, prefix = word_prefix(root, depth)
    returns = {}
    for r, first in enumerate(word):
        for s, second in enumerate(word):
            if first == second:
                returns.setdefault(sub(prefix[s], prefix[r]), (r, s))
    starts = [E(p) for p in prefix[:-1]]
    ends = [E(p) for p in prefix[1:]]
    sources = {}
    for y, rs in sorted(returns.items()):
        shift = E(y)
        for i in range(len(word)):
            # tile j-y intersects tile i iff end_j > start_i+y AND start_j < end_i+y.
            low = bisect_right(ends, starts[i] + shift)
            high = bisect_left(starts, ends[i] + shift)
            for j in range(low, high):
                d = sub(sub(prefix[j], prefix[i]), y)
                state = (word[i], word[j], d)
                if state not in sources:
                    sources[state] = witness(root, depth, rs, (i, j))
    return sources, len(returns)


def certificate():
    digit_values = [C(p) for children in CHILD.values() for _, p in children]
    assert min(digit_values) == 2 * TP and max(digit_values) == 1
    assert 2 * TP / (1 - RHO) == -2
    assert 1 / (1 - RHO) == T
    assert R == T + 2
    assert max(digit_values) - min(digit_values) == SQRT5
    assert RHO * INITIAL_BOUND + SQRT5 < INITIAL_BOUND
    states = potential_states()
    adj = graph(states)
    distance = coincidence_distances(adj)
    if set(distance) != states:
        raise ValueError('Potential overlap without a coincidence continuation')
    ordered = sorted(states)
    ids = {state: index for index, state in enumerate(ordered)}
    rows = []
    for state in ordered:
        row = {'state': state_record(state), 'successors': sorted(ids[t] for t in adj[state]),
               'coincidence_distance': distance[state]}
        if distance[state]:
            row['next_to_coincidence'] = min(ids[t] for t in adj[state]
                                            if distance[t] == distance[state] - 1)
        rows.append(row)
    finite_runs = []
    for depth in (4, 5):
        for root in ('a', 'b'):
            sources, returns = legal_sources(root, depth)
            if not sources.keys() <= states:
                raise ValueError('Witnessed source escaped the proved bound')
            finite_runs.append({'root': root, 'depth': depth,
                                'word_length': len(word_prefix(root, depth)[0]),
                                'distinct_return_vectors': returns,
                                'source_state_count': len(sources),
                                'witnesses': [sources[s] for s in sorted(sources)]})
    omitted = witness('a', 4, (17, 25), (34, 43))
    assert omitted['state'] == ['b', 'a', [-2, 3]]
    assert abs(C((-2, 3))) > R
    return {
        'schema': 1,
        'scope': 'Exact forward-closed potential-overlap superset; legal source coverage uses the prefix/return bound proof, not finite-word saturation.',
        'substitution': {'a': 'aab', 'b': 'ba'},
        'initial_internal_bound': INITIAL_BOUND.record(),
        'lattice_box': list(lattice_box(T, INITIAL_BOUND)),
        'state_count': len(states), 'edge_count': sum(map(len, adj.values())),
        'distance_counts': {str(k): v for k, v in sorted(Counter(distance.values()).items())},
        'states': rows, 'finite_word_enumerations': finite_runs,
        'omitted_from_old_bound': omitted,
        'unwitnessed_states_are_not_declared_illegal': True,
        'pure_point_spectrum_claimed': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', type=Path, help='Write a reproducible evidence packet')
    parser.add_argument('--check', type=Path, help='Recompute and compare a committed packet')
    args = parser.parse_args()
    report = certificate()
    if args.check and json.loads(args.check.read_text()) != report:
        raise SystemExit('Certificate mismatch')
    if args.write:
        args.write.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('state_count', 'edge_count', 'distance_counts',
                                           'initial_internal_bound', 'lattice_box')}, indent=2))
    for run in report['finite_word_enumerations']:
        print({k: v for k, v in run.items() if k != 'witnesses'})


if __name__ == '__main__':
    main()
