# A simultaneous period-42 digit-sum sieve

The submitted table and factorization are correct. The resulting restrictions
exclude every position at each rejected length, but they do not give a maximum
length. This is an ordinary elementary proof with exact finite arithmetic;
no new Lean theorem or exhaustive length interval is claimed.

## Residue table and complete factorization

On the residual domain, divisibility by 49 requires

| `L mod 6` | `i mod 42` |
|---:|---:|
| 1 | 39 |
| 3 | 3 |
| 5 | 15 |

For `Q=10^42-1`, the residue of a positive power of 10 depends only on
its exponent modulo 42. Put `h=L mod 42` in `{1,3,...,41}` and take `r`
from the preceding table. Then

```text
gcd(F(L,i),Q) = gcd(7*10^h-18*10^r-25,Q) = G_h.
```

All 21 exact gcd evaluations give

| Condition on the odd residue `h` | `G_h` |
|---|---:|
| `h=1 mod 6` | `1323 = 27*49` |
| `h=23` | `18963 = 9*49*43` |
| Every other odd `h` | `441 = 9*49` |

Exact division and multiplication establish

```text
B = Q/(27*49*43)
  = 17578090667791664469405333192708607991
  = 11*13*37*127*239*1933*2689*4649*459691*909091*10838689.
```

Every listed factor is prime: the independent checker divides it by every
integer from 2 through its integer square root. This is a deterministic
primality proof for these particular small integers. Each `G_h` is coprime
to `B`. Since `B` divides `Q`, it follows that `gcd(F,B)=1` for every
pair satisfying the modulo-49 table. A full witness also has `9S | F`,
so it must have `gcd(S,B)=1`.

The primes 11, 13, and 37 already appeared among the five inherited
filters (the other two were 5 and 101). The eight additional primes and
their equivalent forbidden length residues are therefore

| Prime `p` forbidden in `S` | Forbidden `L mod p` |
|---:|---:|
| 127 | 55 |
| 239 | 103 |
| 1933 | 829 |
| 2689 | 1153 |
| 4649 | 1993 |
| 459691 | 197011 |
| 909091 | 389611 |
| 10838689 | 4645153 |

The second column is `4*7^(-1) mod p`, because `S=7L-4`.

The prime 43 is not uniformly forbidden: the gcd table has a genuine
exception at `h=23`. If `43 | S` for a full witness, then necessarily
`L=23 mod 42`. Also `43 | S` is equivalent to `L=19 mod 43`; combining
them gives the sharper equivalent necessary class `L=191 mod 1806`.
Neither this class nor the gcd table proves existence of a full witness.

## Effect on the earlier rounded family

For the family in PR #11, `S=3+112222110*q`. The coefficient is invertible
modulo 127, and the unique class making this sum zero is

```text
q = -3*(112222110)^(-1) = 68 (mod 127).
```

Thus every position is excluded at those rounded-family lengths. This is
a restriction on indices in that family, not a bound on its remaining
indices and not a complete exclusion of its lengths.

The first rounded pair `(L,i)=(16031731,6640575)` gives

```text
F mod 49 = 0,
F mod 343 = 147,
F mod (9S) = 123356871.
```

It has `v_7(F)=2` and fails the full digit-sum condition. It remains a
negative control and must not be used as a sum-divisible example.

## Why the rejected primes do not finish the argument

Let `M=5*101*B`. For every positive integer `j`, the length
`L=1+42*43*M*j` is odd, is `1 mod 42`, and has `S=3 mod p` for every
prime factor `p` of `43*M`. All those primes differ from 3, so these
lengths avoid the thirteen forbidden prime divisors (five inherited and
eight new), and also avoid the conditional 43 restriction.

For sufficiently large members, the open interval `(41L/100,42L/100)`
contains positions `i=39 mod 42`. Such positions satisfy the modulo-49
table, and the entire ratio interval avoids the seven proportional strips;
the fixed midpoint strip is also avoided for sufficiently large `L`.
This construction is only a demonstration that the listed rejections leave
arbitrarily large admissible lengths and positions. It does not assert
`9S | F`, a higher seven-power congruence, or full divisibility there.
Any argument using these rejected factors to settle the problem still
needs a proof that a forbidden prime divides the actual varying `S` of
every putative full witness. The current list supplies no such proof.

## Reproduction and independent decimal controls

Run from the repository root:

```sh
python3 research/a398769/five-seven/depth/independent_checks.py
python3 -O research/a398769/five-seven/depth/independent_checks.py
```

The checker independently reconstructs each control's decimal number as
four constant-digit blocks, using binary concatenation of repunits modulo
the chosen divisor. That path uses neither the formula for `F` nor division
by 9. It compares `9*n` with direct modular exponentiation for the rounded
negative control, the supplied enormous length parameter in [FAMILY.md](FAMILY.md),
and the inherited `(23,15)` regression. The enormous decimal word is never
allocated. Small direct decimal strings cross-check the block routine.
For the supplied large control it confirms `F mod (9S)=0`,
`F mod 16807=9604=4*2401`, and `225*2401*S | F`.
These are targeted validations, not a new exhaustive search certificate.
