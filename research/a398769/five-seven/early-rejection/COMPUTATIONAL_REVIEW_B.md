# Independent computational review B

Reviewer context: `/root/checker_b`, 25 November 2026. This reviewer authored
Implementation B independently, completed its first full audit, and only then
read Implementation A. No A or inherited checker code was read while deriving
or implementing B, and B imports no checker code.

## Reviewed implementation A

Reviewed source: `checker_a.py`, SHA-256
`ca74c198c634347eca2a719bd2d31ab8fc3a43e038df95ebf3d734fdeea440e8`.

No mathematical or computational must-fix finding was found in this source.
The complete unit cycle rejects an early repetition and verifies closure and
the exact unit-group cardinality. Recovering the exponent uses the inverse of
18 modulo a power of seven. Every returned representative is separately
checked by modular exponentiation at the original length. The full-sum test
uses the entire modulus `9S`, including the cases where `3 | S`.

The strict `T_K > L` test, actual interval `3 <= r_K < L`, four categories,
odd-length endpoints, and coverage count agree with the mathematical domain.
The full range contains both parity possibilities before the modulo-seven
condition; the literal controls enumerate both position parities. No inherited
full-witness filter is used to discard a possible broad-(E) violation.

All modular products are Python arbitrary-precision integers. Only the inverse
table's exponent storage is fixed width: its four-byte width is checked,
`K <= 9` is enforced for constructed cycles, and its largest stored exponent
is below `34,588,806`, well below its `2^32-1` sentinel. Unsupported CLI
intervals are explicitly rejected. Essential checks use exceptions, not
removable assertions.

## Independent implementation B and observed reproduction

Final reviewed/executed B source SHA-256:
`8e697625fa29102dee4a4edc8d900e0aa810825c32f8f1b4a8298d0474e98125`.

B recursively constructs its representatives by successive linearized lifts.
The cache is indexed by odd length residues modulo `T_(k-1)`: multiplying the
length-side power by seven reduces the needed length period to that of
`10 modulo 7^(k-1)`. Each cached value is a lift from the preceding depth,
with exact-division and outgoing-congruence checks. Each streamed length then
receives a separate defining-congruence verification.

B computes `R_L modulo S` by binary decimal-block concatenation, with no
division by nine. It forms `n modulo S`, and normalizes to `9*(n modulo S)`.
This provides independent representative recovery and independent digit-sum
arithmetic from A.

Final B commands, run from the repository root:

```sh
python3 research/a398769/five-seven/early-rejection/checker_b.py > /tmp/early-b-normal.json
python3 -O research/a398769/five-seven/early-rejection/checker_b.py > /tmp/early-b-optimized.json
cmp /tmp/early-b-normal.json /tmp/early-b-optimized.json
cmp /tmp/early-b-normal.json research/a398769/five-seven/early-rejection/receipt_b.json
```

The observed final normal and optimized runs took 18.926 and 18.947 seconds
respectively and produced byte-identical receipts. The normal receipt was
written directly to `receipt_b.json`; the commands above are the equivalent
non-mutating reproduction procedure. Earlier benchmarking used the small row;
final receipts include the additional explicit control-depth labels requested
during review.

Both reported rows reproduced exactly:

| Odd lengths | Examined | Actual representative | Actual and five-free | Full-sum passes |
|---|---:|---:|---:|---:|
| 5 through 100001 | 49,999 | 28,371 | 22,713 | 0 |
| 5 through 9999999 | 4,999,998 | 1,958,137 | 1,566,063 | 0 |

The main four-way partition is
`[3041861, 392074, 1566063, 0]`; the small partition is
`[21628, 5658, 22713, 0]`.

After both implementations completed, this reviewer directly compared the
overall ordered digest and every block's first length, last length, count,
and digest. All **100 blocks** agree, not merely the aggregate counts.
The common main SHA-256 is
`037a7a03e48eceea6893641af0459885380975e2234aa11b6820a0d2a6c5f08f`;
the prefix SHA-256 is
`26f81c8c6d9f43786390b9aea1974965afe5906b280d30225a658bdb2e28c374`.

## Required controls

Both sources include literal decimal checks for every position at every odd
length 5 through 201: 9,900 pairs, with both even and odd positions. These
verify digit product, digit sum, `9n=F`, the exact full divisor, the separated
condition on five-free sums, and sole-representative coverage. B independently
checks full-sum residues against the literal numbers; A additionally records
suffix/five-valuation checks and shallow seven-power comparisons.

Strict period checks cover `T_k-1`, `T_k`, and `T_k+1`, including even equality
lengths. B covers `k=1..9`; A covers `k=1..12` and independently checks exact
orders at those depths.

* `(13,12)` is a **shallow full-sum positive control**: `S=87`, full-sum
  residue zero, exact depth zero, `K=2`. It is not a uniqueness-depth survivor.
* `(151,8)` is the **loss-of-nine negative control**: `F mod S=0` but
  `F mod(9S)=8424`.
* `(23,15)` is the inherited **valuation regression**: `F mod49=0`,
  `F mod343=245`, exact depth two.

The finite result proves (E) over the audited odd lengths only. It does not
bound an unexamined length and does not extend inherited consecutive
full-witness exclusion beyond length 10,000,000. These are exact finite
computations outside Lean.

## Separate verifier review finding

During review of the first `verify.py` draft, this reviewer found that B's
coverage fields were read from the receipt root instead of its `audit`
object. This schema-integration defect was reported to the parent reviewer
for repair before final verification. The checker sources and their finite
results are unaffected. The final verification receipt and overall review
record must establish that the repaired verifier executes successfully.
