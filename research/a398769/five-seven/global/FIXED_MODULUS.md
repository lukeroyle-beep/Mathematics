# Every fixed modulus admits central candidates

This is an ordinary elementary proof, not a Lean theorem. It verifies the
fixed-modulus statement in the supplied prompt. Its quantifiers matter: the
position and the modular quotient may depend on the modulus and the length.
It does **not** give a witness for the actual, length-dependent divisor.

For a word of length `L` with fives at positions `0,i`, and sevens elsewhere,
write

```text
n = (7*10^L - 18*10^i - 25)/9,
P = 25*7^(L-2),     S = 7L-4.
```

## Theorem

Fix an integer `M >= 1`. Let `D` be the product of the distinct odd primes
dividing `M`, with empty product 1. Put

```text
k = max(1,v_7(M)),     T = 6*7^(k-1).
```

For **every odd multiple** `L` of `D` with `L >= 3T`, there exist integers
`i,q` such that

```text
ceil(L/3) <= i <= floor(2L/3),
i = 3 (mod 6),
n = q*P*S (mod M).
```

The corresponding `n` is a positive decimal integer of exactly `L` digits
in `{5,7}`. One may choose `q` positive, but no claim is made that
`q=n/(PS)` as an ordinary rational number.

## Proof of the order used

Modulo 7, 10 has order 6. Moreover

```text
10^6-1 = 999999 = 7*142857,
142857 = 1 (mod 7).
```

For every positive integer `r`, elementary binomial expansion gives

```text
v_7((10^6)^r-1) = 1+v_7(r).
```

Indeed, raising a number `1+7^a*u`, with `7` not dividing `u`, to the
seventh power increases `a>=1` by exactly one: the first binomial term has
valuation `a+1` and all later terms have greater valuation. Raising it to
an exponent coprime to 7 leaves the valuation equal to `a`, by the same
expansion. Factoring `r` into its 7-power and coprime parts proves the
identity. Every exponent giving 1 modulo `7^k` is already divisible by 6,
so this identity proves

```text
ord_(7^k)(10) = 6*7^(k-1) = T.
```

There are exactly `T` invertible residues modulo `7^k`. Thus powers of 10
exhaust them.

## Solve for the position and check the endpoints

The residue

```text
u = (7*10^L-25)*18^(-1) (mod 7^k)
```

is invertible modulo `7^k`: 18 is invertible and the numerator is `-25`,
nonzero modulo 7. Consequently some residue class `i mod T` solves

```text
18*10^i = 7*10^L-25 (mod 7^k).
```

Modulo 7, `u=6=10^3`, so this class has `i=3 (mod 6)`.

The interval from `ceil(L/3)` through `floor(2L/3)`, inclusive, contains
at least `floor(L/3)` integers. This can be checked by writing `L=3a+r`
for `r=0,1,2`; the respective counts are `a+1,a,a+1`. Since `L>=3T`,
it contains at least `T` consecutive integers and therefore a representative
of every class modulo `T`.

Select the representative of the solved class. We have `T>=6`, hence
`L>=18`, `i>=6`, and `i<=L-2`. The digit formula therefore describes a
positive `L`-digit number with two distinct fives and suffix 775. In
particular, `25 | n` and `v_5(n)=2`. Since 9 is invertible modulo `7^k`,
the solved congruence gives `7^k | n`.

## Solve the modular quotient

First, `gcd(S,M)=1`. The number `S=7L-4` is odd. For every odd prime
`p | M`, the definition of `D` gives `p | L`, and hence

```text
S = -4 (mod p),
```

which is nonzero. Thus neither 2 nor any odd prime factor of `M` divides
`S`. It follows that

```text
gcd(PS,M) = gcd(P,M)
          = 5^min(2,v_5(M))*7^min(L-2,v_7(M)).
```

This divides `n`, using the suffix and the constructed `7^k` divisibility.
A linear congruence `PS*q=n (mod M)` is solvable exactly when
`gcd(PS,M) | n`: dividing by the gcd reduces it to inversion modulo
`M/gcd(PS,M)`. This proves the theorem, including `M=1`, where the
congruence is vacuous. Adding multiples of the reduced modulus makes a
chosen quotient positive if desired.

## Finite lists and the inherited filters

For any finite list of fixed moduli, apply the theorem to their least
common multiple. The **same** position and quotient then work for the
whole list.

The result persists after imposing the inherited necessary filters. To
see this, first enlarge the chosen modulus to

```text
M' = lcm(M, 49*5*11*13*37*101).
```

Choose arbitrarily large odd multiples of the odd radical of `M'`. These
lengths are 0 modulo each of 5, 11, 13, 37 and 101 and therefore avoid all
five excluded length residues from PR 8. The constructed pair satisfies
`49 | n` and `i=3 (mod 6)`, hence the inherited modulo-49 table. For large
enough `L`, its central position also has `i>=417` and `L-i>=396`.

The two inequalities from PR 8 do not obstruct these central pairs.
Indeed both `i` and `L-i` are at least `L/3`, and
`max(log L+2,20)^2>=400`. Each right side is consequently at least
`63*(L/3)*400=8400L`, larger than either required left side.

This corollary states compatibility with fixed congruences and necessary
filters only. It does not state `S | n`, nor `7^(L-2) | n`. The growing
prime power and the varying digit sum are precisely the information lost
when the actual divisibility problem is replaced by finitely many fixed
congruences with an existential quotient.
