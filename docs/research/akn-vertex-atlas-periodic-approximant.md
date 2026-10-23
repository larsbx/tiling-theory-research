# AKN vertex atlas admits a periodic tiling

**Claim ID:** AKN-ATLAS-PERIODIC  
**Status:** finite-domain  
**Date opened:** 2026-10-16  
**Scope:** exact certificate committed under `research/akn/`; regression-tested in `tests/test_akn_approximant.py`.

## Statement

Notation: `e_i = A_i + tau B_i` (`i = 1..6`) are the six 5-fold axes in `research/akn/geometry.py`,
`pi_par(n) = sum n_i e_i`, and `pi_x(n) = sum n_i e_i|_{tau -> x}`. A *vertex star* is the set of
cells at a vertex, read as signed edge triples, up to the icosahedral group `I_h` (order 120).

**Proposition (3/2 approximant).** Let `x = -2/3` (the 3/2 approximant of `tau' = -1/tau`) and
let `gamma` be the rational shift in `research/akn/certificate_3_2.json`. The canonically
selected 3-cells, realized by `pi_par` as golden rhombohedra, form a face-to-face tiling `T` of
`R^3` such that

1. `T` is periodic with period lattice `pi_par(L) = 2 tau^4 Z^3` (simple cubic), where `L` is the
   saturated rank-3 kernel of `pi_x` on `Z^6`;
2. one period holds 576 vertices, 356 prolate and 220 oblate cells (volume = covolume
   `(2 tau^4)^3 = 1288 + 576 sqrt5`);
3. every vertex star of `T` is `I_h`-equivalent to a vertex star occurring in the AKN tiling;
   21 of the 24 atlas classes occur.

**Status:** finite-domain: items 1-3 are checked exactly by `research/akn/certify.py`.

## What the certificate checks

`certify.py` uses no window test. From `L` and the vertex/cell representatives in `Z^6` it checks,
in exact `Q(sqrt5)` arithmetic:

- `L` lies in `ker pi_x`, `pi_x` has rank 3 and `L` is saturated (gcd of 3x3 minors is 1), so
  `pi_x(n)` labels `n mod L` faithfully;
- each cell corner is a listed vertex; each 2-face lies in exactly two cells, on opposite sides;
- dihedral angles (all multiples of `pi/5`, matched exactly via `cos^2`) sum to `2 pi` around
  every edge; corner solid angles sum to `4 pi` around every vertex;
- the summed cell volume equals the covolume of `pi_par(L)`.

The face, edge and vertex conditions make the glued complex a closed 3-manifold mapping to
`R^3 / pi_par(L)` by a local homeomorphism, hence a finite covering; the volume identity makes it
one-sheeted. So the cells lift to a tiling of `R^3`. Each star is then looked up in
`research/akn/atlas.json`, whose 24 classes each carry a rational shift `gamma` at which the star
is re-derived exactly in the true (irrational) AKN cut-and-project, so every atlas class occurs
in a genuine AKN tiling.

## Consequence

A perfect local rule forces every legal tiling into the AKN local-isomorphism class, which has
no periodic member, so the 24 undecorated vertex stars are not a perfect local rule. They are not
a weak local rule either, in Levitov's sense of bounded perp-space deviation from a plane of the
icosahedral slope: the `Z^6` lift of `T` stays within bounded distance of the rational plane
`ker pi_x`, which is not parallel to `pi_par`'s plane, so its distance from every translate of
that plane grows linearly. Decorations, or a larger radius, are therefore necessary. This agrees
with Katz (1988) and Levitov (1988), whose icosahedral results concern decorated rules and
weak rules.

This deduction uses the standard definitions and is not separately machine-checked; the
finite-domain status covers items 1-3 above.

## Provenance and limits

