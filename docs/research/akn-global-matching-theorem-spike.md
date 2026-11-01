# AKN global matching-rule theorem: falsifiable proof spike

**Parent:** KATZ-AKN-PERFECT — **Status: open, unchanged**  
**Date:** 2026-11-01  
**Scope:** exact algebraic lemmas, finite counterexample, conditional global bridges, and explicit unproved obligations. Not a new proof of the Katz theorem or a priority claim.

## C2: the theorem to establish

Fix a finite, explicit inventory D of decorated prolate/oblate rhombohedra, oriented face labels, and matching conditions. Let X_D contain **every complete infinite face-to-face tiling** admitting a globally consistent D-decoration (not just periodically decorated tilings or a seeded growth run). Fix the intended *closed* canonical irrational AKN translation hull X_AKN, including a stated singular-boundary convention.

**Global perfection (still open for an explicitly transcribed D):** every tiling in X_D, after forgetting labels, belongs to X_AKN. If equality of decorated and undecorated languages is claimed, additionally prove that every intended AKN tiling admits a legal decoration.

Aperiodicity, weak perpendicular boundedness, one-radius atlas equality and local growth are individually insufficient to establish this target. C1(D) and C2(D) do not imply one another without additional hypotheses.

## Proven algebraic lemma: the bare integer height already exists

Write the six physical edge directions as e_i=A_i+τ B_i, where τ²=τ+1. Stack the coefficient matrices M=[A;B]. Exact determinant: **det(M)=8**.

If a closed walk in the golden-rhombohedron edge graph has net signed-axis count n∈ℤ⁶, then its physical displacement A n+τ B n is zero. Irrationality of τ and det(M)≠0 imply n=0. Consequently, every connected tiling by these oriented rhombohedra already has a path-independent vertex lift h:V→ℤ⁶, unique up to translation. The same determinant proves injectivity of the true perpendicular projection A+(1−τ)B on ℤ⁶.

**Warning:** simple cochain integrability is automatic even for the certified *periodic* radius-one atlas counterexample. A decorated Ammann-bar/plane cochain may carry extra information; do not conflate it with this trivial coordinate cochain. Global matching must **add** slope or window restrictions.

## Conditional global aperiodicity theorem (proved)

Suppose every D-legal complete tiling T obeys, for some γ and some finite C_T, the bound

    || π_perp(h(v)) − γ || ≤ C_T   for every vertex v.

Then T has no nonzero translational period. If t is a nonzero period, the unique integer lift gives h(v+t)−h(v)=q≠0 independent of v. Repeating t k times gives an internal displacement k π_perp(q). Uniform boundedness forces π_perp(q)=0, contradicting injectivity on ℤ⁶. Even sublinear displacement along a period orbit suffices.

**Unproved hypothesis:** that any *particular finite decorated face-matching rule* enforces the required bound. Proving this yields **weak aperiodicity**, not perfection.

## Exact finite counterexample: two remote cells, disjoint closed windows

The 3/2 certificate has period lift L₁=(3,3,2,−2,0,0), physical displacement (0,4+6τ,0) and true perpendicular displacement (0,10−6τ,0). The existing cell with 6D base (0,0,−1,0,0,0), zero-based axes I=(1,2,4), and its translate by three L₁ have complementary window normal N=W₀×W₅. Exact values:

    δ = ⟨π_perp(L₁),N⟩ = −10 + 6τ
    H = Σ_{j∉I}|⟨W_j,N⟩| = 4 − 2τ
    2|δ| ≤ H < 3|δ|.

Therefore, even using **closed** acceptance windows, those two cells cannot have a *single common AKN phase*. The executable checker verifies the exact Z[τ] inequalities and rejects corrupt period lattices. They are separated by three physical periods: the witness has small *cardinality* (two cells) but not necessarily bounded *geometric diameter*. It is **not** a local decorated-rule theorem.

## Conditional global phase-coherence theorem (proved)

