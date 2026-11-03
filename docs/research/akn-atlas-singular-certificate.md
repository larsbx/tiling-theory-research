# Exact singular AKN atlas certificate

This experiment advances issue #24 for the fixed 135-plane arrangement in the
closed AKN vertex window. The arrangement has fifteen ordered normal families,
each with nine distinct levels. The extreme levels are the thirty supporting
window planes. The existing twenty-four generic star orbits are the comparison
baseline. This experiment does not update the registered claim status.

## Enumeration and completeness

A stratum key has one code per family. Code `2k` means equality at level `k`.
Code `2k+1` means the open interval immediately above level `k`. Each key is
an intersection of affine hyperplanes and open halfspaces in its affine hull,
so it is convex. A valid witness establishes nonemptiness. The equality-normal
rank determines the dimension.

The enumerator computes the affine line for each pair of nonparallel planes
and sweeps the transition events in the window along that line. Coincident
lines use the lexicographically first active plane pair. Each event is an
exact point, and adjacent events bound a relative-open edge. The two
transverse directions within each plane containing an edge identify its
adjacent face keys. Window signs discard exterior sides. The mean of all
distinct boundary vertices gives a relative-interior face witness. Witness
coordinates are rational pairs in the basis `(1, tau)`, with the same doubled
window-coordinate scaling as the generic atlas.

The independent checker projects each plane into a coordinate section, clips
every pair-intersection chord against the window strips, and checks the exact
ordered edge endpoints for complete coverage, including singleton chords.
A rank-three vertex lies on at least one such chord and its third independent
equality cuts that chord. An edge witness and its two endpoint sign keys
certify that no transition can occur in the open segment. Chord coverage
therefore certifies every edge and vertex without reconstructing the event
sweep.

For each plane the certified embedded graph includes the polygon boundary
and all cutting chords. It is connected because each chord reaches the
section boundary. Euler's formula gives the exact number of bounded faces
as `1 + edges - vertices`. Distinct, exact face keys can therefore certify
completeness by count. The checker also verifies each boundary reference by
sign specialization and requires one incident face per section boundary edge
and two per interior edge, for every plane containing the edge. A vertex is
incident to a face through its certified boundary edges. Coincident lines and
concurrent planes are handled by exact equality and set membership.

## Cell selection and orbit evidence

For every stratum the packet records forced and boundary-dependent incident
cells from the full catalogue of 160 signed choices. The complement is absent.
The strict rule takes only forced cells. The closed rule takes both sets.
The checker independently reconstructs the cell thresholds and verifies
both selections. A strict rule on the supporting window boundary excludes
the center itself, so its cell pattern is formal. The replay separates
window-interior and window-boundary counts and labels center eligibility
on each counterexample.

The replay canonicalizes cell patterns under the full 120-element
icosahedral group and classifies stabilizer subgroups up to conjugacy. A
pattern outside the generic orbit list produces a separate exact witness
with its stratum, selection rule, signed cells and stabilizer signature.
These are finite counterexamples to extending the generic orbit list under
the specified local threshold rules. Global realizability of singular
selection conventions, matching rules and aperiodicity remain open here.

## Replay and resource limits

```sh
python research/akn/atlas_strata_driver.py --out evidence-singular
python -m unittest discover -s tests -p 'test_akn_strata.py' -v
```

The run record gives the source commit and SHA-256 hashes of the certificate
and independent replay. A cap below 8,505 ordered nonparallel pair candidates
returns an inconclusive failure and retains the exact unprocessed pair
suffix. The prefix packet omits face rows because their boundary lists may
be partial. Increase the cap and rerun the deterministic enumeration to
obtain a complete packet. The source workflow runs at the PR head. Homelab
can use the same driver on its existing weekly schedule once the driver is
on the selected source ref.
