# Singular AKN stars from a common window translation

This experiment advances issue #24 using the independently verified generic
and singular packets for the same 135-plane arrangement. It does not change
any registered claim status.

For a singular shift in a stratum S, a generic chamber C can be approached
by one common translation exactly when S lies in the closure of C. For
each normal family, a chamber slab closes up to include its two endpoint
levels. A singular key belongs to that closure if and only if all fifteen
family tests hold. For sufficiency, let x be the singular witness and y
the certified chamber witness. Every strict slab inequality holds on
x+t(y-x) for 0<t<=1, since x satisfies its weak form and y its strict form.
Necessity follows by continuity of the fifteen projections. The same
incidence criterion applies to any point of the relative-open stratum.

These choices have a pointwise interpretation for the cut-and-project
construction. The direction can be chosen in the open incident cone
while avoiding directions parallel to the window facet planes. There are
countably many lattice translates of the boundary planes. Along that
direction the parameter values that hit one of those planes are countable.
A sequence of generic shifts tending to zero along the ray gives a
common choice for the construction. Each fixed lattice candidate has a
finite collection of affine membership tests, so its membership stabilizes
as the parameter decreases. This yields a local limit of generic patterns.
Every centered star in the experiment therefore belongs to the generic
24-orbit catalogue. The scope is centered stars and limits of generic
window translates. Existence under broader singular conventions or
matching-rule hypotheses remains a separate question.

The replay joins the two packets by a slab trie and checks the complete
incidence list independently using inverted bitsets for closed slab
membership. It reconstructs each adjacent chamber's raw signed-cell set
from the thresholds. For each singular stratum, the output lists all
incident chamber indices and tests whether one gives exactly the strict
or the closed selection. At a supporting window stratum, strict selection
excludes the center, so there is no centered strict limit to compare.

Run both existing atlas drivers, then join their verified outputs.

```sh
python research/akn/atlas_research_driver.py --require-full --out evidence-full
python research/akn/atlas_strata_driver.py --out evidence-singular
python research/akn/atlas_perturbation_limits.py \
  --generic evidence-full --singular evidence-singular \
  --out perturbation-limits.json
```

The join checks the recorded hashes of both input packets and independent
replays. The source workflow runs it after the two atlas jobs succeed.

The exact replay checks 336,720 chamber incidences across 87,557 strata.
Of the 81,915 interior strata, 49,175 have no boundary-dependent cells
and realize both rules. The other 32,740 have boundary-dependent cells
and realize neither rule. On the supporting boundary, the closed rule
is attained at 5,310 of 5,642 strata.

At the previously recorded interior edge witness `(0, -1, 1+tau)` in
doubled window coordinates, six incident chambers yield six distinct
raw selections. The strict two-cell and closed fourteen-cell patterns
are both absent from these six selections.
