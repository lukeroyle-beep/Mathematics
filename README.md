# Mathematics
Repository for mathematical conjectures. Solutions are verified in Lean.

The [trillion-length witness investigation](research/a398769/five-seven/trillion-witness/README.md)
independently excludes the next million odd lengths above a trillion,
checks 1,808 larger sampled lengths and all digit-sum-compatible positions
at 32 selected giant lengths. No witness or all-length proof was found.
The reported earlier trillion-length archive was unavailable; the new
interval is certified separately. These are exact computations and ordinary
proofs, with no new Lean formalization.

The [uniform-bound investigation](research/a398769/five-seven/uniform-bound/README.md)
proves the proposed quadratic valuation bound would close the `{5,7}`
subclass, gives uniform derivative control and a general Hensel reduction,
and quantifies the limits of specified degree-and-span rational-centre
estimates. General position thresholds retain their earlier
finite obligations. The valuation target remains unproved; all conjecture
statuses and whole-length coverage are unchanged. These are
ordinary proofs and exact checks, not new Lean formalizations.

The [three-deduction audit](research/a398769/five-seven/three-deductions-audit/README.md)
certifies the first depth-44 exception and restricted minus-line (E) through
`L<6*7^99`, excludes the closed strip `abs(12i-7L)<=L/10^9`, and excludes
the opposite line `12i-5L=+1`. These are position results; complete length
coverage and the open status of both conjectures are unchanged.

The [five-twelfths strip audit](research/a398769/five-seven/strip-audit/README.md)
excludes `abs(12i-5L)<=L/10^9` from full `{5,7}` witnesses and, with an
independently reproduced modular certificate, excludes every admissible
position on `12i-5L=-1` without a Fermat hypothesis. Complete length and
broad (E) coverage are unchanged; the wider conjectures remain open.

Lean proofs use the pinned toolchain and Mathlib dependency at the repository root.
The [Stage 2 counterexample restrictions](research/a398769/stage2/README.md) apply to all decimal digit lengths. The [Stage 4 reduction](research/a398769/stage4/README.md) treats numbers whose digits are all 3 or 9.

The [Stage 5 checkpoint](research/a398769/stage5/README.md) proves that a counterexample without a 7 uses only 3 and 9, and independently extends the finite search bound to `n < 10^24`.

The [two-five audit](research/a398769/five-seven/README.md) excludes position `i=3` at every length and proves that only finitely many `{5,7}` candidates remain. These analytic deductions are ordinary proofs; Lean checks the preserved at-most-two-fives and no-single-five restrictions. No numerical cutoff or complete `{5,7}` exclusion is claimed.

The [two-five follow-up](research/a398769/five-seven/settlement/README.md) independently excludes all lengths through 10,000,000 and proves all-length exclusions when the second-five position or its gap from the length is at most 395. The region where both grow remains open; these new results are ordinary proofs and exact finite computations, not new Lean theorems.

The [global follow-up](research/a398769/five-seven/global/README.md) verifies the limitation of fixed-modulus quotient tests and an exact two-quotient procedure for each length, correcting the supplied numerical bounds. It adds a seven-adic spacing lemma and a large digit-sum-only control. The subclass remains open; no global cutoff or new exhaustive interval above 10,000,000 is claimed.

The [effectivity investigation](research/a398769/five-seven/effective/README.md) proves uniform qualitative `v_7(F)=o(L)` and an effective all-length exclusion of the central strip `|L-2i|<=47`, with its finite obligation covered by the reproduced ten-million certificates. It also refines the exact quotient and digit-sum reductions. The full `{5,7}` subclass remains unresolved: no global effective cutoff or full witness is established, and the certified complete interval is unchanged. These are ordinary proofs and exact arithmetic, not new Lean formalizations.

The [proportional-position investigation](research/a398769/five-seven/proportional/README.md) verifies all five proposed proportional exclusions, strengthens the all-length midpoint strip to `|L-2i|<=179`, and excludes positive-width regions around `2/5` and `3/5`. It gives exact remaining ratio intervals and an explicit admissible family missed by the uniform rational-centre degree/height estimate. Both ten-million certificates were rerun; complete length coverage is unchanged, and no global cutoff, witness, or new Lean formalization is claimed.

The [digit-sum and depth investigation](research/a398769/five-seven/depth/README.md) audits an infinite family passing the full digit sum and the fourth power of seven, proves eight further forbidden prime divisors of the digit sum, and tracks exact bounded exponent representatives. At that stage the arbitrary fixed-depth construction and global effective cutoff remained unproved; complete consecutive length coverage remained through 10,000,000, with no new Lean formalization.

The [arbitrary fixed-depth audit](research/a398769/five-seven/fixed-depth/README.md) verifies the submitted theorem as written: every fixed positive seven-adic depth occurs exactly, with the full digit sum, at infinitely many odd lengths and actual positions in every open ratio interval. The two numerical examples and grid checks pass independent exact verification. The growing witness threshold at the same length, the all-length `{5,7}` subclass, and the full digit-1 conjecture remain unresolved. Inherited complete coverage is unchanged, including PR #12's one isolated excluded length; no new Lean formalization is claimed.

The [whole-length audit](research/a398769/five-seven/whole-length/README.md) strengthens this to infinitely many entire excluded lengths for each fixed maximum depth and each open position-ratio interval, including depth one via a checked choice of lift. Complete enumeration of both appendix lengths gives maxima four and seven. These are distinct from the earlier maximum-six isolated length and do not extend the consecutive certificate through 10,000,000. The all-length subclass and full digit-1 conjecture remain open.

The [high-depth position investigation](research/a398769/five-seven/high-depth/README.md), starting from merged PR #14, independently checks the unique bounded representative and zero-lift criterion. It proves that full-sum exponent CRT compatibility already stabilizes at the first depth with `T_k>L`, but obtains no bound forcing that representative to escape before depth `L-2`. Independent exact bounded diagnostics agree under ordinary and optimized Python. **No closing advance:** no global cutoff, full witness, added length interval, or new Lean formalization; consecutive coverage remains 1 through 10,000,000 inclusive.

The [early-rejection investigation](research/a398769/five-seven/early-rejection/README.md), starting from merged PR #15, independently reproduces both reported rows and certifies the stronger finite implication `9S|F => v_7(F)<K(L)` for every odd length 5 through 9,999,999. Complete power-cycle and linearized-lift/repunit implementations agree on ordered per-length digests under normal and optimized Python. A declared search of 2,768 structured lengths, including 2,721 beyond that interval, finds no counterexample. **No structural advance:** broad early rejection remains unproved, both conjectures remain open, and consecutive exclusion remains 1 through 10,000,000 inclusive. No new Lean verification is claimed.