For a fixed oriented ℤ⁶-lift, each required cell c has a closed convex acceptance set K_c of allowable true internal shifts. Fix a justified compact convex normalization box K; put F_c=K∩K_c. If every subfamily of **at most four** F_c intersects, there exists one global γ in the intersection of all F_c.

Proof: Helly's theorem in dimension 3 implies that each finite subfamily intersects. The nonempty closed subsets of compact K satisfy the finite intersection property, so their total intersection is nonempty.

**Critical gap:** four-wise means cells anywhere in the infinite tiling. Helly bounds contradiction *cardinality*, not *spatial radius*. Also global weak containment of required cells does not establish that all and only the canonical cells occur; saturation and singular boundary choices remain.

The missing local-to-global theorem must force a **uniform local transport bound** so that every remotely inconsistent four-cell phase constraint produces a bounded-radius forbidden decorated configuration. This is a specific falsifiable target for the Katz topological proof.

## Conditional strong global theorem via patch-language exhaustion (proved)

Let X_AKN be closed in the finite-local-complexity tiling topology. If for an unbounded sequence of radii r_k **every** radius-r_k patch of **every** globally D-legal tiling occurs in X_AKN (with precisely fixed translations/rotations), then every D-legal tiling belongs to X_AKN.

Proof: for a fixed T and each k pick S_k∈X_AKN whose central r_k patch agrees with T. Then S_k converges to T locally; closedness of X_AKN yields T∈X_AKN.

This is mathematically valid but **not a finite certificate**: checking finitely many k does not imply all-k coverage. A possible finite-to-infinite bridge is a genuinely recognizable collared supertile hierarchy, with an exactly proved induction preserving *all* supertile interiors, boundaries and seam/corner configurations. No such induction is certified here.

## Stronger bridge proved: four-wise *open* phase consistency forces the AKN hull

The previous closed-Helly result is deliberately weak: it may select a
singular phase, and it assumes a compact normalization box. For the actual
**closed local-isomorphism hull**, both limitations can be avoided by
working with open cell windows and finite-patch convergence.

For a fixed oriented integer height h on an infinite, locally finite,
complete face-to-face tiling T, every lifted cell c=(n,I) has an **open,
convex, nonempty** true-perpendicular acceptance region

    U_c = π_perp(n + 1_I/2) + int Z(W_{I^c})  ⊂ ℝ³,

with W_i=A_i+(1−τ)B_i. Use one consistent global h for all cells; no
independent relifting of distant patches is permitted.

**Theorem (Helly–patch local-isomorphism criterion).** Assume every
subcollection of at most four required cells of T has a common phase:

    ∀F ⊂ Cells(T), |F| ≤ 4 :  ⋂_{c∈F} U_c ≠ ∅.

Then **T belongs to the closed hull X_AKN of generic canonical AKN
cut-and-project tilings** (with precisely these physical axes and
orientation conventions).

**Proof.** Fix any finite F of cells. Its open convex sets U_c satisfy
the four-wise intersection hypothesis, so finite-dimensional Helly's
theorem gives a nonempty **open** intersection U_F. The nongeneric
shifts for the canonical selection are contained in a countable union
of affine selection-boundary planes, and cannot exhaust U_F. Choose a
fully generic γ_F∈U_F. The canonical cut-and-project tiling S_F
contains each required cell of F **at exactly the same physical
position**, after fixing the integer lift's origin.

Now fix any growing ball B_R and let F_R be all tiles of T meeting a
slightly larger ball B_{R+1}; local finiteness makes F_R finite. Since
both T and S_{F_R} are complete tilings with disjoint cell interiors
and S_{F_R} contains every T-cell covering B_R, no extra S-cell can
intrude into B_R. Thus S_{F_R} and T agree on B_R. The sequence
S_{F_R} converges locally to T, so T∈X_AKN by closedness. QED.