- **Atlas.** `atlas.py 200000 20261016` samples the AKN window uniformly; samples within `1e-9`
  of a selection boundary are dropped. It finds 24 classes (rarest: 159 hits), including the
  icosahedral `P20,O0` and three distinct `P10,O10` types. Completeness of the atlas is not
  certified here; it matches the 24 configurations reported in the literature and is not needed
  for item 3, which only requires membership.
- **Shift search.** `approximant.py` screens random rational shifts in floats, then rebuilds the
  first clean one exactly. Screening 200 shifts (seed 1) gives clean shifts for 3/2 in 3/200,
  for 5/3 in 14/200, and for 2/1 in 0/200. The 1/1 slope `x = -1` has coplanar perp triples, so
  canonical selection is degenerate. These rates are non-authoritative float screens; only the
  committed certificate is exact.
- **Novelty.** Unresolved; no priority is claimed. The audit below records the inspected
  material and three primary-source bodies that remain inaccessible.

## Literature audit (2026-10-16; continued 2026-10-17)

**Audit outcome: incomplete primary-source access; novelty and priority unresolved.**
No explicit periodic all-atlas example was identified in the material actually inspected.
This is a bounded search result, not a finding that the result is absent from the literature
or even from the three requested sources. All three bodies remain unexamined. The first
search, merged in PR #16, is extended here without changing the certificate's claim class.

### Three requested sources: access and evidentiary limits

