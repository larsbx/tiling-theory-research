# Repository architecture

Governed research notes, candidate claims and exact finite computations for
tiling theory (Katz/AKN matching rules, phase-4 overlap coverage).

The machine-readable source of repository structure and authority is
[`ESTATE.toml`](ESTATE.toml), validated by the estate audit pinned there
(`larsbx/estate-governance`, contract `estate-repository-v2`). Claim surfaces
and status classes are registered in [`claim_governance.toml`](claim_governance.toml)
and checked by the shared `claim_governance` checker from `larsbx/finite-math-kernels`.
The layout is `transitional`.

| Plane | Target | Current | Content |
| --- | --- | --- | --- |
| policy | `ESTATE.toml` | `ESTATE.toml`, `claim_governance.toml` | estate manifest; claim registry and status classes |
| research | `docs/research/` | `docs/research` | claim dossiers (claim state) |
| evidence | `research/` | `research/candidates.json` | candidate metadata; exact certificates and their checkers |
| docs | `docs/` | `README.md`, `docs/roadmap.md` | README and roadmap |
| kernel | `kernel/` | — (not yet populated) | no canonical kernel yet |
| conformance | `tests/` | `tests` | claim-surface mutation tests and certificate re-checks |

## Authority boundary

Python is the canonical language and declares `acceptance_authority = false`:
the repository owns no acceptance boundary. Claim status is decided by the
registered dossiers under review and audited by the external claim-governance
checker; the exact certificate checks in `research/` are evidence for
finite-domain claims and never promote a finite local check to a global
perfection theorem. Nothing here may emit an `accepted`, `proved`,
`authorized` or deployment verdict.

## Migration

Boundary first, no mass move. Pending steps:

1. Decide whether the exact certificate checkers in `research/akn/` become the kernel plane or stay evidence.
2. Estate policy: every repository with a kernel holds acceptance authority; this one switches `acceptance_authority` to true in the change that lands its first kernel.
