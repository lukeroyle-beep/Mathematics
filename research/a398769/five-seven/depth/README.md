# Full digit-sum survivors, prime filters, and bounded seven-adic depth

25 November 2026. Starting `main` and verified PR #11 merge:
`5f262828091f50039da1605f660a98b85c121f5c`.
Separate branch: `research/a398769-digit-sum-depth`.

**Both submitted deductions pass independent audit. The full `{5,7}`
subclass remains unresolved.** There is an infinite family of actual
positions in the gap `(41/100,42/100)` passing the full digit-sum condition
and the fourth power of seven. Eight further prime divisors of the digit
sum are forbidden in any full witness. Neither result bounds all lengths.

For every residual pair retain

```
F=7*10^L-18*10^i-25, n=F/9,
P=25*7^(L-2), S=7L-4,
full test: 225*7^(L-2)*S | F,
full digit-sum test: 9*S | F.
```

The seven proportional exclusions, fixed midpoint exclusion through 179,
earlier discrete restrictions, and the `(23,15)` regression are preserved.
All results here are ordinary proofs or exact computations. No Lean source
changes, new formal theorem, or fresh Lean build are claimed.

## Audited deductions

[FAMILY.md](FAMILY.md) proves that, for every `t>=0`,

```
a=193+1470t, S=898129*3^a, L=(S+4)/7
```

has a position `41L/100<i<42L/100` with `225*7^4*S | F`.
The proof retains the factor nine, verifies every overlapping exponent
class, and uses the actual spacing to put a representative in the strict
interval. The supplied enormous sample has valuation **exactly four**,
so it is not a full witness. Direct modular exponentiation and independent
concatenation of its decimal blocks verify both claims without constructing
the decimal integer.

[PRIME_FILTERS.md](PRIME_FILTERS.md) verifies all 21 gcd rows, the complete
factorization and primality certificates. The eight new forbidden prime
divisors of `S` are

```
127, 239, 1933, 2689, 4649, 459691, 909091, 10838689.
```

The prime 43 has the stated genuine exception; if it divides a full
witness's sum, then `L=191 mod 1806` is necessary. The new 127 filter
excludes `q=68 mod 127` in PR #11's rounded family. That family's first
pair remains a negative control: it fails the full sum and has valuation
two. An explicit infinite progression avoids all thirteen forbidden
prime factors, demonstrating why this finite prime list does not force
an upper length bound.

## A complete exclusion at one enormous length

[checks_depth_samples.py](checks_depth_samples.py) independently enumerates
**all 14,997 full-digit-sum positions** `3<=i<L` at the supplied length
`L=(898129*3^193+4)/7`, not only positions in the target ratio interval.
Their exact valuation distribution is

| `v_7(F)` | Number of positions |
|---:|---:|
| 0 | 7,499 |
| 2 | 6,427 |
| 3 | 918 |
| 4 | 131 |
| 5 | 19 |
| 6 | 3 |

Every position is independently checked by concatenating the four decimal
blocks modulo `S` and `7^7`. The maximum six excludes **all residual
positions at this one length**, hence the whole original subclass at that
length using the inherited reduction. In the strict ratio interval there
are exactly 150 sum-compatible positions, with maximum four. The receipt
[depth_samples.json](depth_samples.json) retains the exact class, endpoints,
three maximal positions, counts, and deterministic position/valuation digest.
No bound on all members of the infinite family follows from this calculation.

## Growing power and the precise gap

[BOUNDED_DEPTH.md](BOUNDED_DEPTH.md) gives an exact least-representative
criterion and count at **every** residual length passing the inherited
5 filter, including lengths outside the special family. If `rho_k` and
`W_k` are the compatible CRT representative and period, its first point
in the strict target interval is

```
A=floor(41L/100)+1, B=floor((42L-1)/100),
j_k=A+((rho_k-A) mod W_k).
```

Existence is equivalent to `j_k<=B`; a large period alone does not exclude
a small representative. The checkers compare this exact criterion with
literal decimal words over complete small domains and include positive,
incompatible, and too-large representative controls.

For a variable `c,k` construction, the proof records both subgroup
membership and CRT overlap obligations and the sufficient spacing bound
`700J<=9cg`, where `J=lcm(ord_c(10),6*7^(k-1))` and
`g=gcd(J,3^(a-2))`. Raising `a` with the present fixed `c` does not make
this sufficient condition hold at arbitrary depth.

The first unproved step for the intermediate question is to establish,
**for every fixed `k>=4`**, compatible parameters with a representative
inside the actual interval, or a uniform upper bound on attainable depth.
For regional exclusion, the missing statement is rejection at `k=L-2`
for every remaining length. No such uniform statement, regional theorem,
global effective cutoff, or full witness is obtained here. The inherited
uniform `v_7(F)=o(L)` still has no effective starting length. The other
ratio regions remain as recorded in the merged coverage note.

## Validation and complete coverage

Both inherited ten-million certificate programs were rerun unchanged.
The lifting result matches the retained receipt apart from elapsed time;
the independent fixed-modulus result matches every field. Complete
consecutive length coverage remains **1 through 10,000,000 inclusive**.
The one additional isolated length above is excluded; no new consecutive
interval above ten million is certified. There is no new analytic threshold
or finite bridge being claimed.

Use Python 3.9+ and a C++17 compiler for the inherited lifting program:

```sh
python3 research/a398769/five-seven/depth/checks_family.py
python3 research/a398769/five-seven/depth/independent_checks.py
python3 research/a398769/five-seven/depth/checks_crt.py
python3 research/a398769/five-seven/depth/checks_depth_samples.py
python3 research/a398769/five-seven/settlement/verify.py --output /tmp/depth-lifting.json
python3 research/a398769/five-seven/settlement/verify_fixed.py --output /tmp/depth-fixed.json
git diff --check
```

All four new programs are also run under `python3 -O`; their checks remain
active and deterministic output must match. The programs do not import
one another. Retained JSON outputs, [verification.json](verification.json)
and [REVIEW.md](REVIEW.md) record the computation and independent review.
The requested draft PR is for owner review; merging remains with the owner.
