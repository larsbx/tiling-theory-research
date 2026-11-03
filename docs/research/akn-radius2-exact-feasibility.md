# AKN radius-two and exact atlas-arrangement research note

**Claim ID:** AKN-3-2-RADIUS2  
**Status:** finite-domain  
**Date:** 2026-11-01  
**Parent:** [AKN-ATLAS-PERIODIC](akn-vertex-atlas-periodic-approximant.md)

This registration is narrowly limited to the 576 centers of the specified
3/2 certificate and *generic true-AKN common-shift feasibility* for one fixed
signed-axis Z^6 lift, not a universal radius-two matching-rule statement.

## Input and scope

The existing 3/2 rational approximant has a separately certified periodic
face-to-face realization with 576 vertex orbits and 576 cell orbits. This
study extracts local full cell stars from that exact periodic quotient, then
tests whether their union can occur in a single *generic* ideal AKN
cut-and-project configuration at the irrational perpendicular slope
tau' = 1 - tau.

The radius convention is **not Euclidean distance two**:

- Radius 1: the full incident-cell star of the centered vertex.
- Radius 2: that star, together with the full stars of every vertex joined
  to the center by one rhombohedron edge.

Each neighboring star is re-lifted into Z^6 relative to the same central
vertex. This is necessary when a patch crosses a period-cell boundary.

## Exact membership decision

For a required cell with axes I and 6D base n, put

- W_i = A_i + tau' B_i in Z[tau]^3;
- N = W_j x W_k, for each pair j,k in the 3-axis complement of I;
- C = 2*pi_perp(n) + sum_{i in I} W_i;
- H = sum_{l not in I} abs(dot(W_l,N)).

The cell occurs for a common shift gamma only if all three facet pairs
satisfy the strict inequalities

    2 dot(N,gamma) < dot(N,C) + H
   -2 dot(N,gamma) < H - dot(N,C).

The central vertex's six-generator window gives 15 additional facet pairs.
All selected cells must be present simultaneously, so their inequalities
are intersected, not checked independently. If an open common shift exists,
every listed cell is realized in one nonsingular AKN tiling.

The exact decision procedure uses an independently implemented integer
ring Z[tau] (tau^2=tau+1), exact sign tests via sqrt(5), reduction to the
tightest halfspace in each oriented-normal direction, and strict
Fourier-Motzkin elimination over three coordinates.

Eliminating a variable combines a positive-coefficient and a
negative-coefficient constraint with *positive* multipliers. A resulting
constant 0 < b with b <= 0 rejects strict feasibility. Otherwise the
elimination steps can be reversed to select a point between strict bounds.
No floating-point tolerance is used anywhere in the decision.

**Interpretation:** Rejection means no *generic* true-AKN shift can contain
all required cells. Equality-only obstructions could potentially be
realized by singular boundary conventions and require separate analysis.
An infeasible open intersection is not proof that the same unlabeled
combinatorial patch cannot occur in another orientation, a different lift,
or a boundary-selection variant. The current test fixes the certificate's
six signed axes and the natural Z^6 relative lift, and allows a free common
shift of that lift.

## Exact radius-two census (research result awaiting exact-head CI)

A separately implemented BigInt Z[tau] strict-elimination calculation
reconstructed all 576 periodic vertex patches and found:

| Centered patches | Count |
| --- | ---: |
| Radius 1, generic feasible | 576 |
| Radius 2, generic feasible | 286 |
| Radius 2, no strict common-shift solution | 290 |
| Of those, closed-halfspace intersection nonempty (boundary only) | 287 |
| Of those, even the closed intersection is empty | 3 |

These are **not atlas class counts**, nor do they show 290 distinct defect
types. The first strict-elimination contradiction can be a zero-margin equality
even when stronger constraints elsewhere make the **closed** system empty.
Each rejected patch is therefore tested again using non-strict Fourier-Motzkin
elimination. Only closed-feasible patches are classified boundary-only.
All open and closed rejection proofs are replayed from strictly positive
linear combinations of the original halfspaces. The committed Python implementation and GitHub CI
must corroborate this preliminary count before treating the census as an
accepted exact numerical result. A separate reproducible positive witness
and contradiction trace for each distinct patch would strengthen the
packet further.

## Finite hyperplane arrangement for an exhaustive radius-one atlas proof

At a generic vertex, the complete 160 candidate incident cells are
enumerated by choosing a 3-axis set I (20 choices) and one of 8 corners.
Cell presence can change only when one of its complementary window
inequalities becomes an equality. Every facet normal is parallel to
W_i x W_j for one of 15 unordered 6-axis pairs.

For each axis pair (i,j), the exact transition levels on

    2 dot(W_i x W_j, gamma)

are the expressions

    dot(N, sum_{k in I}(1-2*S_k)*W_k) +/- H_{I,N}

for all I disjoint from (i,j) and S in {0,1}^3, together with the vertex
window thresholds +/- H_{W,N}.

Direct exact enumeration in Z[tau] reduces to **nine distinct levels for
each of fifteen normal directions, 135 candidate planes in total**.

This is an exact finite arrangement *definition*, not a proof that the
resulting chambers have only 24 AKN star classes. The completeness theorem
still requires:

1. Enumerate **all nonempty open chambers** inside the vertex window.
2. Produce an exact interior witness for each chamber.
3. Compute and canonicalize the complete 160-choice incident-cell star.
4. Show every chamber maps to one of the 24 classes, with no unclassified
   chambers, and audit boundary/singular configurations separately.
5. Store a compact chamber cover / adjacency certificate that an
   independent checker can reconstruct and reject when truncated.

Until that exhaustive enumeration is committed, atlas completeness is
**literature-supported and not mechanically certified**.

## Reproduction

From the repository root:

    python research/akn/radius2_exact.py --json
    python research/akn/atlas_arrangement.py
    python -m unittest discover -s tests -v

All scripts use Python's standard library only. The new radius-two checker
does not import the earlier AKN geometry/checker or third-party packages.

## Mathematical firewalls

- Existing AKN-ATLAS-PERIODIC remains finite-domain and unchanged.
- The separately registered AKN-3-2-RADIUS2 is **only** this exact finite
  576-center census and the associated generic patch-membership test.
- Failure of radius-two admissibility for this single periodic approximant
  does **not** prove that every periodic tiling violates radius-two rules.
- No claim of an all-radii aperiodicity theorem, minimal radius, perfect
  matching rule, decoration minimality, atlas exhaustiveness, or novelty.
- Singularity/boundary rules, local-isomorphism conventions and arbitrary
  non-conjugate lifts are **separate** questions.
