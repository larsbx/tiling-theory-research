# Phase 4 audit: strong coincidence, strand-overlap coverage, and typed presentations

**Status:** candidate  
**Audit date:** 2026-10-15  
**Scope:** independent critical audit of the Phase 4 algebraic-kernel synthesis and the two-letter computations for σ(a) = aab, σ(b) = ba. This document preserves negative findings and proof obligations; it is **not** a new pure-point theorem or a certificate of full overlap-coincidence coverage.  
**Reproducer:** [research/phase4_thread_audit.py](../../research/phase4_thread_audit.py) (finite, partial graph and explicit omitted-overlap witness).

## Subsequent coverage repair (2026-10-16)

The [exact follow-up](phase4-exact-overlap-coverage.md) gives a separate
prefix/return-vector bound and a 64-state covering supergraph for the stated
substitution-language tilings. The old 32-state coverage claim remains refuted.
The reproducer now uses exact quadratic-field comparisons throughout. The
sections below retain the original audit and its broader outstanding obligations.

## Executive finding

The strong-coincidence (SC) arithmetic and the depth-two word witness withstand checking. The reported 32-state strand calculation also checks **as a finite truncated graph**, with 30 noncoincident states and maximum shortest coincidence depth four. However, an explicit legal return-vector overlap lies outside the graph's assumed contracting bound. Thus the 32-state result **cannot certify the complete overlap-coincidence criterion** until a coverage proof is supplied.

A second defect persists after earlier corrections: the one-dimensional *real stable eigenspace* was conflated with a rank-one *integer module*. A positive consequence is that the SC finite-search argument extends to diagonalizable incidence matrices with **no unit-modulus eigenvalues**, not just the irreducible Pisot class. This extension is a candidate derived proposition; external novelty and edge hypotheses have not been fully audited.

| Component | Audit classification | Disposition |
| --- | --- | --- |
| Arithmetic of σ(a)=aab, σ(b)=ba | finite-domain computation | Retain. |
| Aligned SC witness at depth two | finite-domain computation | Retain. |
| Finite SC search for irreducible Pisot inputs | conditional mathematical argument | Write formal statement and certificate construction. |
| Extension to hyperbolic diagonalizable matrices | candidate | Formalize, check literature. |
| 32-state strand graph and BFS | finite-domain, **truncated domain** | Retain as regression only. |
| Coverage of all legal overlap states by those 32 states | **refuted** | Withdraw coverage claim. |
| Rank-one projected integer displacement module | **refuted** | Replace with stable real dimension / projected-module rank distinction. |
| Full super/overlap coincidence from the 32-state graph | open | Requires correct legal overlap universe and finite bound. |
| Presentation-independent legality interface | candidate architecture | Distinguish legality from membership and MLD from factors. |

## 1. Critical coverage defect: a legal overlap omitted from the 32-state graph

Write τ = (1+√5)/2 and τ' = (1−√5)/2. For column-abelianization convention,

~~~text
M = [ [2,1], [1,1] ]
e(x,y) = τ x + y
c(x,y) = τ' x + y
λ = τ² ; λ' = (τ')²
~~~

The strand graph uses tile lengths ℓ_a = τ, ℓ_b = 1 and the ordered overlap condition

\[
-\ell_j < e(\Delta) < \ell_i.
\]

For paths **seeded at displacement zero**, the contracting-coordinate recurrence gives the legitimate invariant bound

