# AGENTS.md

## Scope

This repository is the post-PSC higher-dimensional substitution-tiling research program.

## Authority rules

1. Never use a bounded computation as a universal theorem.
2. Keep imported literature conclusions visibly imported and record exact hypotheses.
3. Penrose is a calibration specimen, not the theorem target.
4. Do not reopen PSC here; reuse its architecture through explicit downstream references.
5. Exact overlap acceptance must not depend on floating-point geometry.
6. Any state/collar/search cap fails closed.
7. Do not silently add unimodularity, connectedness, representability, legality, or Euclidean-only internal-space assumptions.
8. Preserve order/context until a theorem proves a quotient loses no information.
9. Perron growth equality of a residual component is a hard case, not by itself a contradiction.
10. Counterexamples to proposed lemmas become permanent replay fixtures.

## Implementation preference

Mojo is the intended canonical finite acceptance/replay boundary once executable work begins. Julia may serve as an independent research oracle. Reusable stable kernels should migrate to `larsbx/finite-math-kernels`; theorem policy remains here.

## Review gate

Every research PR must answer:

- What claim status changed?
- What exact hypotheses are in force?
- What is proved versus imported versus evidence?
- Does any finite cap affect completeness?
- Is the result class-wide or specimen-only?
- Which theorem-ladder node does it advance?
