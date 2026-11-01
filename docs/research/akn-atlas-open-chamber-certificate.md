# Exact AKN open-chamber cover: bounded reproducible pilot

**Date:** 2026-11-01  
**Upstream:** PR #22, `b0c07fd04862895ef512ede4b2f668f3f328e407`  
**Status:** experimental finite enumeration and independent replay; **no completed 135-plane exhaustive certificate yet**.

## Mathematical object

Let `tau^2=tau+1`, `tau'=1-tau`, and `W_i=A_i+tau'B_i`.
Write `y=2 gamma` for the internal shift coordinate. For each pair
`(i,j)`, let `N_ij=W_i x W_j`. The original exact arrangement has 15
such directions, each with nine strictly ordered levels in `Z[tau]`.
The candidate vertex window is the intersection of the 15 open slabs
between the first and last levels. A generic incident star is constant
in each connected component of this window after deleting all 135 planes.

Each family admits exactly eight *interior consecutive-level slabs*.
A prefix `(k_0,...,k_{r-1})` selects the first `r` slabs; all remaining
families are only bounded by the original vertex window. This is an open
convex system, not a numerical sample. The polytope's closure may have
degenerate faces, but it is a feasible open region precisely when its
vertices affinely span three dimensions.

## Enumerator and independently replayed cover

`research/akn/atlas_chambers.py` reconstructs the window from its
64 exact signed-generator sums, discards non-extreme candidates, and
intersects its 3D convex polytopes with consecutive parallel planes.
Vertices and edge-plane intersections use only rational arithmetic in
`Q(tau)`; all sign tests are exact. Every full-dimensional child
receives an exact witness (the vertex barycenter). The process is
deterministic, but an interrupted or capped search leaves explicit
unclassified *frontier prefixes*.

`research/akn/atlas_chamber_check.py` **does not import the enumerator**
or trust any claimed list of feasible branches. Instead it rebuilds
the 160 incident-cell transition levels from the independent plane
fixture; represents every prefix as strict `Z[tau]` halfspaces; and
uses exact strict Fourier-Motzkin elimination to test **all eight**
possible next slabs, including every missing branch. Infeasible
branches replay positive-multiplier contradictions from their original
inequalities. The certificate is a sorted prefix trie: each leaf is
either a complete 15-family class with exact witness or a nonempty
frontier subtree. Coverage holds inductively because the open
window is partitioned by each family's consecutive levels; omitted
feasible siblings are rejected.

For every completed chamber, the checker recomputes its entire
160-candidate cell star in the original exact `geometry.CutProject`,
then verifies its comparison against the 24 existing atlas
representatives. An unknown orbit is **preserved as an explicit exact
counterexample**, not silently discarded.

A **complete** packet requires *no frontier leaves*, independent
replay of every feasible branch, a strictly interior rational
`Q(tau)` witness for every chamber and no unknown orbit.
Even if it succeeds, it covers **generic open chambers only**;
singular-plane faces, edges and vertices need their own membership rule.

## Orbits versus conjugacy

The 24 atlas entries are **orbits of vertex stars under the full signed
icosahedral point group `I_h` (order 120)**. A group orbit is not
literally a conjugacy class of elements or subgroups.

To address the additional conjugacy question, the packet separately
records the **conjugacy class of each star's stabilizer subgroup**
`Stab_{I_h}(S)`. Its canonical hash is computed by enumerating
`g Stab(S) g^{-1}` for every `g in I_h` and choosing the
lexicographically least set of group indices. The checker computes
this by separate code, and rejects false stabilizer order or
conjugacy data. Distinct star-orbits may have conjugate stabilizers:
**the number of stabilizer conjugacy types need not be 24**.
No rotations-only/enantiomorph count is inferred from the
full-group 24-orbit catalog.

## Reproducible bounded packet and replay

Run from the repository root:

```sh
python research/akn/atlas_chambers.py --max-depth 1 --max-nodes 1 --out akn-chamber-depth1.json
python research/akn/atlas_chamber_check.py akn-chamber-depth1.json
python -m unittest discover -s tests -v
```

This depth-one packet is a **finite partition cover at one family**:
it proves that the first family has eight nonempty open slabs, while
all eight subtrees remain unresolved. It does not support a claim
of 24-class atlas completeness. The generated JSON and replay
summary are uploaded as deterministically regenerated GitHub Actions
artifacts; changing a witness, deleting a feasible branch or
falsifying a conjugacy signature causes rejection.

An exploratory deeper packet can be generated with:

```sh
python research/akn/atlas_chambers.py --max-nodes 1000 --max-depth 15 --out akn-chambers.json
python research/akn/atlas_chamber_check.py akn-chambers.json
```

A resource cap is **inconclusive**, and is represented by complete
prefix-trie frontier leaves. Increasing the cap is not itself a
coverage proof. For a future unbounded completion, use a cap above
the actual number of expanded prefixes and obtain a packet with zero
frontier leaves. Run the independent checker on that **exact** packet
before proposing any alteration to `AKN-ATLAS-PERIODIC`.

## Independent acceptance obligations

1. Record exact-head CI for this branch and upstream PR #22; pending
   hosted jobs are not pass results.
2. Run larger bounded enumerations, measure total feasible prefixes,
   number of classified chambers, and distinct **star orbits** and
   **stabilizer subgroup conjugacy classes**, preserving frontier.
3. Complete full enumeration and independently verify its trie.
   If any `orbit_class=-1`, retain witness and canonical star as
   counterexample to the proposed 24-orbit list.
4. Verify singular-boundary configurations separately under explicit
   inclusion conventions. Do not infer singular membership from an
   open chamber cover.
5. Do not infer a universal matching rule, aperiodicity, optimal
   radius, or nonexistence of other periodic configurations.

**Governance:** No claim status changes in this pilot. The
`AKN-ATLAS-PERIODIC` finite-domain result, `AKN-3-2-RADIUS2`
576-center census and `KATZ-AKN-C1`/`KATZ-AKN-PERFECT` claims
retain their registered scope; the present branch only adds a
candidate completeness certificate process and an explicit stopping
criterion.
