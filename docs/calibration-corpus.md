# Calibration corpus

**Status:** open corpus design. Calibration results are finite evidence unless a cited theorem supplies the conclusion.

## Goals

The corpus must test the abstraction, not just demonstrate successful cases.

### Positive families

Start with several structurally different examples:

1. Penrose substitution tilings — calibration for a classical pure-discrete/model-set example.
2. At least one non-Penrose planar self-similar substitution with an independently known coincidence/model-set description.
3. At least one self-affine (not scalar self-similar) example satisfying the chosen T1 hypotheses.
4. A non-unimodular example if the first theorem class permits it.

Exact specimens are to be pinned only after the literature audit.

### Negative controls

Include substitution systems outside the target class or known not to have pure discrete spectrum. Their role is to ensure:

- the hypothesis gate rejects them, or
- the overlap graph retains a recurrent noncoincident obstruction.

Do not choose negative controls merely because an implementation happens to fail on them.

## Required fixture data

Each specimen records:

```text
name
dimension
prototile types
substitution rule
expansion Q
control-point convention
exact coordinate/algebraic domain
declared hypotheses
source for expected spectral/coincidence status
overlap-state digest
result
authority: calibration/evidence/imported expectation
```

## First corpus acceptance

Before any T2 theorem work depends on the executable layer:

- at least 3 positive families;
- at least 2 negative controls;
- one example with nontrivial recurrent noncoincident state behavior;
- exact replay from repository data;
- no uncited expected verdict.
