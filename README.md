# tiling-theory-research

Post-PSC research program for substitution tilings in dimension (d \ge 2).

## Mission

The theorem target is **not Penrose** and not any single named tiling. Penrose is a calibration specimen.

The program asks:

> For which natural class \(\mathcal C\) of higher-dimensional substitution tilings can finite, exact obstruction theory force overlap/algebraic coincidence, and hence pure discrete dynamical spectrum through an audited imported theorem?

The intended proof spine is

```text
substitution / tile-substitution data
=> exact finite overlap representation
=> bad recurrent overlap-component normal form
=> class-wide exclusion of every noncoincident recurrent component
=> overlap or algebraic coincidence
=> pure discrete spectrum [imported theorem, hypotheses audited]
```

## Repository boundary

- **This repository:** theorem design, higher-dimensional overlap geometry, literature imports, calibration families, conjectures, and proofs.
- **pisot-substitution-conjecture-research:** upstream proof lineage and source of reusable proof architecture. This repository does not reopen or re-prove PSC.
- **finite-math-kernels:** reusable exact, dimension-agnostic computational primitives once an interface is stable.
- **semantic-categorical-oracle:** semantic/contract checking only; never mathematical proof authority.

## Initial theorem ladder

- **T0 — Calibration:** reproduce known pure-discrete examples from exact substitution/tiling input. No novelty claim.
- **T1 — Representation bridge:** prove that the executable overlap states coincide with the literature overlap object under explicit hypotheses.
- **T2 — Automatic coincidence:** identify a natural class \(\mathcal C\) and prove every tiling in it satisfies overlap/algebraic coincidence.
- **T3 — Spectral consequence:** combine T2 with an audited imported theorem to obtain pure discrete dynamical spectrum.
- **T4 — Class enlargement:** weaken hypotheses toward broader Pisot-family / Meyer / self-affine regimes.

The main new mathematics is expected at **T2**.

## Candidate first class

The first class is deliberately provisional:

```text
primitive FLC self-affine/self-similar substitution tilings
+ Meyer return/displacement structure
+ exact finitely representable overlap types
+ hypotheses needed for the selected overlap-coincidence theorem
```

Connected/non-rod, representability, diagonalizability, Pisot-family, and unimodularity conditions are **not silently assumed**. Each belongs in the hypothesis ledger until its role is audited.

## Working discipline

Every claim is labelled as one of:

`proved`, `imported`, `finite-domain`, `conditional`, `open`, `bridge`, `evidence`, `retired`.

A finite census never becomes a universal theorem without an independent completeness result. Numerical geometry never becomes an exact overlap decision. Capped graph construction is inconclusive.

See:

- `docs/research-program.md`
- `docs/theorem-ladder.md`
- `docs/hypothesis-firewall.md`
- `docs/literature-import-ledger.md`
- `docs/executable-architecture.md`
- `docs/calibration-corpus.md`