\[
|c(\Delta)|\le R = \frac{\sqrt5}{1-\lambda'}=\sqrt5\,\tau
=\frac{5+\sqrt5}{2}\approx3.618.
\]

The mistaken inference was that this seeded bound contains **all geometrically legal return-vector overlaps**, even those whose initial displacement is not zero.

### Explicit finite-word counterexample to coverage

In the level-four word σ⁴(a), of length 55, use zero-based indices:

| Index | Letter | Abelianized prefix |
| ---: | :---: | :---: |
| 17 | a | (10,7) |
| 25 | a | (16,9) |
| 34 | b | (22,12) |
| 43 | a | (26,17) |

Positions 17 and 25 determine a same-type tile return vector

\[
y=(16,9)-(10,7)=(6,2).
\]

Compare the tiles at positions 34 and 43 under this return translation. The relative displacement is

\[
\Delta=(26,17)-(22,12)-y=\boxed{(-2,3)}.
\]

For the ordered tile pair (b,a), its physical displacement is

\[
e(-2,3)=3-2\tau=2-\sqrt5\approx-0.236.
\]

It satisfies the geometric overlap window

\[
-\tau < e(\Delta) < 1.
\]

But the contracting coordinate is

\[
c(-2,3)=3-2\tau'=2+\sqrt5\approx4.236>R.
\]

Therefore **(b,a,(-2,3)) is an explicitly realized legal overlap not represented in the 32-state truncation**. This establishes a counterexample to *coverage*, not a counterexample to overlap coincidence or pure point. The state itself has a coincidence continuation; the missing state merely shows the quantified source universe was incomplete.

### What the earlier BFS actually certifies

The finite graph contains 32 ordered states, including two coincidence states, with the following shortest-path distribution:

| Shortest coincidence distance | State count |
| ---: | ---: |
| 0 | 2 |
| 1 | 6 |
| 2 | 12 |
| 3 | 6 |
| 4 | 6 |

All 32 states in this **explicitly restricted** graph reach coincidence. The graph is useful as a test fixture, but there is no certificate that it contains every legal return-vector overlap.

**Correction required:** derive a finite initial-overlap bound from legal return vectors / potential overlaps, prove its completeness under exact geometric and FLC/Meyer hypotheses, then rerun BFS on the resulting complete graph. No claim of general Akiyama–Lee coverage may be made from the present seeded invariant ball.

## 2. The rank assertion confuses real dimension and integer-module rank

In the two-letter example the stable real eigenspace is one-dimensional:

\[
\dim_{\mathbb R}E^s=1.
\]

However its scalar projected integer displacement group is

\[
c(\mathbb Z^2)=\mathbb Z\tau'+\mathbb Z,
\]

which has \(\mathbb Z\)-rank **two** because \(\tau'\) is irrational, and is dense in \(\mathbb R\). Thus the phrase “rank-one integer displacement module” is false.

The reliable statement is that the stable *real vector-space dimension* is one in the two-letter irreducible Pisot case, affording a total order in that coordinate. Integer discreteness enters only after both expanding and contracting coordinates are bounded **together** in the original integer lattice. For irreducible characteristic polynomial of degree |A|, the stable real dimension is |A|−1; this does not imply rank |A|−1 for the projected integer subgroup.

The rank-jump account of the ≥3-letter difficulty is a **heuristic research program**, not an established complexity reduction.

## 3. Broader SC finite-search theorem candidate

For the weighted prefix-pair automaton, let

\[
\Delta_{n+1}=M\Delta_n+\delta_n,
\quad \Delta_0=0,
\]

where digit differences δ belong to a finite computable set. Suppose \(M\) is diagonalizable over \(\mathbb C\), with no eigenvalues on the unit circle. For left eigenfunctionals \(\ell_i\), eigenvalues \(\mu_i\), and \(D_i=\max_{\delta}|\ell_i(\delta)|\):

- If \(|\mu_i|<1\), all zero-seeded paths satisfy \(|\ell_i(\Delta_n)|\le D_i/(1-|\mu_i|)\).
- If \(|\mu_i|>1\), a state with \(|\ell_i(\Delta)|>D_i/(|\mu_i|-1)\) **cannot** have a future continuation reaching displacement zero.

The eigenfunctionals form an invertible coordinate map. Therefore any displacement that lies on a successful zero-to-zero path lies in a bounded real region, containing finitely many integer vectors. Finite graph search decides the aligned SC reachability property, provided the chosen weighted-automaton convention precisely represents the intended SC definition.

This covers the irreducible Pisot situation and also hyperbolic non-Pisot cases. For example,

\[
M=\begin{pmatrix}2&1\\1&3\end{pmatrix},
\qquad
\operatorname{spec}M=\left\{\frac{5+\sqrt5}{2},\frac{5-\sqrt5}{2}\right\};
\]

both eigenvalues have modulus greater than one.

**Status:** conditional mathematical argument awaiting a precise formal proposition and implementation with exact algebraic comparisons, complex eigenvalue handling, and verified path/word correspondence. Do not claim new literature priority. The earlier roadmap item “SC decidability outside Pisot: open” is **too broad**; target nonhyperbolic (notably unit-modulus) regimes instead.

## 4. Coincidence reachability is existential, not universal along paths

SC requires, for every aligned source, **some** path to a zero-displacement diagonal. It does not require all paths to coincide. A noncoincident self-loop may coexist with a path to coincidence (as it does in the truncated strand graph).

Thus a nonzero recurrent state or merely a noncoincident recurrent component is **not** by itself a negative certificate. A correct NO certificate identifies an aligned source whose **entire reachable set** in a complete finite graph avoids all coincidence targets; that reachable set is forward-closed relative to the graph.

The proposed two-letter Markov lemma must not attempt to rule out every nonzero recurrent state. The separation sweep must search for properly quantified legal noncoincident source regions, with graph completeness established independently.

## 5. Presentation transports and legality must be typed more finely

**Decorated local-rule enforcement is not automatically MLD.** Goodman–Strauss-style constructions may produce a decorated local-rule extension or a factor map. Mutual local derivability requires local maps in **both** directions and cannot be inferred simply from enforcement by matching rules. Transport certificates only under the morphism and invariant predicates explicitly justified.

**WindowPredicate is an operation inside LegalityOracle, not the whole oracle.** Single-point CPS membership differs from simultaneous patch/overlap realizability, which may require intersections of translated windows, phase coherence, boundary conventions, and lattice conditions. For example a simultaneous occurrence may impose \(W_i\cap(W_j-t^\star)\ne\varnothing\), plus further constraints. Singular boundary points require especially careful treatment.

The surviving architecture is a finite weighted-reachability core *parametrized* by state presentation, initial-state legality, geometric coverage, exact arithmetic bounds, and quantifier domain. It has not yet been shown to be fully presentation-independent.

## 6. Table cells requiring additional source or hypothesis audit

- CPS “pure point iff regular window” is not valid in this generality; regularity is an important sufficient hypothesis, not a universal characterization. Weak model sets of extremal density require separate treatment.
- The Hat/Spectre fractal-window classification as exactly automaton-definable with total boundary membership is unverified. Graph-directed windows alone do not supply an exact terminating legality procedure.
- Repetitivity/minimality for CPS requires the intended hull and window hypotheses; distinguish individual point sets from dynamical hulls.
- SFT aperiodicity complexity requires a precisely chosen predicate, especially for empty systems, periodic points, and full versus partial periods.
- “Pisot(λ) is O(1)” cannot be a uniform bit-complexity claim; say “algebraically decidable” with input representation and complexity left explicit.
- The transient-boundary observation was checked for the finite example only; no general transient-boundary theorem is established.
- Symbolic versus geometric suspension can change the action and the precise spectral statement. Shared substitution data alone is not a transfer proof.

These are **audit obligations**, not a blanket rejection of the typed-predicate method.

## 7. Repair order and claim-status firewall

1. **Formalize the SC decider** for diagonalizable hyperbolic matrices, with exact algebraic bounds and an explicit convention for strong coincidence. Seek relevant prior literature before making novelty claims.
2. **Repair geometric coverage** starting from the omitted overlap (b,a,(-2,3)): define the return-vector overlap universe and give an independently checkable finite bound that covers every legal source state.
3. **Rerun the complete overlap graph** and provide YES/NO certificates with the correct quantifier scope. Treat the 32-state graph as a regression specimen, not a full super-coincidence result.
4. **Refine presentation morphisms and legality**, distinguishing MLD equivalences, factors, decorated extensions, and simultaneous CPS window realizability.
5. **Then** conduct SC/super separation sweeps. Keep the Hat/Spectre example as a later stress test, not a substitute for basic coverage correctness.

No new pure-point theorem, general correspondence theorem, or counterexample to PSC is asserted by this audit. The key negative result is narrower but concrete: **a valid finite graph search was promoted to a complete overlap certificate without proving coverage of the initial state universe**.

## Evidence and research provenance

- Original working synthesis: *Algebraic Kernel for Substitution Tilings — Phase 4 Synthesis* (uploaded discussion artifact \`phase4-synthesis.md\`, not currently a committed repository file).
- Reproducer in this PR: [research/phase4_thread_audit.py](../../research/phase4_thread_audit.py). It now uses exact quadratic-field comparisons for the bounded graph count and inequalities; word positions and Parikh-vector identities remain integer-exact.
- Contextual sources to audit, not automatic imports: Akiyama–Lee on overlap coincidence (arXiv:1003.2898); Akiyama–Lee on coincidence relations (arXiv:1403.0377); Goodman–Strauss on matching rules; Hollander–Solomyak on two-symbol Pisot pure discreteness; weak-model-set results on extremal density.

**Promotion rule:** leave the full 3b overlap result **open** until the complete geometric state universe is proved and checked. Preserve independently verified finite calculations under their restricted domains.