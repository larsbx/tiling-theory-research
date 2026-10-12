# Katz/AKN matching rules: local-completeness target

**Claim ID:** KATZ-AKN-C1  
**Status:** candidate  
**Date opened:** 2026-10-11  
**Scope:** salvage note from a research thread; no source data or executable enumeration is committed yet.

## Salvageable core

The useful research content is not a claim that Katz's decoration count has been minimized. The defensible target is narrower:

> compute the minimum number of decorated prolate/oblate rhombohedral prototiles needed for local vertex-atlas completeness.

This separates a finite, checkable condition from the global perfection theorem.

## Background distinction

Let `AKN` denote the Ammann--Kramer--Neri / 3D Penrose rhombohedral setting, with prolate and oblate rhombohedra and Katz-style facet decorations.

The thread identified two different obligations:

- `C1`, local completeness: the vertex coronae admitted by a decoration equal the admissible AKN vertex atlas.
- `C2`, global perfection: every tiling satisfying the local matching rules belongs to the intended AKN tiling class.

Only `C1` is currently framed as a finite search problem. `C2` is the hard global matching-rule/perfection problem and must not be inferred from a finite local atlas computation.

## Formal target

Let:

- `V_AKN` be the admissible AKN vertex-corona atlas.
- `D` be a decoration scheme assigning oriented face labels to decorated prolate and oblate rhombohedra.
- `V_D` be the set of vertex coronae locally admitted by `D`.

The local-completeness condition is:

```text
C1(D): V_D = V_AKN.
```

The finite optimization problem is:

```text
m*(C1) = min_D (|D_P| + |D_O|)
```

subject to:

1. every admissible AKN vertex corona has at least one decorated lift;
2. every geometrically possible non-AKN vertex corona has no decorated lift;
3. face-gluing legality is defined over oriented rhombic faces of prolate/oblate cells;
4. symmetry-equivalent decorations are quotiented by the icosahedral action where possible.

The resulting inequality is only:

```text
m*(C1) <= m*(perfect) <= 22.
```

The upper bound records the Katz-style `14 + 8` benchmark as imported background, not as newly proved here.

## Thread-derived observations to preserve

The following items are potentially valuable, but are **not certified** until the underlying cut, atlas, and extraction scripts are committed:

1. Face-gluing extraction reportedly found 223 interior faces shared by exactly two cells and 118 boundary faces shared by one cell, consistent with a face-to-face finite patch.
2. The observed AKN gluing data reportedly collapses to three oriented face-gluing types: `P-P`, `P-O`, and `O-O`.
3. The admissible vertex-corona database reportedly contains 24 configurations with exact prolate/oblate content.
4. The size-20 all-prolate corona `P20,O0` is the high-symmetry icosahedral vertex.
5. Some size-20 prolate/oblate mixtures split into multiple geometric types; the thread specifically noted `P10,O10` as splitting into three geometric types.
6. Each rhombohedron type was treated as lying in a 10-element `I_h` orbit with stabilizer order 12; each cell has six rhombic faces.

These observations should be treated as candidate evidence requirements, not as repository facts.

## Constraint-search plan

A robust implementation should use a counterexample-guided loop rather than trusting one monolithic SAT instance.

1. Import or generate the full oriented cell/face model.
2. Import or generate the full vertex-corona universe, separating admissible AKN coronae from non-AKN coronae.
3. For a fixed pair `(m_P, m_O)`, create variables for decorated prolate and oblate prototiles.
4. Add positive constraints requiring every admissible AKN corona to have a decorated lift.
5. Solve for a candidate decoration.
6. Search for a non-AKN corona that still has a decorated lift.
7. If found, add a blocking clause and repeat.
8. If no bad corona lifts, record a finite-domain `C1` witness.
9. Sweep `m = m_P + m_O` upward to establish a lower bound.

## Certification requirements before promotion

`KATZ-AKN-C1` may be promoted from `candidate` to `finite-domain` only after the repository contains:

- the exact cut/window or combinatorial source for the rhombohedral cells;
- a deterministic face-gluing extraction;
- the complete vertex-corona atlas, including non-AKN coronae considered by the exclusion check;
- a solver-independent certificate or reproducible exhaustive search log;
- symmetry-reduction documentation showing which duplicates are quotiented;
- regression tests checking the reported face counts, gluing classes, and corona counts.

## Explicit non-claim

`KATZ-AKN-PERFECT` remains open. A proof of `C1(D)` does not prove that `D` is a perfect matching rule. A local-complete decoration may still admit globally legal non-AKN tilings or fault structures.
