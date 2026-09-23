# Mojo tiling research kernel

This directory is reserved for theorem-facing exact prototypes.

Planned modules, subject to issue #2:

```text
expansion.mojo
displacement.mojo
overlap_state.mojo
overlap_graph.mojo
recurrent_components.mojo
coincidence.mojo
growth.mojo
```

Nothing here should become a stable cross-repo API until issue #5's extraction gate is satisfied.

Rules:

- exact/fail-closed decisions only;
- no floating-point overlap acceptance;
- caps produce `inconclusive`;
- retain replayable obstruction witnesses;
- theorem-specific spectral implications do not belong in this directory.
