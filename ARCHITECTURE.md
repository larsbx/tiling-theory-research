# Repository architecture

Estate repository `larsbx/tiling-theory-research`, scaffolded to the estate template before any content landed.

The machine-readable source of repository structure and authority is
[`ESTATE.toml`](ESTATE.toml), validated by the estate audit pinned there
(`larsbx/estate-governance`, contract `estate-repository-v2`). The layout is
`transitional`: planes name their target directory and the paths that
currently fill them.

| Plane | Target | Current | Content |
| --- | --- | --- | --- |
| policy | `policy/` | `ESTATE.toml` | estate manifest |
| kernel | `kernel/` | — (not yet populated) | no kernel yet; create kernel/ with its first module |
| docs | `docs/` | `README.md`, `ARCHITECTURE.md` | README and this architecture entrypoint |

## Authority boundary

Python is the canonical language and declares
`acceptance_authority = false`: the repository owns no acceptance boundary and holds no executable code yet. Nothing here may emit an
`accepted`, `proved`, `authorized` or deployment verdict.

## Migration

Boundary first, no mass move. Pending steps:

1. Owner to confirm class, INV prefix and canonical language (Python is a provisional default).
2. Add planes only as content lands; empty silos are forbidden.
