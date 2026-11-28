# Sources and current-main reconciliation

The fetched starting main is exactly
`61a6fdfd7f4093b77be36ed0a55fbd3ebf798b7c`, the requested PR #30 merge.
Git ancestry and the live GitHub PR metadata both confirm it. There are
no later commits on that fetched main. This work branches from it as
`research/a398769-power-three-carry`, in a separate worktree.

The task's repository inputs were read: `power-three-individual/`'s
`MOVING_POSITION.md`, `COMMON_FACTOR.md` and `INDIVIDUAL.md`,
`power-three/INDIVIDUAL.md`, and `power-three-pair/PAIR.md`. The latest
inherited family endpoint is 259 members through a=1579. PR #30's
valuation estimate is used as a merged theorem; this work does not claim
a new analytic logarithm estimate or a new audit of its external paper.
The inherited pair theorem still permits isolated witnesses.

Before changing the root README, PR #30's `verify.py --run` and
`review_check.py` both passed normally and under optimized Python.
The new aggregate verifies every inherited Git blob against the base
tree, allowing only an additive root README entry. Historical source and
receipt bindings are preserved, not rewritten. To rerun the historical
root-README-bound checks after this change, use a detached checkout at
the base commit; run the new aggregate in this branch.

`certificates.py` explicitly reuses the inherited Newton/logarithm engine
from `power-three/individuals.py`; its exact source is hash-bound. The
second reconstruction imports no arithmetic from that engine: it solves
the original decimal-block congruence by testing all three ternary
children. A modular inverse exponent independently checks the seventh
root. This is two reconstruction methods with disclosed reuse, not two
new Newton implementations. Both recover the preceding representative
without an actuality restriction. Pilot values are compared only after
the recovery and original-word checks.

`corollary_checks.py` independently revalidates all 259 inherited paired
rows using their unique-domain congruences and freshly computed original
decimal blocks. `one_step_checks.py` imports no project arithmetic. It
tests the lift against every child, full small residue periods, differences
and range endpoints. Its synthetic starts test the theorem's algebra;
they are explicitly not claimed to be actual ternary positions. Positive
surviving roots and nonzero residues prevent an all-rejection check from
passing vacuously. The universal one-step assertion rests on the proof,
not on sampled computation.

The full-word product and sum are recomputed from literal decimal digits
for 2,015 small pairs and the separate lost-factor-nine control. The giant
words are checked by exact modular concatenation, not materialized.
No proposed full witness survives these checks; none is inferred from a
necessary congruence. A depth guard is an unresolved computation, never
an exclusion.

The trillion-scale consecutive endpoint is inherited. Neither this work
nor these selected giant lengths extend it. Lean files are unchanged,
and no Lean command was run.
