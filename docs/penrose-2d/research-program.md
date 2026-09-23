# Penrose 2D pilot — research program

## Research question

Can the finite-state architecture that succeeds for one-dimensional substitution dynamics be reformulated in two dimensions using residual interfaces rather than suffixes?

The target is not to copy the 1D proof literally. It is to preserve its architecture:

```
residual state
-> minimal recurrent obstruction
-> identity/symmetry reduction
-> centered embedding/interface graph
-> strict monotone quantity
-> acyclicity
```

## Phase I — residual-interface graph

Define a finite local interface state containing only data that is demonstrably required:

- parent/child tile type;
- boundary-side class;
- unoriented direction class plus traversal orientation;
- collar information;
- separator type;
- handedness/reflection class;
- enough ancestry to make the state transition deterministic.

Do not quotient away any field until a theorem proves the quotient sound.

### Acceptance criterion

A canonical transition relation whose vertices are exact legal interface states and whose edges are one inflation-and-normalization step.

## Phase II — identity and symmetry edges

Classify edges into:

1. identities / forced symmetry copies;
2. genuinely nontrivial interface moves.

Use the frozen reflection maps only as derived machinery, and retain a provenance tag for every reflected row.

### Acceptance criterion

A mechanically checkable quotient with replayable representatives.

## Phase III — strict-growth invariant `Phi`

This is the principal open theorem target.

The invariant should satisfy:

- `Phi(next) > Phi(current)` on every genuinely nontrivial recurrent candidate; or
- a lexicographic analogue with one strictly monotone coordinate.

Candidate ingredients include:

- enclosing supertile scale;
- separator depth;
- boundary-complexity measure;
- collar depth;
- a finite ordered tuple of side/orientation/ancestry data.

### Negative control

The invariant must be tested against every currently derived continuation family, especially the same-side and opposite-side cases.

## Phase IV — 2D hierarchy uniqueness

Only after Phase III is closed, investigate whether hierarchy uniqueness follows directly from the interface theorem or needs a separate ancestry-state argument.

Do not assume that the 1D 'UD for powers' shortcut survives in 2D.

## Phase V — transfer and dimensional generalization

A theorem or kernel graduates out of the Penrose pilot only if its contract is independent of the specific Penrose direction alphabet.

Potential reusable abstractions:

- finite residual-interface graphs;
- canonical orientation/reflection normalization;
- exact symmetry quotients;
- ancestry-aware edge transport;
- finite certificates for acyclicity or strict growth.

## PSC feedback discipline

Potential PSC feedback must name a live obligation:

- P2/G1b-2 renewal finiteness;
- P4 realization/MEF;
- P1b strict-zipper only when the non-unimodular representation-space mismatch is addressed explicitly.

No Penrose computation alone changes PSC theorem status.
