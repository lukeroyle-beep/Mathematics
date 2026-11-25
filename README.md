# Mathematics
Repository for mathematical conjectures. Solutions are verified in Lean.

Lean proofs use the pinned toolchain and Mathlib dependency at the repository root.
The [Stage 2 counterexample restrictions](research/a398769/stage2/README.md) apply to all decimal digit lengths. The [Stage 4 reduction](research/a398769/stage4/README.md) treats numbers whose digits are all 3 or 9.

The [Stage 5 checkpoint](research/a398769/stage5/README.md) proves that a counterexample without a 7 uses only 3 and 9, and independently extends the finite search bound to `n < 10^24`.

The [two-five audit](research/a398769/five-seven/README.md) excludes position `i=3` at every length and proves that only finitely many `{5,7}` candidates remain. These analytic deductions are ordinary proofs; Lean checks the preserved at-most-two-fives and no-single-five restrictions. No numerical cutoff or complete `{5,7}` exclusion is claimed.

The [two-five follow-up](research/a398769/five-seven/settlement/README.md) independently excludes all lengths through 10,000,000 and proves all-length exclusions when the second-five position or its gap from the length is at most 395. The region where both grow remains open; these new results are ordinary proofs and exact finite computations, not new Lean theorems.

The [global follow-up](research/a398769/five-seven/global/README.md) verifies the limitation of fixed-modulus quotient tests and an exact two-quotient procedure for each length, correcting the supplied numerical bounds. It adds a seven-adic spacing lemma and a large digit-sum-only control. The subclass remains open; no global cutoff or new exhaustive interval above 10,000,000 is claimed.

The [effectivity investigation](research/a398769/five-seven/effective/README.md) proves uniform qualitative `v_7(F)=o(L)` and an effective all-length exclusion of the central strip `|L-2i|<=47`, with its finite obligation covered by the reproduced ten-million certificates. It also refines the exact quotient and digit-sum reductions. The full `{5,7}` subclass remains unresolved: no global effective cutoff or full witness is established, and the certified complete interval is unchanged. These are ordinary proofs and exact arithmetic, not new Lean formalizations.
