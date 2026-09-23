# Theorem ladder

**Status:** open research plan.

## T0 — calibration only

For each calibration specimen, construct the exact overlap object and reproduce the expected coincidence verdict.

**Authority:** finite-domain / regression evidence only.

T0 must include more than Penrose so that no implementation accidentally bakes in pentagonal geometry.

## T1 — representation and completeness bridge

**Target theorem.** Under explicit hypotheses \(H_{rep}\), the executable overlap graph contains exactly the realized overlap classes required by the selected literature coincidence criterion, or maps to them by a proved reachability-preserving quotient.

Required sublemmas:

1. exact translation/displacement module;
2. exact tile-overlap predicate;
3. child-overlap inflation law;
4. realization of every graph state;
5. completeness: every relevant realized overlap class appears;
6. coincidence state agrees with geometric full-tile coincidence.

No bounded collar/state cap may substitute for item 5.

## T2 — automatic coincidence

**Flagship target.** Find a natural class \(\mathcal C\) such that

\[
T\in\mathcal C \implies \text{every recurrent overlap component reaches coincidence}.
\]

Equivalent formulations may use algebraic coincidence if the import ledger proves the equivalence in the chosen setting.

Suggested contradiction normal form:

```text
failure of coincidence
=> finite closed irreducible noncoincident component S
=> exact expansion/translation recurrence on S
=> class-specific rigidity
=> contradiction
```

The theorem should be class-wide, not specimen-wise.

## T3 — pure discrete spectrum

**Conditional architecture.**

```text
T in C
=> T2: overlap/algebraic coincidence
=> imported spectral theorem, hypotheses discharged
=> pure discrete dynamical spectrum
```

The imported arrow must remain visibly imported in theorem statements and proof ledgers.

## T4 — enlarge the class

Candidate relaxations, one at a time:

- remove connected-tile assumptions;
- move from self-similar to self-affine expansion;
- weaken explicit model-set adjacency;
- cover non-unimodular/adelic internal spaces;
- approach broad Pisot-family or homological-Pisot classes.

Every relaxation needs a counterexample search and a statement of which T1/T2 lemma stops working.
