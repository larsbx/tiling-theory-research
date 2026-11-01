# Roadmap

This repository tracks tiling-theory research candidates under lightweight estate governance.

## Current programme

| ID | Status | Topic | Next obligation |
| --- | --- | --- | --- |
| KATZ-AKN-C1 | candidate | Local-complete Katz/AKN rhombohedral matching-rule minimization | Commit the exact source atlas, then implement deterministic face/corona extraction. |
| AKN-ATLAS-PERIODIC | finite-domain | Periodic tiling with only AKN vertex stars | Obtain and audit the three inaccessible bodies (Katz 1989 pp. 147-182, Kramer-Neri 1984 pp. 580-587, Ben-Abraham et al. 1993 pp. 132-136); 1994 classification evidence is recorded, novelty remains unresolved; review the exact radius-two generic patch-feasibility pilot (`docs/research/akn-radius2-exact-feasibility.md`), including singular boundaries; certify complete 24-class atlas chamber coverage; then extend periodic searches via non-cubic approximants or SAT over periodic boxes. |
| AKN-3-2-RADIUS2 | finite-domain | Exact generic radius-two patch census for the fixed 3/2 AKN periodic quotient | Verify exact-head CI, preserve witness/obstruction packet, audit singular boundaries and complete exact atlas chamber coverage; does not imply global radius-two aperiodicity. |
| KATZ-AKN-PERFECT | open | Global perfection of a matching-rule decoration | Requires a global/topological proof or an explicit defect search framework; not implied by C1. |
| PH4-OVERLAP-GRAPH | finite-domain | Exact 64-state potential-overlap graph; every state reaches coincidence within five steps. | Retain the exact packet and provenance regressions. |
| PH4-LEGAL-COVERAGE | conditional | Prefix-derived bound covers legal return-vector overlaps for the specified substitution-language tilings. | Audit any spectral transfer separately; no minimal-bound or exact-legality claim. |

## Exact AKN generic-atlas chamber acceptance (stacked PR #23)

The 15-family/135-plane reduction now has a **preliminary local full
open-chamber enumeration** of 21,840 chambers and a separate exact
line-arrangement region count of 21,840. All local complete stars fall in
the established 24 full-icosahedral **star orbits**; their stabilizer
subgroups fall into **six conjugacy types**. The canonical prefix and
independent slice-count checksums are recorded in
`research/akn/atlas_chamber_full_manifest.json`. Research method,
limits and reproduction are in
`docs/research/akn-atlas-open-chamber-certificate.md`.

**Automated execution:** `docs/research/akn-automated-mathematics-research.md`
defines the exact PR-head research cycle. Daily status monitoring and
weekly full independent AKN experiments are now **owned by
`larsbx/my-math-homelab`**, with schedule registration in
`policy/research-schedules.toml` and an active mainline workflow
since homelab PR #7 merged on November 1, 2026. The source PR workflow
continues to validate code at exact PR heads, but its overlapping
weekly cron was removed. The homelab full run records provenance,
generates and replays exact open-chamber evidence, and continues with
105 exact singular-plane probes. Neither schedule promotes claims.

**Next acceptance obligation:** complete PR #22 exact-head tests and
review, obtain a passing PR #23 *automatically triggered* full packet
at its exact head, independently review the proof/data scope, then
consider a narrowly scoped governed generic-atlas coverage claim.
The next mathematical development is exhaustive singular **stratum**
enumeration with a specified boundary-selection convention; the
105-plane probe does not prove that. No generic finite count establishes
a universal matching-rule or aperiodicity theorem.

## Near-term work

1. Add raw or generated AKN cell/face data with provenance. Partly done: `research/akn/` generates exact AKN cells and an atlas of 24 vertex stars with exact witnesses.
2. Implement oriented face-gluing extraction.
3. Generate the vertex-corona atlas and mark admissible versus excluded coronae. The admissible side is in `research/akn/atlas.json`; the 5426 excluded configurations are not yet committed.
4. Encode `C1(D): V_D = V_AKN` as a finite constraint problem.
5. Record solver certificates and regression tests before promoting any finite-domain result.

## Governance rule

No local atlas result may be described as a perfect matching-rule theorem unless a separate global proof is registered under `KATZ-AKN-PERFECT`.
