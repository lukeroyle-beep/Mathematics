# Two-five investigation: still open, with a larger proved exclusion

24 November 2026. Base: latest `main` at
`66f9135254ec4f4dc58acfc6287170fff23e098a`, the merge of PR #7.
Earlier work and the merged audit are preserved.

**Verdict: still open.** No witness or all-length exclusion of the complete
`{5,7}` subclass has been established. The following new exclusions are verified:

1. There is no residual pair at any odd length `5 <= L <= 10,000,000`,
   even for the weaker condition `7^(L-2) | F`. Two independently implemented
   exact searches establish this finite result.
2. At **every length**, there is no residual pair with `i <= 395` or
   `L-i <= 395`. This combines the finite certificate with explicit
   position-dependent and gap-dependent bounds from Bugeaud–Laurent.
   The largest admissible position and gap in those regions are 393 and 394.
3. The full divisor adds the necessary filters `L != 27 (mod 37)` and
   `L != 15 (mod 101)`, in addition to the audited 5, 11 and 13 filters.

The audited elementary reduction covers every positive decimal integer
whose digits are all 5 or 7: zero, one, or at least three fives are excluded;
the remaining number has two fives, at positions 0 and `i`. Thus result 1
also excludes the original subclass at all lengths through 10,000,000,
including even lengths by the parity argument. It does not exclude all lengths.

## Exact domain and remaining obstruction

For odd `L >= 5`, `3 <= i < L`, `i=3 (mod 6)`, write

```text
F = 7*10^L - 18*10^i - 25,
n = F/9, P = 25*7^(L-2), S = 7L-4.
```

The full test is exactly `225*7^(L-2)*(7L-4) | F`. No coprimality is
presupposed in this equivalence. [FULL_DIVISOR.md](FULL_DIVISOR.md) proves
the sum filters and the circumstances under which the test can be separated.

Any still-possible witness must satisfy all of:

```text
L > 10,000,000, L odd,
417 <= i < L, i = 3 (mod 6), L-i >= 396,
(L mod 6, i mod 42) in {(1,39), (3,3), (5,15)},
L != 2 mod 5, 10 mod 11, 8 mod 13, 27 mod 37, 15 mod 101,
L-3 <= 63*(i+1)*max(log L+2,20)^2,
L-2 <= 63*(L-i+1)*max(log L+2,20)^2,
225*7^(L-2)*(7L-4) | F.
```

The position 417 bound uses the modulo-49 table after excluding positions
through 395: 399, 405 and 411 have disallowed residues modulo 42. Position
45 was included in both searches, not discarded by misreading `i=3 mod42`
as the single position 3. Its all-length exclusion is now justified by
the new edge proof.

[EDGE_BOUNDS.md](EDGE_BOUNDS.md) proves the two inequalities and the entire
infinite edge regions, including both branches of the maximum. When both
`i` and `L-i` are comparable with `L`, these inequalities do not contradict
the necessary valuation. The merged Evertse result still supplies only
abstract finiteness, not an effective numerical bound on this region.
No exhaustive partition of that remaining region has been obtained.
[OBSTRUCTION.md](OBSTRUCTION.md) records the additional primary-literature
checks, their hypotheses, and why their effective bounds did not supply
the missing cutoff.

The repository's conjecture is that **every odd positive integer divisible
by its decimal digit product times its digit sum contains a 1**; see the
[owning research note](../../README.md). Neither this subclass nor that
wider conjecture is settled here.

## Why the successive-lifting sieve is exhaustive in its claimed range

The merged audit proves `ord_(7^k)(10) = T_k = 6*7^(k-1)`. Consequently
10 generates every unit modulo `7^k`. Since 18 is invertible modulo 7
and `7*10^L-25` is a unit, the congruence

```text
18*10^i = 7*10^L-25 (mod 7^k)
```

has exactly one exponent class modulo `T_k`. At `k=1` it is `i=3 mod6`.
If `r` is its least nonnegative representative at level `k`, every lift
at level `k+1` is `r+t*T_k`, for exactly one `t` in `0..6`.
Writing `10^T_k = 1+c*7^k (mod 7^(k+1))`, the order theorem ensures
`c != 0 mod7`. If `y=18*10^r`, the lifted left side is

```text
y + y*c*t*7^k (mod 7^(k+1)).
```

Here `y=3 mod7`. Divide the difference between target and `y` by `7^k`
and multiply by the inverse of `3c mod7` to compute `t`. The program checks
both the previous congruence and every new congruence with exact arithmetic.
It independently checks the order using its prime divisors 2, 3 and 7.

Every future representative is at least the current representative. Thus
`r >= L` excludes **all** positions in `3 <= i < L`. Once `T_k > L-1`,
at most one actual position remains, namely `r` if `r<L`. Before that
threshold, the complete class is retained; no unjustified single-position
assumption is used. Each tested power is at most `L-2`, so every rejection
is necessary for the growing-power test.

