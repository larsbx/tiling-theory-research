# Executable architecture

**Status:** implementation design; no mathematical conclusion follows from this document.

## 1. State model

Prototype overlap state:

\[
O=(i,j,z,c)
\]

where:

- \(i,j\) are prototile types;
- \(z\) is an exact translation/displacement;
- \(c\) is optional finite context/collar data, introduced only if T1 completeness requires it.

A coincidence is not merely \(i=j\): the translated supports and control-point convention must make the full-tile equality predicate exact.

## 2. Inflation

For child placements \(p,q\) and expansion \(Q\),

\[
z' = Qz + q-p.
\]

This formula should be tested independently of geometric intersection. Child generation has two stages:

1. algebraic candidate translation;
2. exact decision that child interiors overlap.

## 3. Exact arithmetic boundary

Initial implementation belongs in the research repo until the interfaces stabilize.

Potential later extraction to `finite-math-kernels`:

```text
substitution_tilings/
  expansion.mojo
  displacement_module.mojo
  overlap_state.mojo
  overlap_graph.mojo
  recurrent_components.mojo
  coincidence.mojo
  growth.mojo
```

Do not extract theorem-specific hypothesis logic into the kernel library.

## 4. Geometry adapters

Different tile families may require different exact predicates:

- polygonal tiles with algebraic/rational vertices;
- digit-set/self-affine tiles represented by certified neighbor/contact graphs;
- control-point Delone-set formulations that avoid explicit fractal-boundary intersection.

The research question determines which adapter can support T1 completeness. A floating-point polygon library may visualize but cannot certify.

## 5. Graph analyses

The generic finite layer should support:

- reachability to coincidence;
- SCC decomposition;
- sink/recurrent noncoincident components;
- child multiplicity matrix;
- spectral-radius diagnostics as evidence only unless exact;
- cycle addresses;
- growth of residual noncoincident occurrences;
- replayable witness serialization.

## 6. Fail-closed rules

- state cap reached -> inconclusive;
- unknown intersection -> inconclusive;
- arithmetic overflow/unsupported algebraic domain -> inconclusive;
- incomplete collar radius -> inconclusive;
- missing theorem hypothesis -> imported conclusion unavailable;
- calibration mismatch -> block promotion.

## 7. Oracle split

Preferred long-term split:

- Mojo: canonical exact acceptance/replay boundary;
- Julia: independent algebraic/numerical research oracle where useful;
- Python: orchestration/reference only where retained;
- proof assistants: theorem verification when a stable formal statement warrants it.

No oracle may silently widen the mathematical claim.
