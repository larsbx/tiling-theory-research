# Phase 4: exact return-vector coverage and coincidence reachability

**Claim ID:** PH4-OVERLAP-GRAPH  
**Status:** finite-domain

The committed exact graph has **64 states, each with a coincidence continuation of
length at most five**. This repairs the source-coverage gap for the explicitly
specified substitution-language tilings below. It does not rehabilitate the old
32-state graph as a complete source universe or assert a spectral theorem.

**Claim ID:** PH4-LEGAL-COVERAGE  
**Status:** conditional

The implication is conditional on the language/geometry hypotheses stated below;
the covering bound is proved here under those hypotheses, independently of finite
word enumeration. No claim is made about arbitrary symbolic sequences, decorated
extensions, other suspensions, or other substitutions.

## Scope and conventions

Fix σ(a)=aab, σ(b)=ba, τ=(1+√5)/2, τ'=(1−√5)/2,
λ=τ², ρ=(τ')²=(3−√5)/2. Lengths are ℓ_a=τ, ℓ_b=1.
Use column abelianization, M=[[2,1],[1,1]],
e(x,y)=τx+y and c(x,y)=τ'x+y. In particular c(Mv)=ρc(v),
and 0<ρ<1.

A language-legal tiling here is a tiling of the line by these two labeled
intervals whose every finite consecutive tile word occurs as a factor of some
σⁿ(k), k∈{a,b}. Tile starts have integral relative prefix coordinates. Absolute
origin is immaterial. We use interior intersection: touching endpoints do not
constitute overlaps.

A return vector Y is the integral displacement between two starts of the same
type in a language-legal tiling. Both signs and zero are allowed. For starts u,v
of types i,j and such a return Y, the overlap state is
(i,j,d), d=v−u−Y, with −ℓ_j<e(d)<ℓ_i. The return witnesses and the two compared
tiles can be anywhere in the tiling. The bound also covers returns witnessed in
a different tiling of this same language, although that enlargement is not
needed. Injectivity of e on ℤ² makes the integral representation unambiguous.

## Prefix bound, then return bound, then initial-overlap bound

The proper-prefix digit vectors for individual children are

- a→aab: (0,0), (1,0), (2,0);
- b→ba: (0,0), (0,1).

Their c-values lie in [2τ',1]. Every tile start p inside σⁿ(k), measured from
that supertile's start, has an ancestry expansion

\[
p=\sum_{h=0}^{n-1}M^h d_h.
\]

This follows by repeatedly writing a child position as M times its parent
position plus its proper-prefix digit; it needs no recognizability or canonical
ancestry for an infinite tiling. For n=0 the sum is empty. Since ρ is positive,

\[
2\tau'\sum_{h=0}^{n-1}\rho^h\le c(p)\le
\sum_{h=0}^{n-1}\rho^h,
\qquad -2\le c(p)\le\tau,
\]

using 2τ'/(1−ρ)=−2 and 1/(1−ρ)=τ. Thus the difference between any two tile
starts in one legal supertile has |c|≤τ+2=:R=(5+√5)/2.
For any two starts in a language-legal tiling, a finite word containing both
occurs in some supertile. Their relative displacement is unchanged by the
embedding, so **the same bound applies at arbitrary separation**, not just at
the word depths used by the computation. In particular |c(Y)|≤R for every legal
return vector, and |c(v−u)|≤R. Consequently every legal initial overlap obeys

\[
\boxed{|c(d)|\le 2R=5+\sqrt5=:B.}
\]

This is a proved complete covering bound for the stated language, not an
observed cutoff. It is deliberately conservative; no optimality is asserted.
It uses bounded legal return coordinates, not the zero-seeded displacement
recurrence. The two overlapping tiles need not be the return-witness tiles.

## Finite potential universe and exact closure

Let U consist of all (i,j,(x,y)) with integral x,y,
−ℓ_j<e(x,y)<ℓ_i and |c(x,y)|≤B. This is a **potential superset** of the legal
states, not an assertion of simultaneous realizability of every member.

The physical window implies |e|<τ. Inverting the two embeddings gives

\[
x=(e-c)/\sqrt5,\qquad y=(\tau c-\tau'e)/\sqrt5.
\]

Therefore |x|<(τ+B)/√5 and
|y|<(τB+|τ'|τ)/√5. Exact outward rounding gives the safe enumeration rectangle
|x|≤4, |y|≤6. Filtering that entire rectangle gives exactly 64 states.
The code derives the rectangle from the bounds; it does not choose a search
radius by experimentation.

A child pair with digits p,q has displacement Md+q−p. The digit spread is
1−2τ'=√5, so

\[
|c(Md+q-p)|\le\rho B+\sqrt5 < B.
\]

Retain every child pair with interior intersection. Hence U is forward-closed.
The graph builder additionally rejects any escaping descendant, rather than
silently dropping it. It has 142 distinct directed edges (parallel child
realizations of the same edge are collapsed).

Reverse breadth-first search from (a,a,0),(b,b,0) gives:

| Shortest coincidence distance | Number of states |
| ---: | ---: |
| 0 | 2 |
| 1 | 8 |
| 2 | 28 |
| 3 | 16 |
| 4 | 8 |
| 5 | 2 |

Every graph edge is a literal choice of two children of its parent tiles. If a
source is an actual overlap, that child choice is realized upon inflation of
the same configuration, with return translation MY. A same-type return remains
a return after inflation: choose the first child in each of its two identical
supertiles. Substitution also preserves language legality (substitute an
embedding in a supertile). Repeating this argument lifts every graph path from
a legal source to actual overlapping child tiles. No arbitrary-state legality
oracle is needed for this positive result: both source coverage and path
realizability have separate justifications.

Thus, for the defined language-legal tilings, **every legal return-vector
overlap has a coincident descendant within five substitutions**. The finite
packet verifies the graph part of this implication; the prefix proof and the
path-lifting argument supply its mathematical bridge. A potential source with
no coincidence path would require a legal witness before being used as a
negative overlap-coincidence result. No such source occurs here.

## Legal source enumeration and provenance

`research/phase4_overlap_coverage.py` separately enumerates the same-type return
vectors in a specified σⁿ(k), retaining an actual pair of positions for each.
For each such signed vector it compares all pairs of tile intervals in that
word using exact ordered endpoints. One full witness per resulting state is
stored: root, depth, word length, return type/positions/vector, compared
positions, four integral prefixes, and state. Repeated uses of a vector may
share its representative return pair; no claim is made to list all witnesses.

| Word | Length | Distinct signed return vectors | Witnessed states |
| --- | ---: | ---: | ---: |
| σ⁴(a) | 55 | 223 | 32 |
| σ⁴(b) | 34 | 129 | 26 |
| σ⁵(a) | 144 | 643 | 32 |
| σ⁵(b) | 89 | 389 | 32 |

The witnessed 32-state sets are **not** the historical 32-state truncation:
they include the omitted witness. Equal cardinalities must not be conflated.

These finite enumerations are sound positive witnesses and complete within
the specified word. Absence is never interpreted as illegality or global
coverage, and stabilization across depths is never used in the bound proof.

There is no extendibility assumption hidden in these positive witnesses:
both a and b occur strictly inside σ²(a)=aabaabba. Thus any σⁿ(k) embeds
inside σⁿ⁺²(a), with tiles on both sides. Iterating the interior a embedding
gives arbitrarily long legal extensions on both sides; a nested limit is a
bi-infinite language-legal tiling containing the witness.

The original witness is retained verbatim as a distinguished record:
σ⁴(a), return positions 17,25, vector (6,2), compared positions 34,43,
state (b,a,(-2,3)). Its e-value is 2−√5 and c-value is 2+√5>R.
It is outside the old 32-state ball and inside U; the new graph gives it a
coincidence continuation. The old graph remains a restricted regression only.

## Reproduction and negative controls

All decisive comparisons use rational pairs for Q(√5). Opposite-sign sums
are ordered by comparing rational squares; no float, tolerance, rounded
radical, or numerical eigensolver enters enumeration, overlap, bounds, or BFS.

```sh
python research/phase4_thread_audit.py
python research/phase4_overlap_coverage.py --check research/phase4_overlap_certificate.json
python -m unittest discover -s tests -p 'test_phase4_overlap.py' -v
```

The committed packet includes every state, all outgoing edges, shortest
distances, a decreasing-distance successor for each noncoincidence state, the
finite-word enumerations, and the original omitted witness. The check command
recomputes the complete packet and rejects any mismatch.

Tests cover the historical truncation, exact endpoint exclusions, near-zero
quadratic expressions, exhaustive small-word cross-checks of the interval
search, altered provenance, graph escapes, and corrupted certificate data.
The shared governance check registers the finite graph separately from its
hypothesis-dependent language bridge, with mutation checks on every surface.

## Remaining boundaries

- Minimality of B and an exact classification of all realizable potential
  states are not supplied and are not needed for the positive covering proof.
- Exporting a pure-point spectral conclusion needs a separately audited theorem
  with its precise dynamical hypotheses. This contribution asserts none.
- Generalization to other substitutions, non-language tilings, or different
  geometric suspensions needs new bounds and a new path correspondence.
- This is an elementary proof plus an exact executable finite certificate,
  not a Lean formalization or a claim of literature priority.

This note advances the [independent audit](phase4-weighted-overlap-audit.md);
its original negative control and warning against the 32-state promotion
remain valid. No previously registered AKN claim changes status.
