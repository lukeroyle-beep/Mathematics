# Independent investigation of the all-length {5,7} subclass

24 November 2026. This is a separate mathematical investigation, not a change
to the Stage 5 pull request. No all-length exclusion of the two-five case was
obtained. The reductions below were checked independently.

Let `n > 0` have only decimal digits 5 and 7. Write `L` for its length, `a`
for the number of fives, and `P,S` for its actual digit product and sum.
Assume `P*S | n`. All decimal positions below are counted from zero at the
units digit.

## All-length reductions

1. **L is odd.** The number and digit product are odd. Consequently `S` must
   be odd. Since all digits are odd, the parity of `S` equals the parity of L.

2. **There are at most two fives.** Three fives would force `125 | P | n`.
   An odd multiple of 125 has a three-place suffix in `{125,375,625,875}`;
   none uses only 5 and 7. A number with three fives necessarily has at least
   three places, so there is no short-length exception.

3. **The no-five case is impossible.** Put `R_L = (10^L-1)/9`. Then
   `n = 7*R_L`, and both `P` and `S` are divisible by 7, forcing `49 | n`.
   But 10 has order 6 modulo 7. Odd L is not a multiple of 6, so `7` does
   not divide `R_L`. Thus 49 does not divide n, a contradiction. This also
   handles L = 1.

4. **The one-five case is impossible.** Divisibility by 5 forces the unique
   five to be the units digit. If L = 1, n = 5 and P*S = 25, which fails.
   Otherwise some digit is 7, so `7 | P | n`. On the other hand,
   `n = 7*R_L - 2`, giving `n = -2 (mod 7)`, a contradiction.

Every remaining candidate therefore has **exactly two fives**. Divisibility
by 25 forces its last two digits to be 75. If the second five is at position
i, then initially `2 <= i < L`, and

```text
n = 7*R_L - 2*(10^i + 1)
  = (7*10^L - 18*10^i - 25)/9,
P = 25*7^(L-2),
S = 7*L - 4.
```

Reducing modulo 7 gives `10^i = -1 (mod 7)`. The order of 10 modulo 7 is
6, so **i = 3 (mod 6)**. In particular i is odd and at least 3, while L
is odd and at least 5. This verifies the proposed two-parameter reduction.

## Additional necessary restrictions

Since L is at least 5, the hypothesis forces `49 | n`. Write `i = 6b+3`.
Modulo 49,

```text
10^6 = 1+7,
10^i = 20+42b,
7*10^L - 18*10^i - 25 = 7*10^L - 42 - 21b.
```

Reducing the last expression after division by 7 yields the following exact
necessary classes:

| L modulo 6 | i modulo 42 |
|---:|---:|
| 1 | 39 |
| 3 | 3 |
| 5 | 15 |

In particular, **7 does not divide i**. This also follows by applying the
lifting-the-exponent argument to `10^i+1`: for `i = 3 (mod 6)`, its 7-adic
valuation is `1 + v_7(i)`, whereas `R_L` is a 7-adic unit for odd L.

There are several further restrictions from the digit sum:

- Because i is at least 3, the last three digits of n are 775. Hence
  `v_5(n)=2`, so the two fives in P already consume all its factors of 5.
  Therefore `5` does not divide S, equivalently **L is not 2 modulo 5**.
- For odd L and odd i, `R_L = 1 (mod 11)` and `10^i = -1 (mod 11)`.
  Consequently `n = 7 (mod 11)`. Thus `11` does not divide S, giving
  **L is not 10 modulo 11**.
- The order of 10 modulo 13 is 6. Thus `10^i = -1 (mod 13)` and
  `n = 7*R_L (mod 13)`. Since odd L is not divisible by 6, this is nonzero.
  Therefore `13` does not divide S, giving **L is not 8 modulo 13**.

These restrictions are necessary, not sufficient, and do not cover every
remaining L and i.

## Why a fixed power of 7 cannot finish the proof

There is a precise limitation to seeking a contradiction with one fixed
7-power modulus. Fix the second five at **i = 3**. The numerator becomes

```text
7*10^L - 18*10^3 - 25 = 7*(10^L - 2575).
```

For any fixed integer k at least 2, divisibility by `7^k` is equivalent to

```text
10^L = 2575 (mod 7^(k-1)).
```

10 is a primitive root modulo every positive power of 7: its order modulo
7 is 6, and `v_7(10^6-1)=1`, so its order modulo `7^r` is
`6*7^(r-1)`. Therefore the congruence has an exponent class for every k.
Because `2575 = 6 = 10^3 (mod 7)`, that class always satisfies `L = 3
(mod 6)`, hence is odd. Taking a sufficiently large representative gives
`L > i`, so there are infinitely many valid two-five digit strings passing
each fixed-power test.

Independently computed initial exponent classes illustrate this obstruction:

| Required divisor | L class with i = 3 | First admissible L |
|---|---|---:|
| 7^2 | 3 mod 6 | 9 |
| 7^3 | 39 mod 42 | 39 |
| 7^4 | 81 mod 294 | 81 |
| 7^5 | 1551 mod 2058 | 1551 |
| 7^6 | 1551 mod 14406 | 1551 |
| 7^7 | 30363 mod 100842 | 30363 |
| 7^8 | 30363 mod 705894 | 30363 |
| 7^9 | 2853939 mod 4941258 | 2853939 |

Each row was checked by exact modular exponentiation and lifting the preceding
exponent class through its seven possible next residues. These are **not
counterexamples**: they pass only the stated fixed-power test, much weaker
than the required `7^(L-2)`, and the digit-sum condition was not asserted.
This rules out an obstruction using just one fixed power of 7; it does not
rule out a stronger argument combining additional conditions.

## Exact remaining obstacle

The unresolved class consists of odd L at least 5 and `3 <= i < L`,
`i = 3 (mod 6)`, satisfying the restrictions above. It remains to prove that
no such pair can simultaneously satisfy

```text
7^(L-2) | 7*10^L - 18*10^i - 25
and
(7*L-4) | (7*10^L - 18*10^i - 25)/9.
```

The factor 25 is automatic from the suffix 775, and the necessary exclusion
of `5 | S` makes these conditions, together with it, equivalent to the full
product-times-sum divisibility. An all-length argument must control the
7-adic valuation relative to the varying length, exploit the varying digit
sum, or supply another global restriction. The finite residue checks above
do not supply that argument.

A limited literature lookup located the general Zuckerman-number setting
([OEIS A007602](https://oeis.org/A007602)) and He and Sanna's
[counting and enumeration paper](https://arxiv.org/abs/2403.14812). It did not
establish a prior theorem resolving this exact alphabet. No novelty or
completeness-of-literature claim is made; the reductions here are independently
derived elementary arguments.
