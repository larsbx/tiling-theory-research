# tiling-theory-research

Governed research notes, candidate claims, and finite-computation plans for tiling theory.

## Active candidates

| ID | Status | Summary | Surface |
| --- | --- | --- | --- |
| KATZ-AKN-C1 | candidate | Minimal local-complete decoration problem for Katz/AKN rhombohedral vertex atlases. This is a finite local condition, not a perfect matching-rule proof. | `docs/research/katz-akn-c1-local-completeness.md` |
| AKN-ATLAS-PERIODIC | finite-domain | The 24 AKN vertex stars admit a periodic tiling (3/2 cubic approximant, 576 vertices per period), exactly certified; so the undecorated vertex atlas is not a local rule. | `docs/research/akn-vertex-atlas-periodic-approximant.md` |
| KATZ-AKN-PERFECT | open | Global perfection of a Katz/AKN matching rule: every everywhere-locally-legal tiling belongs to the intended AKN class. | `docs/research/katz-akn-c1-local-completeness.md` |

## Governance

This repository uses lightweight estate governance:

- `ESTATE.toml` records repository planes and promotion principles.
- `claim_governance.toml` registers claim surfaces and status classes.
- `research/candidates.json` records machine-readable candidate metadata.
- `docs/roadmap.md` records next obligations.

No finite local search result should be promoted to a global perfect matching-rule theorem without a separately registered proof obligation.

## Governance validation

The shared checker is `larsbx/finite-math-kernels`, validated at commit
`1887777d815656034d0fb9e5a68ef473b652b75b`. With a checkout of that commit
beside this repository, run from this repository root:

```sh
PYTHONPATH=../finite-math-kernels/tools python -m claim_governance.cli --root .
PYTHONPATH=../finite-math-kernels/tools python -m unittest discover -s tests -v
```

The regression suite audits the unchanged repository and independently mutates
all twelve registered status surfaces in temporary copies. Each mutation must
produce a status mismatch for that exact claim and path. It also checks unique
anchors, windows containing only the intended status class, canonical spellings,
existing aliases, and word boundaries. JSON surfaces are explicitly checked even
though they are outside the prose scan. These tests validate governance coverage;
they do not certify any mathematical claim. The separate stdlib-only suite
`tests/test_akn_approximant.py` re-runs the exact AKN-ATLAS-PERIODIC certificate
check, re-derives every atlas class from its exact witness, and checks that the
certificate checker rejects corrupted input.

The `Claim governance` GitHub workflow runs the audit and mutation regressions
on pull requests, pushes to `main`, and manual dispatch. It fetches the shared
checker at the exact commit above, verifies the checkout, and uses read-only
repository permissions. No dependency installation is needed beyond Python 3.11
or later. A failed audit or regression fails the job. This supplies a CI check;
requiring it for merges is a separate repository branch-protection setting.
