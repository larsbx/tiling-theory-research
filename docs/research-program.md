# Research program — higher-dimensional PSC successor

**Status:** planning surface. No theorem is established by this document.

## 1. Core question

Find a mathematically natural class \(\mathcal C\) of substitution tilings in dimension \(d \ge 2\) for which a **finite exact obstruction theory** proves coincidence uniformly:

\[
T\in\mathcal C
\Longrightarrow
\text{overlap/algebraic coincidence}
\Longrightarrow
\text{pure discrete dynamical spectrum}.
\]

The second implication should be imported from the literature with exact hypotheses checked. The first implication is the intended research contribution.

## 2. Why this is a successor to PSC

The transferable architecture is not one-dimensional interval geometry. It is the proof pattern:

1. encode exact local disagreement states;
2. close them under inflation/substitution;
3. reduce failure to a recurrent nonproductive component;
4. retain enough ordered/geometric information that Perron growth alone cannot erase;
5. force a coincidence or contradict class hypotheses;
6. keep the spectral theorem as a separately audited import.

The higher-dimensional program must re-prove every step whose one-dimensional proof used interval order, left/right boundaries, scalar displacement, or one-dimensional balanced-pair structure.

## 3. Research tracks

### Track A — theorem class

Define candidate classes \(\mathcal C_0\subseteq\mathcal C_1\subseteq\cdots\) with hypotheses separated into:

- substitution dynamics;
- expansion algebra;
- finite local complexity;
- Meyer/displacement structure;
- tile topology;
- representability;
- coincidence criterion prerequisites.

The first successful theorem should use the **weakest class for which a uniform obstruction proof closes**, not the broadest imaginable class.

### Track B — exact overlap object

Generalize the one-dimensional state `(i,j,t)` to a translation-valued overlap state

\[
(i,j,z),\qquad z\in L,
\]

with inflation update

\[
z' = Qz + q-p.
\]

The exact representation of \(L\), and the exact intersection predicate for prototiles, are theorem-facing design decisions.

### Track C — bad-component normal form

Given a finite complete overlap graph, failure of coincidence should reduce to a closed/recurrent SCC with no coincidence state. Record:

- state translations;
- ordered child occurrences;
- multiplicities;
- expansion action;
- geometric incidence/intersection data;
- any collar/context data required for realization.

Do not collapse immediately to an unlabelled count matrix.

### Track D — productivity theorem

Seek a class-wide contradiction for a hypothetical noncoincident recurrent component. Candidate mechanisms include:

- Meyer uniform discreteness;
- contracting/internal-space recurrence;
- algebraic conjugate contraction;
- boundary/contact graph constraints;
- recognizability and supertile alignment;
- homological/cohomological restrictions;
- coincidence-rank or maximal-equicontinuous-factor structure.

Each mechanism must state exactly where the class hypotheses enter.

### Track E — spectral import

Once coincidence is established, invoke the appropriate literature theorem only after:

1. pinning the source;
2. recording the exact theorem statement;
3. mapping every hypothesis to a repository theorem/input;
4. distinguishing dynamical pure point spectrum from topological pure point spectrum;
5. recording whether the conclusion concerns the \(\mathbb R^d\)-action, diffraction, or both.

## 4. Non-goals

This program does not aim to:

- prove that all substitution tilings have pure discrete spectrum;
- use Penrose as the theorem statement;
- treat regular model-set structure as a new conclusion when it is assumed;
- promote finite experiments to a class theorem;
- infer exact tile intersection from floating-point geometry;
- silently impose unimodularity or connectedness.

## 5. First deliverable

The first substantive PR after this scaffold should produce a **candidate-class matrix** comparing 3–5 plausible \(\mathcal C\)'s and identify one T1/T2 target with:

- exact hypotheses;
- known imported implications;
- one explicit unresolved theorem obligation;
- at least three positive calibration families;
- at least two negative controls outside the class.