| Source | Material actually obtained | Finding and remaining gap |
| --- | --- | --- |
| Katz (1989), chapter 4, pp. 147-182, DOI [10.1016/B978-0-12-040602-9.50009-9](https://doi.org/10.1016/B978-0-12-040602-9.50009-9) | [ScienceDirect chapter preview](https://www.sciencedirect.com/science/chapter/bookseries/pii/B9780120406029500099): title, author, pagination and references; no chapter body. [Google Books](https://books.google.com/books?id=OToVjZW9CKMC&pg=PA147) returned a page-unavailable notice, not the chapter. | The 24-count attribution remains mediated by HSS (2016). Neither a periodic example nor its absence can be inferred from the preview. The construction, local definitions and matching-rule discussion on pp. 147-182 still require inspection. |
| Kramer-Neri (1984), Acta Cryst. A40, 580-587, DOI [10.1107/S0108767384001203](https://doi.org/10.1107/S0108767384001203) | [IUCr abstract/access page](https://journals.iucr.org/paper?buy=yes&cnor=a23126); its linked PDF route returned an access/purchase page (also HTTP 401 through another reader). | The abstract describes a periodic projected cubic n-grid with subgroup S(n), and separately a nonperiodic 12-grid projected to three dimensions with subgroup A(5). It does not state that a periodic tiling has only the 24 ideal vertex stars. The body's constructions and their relation to the repository's fixed golden-rhombohedron realization remain unchecked. |
| Ben-Abraham, Baake, Kramer, Schlottmann (1993), J. Non-Cryst. Solids 153-154, 132-136, DOI [10.1016/0022-3093(93)90329-V](https://doi.org/10.1016/0022-3093(93)90329-V) | [Author-institution abstract](https://cris.bgu.ac.il/en/publications/regular-and-defective-vertex-configurations-in-icosahedral-struct-4/) and [publisher access page](https://www.sciencedirect.com/science/article/abs/pii/002230939390329V). Publisher retrieval exposed no body; one route returned HTTP 429. | The abstract gives 5450 configurations, a penalty based on distances between dual acceptance domains, and rank/degree classifications. It does not mention periodic tilings. That observation is limited to the abstract; pp. 132-136 remain unread. |

Exact-title, DOI, author/publication-list and book-preview searches did not yield accessible
full copies of these three works. Search hits and citation lists were treated as discovery
leads, not as evidence of what the unread bodies contain. In particular, the distinct
Kramer-Neri conference contribution, DOI 10.1007/BFb0016179, and the 1985 correction,
DOI 10.1107/S0108767385001350, must not be silently substituted for the 1984 article.

### Additional primary evidence actually inspected

**Baake et al. (1994): accessible full-text extraction.** The author-hosted
[scan](https://bendwavy.org/klitzing/pdf/localConfigs.pdf) of *Classification of local
configurations in quasicrystals* was obtained; relevant text was inspected in §§5-9.
Section 5, pp. 559-560, counts 24 ideal geometries (32 with enantiomers separate) and
5450 random-tiling geometries (10527 with enantiomers separate). Table 2 (p. 558)
lists the ideal vertices; its accompanying text attributes adaptation to the 1990 and
1993 papers. Section 7, pp. 562-563, enumerates stars by exact covering of angular sectors.
Section 8 (p. 563) distinguishes regular configurations from zero-defectivity singular
ones, defines rank by dual-overlap dimension, and treats a vertex as order 1, with
higher orders involving larger complete shells. Section 9 explicitly limits the study
to order 1. No periodic all-atlas construction was identified in these sections.
This is direct evidence from the 1994 paper, not a full-text audit of the 1993 paper.
The 24/32 distinction concerns reflections, not decorations; its terminology also warns
against equating zero penalty with membership in the regular atlas.

**Katz (1988): publisher abstract only in this continuation.** The
[publisher abstract](https://link.springer.com/article/10.1007/BF01218580) explicitly
states that facet decorations force tilings by the two Ammann rhombohedra to be
quasiperiodic Penrose tilings, using an algebraic-topological proof. Thus a stronger
positive matching-rule statement for a *decorated* system is already in the literature.
The body and the particular decoration inventory were not verified here. This statement
does not assert the sufficiency of the 24 undecorated stars and does not contradict the
periodic witness.

**Hann-Socolar-Steinhardt (2016): carried forward from PR #16's full-text reading.**
HSS distinguish 24 geometric configurations, attributed to Katz (1989), from their own
39 decorated configurations. Their growth construction uses the decorated catalog.
Their discussion distinguishes weak Ammann matching rules from Katz's perfect decorated
rules. The 39 count is not attributed to the unread 1989 chapter.

### Comparison with the certificate

| Constraint or construction | What would be needed for equivalence or a stronger conclusion |
| --- | --- |
| Undecorated vertex atlas | A global periodic face-to-face tiling in which **every** star occurs in the ideal AKN tiling. Independent local admissibility is the property certified here; it does not supply a globally compatible decoration. |
| Periodic rational approximant | The same golden rhombohedra and allowed orientations, a periodic realization, and an all-vertices atlas-membership check. The name “3/2 approximant,” periodicity alone, or small average defect density is insufficient. A claimed identical example additionally needs a coordinate/shift and period-cell correspondence. |
| Decorated matching rule | Compatibility of the extra labels across the whole tiling. Forgetting labels can identify distinct decorated states; an undecorated periodic witness need not admit the decorations. |
| Larger-radius local constraints | Membership of whole multi-star patches in the ideal patch language, with an explicit radius/shell convention. Single-star membership supplies no radius-2 conclusion; the 1994 shell convention is not automatically identical to the thread's edge-neighbour convention. |

These comparisons are the present audit's reasoning, not additional statements attributed
to an unread source. The finite-domain registration still covers only Statement items 1-3.
The matching-rule deduction above remains prose reasoning, not a separately machine-checked
claim. No impossibility at every finite radius, minimality of 576 vertices, or priority follows.

**Remaining closure obligation.** Obtain and read Katz (1989) pp. 147-182, Kramer-Neri
(1984) pp. 580-587, and Ben-Abraham et al. (1993) pp. 132-136. For each, record page-level
evidence on periodic constructions, all-star admissibility, decorations and larger patches.
If a related approximant is found, compare its coordinates and selection shift before
calling it the same example. Until then the correct conclusion is “not identified in the
material inspected; three primary-source bodies inaccessible,” not “absent from the
standard references.” Even a completed negative search would not establish novelty.

## Thread observations not reproduced here

These are kept as pending evidence requirements, not repository facts:

1. An assembler count of 24 admissible + 5426 non-admissible = 5450 vertex configurations,
   matching *Regular and defective vertex configurations in icosahedral structures*,
   J. Non-Cryst. Solids 153-154 (1993). This is the corona universe `KATZ-AKN-C1` needs.
2. Radius-2 stars (a star plus its edge-neighbours' stars): 253 AKN classes from 60k samples;
   the defective-vertex fraction in cubic approximants falls with order while the count per
   period grows, so cubic approximants cannot decide radius 2 either way.
3. A thread-level search snippet was interpreted as qualifying a 14 + 8 decoration count.
   The full passage and its referent remain unverified; do not attribute that interpretation
   to Katz until the primary text is inspected.

## Reproduce

```sh
cd research/akn
python certify.py certificate_3_2.json atlas.json          # stdlib only, ~10 s
python atlas.py 200000 20261016 atlas.json                 # numpy, ~4 min
python approximant.py 3 2 40 0 certificate_3_2.json        # numpy, ~45 s
```

## Sources

- P. Kramer, R. Neri, *On periodic and non-periodic space fillings of E^m obtained by projection*, Acta Cryst. A40 (1984), 580-587, https://doi.org/10.1107/S0108767384001203.
- A. Katz, *Theory of matching rules for the 3-dimensional Penrose tilings*, Comm. Math. Phys. 118 (1988), doi:10.1007/BF01218580.
- L. S. Levitov, *Local rules for quasicrystals*, Comm. Math. Phys. 119 (1988), doi:10.1007/BF01218348.
- S. I. Ben-Abraham, M. Baake, P. Kramer, M. Schlottmann, *Regular and defective vertex configurations in icosahedral structures*, J. Non-Cryst. Solids 153-154 (1993), 132-136, https://doi.org/10.1016/0022-3093(93)90329-V.
- A. Katz, *Some local properties of the three-dimensional Penrose tilings*, in M. Jarić (ed.), *Introduction to the Mathematics of Quasicrystals*, Aperiodicity and Order vol. 2, ch. 4, Academic Press (1989), 147-182, https://doi.org/10.1016/B978-0-12-040602-9.50009-9.
- J. E. S. Socolar, *Weak matching rules for quasicrystals*, Comm. Math. Phys. 129 (1990) 599-619, doi:10.1007/BF02097107.
- C. Hann, J. E. S. Socolar, P. J. Steinhardt, *Local growth of icosahedral quasicrystalline tilings*, arXiv:1604.02479 (2016).

- M. Baake, S. I. Ben-Abraham, R. Klitzing, P. Kramer, M. Schlottman, *Classification of local configurations in quasicrystals*, Acta Cryst. A50 (1994), 553-566, https://doi.org/10.1107/S0108767394001649. The publisher spells the last surname “Schlottman”; the 1993 record uses “Schlottmann”.

Consulted in the initial 2026-10-16 search (context only; none states or refutes item 3):

- *Regular and defective vertex configurations in icosahedral structures* (1993), abstract: https://cris.bgu.ac.il/en/publications/regular-and-defective-vertex-configurations-in-icosahedral-struct-2/
- *Non-spiky density of states of an icosahedral quasicrystal*, arXiv:cond-mat/0006018 (cubic `F_{n+1}/F_n` approximants, `Pa-3`).
- *The atomic structure of the Bergman-type icosahedral quasicrystal based on the Ammann-Kramer-Neri tiling*, Acta Cryst. A76 (2020) 180-196, doi:10.1107/S2053273319017339 (search summary only; full text returned 403).
- *Canonical-Cell Tilings and their Atomic Decorations*, https://www.researchgate.net/publication/379318523 (search summary only).
- *Random tiling quasicrystals in three dimensions*, arXiv:cond-mat/9706117 (24 canonical vs 5450 random-tiling vertices; search summary only).
- *Cluster packing geometry for Al-based F-type icosahedral alloys*, arXiv:1301.6823 (3/2 cubic packing; search summary only).
