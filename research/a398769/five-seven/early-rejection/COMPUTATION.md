# Independent finite early-rejection audit

The claim being tested is (E) on every odd length from 5 through 9,999,999
inclusive. No inherited full-witness filters are used. The uniqueness proof
in [PROOF.md](PROOF.md) shows that the sole representative `r_K(L)` exhausts
every possible violation at that length. Full valuations are unnecessary.

## Independent methods

[Implementation A](checker_a.py) enumerates the complete cycle of powers of
10 modulo `7^k`, storing each residue's least exponent. The cycle has
`6*7^(k-1)` distinct entries and returns to one. It looks up the target
`(7*10^L-25)*18^(-1) mod 7^k`, then computes `F mod 9S` by modular powers.
The power of 10 on the length side advances by multiplication by 100 when
the length advances by two. Every recovered representative is separately
checked with fresh modular powers at its actual L.

[Implementation B](checker_b.py) starts with `r_1=3` and performs successive
linearized lifts. With `m=7^k`, `T=6*7^(k-1)`, `y=18*10^r` and
`b=7*10^L-25`, it solves

```
c=(10^T-1)/m mod7,
a=((b-y)/m)*(y*c)^(-1) mod7,
r_(k+1)=r_k+a*T.
```

All divisions are exact divisions of integer differences, and the outgoing
congruence is checked. B caches lifts over odd length residues modulo
`T_(k-1)` at depth k, since the factor seven on `10^L` lowers the necessary
length precision by one. This is a table of successive lifts, not a table
of discrete logarithms. Each output representative receives a separate
modular defining-congruence check at its actual length.

B computes `R_L mod S` by concatenation of blocks `(p,r)=(10^j,R_j)`:
doubling gives `(p*p,r*(p+1))`, and appending one gives `(10*p,10*r+1)`.
It then evaluates `n mod S=(7R_L-2-2*10^r) mod S`. No division by nine
modulo S occurs. The exact identity

```
F mod(9S) = 9*(n mod S)
```

normalizes the result for comparison. If `n=qS+u` with `0<=u<S`, then
`F=9qS+9u` and `0<=9u<9S`, proving that identity even when `3|S`.
Neither checker imports code from the other or from an inherited checker.

## Ordered comparison and results

Each checker hashes one ASCII line for every length, in increasing order:

```
L:K:r:category:residue\n
```

The final character is a single LF byte. All numbers use ordinary unsigned
base-ten notation with no whitespace. `residue` is `-` only in category 1;
otherwise it is `F mod(9S)` in `[0,9S)`, including category 2.

| Category | Definition | 5..100001 | 5..9999999 |
|---|---|---:|---:|
| 1 | `r` outside `3<=r<L` | 21,628 | 3,041,861 |
| 2 | Actual `r`, `5|S` | 5,658 | 392,074 |
| 3 | Actual `r`, `5` does not divide S, nonzero full-sum residue | 22,713 | 1,566,063 |
| 4 | Actual `r`, `5` does not divide S, zero full-sum residue | 0 | 0 |
| Total | Every odd length in the interval | 49,999 | 4,999,998 |

Thus the reported actual counts are respectively **28,371** and
**1,958,137**, and both reported five-free counts also reproduce exactly.
There was no discrepancy in either row. Ordered SHA-256 values agree:

```
5..100001:  26f81c8c6d9f43786390b9aea1974965afe5906b280d30225a658bdb2e28c374
5..9999999: 037a7a03e48eceea6893641af0459885380975e2234aa11b6820a0d2a6c5f08f
```

The new format differs from PR #15's format, which also included exact
valuations. Consequently its digest need not equal the inherited digest.
The two new formats are identical to one another. Both receipts record
100 successive blocks of at most 50,000 lengths; all block endpoints,
counts and hashes agree, not just aggregate counts.

The certified conclusion is precisely: **(E) holds for every odd L from
5 through 9,999,999 inclusive.** This is stronger finite valuation evidence
inside inherited coverage. It does not extend the consecutive full-witness
exclusion of every length 1 through 10,000,000 inclusive.

## Controls and integer safety

Both implementations construct literal decimal words at all 9,900 pairs
with odd `5<=L<=201` and all `3<=i<L`: 4,950 positions of each parity.
They check the digit sum, digit product, polynomial identity, exact full
divisor and separated test, modular full sum, and uniqueness-depth coverage.
There are 74 shallow full-sum positives in this control domain.

* Strict boundaries `T_k-1,T_k,T_k+1` have depths `k,k+1,k+1`.
  The even equality case is explicitly included. A checks k=1..12; B
  checks k=1..9. The general order proof is ordinary mathematics.
* `(L,i)=(13,12)`, S=87, has `F mod9S=0`, exact depth zero and K=2.
  It tests full-sum success with `3|S`; it is **not** a uniqueness-depth
  survivor or a full witness.
* `(151,8)`, S=1053, has `F mod S=0` but `F mod9S=8424`.
  It detects loss of the factor nine and intentionally has an even position.
* `(23,15)` has `F mod49=0`, `F mod343=245` and exact depth two.
  It tests the inherited valuation regression.
* Every representative in the main audit is checked independently against
  its defining congruence and canonical period bounds.

Both checkers use arbitrary-precision Python integers for **all modular
products**. A's four-byte unsigned array stores exponents only, not modular
products: `0<=r<T_k<=34,588,806<2^32-1`, with `2^32-1` reserved as the
empty marker. It checks the array's item size. A rejects lengths above
34,588,805; B rejects lengths above 9,999,999. These are explicit resource
bounds. B uses arbitrary-precision integers in its lift table. Neither uses
floating-point logarithms for K. All essential checks use exceptions rather
than removable assertions, and ordinary and `python3 -O` full runs agree
byte for byte for each implementation.

## Reproduce and isolate a mismatch

From the repository root:

```sh
python3 research/a398769/five-seven/early-rejection/verify.py --recompute
python3 -O research/a398769/five-seven/early-rejection/verify.py
python3 research/a398769/five-seven/early-rejection/search.py > /tmp/early-search.json
cmp /tmp/early-search.json research/a398769/five-seven/early-rejection/search.json
git diff --check
```

`--recompute` executes both full checkers normally and under `-O`, comparing
each byte-for-byte against its committed source-bound receipt. Without that
option, the verifier checks source hashes, both receipts, all block coverage,
unsupported-input controls under normal and optimized Python, ancestry and
inherited preservation. It does not present receipt inspection as a fresh
full computation. [verification.json](verification.json) records the fresh
four-run audit performed in this investigation.

For a mismatch, take the first differing block's first and last odd lengths
from the receipts, then reproduce only that block, for example:

```sh
python3 research/a398769/five-seven/early-rejection/checker_a.py --min-length 5 --max-length 100003 --records /tmp/early-a.txt > /tmp/early-a.json
python3 research/a398769/five-seven/early-rejection/checker_b.py --min-length 5 --max-length 100003 --records /tmp/early-b.txt > /tmp/early-b.json
diff -u /tmp/early-a.txt /tmp/early-b.txt
```

Large raw streams are not committed. Source SHA-256 values are embedded in
[receipt A](receipt_a.json) and [receipt B](receipt_b.json); the verification
receipt additionally hashes both receipts and the verifier. The unchanged
inherited proof, source and large-certificate receipt bytes are checked
against the actual starting commit and the prior manifest. Those inherited
large computations were not rerun. No Lean source changes or new Lean
verification are claimed.