**Why this is stronger than the closed-phase bridge:** There need not
be one common γ for the **entire infinite tiling**. Compactness of a
single phase box and an independent missing-cell/saturation check are
not necessary for this *hull membership* conclusion. Complete
face-to-face coverage, canonical tiling existence for generic phases,
a consistent lifted origin, and the open four-wise assumption are all
essential hypotheses. Singular limit tilings are allowed because the
target hull is **closed**, even though the finite witnesses are generic.

**What is still OPEN for a concrete finite matching rule D:**
proving that *its local facet labels* force the four-wise condition for
**arbitrarily distant** cells. This theorem converts the C2 goal to a
precise globally quantified **4-cell consistency property**; it does
not make that property locally decidable. It is not an unconditional
Katz-rule proof.

**Sharpness of the Helly number.** In ℝ³, the four open convex
halfspaces x>0, y>0, z>0, x+y+z<0 have every triple intersecting but
empty four-way intersection. The new fixture checks exact integral
witnesses. Consequently, *3-wise* convex consistency is not a
generally valid replacement for 4-wise consistency without extra
special structure of the AKN windows.

### New falsifiable local-to-global obligation

To promote a **specific source-derived** decoration D to perfect, show:

1. **Well-defined global lift.** Already holds by det([A;B])=8
   for complete face-to-face tilings in the fixed AKN orientation.
2. **Decoration-to-four-wise forcing.** For *all* D-legal complete
   tilings and every four cells anywhere in the tiling, their true
   internal open windows intersect. This is the nontrivial step.
3. **Canonically selected generic tilings exist** for all generic
   shifts (an imported cut-and-project geometric theorem with
   audited hypotheses).
4. **Apply the Helly–patch criterion** to obtain T∈X_AKN.

For a finite verifier one needs a separate **uniform transport theorem**
which derives item 2 from bounded matching, without assuming it, and
which survives all legal infinite tilings. A finite-box UNSAT search,
four-wise checks on one period, or a radius-k atlas is not enough.

## No-go lemma: finite-state exact internal-height potentials cannot work

Suppose a putative facet-label proof assigns each vertex a state in a
**finite** alphabet Σ, and an exact internal value g:Σ→ℝ³, with the
edge equation

    g(state(w)) − g(state(v)) = π_perp(h(w)−h(v))

for *every* oriented edge of a complete infinite AKN-direction tiling.
Summing along paths gives g(state(v))−π_perp(h(v))=constant. Since g(Σ)
is finite, π_perp(h(V)) is finite. But π_perp is injective on the
integer height group by det([A;B])=8, and a complete locally finite
tiling has infinitely many distinct vertices: contradiction.

**Conclusion:** a finite-label grammar cannot represent the *exact*
irrational internal coordinate at each vertex by a finite-valued
potential obeying this equality. A correct proof must exploit
inequalities, multiscale transport, plane/hyperplane topology,
or a different kind of cocycle. This explicitly rules out a tempting
but impossible simplification of the phase-forcing step.

## Sound finite counterexample mechanism for a specified facet grammar

The executable `research/akn/decorated_quotient.py` reconstructs all
**1,728** oriented face pairings of the certified 576-cell period
quotient. A candidate grammar D specifies explicit oriented states:
cell shape P/O, allowed zero-based 3-axis orientations, six face labels
(low/high for each axis in sorted order), and ordered allowed
(+normal, −normal) face-label pairs.

**Proposition (SAT implies counterexample, for face-only rules).**
If a total assignment of D-states to all periodic quotient cells
passes the independently reconstructed face-gluing check, it extends
periodically to a legal decorated tiling of ℝ³, provided the entire
rule D consists of those facet-pair compatibility conditions and
per-tile state restrictions. Since the undecorated tiling is
periodic and the target AKN hull has no periodic member, D is **not**
a globally perfect matching rule.

