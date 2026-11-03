# Local cone covers at singular AKN shifts

This experiment advances issue #24 on the fixed AKN arrangement. It
keeps the existing claim statuses and uses the certified singular
memberships and common-translation incidences. A selection includes
all forced cells, excludes all absent cells, and may use any subset
of the boundary-dependent cells.

Each signed triple generates a simplicial physical tangent cone at
the center. The 15 planes spanned by pairs of physical axis lines
cut direction space into 120 open chambers. The program generates
sign vectors using flags of the form r + εu + ε²v. Here r is a
signed ray along a plane intersection, u is a signed tangent
direction within an incident plane, and v is a signed normal to
that plane. Signs use the first nonzero coefficient in exact
arithmetic. The incremental arrangement count independently checks
completeness. Adding a plane cut by k distinct lines adds 2k
chambers.

A cone is the intersection of three halfspaces from the physical
arrangement. Its interior membership is therefore constant on each
direction chamber. A selection is a local cover with disjoint
interiors exactly when every direction chamber belongs to exactly
one chosen cone. Coverage on the planes follows by closure. The
search branches on an uncovered direction chamber and enumerates
every compatible cell covering it. It has no search cap.

The local covers are face-to-face near the center. All axis triples
are independent, as checked by the cone construction. Two cones
with disjoint interiors can meet only on their boundaries. A
two-dimensional intersection must lie in one facet plane of each
cone. That plane has exactly two axis lines, so the corresponding
quadrants coincide or meet in a shared ray. In a one-dimensional
intersection, a shared ray cannot be interior to two facets in
distinct planes, since the two inward halfspaces would have
overlapping interiors there. It is therefore a generator of at
least one cone. Independence of axis triples then forces it to be
a generator of the other. These are local statements about the
common center.

Across 87,557 strata and 8,331 membership patterns, the exact
search finds 158,073 stratum–star pairs satisfying this local
condition. Of these, 139,601 are realized by common generic
translations and 18,472 are additional, occurring on 2,494 strata.
All additional stars are outside the 24 generic icosahedral orbits.
They give 96 additional orbits. The artifact records a stratum
witness and raw signed-cell selection for each orbit.

For instance, the interior edge witness (0, 1, 1+tau) in doubled
window coordinates has six common-translation selections and two
additional eight-cell local covers. One of the covers consists
of signed triples

```text
(-4,-3,-2) (-4,-3,6) (-4,-2,5) (-4,5,6)
(-3,-2,-1) (-3,-1,6) (-2,-1,5) (-1,5,6)
```

The source workflow emits the packet after verifying the generic
and singular atlases and generating their translation incidences.
The 96 orbits establish local geometric feasibility. Consistency
of a choice at neighboring vertices and extension to a whole
tiling remain open.
