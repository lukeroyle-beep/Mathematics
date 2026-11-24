# Global follow-up: still open, with exact per-length reduction

24 November 2026. Started from **merged PR #8**, commit
`7b0151105c481b227b26c6198186500ba63a2bd9`, in a separate checkout.

**Verdict: still open.** No all-length exclusion, exact witness, or global
effective cutoff was obtained. The certified exclusion of **every length
1 through 10,000,000 inclusive** is reused and independently reproduced.
No new exhaustive interval of odd lengths above 10,000,000 is certified.
The inherited all-length parity, residue and edge exclusions remain valid.
There is no numerical `B` for which a claim about `(10,000,000,B]` is made.

## New proved results

1. [Every fixed modulus admits central candidates](FIXED_MODULUS.md).
   For any fixed `M`, every sufficiently large odd multiple of its odd
   radical has a central position and modular quotient with
   `n = qPS mod M`. The proof verifies endpoints, the order of 10,
   `gcd(S,M)=1`, and linear-congruence solvability. The statement persists
   with all inherited finite filters. Thus a finite list of these fixed
   modular tests cannot finish the problem.
2. [At most two exact quotient candidates per length](TWO_QUOTIENTS.md).
   With `A=9*7^(L-2)*(7L-4)`, `H=25A`, `X=7*10^L/H`, and
   `K=10^ceil(L/2)/25`, they are `floor(X)` and `-A^(-1) mod K`.
   The position is recovered from valuations, followed by the full
   defining equality and an independent direct-digit check for a witness.
   Both numerical upper bounds printed in the attachment are false;
   the corrected exact bounds, for `L=2r+1`, are

   ```text
   X/K = 49/(9S)*(10/49)^r < 1,
   0 < X-q <= 301/(225S)*(10/49)^r < 1  when i<ceil(L/2).
   ```

   These prove the intended structural reduction, including `L=5`.
3. [A pairwise seven-adic spacing lemma](GROWING_POWER.md).
   Two solutions modulo `7^k` with the same length class modulo 6 have
   `v_7(i-i')=v_7(L-L')+1` when the relevant valuations are below `k`.
   Equal positions or equal gaps force explicit exponential separations.
   The lemma supplies no bound on the first possible solution.

These are ordinary mathematical proofs, not Lean formalizations.

## Pursuing the varying digit sum

The two-quotient test retains the full variable factor `S=7L-4` and the
factor 9. It is an exact decision procedure for any specified odd length,
but is not a finite decision of all lengths without another theorem.

The sum condition itself has central survivors satisfying every inherited
cheap filter. One exact example beyond the finite certificate is

```text
L = 121041229921,  i = 40582608819,
S = 847288609443 = 3^25,
F mod (9S) = 0,  F mod 49 = 0,  F mod 343 = 245.
```

Its length and position have residues `(1,39)` modulo `(6,42)`, obey all
five length filters, and lie in the central third. The edge inequalities
permit central pairs, as proved in the fixed-modulus note. Thus this is a
**digit-sum survivor, not a full witness**: `v_7(F)=2` rejects this pair.
The checker independently concatenates its actual four constant-digit
blocks modulo the required divisors by binary composition; it obtains
`n mod S=0` and `n mod343=294`. It does not allocate 121 billion digits.
The block method is also checked against ordinary digit construction for
all 3,775 residual pairs through length 301.

This rejected pair does **not** exclude all other positions at that huge
length and does not extend the certified interval. A smaller control
`(L,i)=(1225,417)` passes the sum condition but has only `v_7(F)=3`.

## The precise unproved step

Any remaining witness still lies in PR #8's region:

```text
L > 10000000 odd,  i >= 417,  L-i >= 396,  i=3 mod6,
(L mod6, i mod42) in {(1,39),(3,3),(5,15)},
L != 2 mod5, 10 mod11, 8 mod13, 27 mod37, 15 mod101,
L-3 <= 63*(i+1)*max(log L+2,20)^2,
L-2 <= 63*(L-i+1)*max(log L+2,20)^2,
225*7^(L-2)*(7L-4) | 7*10^L-18*10^i-25.
```

What remains unproved is **uniform failure of both quotient candidates
over this entire infinite set of lengths**, or another uniform bound or
contradiction in the central region. In particular:

- No effective bound `v_7(F) <= cL+C log L` with explicit `c<1`, `C` and
  starting length independent of position was established, even on the
  pairs passing the varying digit-sum condition.
- No argument excludes the required ordinary remainder for `floor(X)`
  at every remaining length, or excludes the small inverse residue with
  the necessary valuations and equality for the second candidate.
- The inherited Evertse theorem proves finiteness without an effective
  maximum. A fresh quantitative Subspace Theorem source check likewise
  does not supply effective endpoints for all exceptional heights.

A conditional recipe for a cutoff **if** the missing uniform valuation
estimate were proved appears in the growing-power note. Its constants
have not been established for this problem, so it is not a cutoff.

## Reproduce and review

From the repository root with Python 3.8+ and a C++17 compiler:

```sh
python3 research/a398769/five-seven/certificates.py
python3 research/a398769/five-seven/log_bounds.py
python3 research/a398769/five-seven/settlement/verify.py --output /tmp/a398769-pr8-lifting.json
python3 research/a398769/five-seven/settlement/verify_fixed.py --output /tmp/a398769-pr8-independent.json
python3 research/a398769/five-seven/global/checks.py --output /tmp/a398769-global-checks.json
python3 -O research/a398769/five-seven/global/checks.py --output /tmp/a398769-global-optimized.json
python3 research/a398769/five-seven/global/check_spacing.py > /tmp/a398769-spacing.json
python3 -O research/a398769/five-seven/global/check_spacing.py > /tmp/a398769-spacing-optimized.json
python3 -O research/a398769/five-seven/global/independent_checks.py > /tmp/a398769-independent-global.json
git diff --check
```

For a specified length, for example:

```sh
python3 research/a398769/five-seven/global/checks.py --length 313
```

That command checks exactly one length; it does not certify an interval.
It computes large exact integers, and is not asserted to be practical for
arbitrarily large inputs. No large two-quotient sweep was executed.

[checks.json](checks.json) records 3,775 directly constructed residual
pairs at all 149 odd lengths 5 through 301, 386 fixed-modulus controls,
both corrected bounds, the required `(23,15)` regression, the sum-only
controls and two synthetic positive controls. The synthetic `A` values
are explicitly not original-problem witnesses; one exercises a high
position with `q_2 != floor(X)`. This avoids validating the candidate
recovery only on rejection paths.
[spacing.json](spacing.json) records positive and negative fixed-power
controls for the spacing lemma.
[independent.json](independent.json) records a separate implementation,
importing none of the primary search code: 3,020 directly constructed pairs
at 119 lengths passing the 5-filter, 18,120 digit-block comparisons, three
synthetic positive controls, and the huge sum-only pair from digit blocks.

[PR8 audit receipt](pr8-audit.json) records the unchanged source hashes
and reproduction of both ten-million certificates. The deterministic
fields match the merged receipts; elapsed time is observational metadata.
[Independent review](REVIEW.md) records proof and implementation checks.

No Lean source changed and no fresh Lean build was run. The prior Lean
theorems keep their prior scope. This is a review branch; merging remains
with the repository owner.