**Proof.** Each finite quotient cell carries a permitted oriented
state. Every quotient face is paired with exactly one opposite face;
the complete check shows their labels form an allowed ordered pair.
Replicate this finite labeling along all three spatial periods.
The underlying certified quotient already glues to a face-to-face
tiling, so every face in its infinite lift inherits one of the
checked pairs. Therefore the decorated infinite lift is legal.
Its undecorated geometry has nonzero periods, contradicting
the claimed perfect target. QED.

The converse is **not** established. An exhausted UNSAT search on
one period *never proves D perfect*, does not exclude a larger
decorated period, and does not exclude **nonperiodic** decorations of
the same undecorated periodic tiling. A node cap returns
`INCONCLUSIVE`, not UNSAT. A custom parser/independent witness
checker must re-evaluate every selected tile state and every
face pairing, rather than trusting the solver's state.

The shipped `bare_control_grammar()` is an intentionally permissive
**non-Katz** demonstration: plain labels on both shapes are legal
everywhere, so the actual 576-cell periodic witness passes. The
intentionally inconsistent plain/different grammar is a finite
negative test. Neither says anything about the unpublished,
untranscribed detailed Katz (1988) face inventory.

**Primary source gate:** no variant table may be called
`Katz-1988` or treated as a proof-relevant candidate until its
orientation, rotation, reflection and decorated-prototile counting
conventions are transcribed with exact page citations and audited
against the paper. If Katz requires additional vertex/plane
conditions, the grammar and checker must support them *before*
the SAT soundness proposition is applied to Katz's full D.

## Proof routes and acceptance checkpoints

| Route | Finite/reproducible stage | Global obligation | Status |
| --- | --- | --- | --- |
| Katz (1988) decorated facets | Transcribe the original oriented face-label inventory and matching table with page-level provenance. | Reconstruct its actual algebraic-topological forbidden-plane/phase-forcing argument and precise singular convention. | Published theorem reported in **abstract**, not machine-reproduced. |
| Helly + height | Exact Z[τ] windows and 2–4-cell contradiction certificates. | Bounded-distance transport of remote phase contradictions, then canonical saturation and singular analysis. | Conditional bridge proved, transfer open. |
| Hierarchical forcing | Explicit collared substitutions, child placements and all boundary contacts. | An all-level induction that forces the complete AKN patch language. | Proposed; no AKN induction certificate. |

**Next concrete experiment:** obtain and inspect Katz (1988), CMP 118:263–288, DOI 10.1007/BF01218580; transcribe its facet decoration inventory. Build an orientation-aware constraint search on the committed periodic certificate. A **satisfying periodic decorated witness** disproves perfection for that D. An UNSAT periodic-box search is **inconclusive**: larger-period or nonperiodic decorations can still exist. Then attempt the uniform remote-conflict transport lemma, not another fixed-radius census.

## Reproduction and governance

Run the standard-library-only obstruction checker and negative controls:

    python research/akn/global_rule_obstruction.py
    python research/akn/decorated_quotient.py
    python -m unittest discover -s tests -p 'test_akn_global_rule_obstruction.py' -v
    python -m unittest discover -s tests -p 'test_akn_decorated_quotient.py' -v

The checker is independent of PR #22 (radius-two 286/287/3, provisional exact-head) and stacked PR #23 (generic chamber enumeration, also pending). The new spike does **not** silently import their pending findings.

**Statuses unchanged:** KATZ-AKN-PERFECT=open; KATZ-AKN-C1=candidate; AKN-ATLAS-PERIODIC=finite-domain. This document registers no new unconditional global claim.

**Literature scope:** Katz (1988) abstract reports decorated-facet quasiperiodicity using algebraic topology without self-similarity; the proof body was not retrieved. Levitov (1988), DOI 10.1007/BF01218348, distinguishes strong and weak local rules. Socolar (1990), DOI 10.1007/BF02097107, develops weak rules. Hann–Socolar–Steinhardt (2016), DOI 10.1103/PhysRevB.94.014113, uses an additional decorated catalog. None of these facts is a proof of a novel optimized global decoration in this repository.
