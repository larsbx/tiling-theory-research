# Literature import ledger

**Status:** source-audit queue. Entries below are citation targets inherited from the PSC overlap work; they are **not imported theorem nodes yet**.

## Import candidates

### Akiyama–Lee — overlap coincidence

Target use: connect overlap coincidence for self-affine/Meyer tilings to pure point dynamical spectrum and obtain an algorithmic residual-component formulation.

Audit before import:

- exact self-affine hypotheses;
- role of the Meyer property;
- definition of overlap equivalence;
- finiteness/completeness requirements;
- whether the theorem is iff or one-way in the needed setting;
- whether connected/non-rod hypotheses belong to this theorem or to later strong-coincidence comparisons.

### Lee–Solomyak — Pisot family and Meyer property

Target use: determine when Pisot-family expansion supplies the Meyer property for self-affine tilings.

Audit before import:

- diagonalizability;
- algebraic conjugate multiplicities;
- representability assumptions;
- which direction of the characterization is needed;
- whether the selected candidate class can derive Meyer rather than assume it.

### Lee — substitution Delone sets / inter-model sets

Target use: relate algebraic coincidence, pure point spectrum, and inter-model-set structure for representable substitution Delone sets.

Audit before import:

- representability;
- legality/primitivity assumptions;
- exact equivalences versus implications;
- distinction between inter-model and regular model set.

### Regular model-set spectral theorems

Target use: calibration/endgame only when regular model-set structure has independently been established.

Firewall: assuming regular model-set status and then deriving pure point spectrum is not T2.

### Higher-dimensional Pisot/homological-Pisot literature

Target use: identify ambitious class-enlargement targets after T2 closes for a narrower class.

Firewall: record conjectural versus proved scope exactly; do not import a conjecture as a theorem.

## Import template

Each promoted imported theorem gets a record:

```text
ID:
Source:
Pinned bibliographic data:
Exact theorem number:
Repository paraphrase:
Conclusion type:
  [ ] pure point dynamical spectrum
  [ ] pure point diffraction
  [ ] overlap coincidence
  [ ] algebraic coincidence
  [ ] Meyer property
  [ ] model/inter-model set
Hypotheses:
  H1 ...
Repository discharge:
  H1 -> theorem/input ...
Known non-transfer:
Status: imported | blocked
```

No spectral claim enters the theorem ladder merely because a source is listed here.
