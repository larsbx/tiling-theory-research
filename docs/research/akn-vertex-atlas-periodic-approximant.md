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
- **Novelty.** Plausibly folklore; no priority is claimed. A first literature search is recorded
  below; it found no explicit prior statement, but two primary sources were not read in full.

## Literature search (2026-10-16)

Web search plus full-text reading where open access. Result: **no explicit prior statement found**
that the 24 undecorated AKN vertex geometries admit a periodic tiling; equally, nothing found that
contradicts it. Findings, by what was actually read:

- *Read in full text:* Hann, Socolar, Steinhardt (2016) state that Ammann's markings are "known to
  be at least weak matching rules" [Levitov 1988; Socolar 1990], are not rigorously proven perfect,
  and that Katz's closely related rules are. They count **24 vertex geometries** (attributed to Katz
  (1989)) **but 39 decorated vertex configurations** (from their own subdivision of perp space), and
  grow tilings from the 39-entry decorated catalog.
  This is consistent with item 3 and the Consequence section: the decoration splits atlas classes,
  so the undecorated atlas carries strictly less information than the rule they use.
- *Abstract only:* the 1993 J. Non-Cryst. Solids paper builds all 5450 combinatorially possible
  Ammann-rhombohedron vertex configurations and ranks them by a perp-space penalty; its abstract
  does not mention periodic tilings.
- *Not read (paywalled / not found online):* Katz (1989), the source HSS cite for the 24 count
  and the likeliest place for this observation; Kramer-Neri (1984) on periodic space
  fillings by projection.
- *Context:* cubic `F_{n+1}/F_n` approximants of the 3D Penrose tiling are standard in the
  quasicrystal literature (e.g. the nonsymmorphic `Pa-3` cubic approximants reached by an extra
  internal-space shift), but the sources seen do not discuss whether their vertex stars stay inside
  the AKN atlas.

Obligation to close the search: read Katz (1989) ch. 4, Kramer-Neri (1984) and the 1993 paper's
body; if none states the result, record it as "not found in the standard references" rather than as new.

## Thread observations not reproduced here

These are kept as pending evidence requirements, not repository facts:

1. An assembler count of 24 admissible + 5426 non-admissible = 5450 vertex configurations,
   matching *Regular and defective vertex configurations in icosahedral structures*,
   J. Non-Cryst. Solids 153-154 (1993). This is the corona universe `KATZ-AKN-C1` needs.
2. Radius-2 stars (a star plus its edge-neighbours' stars): 253 AKN classes from 60k samples;
   the defective-vertex fraction in cubic approximants falls with order while the count per
   period grows, so cubic approximants cannot decide radius 2 either way.
3. A search snippet of Katz's paper reads "(it is not proved that this number ...", so he
   flags the 14 + 8 decoration count as unproven himself.

## Reproduce

```sh
cd research/akn
python certify.py certificate_3_2.json atlas.json          # stdlib only, ~10 s
python atlas.py 200000 20261016 atlas.json                 # numpy, ~4 min
python approximant.py 3 2 40 0 certificate_3_2.json        # numpy, ~45 s
```

## Sources

- P. Kramer, R. Neri, *On periodic and non-periodic space fillings of E^m obtained by projection*, Acta Cryst. A40 (1984).
- A. Katz, *Theory of matching rules for the 3-dimensional Penrose tilings*, Comm. Math. Phys. 118 (1988), doi:10.1007/BF01218580.
- L. S. Levitov, *Local rules for quasicrystals*, Comm. Math. Phys. 119 (1988), doi:10.1007/BF01218348.
- *Regular and defective vertex configurations in icosahedral structures*, J. Non-Cryst. Solids 153-154 (1993).
- A. Katz, *Some local properties of the three-dimensional Penrose tilings*, in M. Jarić (ed.), *Introduction to the Mathematics of Quasicrystals*, Aperiodicity and Order vol. 2, ch. 4, Academic Press (1989).
- J. E. S. Socolar, *Weak matching rules for quasicrystals*, Comm. Math. Phys. 129 (1990) 599-619, doi:10.1007/BF02097107.
- C. Hann, J. E. S. Socolar, P. J. Steinhardt, *Local growth of icosahedral quasicrystalline tilings*, arXiv:1604.02479 (2016).

Consulted in the 2026-10-16 search (context only; none states or refutes item 3):

- *Regular and defective vertex configurations in icosahedral structures* (1993), abstract: https://cris.bgu.ac.il/en/publications/regular-and-defective-vertex-configurations-in-icosahedral-struct-2/
- *Non-spiky density of states of an icosahedral quasicrystal*, arXiv:cond-mat/0006018 (cubic `F_{n+1}/F_n` approximants, `Pa-3`).
- *The atomic structure of the Bergman-type icosahedral quasicrystal based on the Ammann-Kramer-Neri tiling*, Acta Cryst. A76 (2020) 180-196, doi:10.1107/S2053273319017339 (search summary only; full text returned 403).
- *Canonical-Cell Tilings and their Atomic Decorations*, https://www.researchgate.net/publication/379318523 (search summary only).
- *Random tiling quasicrystals in three dimensions*, arXiv:cond-mat/9706117 (24 canonical vs 5450 random-tiling vertices; search summary only).
- *Cluster packing geometry for Al-based F-type icosahedral alloys*, arXiv:1301.6823 (3/2 cubic packing; search summary only).
