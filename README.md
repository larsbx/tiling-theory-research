# tiling-theory-research

Research workspace for higher-dimensional substitution tilings, beginning with a 2D Penrose pilot and designed to test which finite-state ideas from substitution dynamics survive when words are replaced by geometric interfaces.

## Current program: Penrose 2D pilot

The pilot uses Robinson-triangle prototiles and a frozen finite direction alphabet to study:

- exact child placements and parent-boundary partitions;
- oriented and reflected interface data;
- collar propagation;
- separator fields;
- symmetry/handedness quotients;
- residual interface state spaces;
- strict-growth candidates that could exclude recurrent ambiguity.

Start here:

1. `docs/penrose-2d/status-and-conventions.md` — source-grounded facts, mechanically derived facts, and open obligations.
2. `docs/penrose-2d/research-program.md` — theorem program and experiments.
3. `docs/psc-bridge.md` — what may transfer back to the PSC program and what must not be inferred.

## Current status

The pilot has frozen the core direction/prototile conventions and mechanically closed several table-completion tasks. The principal open mathematical target is the strict-growth invariant `Phi` (`G2D-2`), together with deeper continuation of the oriented separator data and the rhomb↔triangle aggregation writeup.

This repository is a sibling of `larsbx/pisot-substitution-conjecture-research`, not a theorem-status extension of it. Penrose computations and conjectures do not change PSC claim status unless a separate bridge theorem is proved with explicit hypotheses.

## Research discipline

- Keep **source-grounded**, **mechanically derived**, and **conjectural/open** facts visibly separated.
- Treat `D0,...,D4` as unoriented line-direction classes; reversed traversal is not a new alphabet symbol.
- Preserve orientation, side, handedness, collar, and ancestry data until a quotient is proved sound.
- Do not promote finite collar depth or finite state-space exhaustion to a universal theorem without a completeness proof.
- Store reusable dimension-independent kernels separately from Penrose-specific tables.
