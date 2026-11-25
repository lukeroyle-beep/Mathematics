# Independent review and acceptance record

25 November 2026. Base `2aea8ff77232225a68f5ebe694b812bc3a9438b8`.
Review was performed by separate assistant agents with distinct authorship
and checking responsibilities, followed by the primary investigator's
reconciliation. This is an internal mathematical/code review, not a claim
of external peer review or Lean verification.

## Review scope and independence

1. **Five-inequality auditor:** independently read the attached submission,
   the merged algebraic reductions, and the primary Bugeaud--Laurent
   definitions and Corollary 1. Authored `AUDIT.md`, checked all five
   verdicts and constants, both cubic offset signs, simple roots,
   reducibility, multiplicative dependence, and the midpoint refinement
   through 179. Ran a separate temporary rational/logarithm and cubic
   checker before inspecting the primary implementation.
2. **Rational-coverage investigator:** independently derived and authored
   `COVERAGE.md`, including the quintic strips and quantitative obstruction.
   Reviewed `AUDIT.md`, the primary checker's code, the independent
   checker's code, and the final mathematical summary; reran both checkers.
3. **Independent arithmetic reviewer:** implemented `independent_checks.py`
   without importing the primary checker or project proof modules. Reran
   both complete ten-million certificates. Reviewed the primary checker,
   both proof notes, and final receipt/summary claims, with checks normally
   and under `python3 -O`.
4. **Primary investigator:** authored `checks.py` and the summary, reviewed
   both proof notes and the independent checker, verified the actual base
   and PR #10 merge, reran both new checkers in normal/optimized modes,
   and compared the two inherited certificate receipts field by field.

The final substantive file hashes and each independent review's scope
are listed in `review.json`. No unresolved mathematical defect was found
within these claims. The final wording preserves the qualifications below.

## Verified claims

- Each of the five submitted strict necessary inequalities is valid;
  equality endpoints are excluded. The correct radii are obtained by
  dividing the offset coefficient by the denominator of the centre.
- The source parameter is exactly `(k/H+1/D)/log 10`. Local `e=f=1`
  is justified by the selected Hensel root lying in `Q_7`; the global
  degree remains in the theorem coefficient and height parameter.
- The midpoint consequence through 165 is correct. An additional
  fixed-height proof excludes every odd offset through 179 at every
  length, using a strict comparison valid for all `L>=10000000`.
- Both new fifths exclusions have ratio radius `1/10000000`, use a
  changing offset, handle negative cleared exponents and all possible
  root degrees/dependence cases, and start at the same certified length.
- The four and six displayed proportional-complement intervals are
  exact. The fixed 179 strip additionally changes the midpoint endpoints
  when `10000000<L<10740000`.
- The standard degree-`b`, coefficient-span height majorant cannot cover
  the stated family near `sqrt(2)-1`. The proof checks the actual-length
  threshold; it does not rely on density or finite plots.
- The full divisor, the factor 9 in the digit-sum condition, and the
  `(23,15)` regression remain intact. Modular controls are not witnesses.

## Observed finite verification

The primary checker passed 9,800 cleared-polynomial identities and 8,500
root-distance comparisons, with 1,700 positive modulo-7 controls. Its
finite signed exponent cases include negative, zero, and positive values.

The independent checker reconstructed 3,540 decimal pairs and their
actual digit products and sums; checked 17,700 polynomial identities,
18,300 root-distance comparisons through `7^6`, and 180 nonsquare
midpoint discriminants; and checked six exact gap-family samples against
4,146 rational centres. These finite checks support the arithmetic and
boundary calculations. They are not the proof of the infinite coverage
failure or of all-length strip exclusion.

Both checkers passed normally and under `-O`, with byte-identical output.
The full lifting certificate rerun matched its retained receipt in every
field except observed elapsed time. The independent fixed-modulus rerun
matched every field. Exact source and receipt hashes, commands, and
comparison fields are retained in `verification.json`.

## Explicit limits

Complete length coverage remains 1 through 10,000,000 inclusive. No
analytic threshold for a claimed strip exceeds that certificate, so no
finite bridge remains outstanding. There is no global cutoff or full
witness; no new exhaustive interval above ten million is claimed.

The gap family is known to pass only the specifically listed congruence,
length, and position filters. Its growing-power and full digit-sum
divisibility are not asserted. The obstruction concerns a specified
uniform estimate, allowing possible refinements from actual proper
factors, sharper root heights, dependent roots, the full digit-sum test,
or the exact quotient candidates. Uniform exclusion over the remaining
positions is still unproved.

No Lean source changed and no fresh Lean build was performed. Publication
is a draft PR for owner review; merge is outside this investigation.
