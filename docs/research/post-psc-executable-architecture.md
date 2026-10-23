# Post-PSC executable architecture

**Status:** candidate implementation design. No mathematical claim is promoted by this document.

## 1. State model

Prototype higher-dimensional overlap state:

\[
O=(i,j,z,c),
\]

where (i,j) are prototile types, (z) is an exact translation/displacement, and (c) is optional finite context introduced only if a completeness argument needs it.

A coincidence is not merely (i=j): the translated supports and control-point convention must make full-tile equality exact.

## 2. Inflation

For child placements (p,q) and expansion (Q),

\[
z' = Qz + q-p.
\]

Child generation separates:

1. the exact algebraic candidate translation;
2. the exact decision that the child interiors overlap.

## 3. Current repository authority

Under the current `ESTATE.toml`:

- Python is canonical;
- the repository has no acceptance authority;
- `research/` contains evidence/checkers;
- the kernel plane is empty.

Therefore initial overlap prototypes belong under `research/post_psc/` and are research evidence only. A future canonical kernel requires a deliberate estate migration that populates `kernel/` and changes acceptance authority according to estate policy.

## 4. Geometry adapters

Different classes may require different exact predicates:

- polygonal tiles with exact algebraic/rational vertices;
- self-affine tiles represented by certified neighbor/contact graphs;
- control-point Delone-set formulations that avoid explicit fractal-boundary intersection.

Visualization may use approximate geometry, but approximate geometry cannot certify an overlap.

## 5. Graph analyses

The reusable research layer should support:

- reachability to coincidence;
- SCC decomposition;
- recurrent noncoincident components;
- child multiplicities;
- exact cycle addresses where available;
- residual noncoincident growth diagnostics;
- replayable witness serialization.

Do not erase ordered/context data before a theorem licenses the quotient.

## 6. Fail-closed rules

- state cap reached -> inconclusive;
- unknown intersection -> inconclusive;
- unsupported arithmetic domain -> inconclusive;
- incomplete collar radius -> inconclusive;
- missing imported-theorem hypothesis -> spectral implication unavailable;
- calibration mismatch -> block promotion.

## 7. Cross-language work

Independent implementations in Mojo, Julia, or other languages may be useful research oracles, but they are non-authoritative unless the estate contract is updated. Cross-language disagreement fails closed.
