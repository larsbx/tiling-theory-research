#!/usr/bin/env python3
"""Independent finite-state audit for substitution a -> aab, b -> ba.

Reproduces the truncated graph using exact quadratic-field comparisons and
exhibits an exact finite-word counterexample to its claimed source coverage.
This is NOT a complete overlap-coincidence verifier; see phase4_overlap_coverage.py.
"""
from collections import Counter, defaultdict, deque
try:
    from .phase4_exact import T, TP, R, LENGTH as length, CHILD as child, E, C, M, overlap, vectors
except ImportError:
    from phase4_exact import T, TP, R, LENGTH as length, CHILD as child, E, C, M, overlap, vectors


# SC/pruned bound for paths initiated at displacement zero only.
sc_vectors = vectors(2, R)
truncated = {
    (i, j, v)
    for i in length
    for j in length
    for v in sc_vectors
    if overlap(i, j, v)
}
assert len(sc_vectors) == 15
assert len(truncated) == 32

adj = defaultdict(set)
for i, j, d in truncated:
    for ip, p in child[i]:
        for jp, q in child[j]:
            md = M(d)
            nd = (md[0] + q[0] - p[0], md[1] + q[1] - p[1])
            tar = (ip, jp, nd)
            if tar in truncated:
                adj[(i, j, d)].add(tar)

coinc = {(i, i, (0, 0)) for i in length}
back = defaultdict(set)
for source, dests in adj.items():
    for dest in dests:
        back[dest].add(source)

distance = {s: 0 for s in coinc}
queue = deque(coinc)
while queue:
    v = queue.popleft()
    for u in back[v]:
        if u not in distance:
            distance[u] = distance[v] + 1
            queue.append(u)
assert len(distance) == len(truncated)
assert max(distance.values()) == 4
assert Counter(distance.values()) == {0: 2, 1: 6, 2: 12, 3: 6, 4: 6}
print("SC vectors:", len(sc_vectors))
print("Truncated overlap states:", len(truncated))
print("Truncated BFS depth counts:", dict(sorted(Counter(distance.values()).items())))

# A legal return-vector overlap excluded by the zero-seeded c-ball.
word = "a"
for _ in range(4):
    word = "".join("aab" if z == "a" else "ba" for z in word)
assert len(word) == 55

prefix = [(0, 0)]
for z in word:
    x, y = prefix[-1]
    prefix.append((x + (z == "a"), y + (z == "b")))

r, s, i, j = 17, 25, 34, 43
assert (word[r], word[s], word[i], word[j]) == ("a", "a", "b", "a")
y = (prefix[s][0] - prefix[r][0], prefix[s][1] - prefix[r][1])
d = (
    prefix[j][0] - prefix[i][0] - y[0],
    prefix[j][1] - prefix[i][1] - y[1],
)
assert y == (6, 2) and d == (-2, 3)
assert overlap(word[i], word[j], d)
assert abs(C(d)) > R
assert (word[i], word[j], d) not in truncated
print("Explicit legal omitted overlap:")
print("  return positions:", (r, s), "return vector:", y)
print("  overlap positions:", (i, j), "types:", (word[i], word[j]), "displacement:", d)
print("  e(displacement):", E(d), "c(displacement):", C(d), "bound:", R)
