# Roadmap

This repository tracks tiling-theory research candidates under lightweight estate governance.

## Current programme

| ID | Status | Topic | Next obligation |
| --- | --- | --- | --- |
| KATZ-AKN-C1 | candidate | Local-complete Katz/AKN rhombohedral matching-rule minimization | Encode decorated lifts over the committed 5450-class universe; obtain Katz's decoration rules as the benchmark. |
| AKN-ATLAS-PERIODIC | finite-domain | Periodic tiling with only AKN vertex stars | Literature search for priority; extend to radius-2 stars via non-cubic approximants or SAT over periodic boxes. |
| AKN-CORONA-UNIVERSE | finite-domain | All vertex configurations of golden rhombohedra | Certify atlas completeness (24 AKN classes) to drop the literature dependence. |
| KATZ-AKN-PERFECT | open | Global perfection of a matching-rule decoration | Requires a global/topological proof or an explicit defect search framework; not implied by C1. |

## Near-term work

1. Add raw or generated AKN cell/face data with provenance. Partly done: `research/akn/` generates exact AKN cells and an atlas of 24 vertex stars with exact witnesses.
2. Implement oriented face-gluing extraction.
3. Generate the vertex-corona atlas and mark admissible versus excluded coronae. Done at vertex radius: `research/akn/corona_universe.json` (5450 classes, 24 flagged AKN).
4. Encode `C1(D): V_D = V_AKN` as a finite constraint problem.
5. Record solver certificates and regression tests before promoting any finite-domain result.

## Governance rule

No local atlas result may be described as a perfect matching-rule theorem unless a separate global proof is registered under `KATZ-AKN-PERFECT`.