[lift_sieve.cpp](lift_sieve.cpp) tests every odd length from 5 through the
inclusive input bound, using powers through `min(20,L-2)`. For a survivor
it enumerates the entire class in range. [verify.py](verify.py) would then
construct its digits and check both the actual growing power and the full
product-times-sum divisor. **There were no such survivors** in the recorded
run; no full-divisor test on a large weak survivor is claimed.

The main run visits 4,999,998 lengths: `5,7,...,9,999,999`. The last even
endpoint 10,000,000 is excluded by parity. Every length was rejected by
power 18 or earlier. Counts for each rejection power sum to 4,999,998 in
[lifting.json](lifting.json). This is an exact finite certificate obtained
by rerunning the small program, not a Lean theorem or a numerical global bound.

All moduli are at most `7^20 = 79,792,266,297,612,001 < 2^57`.
Modular products use unsigned 128-bit intermediates, so their products
are below `2^114`, safely below `2^128`. Exponents and periods are below
`6*7^19 < 2^57`; additions used in lifting and differences remain within
64 bits. No floating-point operation is used by either sieve.

## Independent fixed-modulus certificate

[verify_fixed.py](verify_fixed.py) imports no lifting implementation and
uses Python arbitrary-precision integers. For every `i=3,9,...<10,000,000`,
it stores `(18*10^i+25) mod 7^20` with its position. There are 1,666,667
entries. The keys are distinct: equality would imply that the difference
of the positions is a multiple of
`6*7^19 = 68,393,371,112,238,858`, exceeding the entire position range.
The program also explicitly checks for collisions.

It scans every odd `L` from 23 through 9,999,999, updating `10^L` by
multiplication by 100 modulo `7^20`. The lookup key is `7*10^L mod7^20`;
a match counts only if its position is less than `L`. There were zero
matches across 4,999,989 lengths. For these lengths `20 <= L-2`, so a
weak solution would necessarily have matched. All 18 residual pairs at
the nine odd lengths 5 through 21 are checked separately by direct decimal
construction and the **exact** power `7^(L-2)`. None survives.
[independent.json](independent.json) records the complete coverage counts,
order witnesses, and zero-survivor lists.

## Independent arithmetic cross-checks

- The primary runner reconstructs all 3,775 residual pairs at odd lengths
  5 through 301 directly from digits, computes their actual `P,S`, and
  compares every congruence class for power caps 1 through 5 against the
  lifting implementation. Lower power runs have nonempty positive controls.
- It also directly enumerates all 43,690 original `{5,7}` words at odd
  lengths 1 through 15, without the two-five reduction. None passes `P*S | n`.
- The independent runner reconstructs **all** 9,900 two-five position pairs
  at odd lengths 3 through 199, including positions not admitted by `i=3 mod6`.
  It verifies `9n=F`, the digit product and sum, and both exact divisibility
  tests. None passes either the growing-power or full test.
- Required regression: `(L,i)=(23,15)` gives `F mod49=0`, `F mod343=245`.
  A separate control `(51,45)` passes the modulo-49 test and retains `i=45`.
- Complete finite residue tables check the full-divisor filters with their
  parity and position hypotheses. Rational log intervals check the analytic
  coefficient and the cutoff inequalities; they do not formalize the
  external theorem.

## Reproduce

From the repository root, with Python 3.8+ and a C++17 compiler supporting
`unsigned __int128` (Clang or GCC):

```sh
python3 research/a398769/five-seven/certificates.py
python3 research/a398769/five-seven/log_bounds.py
python3 research/a398769/five-seven/settlement/verify.py --output /tmp/a398769-lifting.json
python3 research/a398769/five-seven/settlement/verify_fixed.py --output /tmp/a398769-independent.json
git diff --check
```

`verify.py` compiles into a temporary directory. Both JSON files include
source hashes; the primary receipt also records runtime/compiler versions.
Elapsed runtime is observational metadata, not a deterministic certificate
field. Default commands reproduce the ten-million bound. A smaller input
bound does not reproduce the all-length edge conclusion, which specifically
uses the ten-million finite exclusion.

For a positive fixed-modulus control and boundary checks:

```sh
python3 research/a398769/five-seven/settlement/verify_fixed.py --limit 23 --exponent 2 --direct-limit 23
python3 -O research/a398769/five-seven/settlement/verify.py --max-length 301
```

The first command intentionally reports a nonempty truncated-modulus list
including `(23,15)`, and does not claim exclusion. `--residues` on the C++
program emits exponent classes only and explicitly makes no exclusion claim.
Runtime checks remain enabled under Python `-O` and C++ `-DNDEBUG`.

## Proof boundary and review

The reduction, sum filters, order reasoning, sieve coverage argument and
analytic bounds are **ordinary mathematical proofs**. The two executed
programs and rational-enclosure checks are **machine-checked finite
arithmetic**, outside Lean. Independent mathematical and computational
review is recorded in [REVIEW.md](REVIEW.md).

No Lean source was changed, and no new theorem was checked by Lean in this
investigation. The three preserved `A398769.FiveSeven` results retain
exactly the scope stated in the [merged audit](../README.md). A new clean
Lean build is not claimed; the unchanged formal artifacts are not evidence
for the new analytic or computational statements.

This work is prepared on a review branch. Merging remains with the owner.
