# AKN rhombohedral vertex-configuration universe

**Claim ID:** AKN-CORONA-UNIVERSE  
**Status:** finite-domain  
**Date opened:** 2026-10-16  
**Scope:** exhaustive exact enumeration committed as `research/akn/corona_universe.json`; regression-tested in `tests/test_akn_corona_universe.py`.

## Statement

A *corner* is a signed axis triple `{s_a, s_b, s_c}` over three distinct 5-fold axes, i.e. the
corner of a golden rhombohedron with edge vectors `+-e_a, +-e_b, +-e_c` at a vertex. There are
`20 x 8 = 160` corners in 4 `I_h`-orbits (prolate acute, prolate other, oblate obtuse, oblate
other). A *vertex configuration* is a set of corners whose link triangles on `S^2` have pairwise
disjoint interiors and cover `S^2`. Equivalently, the cells meet face-to-face around the vertex
and fill its full solid angle `4 pi`.

**Proposition.** Up to `I_h`, there are exactly 5450 vertex configurations. They have 4 to 20
cells:

| cells | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| classes | 1 | 3 | 20 | 71 | 277 | 742 | 1531 | 1735 | 1070 |

All 24 classes of `research/akn/atlas.json` are among them, so 5426 classes lie outside the
atlas.

**Status:** finite-domain. The 5450 count and the atlas inclusion are computed exactly. The
reading "5426 non-AKN" takes the atlas to be complete; that completeness is imported from the
literature (24 AKN vertex configurations), not certified here.

The total 5450 matches "all 5450 combinatorially possible vertex configurations formed by the
Ammann rhombohedra" in *Regular and defective vertex configurations in icosahedral
structures*, J. Non-Cryst. Solids 153-154 (1993), an independent count by different means.

## Method

`research/akn/corona.py`:

1. **Conflicts.** For each pair of the 160 corner cones, interiors are disjoint iff some
   plane through 0 separates them. For simplicial cones it suffices to test the planes spanned
   by two of their rays. The test is exact in `Q(sqrt5)`.
2. **Edge-to-edge.** A geodesic between two non-antipodal icosahedral directions contains no
   third one, so adjacent link triangles share whole arcs.
3. **Exact cover.** Backtrack from each of the 4 corner-orbit representatives. Each step
   closes the open arc with the fewest compatible corners on its open side, and the search
   ends when no arc is open. Every class contains a corner from some orbit, so some `I_h`
   image of it contains that orbit's representative and is reached.
4. **Classes.** Each new labeled configuration contributes its whole `I_h` orbit to a seen-set.
   The class is recorded by its least corner bitmask.

## Independent checks (tests)

- **Sphere tiling.** Every committed configuration is a closed edge-to-edge link: each arc lies
  in two corners on opposite sides. Its corner solid angles also sum to `4 pi`, using exact
  dihedral angles in multiples of `pi/5`. A closed link of total area `4 pi` is a one-sheeted
  cover of `S^2`, which re-derives disjoint interiors without the enumerator's conflict table.
- **Corruption.** The sphere check rejects a configuration with a corner removed and one with a
  corner doubled.
- **Distinctness and atlas.** The 5450 classes are pairwise inequivalent under `I_h`, and the
  `akn` flags equal the atlas exactly.
- **Reproduction.** Re-running the enumeration reproduces the committed file.
- **Float audit.** A Monte-Carlo audit agreed with the exact conflict table on all 25440
  ordered pairs. It was run once during development and is not committed.

## Use for KATZ-AKN-C1

This is the corona universe that `KATZ-AKN-C1`'s exclusion check needs, at vertex radius:
`V_AKN` is the 24 flagged classes and the excluded set is the other 5426. A decoration `D`
satisfies `C1(D)` iff every flagged class has a decorated lift and no unflagged class does.
Lifts must be computed per labeled configuration, or per class with stabilizer care, because a
decoration need not be `I_h`-invariant.

## Reproduce

```sh
cd research/akn
python corona.py corona_universe.json      # stdlib only, ~70 s
```
