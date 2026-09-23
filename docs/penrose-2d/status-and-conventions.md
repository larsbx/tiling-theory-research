# Penrose 2D pilot — status and conventions

## Purpose

This is the live source/process boundary for the current Penrose pilot.

## Source-grounded facts

- Direction alphabet: `D0,D1,D2,D3,D4`, each an **unoriented** line-direction class.
- Atomic prototiles: Robinson triangles `A` and `B`.
- Substitution counts:
  - `A -> 1A + 1B`
  - `B -> 1A + 2B`
- Substitution matrix:
  ```
  [[1,1],
   [1,2]]
  ```
  with PF eigenvalue `phi^2`.
- Parent orientation freeze:
  - A-parent edges: `D0,D1,D3`.
  - B-parent edges: `D0,D3,D4`.
- Positive certified child-placement rows are available for `B0,A0,B1,B2,A1`.
- Parent-boundary partitions are source-grounded.
- Original audit items:
  - `G2D-1`: rhomb↔triangle aggregation writeup;
  - `G2D-2`: strict-growth invariant `Phi`;
  - `G2D-3`: missing `B2:Q_L`;
  - `G2D-4`: missing reflected `epsilon=-` rows.

## Mechanically derived project facts

- `G2D-3` closed:
  `Q_L(B2)=phi^2+1`.
- Reflected `epsilon=-` rows derived from the positive packet.
- First oriented separator field:
  - `PX-SS -> (D1,D1)`
  - `PX-SO -> (D1,D0)`
  - `PX-OS -> (D0,D1)`
  - `PX-OO -> (D0,D0)`
- Process-level side field:
  - same-side: `PX-SS,PX-OO`
  - opposite-side: `PX-SO,PX-OS`
- Prefix continuation currently reaches four symbols for the two primary cases, with the reflected cases derived by symmetry.

These facts must remain labelled **derived**, not source-verbatim.

## Direction convention

`Di` records an unoriented line class only.

Therefore:

- `D4`
- `D4 (reversed)`

are the same direction-class symbol with opposite traversal.

No reversed direction is added to the alphabet.

## Open obligations

The live mathematical bottlenecks are:

1. **G2D-2: strict-growth invariant `Phi`.**
   This is the primary theorem target.
2. Complete continuation of `I_oriented_2` beyond the current prefix.
3. **G2D-1:** write and verify the rhomb↔triangle aggregation bridge.

## Current process-level continuation data

| case | `I_oriented_1` | `I_side` | current prefix of `I_oriented_2` |
| --- | --- | --- | --- |
| PX-SS | `(D1,D1)` | same-side | `[A_unit_minus[D1], B_base[D0], B_leg[D4], B_base[D4(reversed)]]` |
| PX-SO | `(D1,D0)` | opposite-side | `[A_unit_minus[D0], B_base[D4], B_leg[D3], A_short[D3(reversed)]]` |
| PX-OS | `(D0,D1)` | opposite-side | reflected from PX-SO |
| PX-OO | `(D0,D0)` | same-side | reflected from PX-SS |
