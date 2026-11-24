# Independent Stage 5 review

Reviewed on 24 November 2026 by a separate reviewer agent, against the supplied
archive and the integrated branch based on
`0c13017980679832e6f03b31e6a304da7749dc4f`.

**Result: no unresolved correctness finding for the documented checkpoint.**
The original Python argument-validation defect was reproduced and then verified
fixed. The searches' enumeration logic is unchanged. This review distinguishes
independent reviewer checks below from the implementation agent's full Mac runs
recorded in [run-receipt.json](run-receipt.json).

## Mathematical and code review

The no-7 proof is an all-length reduction: digits in `{3,5,9}` cannot form a
multiple of 25. A candidate containing 5 must therefore contain exactly one 5,
making its residue modulo 3 equal to 2. A 3 or 9 would divide the digit product
and hence the number, which is impossible. An all-5 digit list would make both
the product and sum divisible by 5, again forcing a multiple of 25.

The C++ search covers every multiset and every permissible prefix. With
`B <= D = P*S`, at most one suffix in `[0,B)` is congruent to `-prefix*B`
modulo `D`; checking that residue against the exact remaining digits is
exhaustive. Fixed-width zeros are rejected. The maximum divisor at length 23
is `207*9^23 = 1834628190768067726857303 < 2^128`; decimal values are below
`10^23`, and prefix counts are bounded by `5^23 < 2^64`.

The Python search independently enumerates quotient residue classes within
exact arrangement bounds. Dividing out the gcd in each congruence leaves
invertible factors. The remaining decimal-suffix and modulo-9 moduli are
coprime. Exact digit counts reject every incompatible candidate, using
arbitrary-precision arithmetic. The final diff changes input handling and
count-only reporting, without changing this enumeration.

The README correctly distinguishes the all-length no-7 reduction from finite
exclusions. The retained bound below `10^22`, the new length-23 computation,
and parity exclusion of every even length imply no counterexample below
`10^24`. The no-7 result through 75 digits additionally depends on the retained
Stage 4 computation. No all-length exclusion of `{3,9}`, `{5,7}`, or the full
alphabet is established here.

## Independent checks of the original archive

Direct brute force used the original condition `n % (P(n)*S(n)) == 0`, without
reusing either search's pruning or quotient congruences.

- **482 Python comparisons passed:** all `{3,5,7,9}` words through length 8
  at multiple suffix widths (20 comparisons); every odd-digit multiset through
  length 6 against all distinct permutations (461 comparisons, four hits);
  and the full 23-digit positive control (one comparison, ten hits).
- **16 C++ comparisons passed:** all `{3,5,7,9}` words through length 8;
  all `{1,3,5,7,9}` words through length 7 (seven hits); and the full 23-digit
  positive control. Compilation with `-Wall -Wextra -pedantic` was clean.
- Both controls matched all ten integers found by checking the 253 placements
  of two threes among 21 ones directly. C++ reported 232 prefixes and 96 tails
  in range; Python reported 27 candidate checks.

The original Python accepted `search(3,4,'111',True)` and incorrectly presented
zero hits, whereas width 3 finds 111. It also accepted `search(23,3,'111',True)`
and labelled the three-digit hit as length 23. Both malformed cases now raise
`ValueError` before printing a result.

## Independent checks of the final integrated sources

The reviewer verified all seven `tested_source_sha256` entries in the run
receipt against the files on disk, plus the archive digest and all four archive
member digests. `A398769/Stage5.lean` is byte-identical to `NoSeven.lean`.
The C++ difference from the archive consists only of two header comments.

The reviewer separately compiled the final C++ source and reran
`check_controls.py`: **259 prefix checks, 711 quotient checks, 18 invalid-command
checks, and the count-only check all passed**. The control suite itself was
reviewed: it compares exact results against direct decimal arithmetic, checks
complete multiset counts, and includes nonzero full-width controls.

Eight additional direct-API malformed-input cases were independently rejected
before output. Four positive controls (111 and 135, each at widths 1 and 3)
confirmed that count-only runs retain the same candidate counts while displaying
`NOT_CHECKED`, and `--run`/`perform=True` returns the known hit.

The receipt records successful clean project Lean compilation and the theorem's
axioms `[propext, Classical.choice, Quot.sound]`, plus both complete length-23
zero-hit runs. Those full runs were inspected as retained evidence, not repeated
by this reviewer. Upstream Lean artifacts were reused, and the earlier Stage 3
and Stage 4 full searches were not rerun. The finite searches are computational
evidence, not Lean kernel certificates.
