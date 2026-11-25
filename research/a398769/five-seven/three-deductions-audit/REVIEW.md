# Independent review of the three deductions

25 November 2026. **No must-fix finding.** The implementation reviewed was
`191f1448eed3e60ced979f9d30131cc61188b503`, based on
`8677446ad39f3a8d72f3a2123c6012c012f2d271`. The final delivery head is
checked separately after the review artifacts and aggregate integration
are committed; that exact-head confirmation is recorded in the draft PR.

The reviewer read the three new proofs, all four new checkers and their
receipts, the aggregate verifier, and the README claims. The inherited
five-twelfths proof, modular certificate, definition of (E), and coverage
record were also read. Reported PASS values and submitted constants were
treated as claims to test. The independent review added the new files
`review_check.py`, `review_results.json`, and this record; it changed no
implementation or inherited file.

## Mathematical findings

The minus-line polynomial identity and exact order of ten give one
exponent class at each depth. The proof correctly tests that class against
both endpoints of its own K band and discards `u=0`. Exhausting these bands
proves the stated minimality, including all earlier admissible positions.
The only own-band depths through 100 are 44, 56, 85, and 92. Their exact
next-depth residues and digit-sum residues agree with the submitted table;
each has `gcd(F,S)=1`. This proves restricted (E) below `6*7^99`, and the
first exception disproves only the version without the digit-sum premise.

For the seven-twelfths strip, the derivative identity gives valuation one
at positive depth for odd L. Strong Hensel applies only when `t>=3` and
gives distance `t-1`, with local uniqueness in `x+49Z_7`. This is precisely
the applicable statement of [Conrad, Theorem 4.1, printed p. 6](https://kconrad.math.uconn.edu/blurbs/gradnumthy/hensel.pdf),
which the reviewer reopened directly. The coefficient span handles both
signs of s, and the Mahler-measure argument permits reducible Q and content.

The reviewer also reopened [Bugeaud--Laurent, printed pp. 2--4,
Corollary 1](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf).
Both bases are units; the exponents are positive; the local degrees are
`e=f=1`; and the source's D therefore equals the global degree used here.
Both height hypotheses and every entry of the maximum are satisfied.
The `D^4` factor becomes `D^3*H` after the height substitution, giving
the claimed slope `47628/78125`. The additive Hensel loss leaves positive
margin `390361597` at `L=10^9`. A second independent focused proof review
reached the same conclusion after reopening both sources.

In the dependent branch, the norm makes j integral, the height bound gives
`|j|<H`, and torsion and signed LTE give
`t=2+v7(Dq-j)-v7(D)`. The subtraction at D=7 is retained. The size bound
therefore contradicts the full threshold. The small strip is empty by
odd parity, and the closed endpoints are covered.

For the opposite line, the parametrization includes `u=0`. Both unseeded
routes exhaust the depth-eleven classes and give `313281594` modulo
`1694851494`, with least length `3759379135`. The separate small case and
the inherited five-twelfths strip cover every admissible position without
a gap. Combining the two line exclusions with odd parity proves
`abs(12i-5L)>=3` for full witnesses.

## Independent arithmetic and reproduction

[review_check.py](review_check.py) imports no submitted checker. It finds
the polynomial roots by Newton iteration with doubled precision, starting
from every residue modulo seven. It then recovers the principal-unit
exponent one base-seven coefficient at a time. Neither submitted exponent
classes nor logarithm-series code enter discovery. Reduction from the
depth-100 root independently reproduces all 100 minus-line exponent
classes, and original-F modular evaluations reproduce all four exception
records. The same method reproduces all eleven opposite-line classes.

Additional controls exhaust the original F predicate over all 14,406
exponents of a complete depth-five period on each line. Three direct
enumerations of Q in its local class, at depths 3, 4, and 5, find seven
modular roots and exact distances 2, 3, and 4. These deliberately check
the distinction between a unique p-adic root and multiple modular roots.
An alternate rational logarithm enclosure uses the alternating
`log(1+z)` series scaled by `3/2`, independently verifying the constants.
Four deliberate false controls raise explicit exceptions.

The reviewer reran every submitted new checker in ordinary and optimized
Python. In all four cases the two outputs and committed receipt were
byte-identical. The independent review checker also passed in both modes,
with byte-identical output retained in [review_results.json](review_results.json).
Reproduce it from the repository root:

```sh
python3 research/a398769/five-seven/three-deductions-audit/review_check.py > /tmp/a398769-review.json
python3 -O research/a398769/five-seven/three-deductions-audit/review_check.py > /tmp/a398769-review-O.json
cmp /tmp/a398769-review.json /tmp/a398769-review-O.json
cmp /tmp/a398769-review.json research/a398769/five-seven/three-deductions-audit/review_results.json
```

These computations corroborate the finite claims and proof constants.
They do not numerically prove the all-length strip or rerun the inherited
ten-million searches. Those distinctions are correctly preserved in the
proofs and aggregate receipt. Consecutive whole-length coverage remains
1 through 10,000,000; broad (E) remains certified at odd lengths 5 through
9,999,999. No new whole-length coverage, global cutoff, Lean proof, or
settlement of either open conjecture follows.
