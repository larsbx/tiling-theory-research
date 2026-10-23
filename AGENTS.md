# AGENTS.md

## Scope

This repository contains governed tiling-theory research. The post-PSC higher-dimensional substitution-tiling program is one research track alongside the Katz/AKN and Phase-4 work already on `main`.

## Authority

`ESTATE.toml` is authoritative for repository planes, language roles, and acceptance authority. At present:

- Python is the canonical language.
- `acceptance_authority = false`.
- the kernel plane is not populated.
- exact code under `research/` is evidence, not an acceptance boundary.

Do not create a competing kernel or language-authority rule in a research PR. A future kernel must update the estate contract in the same change.

## Research rules

1. Never use a bounded computation as a universal theorem.
2. Keep imported literature conclusions visibly imported and record exact hypotheses.
3. Penrose may be a calibration specimen but is not the class-wide theorem target.
4. Do not reopen PSC here; downstream use of PSC architecture must be explicit.
5. Exact overlap certification must not depend on floating-point geometry.
6. Any state, collar, or search cap is inconclusive unless a completeness theorem covers it.
7. Do not silently add unimodularity, connectedness, representability, legality, or Euclidean-only internal-space assumptions.
8. Preserve order/context until a theorem proves the quotient loses no relevant information.
9. Perron growth equality of a residual component is a hard case, not by itself a contradiction.
10. Counterexamples to proposed lemmas should become replayable research fixtures.
11. New mathematical claims must be registered consistently with `ESTATE.toml`, `claim_governance.toml`, and `research/candidates.json`; planning notes do not promote themselves.

## Review gate

Every research PR should identify:

- what registered claim status, if any, changes;
- the exact hypotheses in force;
- what is repository-derived, imported, finite-domain, or still open;
- whether a finite cap affects completeness;
- whether the result is class-wide or specimen-only;
- which research obligation it advances.
