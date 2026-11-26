# Independent review record

Builder context: `/root`. Enumeration implementations were authored separately
by `/root` and `/root/independent_enumerator`; the analytic audit was authored
by `/root/analytic_audit`.

The fresh mathematical reviewer `/root/analytic_audit/fresh_math_review`
reported **PASS, no must-fix findings**. The reviewer read the primary
Bugeaud–Laurent theorem, independently reconstructed all six exact rational
endpoint margins, and checked root transport, actual degree, derivative,
multiplicative independence, every logarithm branch, all-b/all-L propagation
within each K-band, and the inherited small-b/large-K coverage. Normal and
optimized checker outputs matched the retained analytic receipt.

Mathematical review bindings:

| File | SHA-256 |
|---|---|
| ANALYTIC.md | `11bd393afad213ee9f90839f965af046b0fb69cc0fd49a49447c6798ae447344` |
| analytic_checks.py | `1b221dd71a78271a1579e210594c3f6daa4bf91a2281b40544d5f8134a9e1ca4` |
| analytic-checks.json | `3f1ac53fa70cd0e70af059bbce5b532f3914c05eb845c97ca4928cd1c9837c03` |

Fresh computational review by `/root/computational_review`, with a separate
boundary reviewer, reported **PASS, no unresolved or must-fix findings** at
implementation commit **`9eaa913f515e62667dbf706ec723043c5b0a193c`**.
The reviewer audited both complete enumerations, arithmetic types and bounds,
line parameterizations, periodic coverage, singular children, actual-pair
recovery, original decimal arithmetic, canonical hashes and aggregation.
Every one of the 301 partitions agreed. The reviewer freshly reran the
**entire original b=289 interval with both engines**, reproducing all its
counts and the `c004ba62...` pair-stream digest.

Both authors' control programs and aggregate verification were independently
run normally and under `python3 -O`, matching their retained receipts. The
reviewer's separate boundary tests covered 234 small intervals and 48
intervals around giant endpoints: 14,839 labelled pair occurrences, including
even endpoints, singleton intervals, `7|a`, `49|a`, and `h=-K²,0,+K²`.
Nine deliberate receipt corruptions (missing/duplicate partition, wrong
denominator, bound, source, line count, pair hash, pair count or survivor
list) were rejected. All 618 aggregate artifact bindings were checked.
The README conclusion and reproduction commands were reviewed at the same
implementation commit.

Reviewer-owned reproducible artifacts, added after that implementation
commit without modifying its mathematics, engines or original receipts:

```sh
rc=research/a398769/five-seven/rational-centres
python3 "$rc/review_checks.py" > /tmp/centres-review.json
python3 -O "$rc/review_checks.py" > /tmp/centres-review-O.json
cmp /tmp/centres-review.json /tmp/centres-review-O.json
cmp /tmp/centres-review.json "$rc/review-checks.json"
python3 "$rc/boundary_review.py" > /tmp/centres-boundary.json
python3 -O "$rc/boundary_review.py" > /tmp/centres-boundary-O.json
cmp /tmp/centres-boundary.json /tmp/centres-boundary-O.json
cmp /tmp/centres-boundary.json "$rc/boundary-review.json"
```

The original aggregate `verification.json` deliberately binds the reviewed
implementation, excluding the subsequently added review record and review
programs. Its normal/optimized reproduction remains byte-identical after
the review-only addition. All 377 inherited tracked files other than root
README remain byte-identical to main. The prepublication main refresh is
still `81dce203b1eecc61ec9fda36bc812095e2c89724`.

The mathematical conclusion is an all-length exclusion for the stated
reduced K²-centre subfamily. It does not extend B or settle either open
conjecture. No new Lean formalization was performed. No merge is authorized
by this review record; publication is a separate draft PR for Luke.
