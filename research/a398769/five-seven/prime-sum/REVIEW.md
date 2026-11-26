# Fresh independent review

Reviewed implementation commit:
`99306e407dc0dee6bbbd8d883daf1c3594b93e05`.

Reviewer context: `/root/fresh_review`, 26 November 2026. This reviewer
did not write the prime-density proof, signed bound, archive enumerators,
archive verifier, or integration report. Review covers the actual files
at this commit, with the ordinary-proof and finite-computation status
retained. **No unresolved must-fix finding. The global target remains
unresolved.** Acceptance of these partial results is not acceptance of an
all-length proof or a counterexample.

## Mathematical audit

* **Prime digit sums.** The derivation retains the units-indexed position,
  `i=3 mod6`, and the full divisor `225S7^(L-2)`. The root conditions are
  necessary whole-length tests. The Eisenstein/binomial degree argument,
  affine group of order 42, unique fixed root, conjugacy of multiplier-three
  elements, and sufficient good-prime condition all check out. Aligning the
  Frobenius restrictions at 31/59 genuinely puts their ratio in the kernel;
  opposite actions on the fixed square-root fiber prove surjectivity and
  equal fiber sizes. This does not assume an unproved full Kummer group.
* **Sixth powers.** The intersection with `Q(zeta_6)` is trivial by
  ramification at three. The 199/283 controls both fix sixth roots of unity;
  their aligned ratio has a primitive sixth-root multiplier. This proves
  the required kernel character is onto. For the other congruence class,
  the action is a reflection, not a translation. Counting elements with a
  fixed point gives pass fractions `1/6` and `1/2`, hence overall exclusion
  `2/3`. The two-thirds denominator is all primes `p=3 mod7`; among all
  primes the exclusion is `1/9`, and among all lengths this prime-sum
  subset has density zero.
* **Signed bound.** The reviewer read Bugeaud's original
  [Theorems 2.2 and 2.3](https://arxiv.org/pdf/1609.07926). The positive real
  form uses `(7,10,M/7)` and exponents `(t,-L,1)`; the signed two-adic form
  uses `(7,-M/25)` and `(t,1)`. The heights, nonzero forms, normalized real
  exponent bound, minimal two-adic exponent valuation, choices
  `B=t`, `B_n=1`, `delta=log(A)/B`, and numerical coefficient majorants
  satisfy the stated inputs. The split covers every position and the
  `t<L/2` case is handled separately. A requested clarification explicitly
  supplying `log7>3/2` for `t<2L` was incorporated before the reviewed
  commit. The resulting exponent `1-1/(3*10^16)` is valid from `L=5` but
  exceeds `log7/log10`; it gives no closing cutoff.
* **Conditional cutoff.** Raising the proposed `5/6` bound to the sixth
  power and using `F<7*10^L` gives exactly
  `(117649/100000)^L<C^6*7^17`. Integer comparisons confirm the first
  excluding exponents 204, 323 and 714 for the displayed values of C.
  These remain conditional, and the effective starting length cannot be
  dropped. The required failed-lift index is at most `L-3`, not `L-2`.
* **Archive completeness.** Both archived source programs and both
  completeness proofs were reviewed. Base representatives are unique;
  the first-order expansion is an exact congruence at depth `2d-1`;
  lattice line/point intervals and recursive floor counts enumerate the
  full rectangles. The floor rectangle may include `i=B`, which its final
  `i<L<=B` predicate correctly rejects. Lattice bounds already use `B-1`
  for the position. All odd lengths through B are retained. The supported
  integer bounds suffice; the diagnostic wrapping signature is not used
  in place of pairwise list comparison.
* **Density one among lengths.** The fixed-progression character argument,
  second-moment bound, and finite periodic iteration in the archive are
  valid. [Akbary–Yazdani Lemma 2.3(i)](https://www.cs.uleth.ca/~akbary/Akbary-Yazdani.pdf)
  explicitly states the unconditional order result for a positive
  function tending to zero, supporting the specified fixed-M choice.
  The original Erdős–Murty article could not be opened by this reviewer;
  no claim to have read that original is made. The character events need
  not be independent: their intersections are bounded by the CRT
  divisibility events. Taking an upper-density bound after each finite
  stage is legitimate and leaves possible exceptional lengths.

## Fresh reviewer checks

The reviewer ran `prime_density_checks.py`, `global_checks.py`,
`independent_checks.py`, and `archive_audit.py`, then `verify.py` against
the reviewed commit. The aggregate checks 18 new artifact bindings and
35 inherited PR #21 bindings. Arithmetic checks reproduced all retained
outputs; for the default archive invocation its explicit `not_rerun`
enumeration field was separated before comparing the decimal receipt.

This independently rechecked all 74,601 archive candidates by original
decimal-run concatenation, their exact valuation histogram and three
depth-27 residues, and all 182 small words. The polynomial checker
exhaustively tested all 207 good primes in its declared range, and the
separate literal checker tested 9,900 decimal pairs and all 71 primes
in its smaller range. Nonzero positive and negative controls were
retained; no sampled valuation was promoted to a full witness.

An additional independent floor-count check compared the archived
Euclidean recurrence with the direct count
`sum((a*j+c)%m < lim for j in range(n))` for every
`1<=m<=39`, `0<=n<=20`, `0<=a,c<m`, and
`lim` in the five-entry list `[0,1,m//2,m-1,m]`.
All **2,156,700** comparisons passed, including zero slope, empty
intervals and the `c=lim` boundary.

The reviewer did **not** rerun either full C++ enumeration. Their fresh
builder executions, exact source/output bindings, complete pairwise
comparisons, and completeness proofs were inspected. The separate
842-million-length early-rejection search, PR #21's million-length
arithmetic scan, and Lean build were not rerun. Direct child-program
normal/optimized comparisons are builder evidence; invoking the aggregate
with `-O` alone would not propagate that flag to its child invocations.

## Coverage and verdict

The freshly audited archive excludes 1 through `10^12`. The adjacent
PR #21 interval ends at `1,000,002,000,000`, including its final even
length via the inherited parity reduction. The two intervals join without
a gap and retain distinct provenance. This adds no consecutive length
beyond their union and does not extend broad `(E)`.

The integration report correctly labels the exact-density results as
subclass theorems, the signed bound as insufficient analytic progress,
the combined endpoint as finite coverage, and the all-length question
as open. The first unsupported global step is still a uniform failed
lift for every remaining sum-compatible actual representative, including
composite digit sums. No other digit family is settled by these results.

Only this review record and its manifest binding are expected after the
reviewed implementation commit. Any mathematical, checker, source, or
coverage change requires renewed review. Publication as a draft PR and
leaving merge to the owner are consistent with this verdict.
