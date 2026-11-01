# AKN periodic-cover falsification: a finite quotient can give false confidence

**Date:** 2026-11-01  
**Parent:** [Global matching-rule spike](akn-global-matching-theorem-spike.md)  
**Claim scope:** synthetic finite mathematical negative control, **not** Katz's 1988 decoration and **not** a new accepted perfect-rule theorem.

## Sound finite-cover experiment

The existing 3/2 golden-rhombohedral certificate has one-period data:
576 cells and 1,728 oriented face pairings. The *same* undecorated
geometry is periodic for every integer multiple of its period lattice.

To search for face-only decorations D, the tester must permit decorations
with a **strictly larger period** than their underlying geometry.
Checking only the smallest quotient can incorrectly conclude that a
periodic geometry carries no D-decoration.

The cover construction represents a face by its 6D integer corner and
the two in-face axis indices J. Two face origins in the quotient differ
by one exact lattice vector:

    origin(positive face) - origin(negative face)
      = k0 L0 + k1 L1 + k2 L2,  with k∈ℤ³.

The k coefficients are solved by exact Cramer fractions on an invertible
3×3 minor and independently checked in all six coordinates. For deck
coordinates d in ℤ/m0×ℤ/m1×ℤ/m2, pair the original positive face in
copy d with the original negative face in copy d+k (mod m).

This lifts all faces *without* conflating different period sheets under
the rational 3D quotient map. Each one of the six faces of every lifted
cell is incident to exactly one opposite face.

Observed independent exact integer counts for the committed certificate:
- one period: 576 cells, 1,728 face pairs;
- 308 of the 1,728 quotient-face pairings cross a nonzero lattice deck seam;
- twofold cover along L0: 1,152 cells, 3,456 face pairs.

These counts are combinatorial properties of the fixed committed
specimen, not statements about all AKN tilings.

## Two-sheet parity counterexample

For each 0-based axis triple I and p in {0,1}, introduce one synthetic
decorated tile state (I,p) of the matching geometric P/O shape.
For a face in the direction of axis i with lower/high side s∈{0,1},
give it the label

    label(I,p,i,s) = p + (s if i==0 else 0) (mod 2).

Allowed oriented face pairs are only (0,0) and (1,1). Thus a label is
the parity of the **first integer coordinate of the common 6D face
origin**, so face matching propagates a consistent height parity.

The first primitive period has L0[0]=3 odd; the other two have even
first coordinate. One copy of the primitive period therefore contains
a closed parity-transport contradiction, even though it has the same
undecorated periodic geometry. A twofold cover in the first period
direction has all period translations with even first coordinate.
The explicit assignment

    p(cell at n in deck d)=n[0]+d*L0[0]  (mod 2)

is then globally consistent and is independently verified against
**all 3,456 oriented face pairings**.

An independent direct parity-constraint audit of the 576-cell base
quotient found a connected dual-face graph with an inconsistent parity
cycle; its lifted twofold assignment is given above.

**Result:** base-quotient UNSAT and a larger-cover periodic SAT can both
hold for the *same* finite-alphabet local facet grammar. Thus the base
period's finite UNSAT result is not evidence that the decorated rule
forbids all periodic tilings, let alone that it is perfect.

The rule here is **synthetic**, not Katz's 1988 rule. It tests the
logic of the experiment and is not a counterexample to Katz's theorem.

## Reproducibility and honesty

Run from repository root:

    python -m unittest discover -s tests -p 'test_akn_decorated_covers.py' -v

This uses only standard-library Python, the existing exact `geometry.py`
and the existing decorated-quotient solver. The cover module
`decorated_covers.py` supports arbitrary positive three-component
period multipliers, with fail-closed SAT, finite-cover UNSAT, and
INCONCLUSIVE outcomes. Every claimed SAT witness is checked afresh by
`verify_cover_assignment`.

No enumerated finite collection of covers, however large, can prove
global perfection. The search could still miss infinitely aperiodic
decorations of a periodic undecorated geometry.

## Next substantive research gate

1. Obtain actual Katz (1988) facet-label inventory and certify it is
   complete (shape, orientation, reflections, face, corner and any
   multibody conditions).
2. Replace the synthetic parity grammar with only the **fully
   source-supported** rules, retaining provenance and independent replay.
3. Test period covers while preserving an explicit budget and
   never interpreting finite UNSAT as global truth.
4. Seek a **source-grounded unbounded forbidden-plane transport proof**
   that yields global four-cell open-phase consistency; Helly then
   gives the closed AKN hull criterion.

**KATZ-AKN-PERFECT remains open.** `AKN-ATLAS-PERIODIC` and the
finite radius-two claims retain their original scopes.
