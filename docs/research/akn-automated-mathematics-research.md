# AKN as an automated mathematics research programme

**Research authority:** `ESTATE.toml` and `claim_governance.toml`.
**Execution:** Python standard-library exact arithmetic, GitHub Actions,
independent certificate checkers, immutable workflow artifacts.
**Current scope:** 135-plane AKN generic atlas, radius-two periodic-patch
census, and next singular-window obligations. No universal theorem promotion.

## Research loop (not a one-off test)

The experiment is a repeatable state machine:

```
registered conjecture and stated finite hypotheses
    -> deterministic candidate enumerator
    -> independent certificate checker (different mathematical algorithm)
    -> adversarial mismatch / counterexample detector
    -> exact evidence + source revision + SHA-256 manifest
    -> machine-readable research verdict
    -> bounded next experiment, or explicit unresolved obligation
    -> reviewed claim-governance update (separate operation)
```

The pipeline now runs **automatically on every PR-head update** and,
after integration into `main`, on a **weekly schedule** (UTC Monday
04:17). The manual dispatch remains optional, not a prerequisite.
Concurrent superseded runs are cancelled. Both jobs check out the PR's
exact `head.sha`, not the synthetic merge commit.

The first job validates the exact arithmetic and deliberately incomplete
eight-slab cover, plus an independent full 2D-section region count.
The second job uses the independent research driver to enumerate all 15
families, rederive the complete 24-orbit and six stabilizer-conjugacy
classification, and compare region-count, witness-count and checksum
evidence. It uploads source-bound evidence even on failure, with a 90-day
retention period. It then automatically generates and independently
checks **105 exact singular-plane probes**, distinguishing cells strictly
required from cells possible under closed-window membership.

## Machine states and permitted claims

| State | Meaning | Claim authority |
| --- | --- | --- |
| `frontier_inconclusive` | Exact bounded search leaves feasible prefixes. | No completeness claim. |
| `counterexample_candidate` | A witnessed star is outside the current atlas. | Preserve witness; independent investigation required. |
| `verification_failed` | The replay is missing, inconsistent or not exhaustive. | No claim promotion. |
| `baseline_disagreement` | An independent count, digest, orbit or conjugacy check disagrees. | Quarantine and review the discrepancy. |
| `generic_candidate_verified` | The exact head yields full enumerator/checker agreement on open chambers. | Candidate finite *generic* proof; separate review and claim registration. |
| `execution_or_verification_error` | A job or checker failed. | Retain logs and rerun only after investigating. |

A green CI job is evidence that its *declared finite predicates* passed,
not automatic authority to assert a global aperiodicity theorem.
The automated driver does not rewrite `claim_governance.toml`, change
`research/candidates.json`, merge a PR or silently resolve review threads.

The 24 full `I_h` classes are star **orbits**. The distinct conjugacy
classification of their stabilizer subgroups has **six types**. Neither
count should be misreported as the number of conjugacy classes of group
elements. A more detailed named subgroup taxonomy and rotational-only
orbit/enantiomorph comparison are follow-up research tasks.

## Independently checked investigations

**Generic chamber coverage:** Compare an exact 3D convex-polytope
enumerator against a 2D planar-section hyperplane-arrangement region
count. A checker enumerates strict cell incidence using independent
formulas and checks exact `Q(tau)` interior witnesses. A complete packet
requires a zero frontier and the independently derived total.

**Adversarial modes:** Remove a feasible branch, falsify a witness,
change a class assignment, corrupt the purported stabilizer-conjugacy
signature, alter a checksum, or change the independent region count.
Tests must reject corrupt packets; errors are not evidence of
infeasibility.

**Singular pilot:** For every interior transition plane, two generic
witnesses on opposite sides are interpolated to an exact point in that
plane and the open vertex window. A separate arithmetic implementation
checks all 160 possible cells for strict and closed inclusion.
This is an exact **plane-sampling experiment**, not an exhaustive cover
of singular 2D facets, 1D intersections, 0D vertices or all boundary
selection conventions.

## Commands, independent of GitHub Actions

```sh
python research/akn/atlas_research_driver.py --max-nodes 1 --max-depth 1 --out /tmp/akn-bound
python research/akn/atlas_research_driver.py --max-nodes 100000 --max-depth 15 --require-full --out /tmp/akn-full
python research/akn/atlas_singular_probe.py --packet /tmp/akn-full/chambers.json --out /tmp/akn-full/singular-probes.json
python research/akn/atlas_singular_check.py /tmp/akn-full/singular-probes.json --out /tmp/akn-full/singular-replay.json
```

Every completed cycle writes a structured `research-run.json` with
evidence hashes and a new scoped obligation. A failed full experiment
returns a nonzero status but still attempts to write its state, stderr,
and traceback for debugging. A full packet is not stored in the repo
because the deterministic generation and verification logic, not the
commit size, are the primary reproducibility artifacts.

## Next mathematical frontier

The next automated mathematics *implementation* is **complete singular
stratification**, not rerunning the same generic result indefinitely.
The programme must construct every nonempty relative-open face, edge,
and vertex of the exact arrangement within the vertex window and
validate disjoint stratification by an independent face-lattice or
oriented-matroid checker. Only then should each explicit singular
selection convention be tested and possible stars compared with
existing orbit/conjugacy tables.

Other independent directions are arbitrary periodic certificates beyond
the fixed 3/2 example, robust radius-two obstruction classes, and
a counterexample-focused matching-rule search. No finite sample may
be extrapolated into the global periodicity or perfect-rule theorem.

**Safety/authority invariant:** A science automation can propose,
derive, falsify, and report new claims. Publishing an accepted
mathematical theorem additionally requires a clearly stated scope,
reviewable exact certificate, independent replay, literature
hypotheses, and a governed status change.
