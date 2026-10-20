# Roadmap

This repository tracks tiling-theory research candidates under lightweight estate governance.

## Current programme

| ID | Status | Topic | Next obligation |
| --- | --- | --- | --- |
| KATZ-AKN-C1 | candidate | Local-complete Katz/AKN rhombohedral matching-rule minimization | Commit the exact source atlas, then implement deterministic face/corona extraction. |
| AKN-ATLAS-PERIODIC | finite-domain | Periodic tiling with only AKN vertex stars | Obtain and audit the three inaccessible bodies (Katz 1989 pp. 147-182, Kramer-Neri 1984 pp. 580-587, Ben-Abraham et al. 1993 pp. 132-136); 1994 classification evidence is recorded, novelty remains unresolved; extend to radius-2 stars via non-cubic approximants or SAT over periodic boxes. |
| KATZ-AKN-PERFECT | open | Global perfection of a matching-rule decoration | Requires a global/topological proof or an explicit defect search framework; not implied by C1. |
| PH4-OVERLAP-GRAPH | finite-domain | Exact 64-state potential-overlap graph; every state reaches coincidence within five steps. | Retain the exact packet and provenance regressions. |
| PH4-LEGAL-COVERAGE | conditional | Prefix-derived bound covers legal return-vector overlaps for the specified substitution-language tilings. | Audit any spectral transfer separately; no minimal-bound or exact-legality claim. |

## Near-term work

1. Add raw or generated AKN cell/face data with provenance. Partly done: `research/akn/` generates exact AKN cells and an atlas of 24 vertex stars with exact witnesses.
2. Implement oriented face-gluing extraction.
3. Generate the vertex-corona atlas and mark admissible versus excluded coronae. The admissible side is in `research/akn/atlas.json`; the 5426 excluded configurations are not yet committed.
4. Encode `C1(D): V_D = V_AKN` as a finite constraint problem.
5. Record solver certificates and regression tests before promoting any finite-domain result.

## Governance rule

No local atlas result may be described as a perfect matching-rule theorem unless a separate global proof is registered under `KATZ-AKN-PERFECT`.
