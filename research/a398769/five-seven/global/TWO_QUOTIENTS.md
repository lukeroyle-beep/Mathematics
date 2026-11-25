# An exact two-quotient decision at each length

This is an ordinary elementary proof, not a Lean theorem. It verifies the
structural reduction in the supplied prompt, with corrections to its two
numerical bounds. It reduces every individual length to at most two
exact integer candidates; it does not bound the number of lengths.

## Domain and identities

Work on the inherited residual domain

```text
L >= 5 odd,   3 <= i < L,   i = 3 (mod 6),
g = L-i >= 2,  S = 7L-4,   5 does not divide S.
```

In particular `S>=31`. For any full witness define

```text
A = 9*7^(L-2)*S,   H = 25*A,
X = 7*10^L/H,      q = n/(P*S).
```

Here `q` is a positive integer. The full equation `H*q=F` gives exactly

```text
X-q = (18*10^i+25)/H > 0,                    (1)
A*q+1 = (10^i/25)*(7*10^(L-i)-18).           (2)
```

The factor 9 is included in `A`. These identities therefore encode the
full digit-sum divisibility, not its weakened test `S | F`.

Put `L=2r+1`, so `r>=2`, and define

```text
m = r+1 = ceil(L/2),   K = 10^m/25.
```

The integer `K=2^m*5^(m-2)` is positive. Since `L` and `S` are odd and
`5` does not divide `S`, the integer `A` is coprime to 10, and thus
`gcd(A,K)=1`.

## Correct numerical bounds

A direct cancellation, without real logarithms or approximate arithmetic,
gives

```text
X/K = 49/(9*S) * (10/49)^r < 1.             (3)
```

Indeed `S>=31`, so even the first factor is less than 1, and `r>=2`.
Thus every witness satisfies `0<q<X<K`.

When `i<m`, we have `i<=r`. Since `10^r>=1`,

```text
18*10^i+25 <= 43*10^r,
0 < X-q <= 301/(225*S) * (10/49)^r < 1.     (4)
```

Again each assertion is an exact rational inequality, with
`301<225*31` and `0<10/49<1`.

The attached prompt literally states instead

```text
X/K <= 343/(9*S)^L,
X-q <= (43*49)/(225*S)^L.
```

Those displayed upper bounds are false. For example, at `L=9`, `S=59`,
the first bound fails by direct rational comparison. At `(L,i)=(9,3)`,
the proposed upper bound on the positive correction `(18*10^i+25)/H`
also fails. This is a comparison of that correction expression; this pair
is not asserted to be a witness. The errors persist at arbitrarily large
lengths. In fact, throughout the stated domain `9S>49` and `225S>49`, so

```text
(X/K) / (343/(9*S)^L)
  = 10^(L-m)*(9*S)^(L-1)/7^L > 7^(L-2) > 1,

((18*10^i+25)/H) / ((43*49)/(225*S)^L)
  = (18*10^i+25)*(225*S)^(L-1)/(2107*7^(L-2))
  > 25*7^L/2107 > 1.
```

Equations (3) and (4) provide valid bounds
and preserve the intended two-candidate conclusion. They also work at
`L=5`, where `S=31`, without the prompt's stronger `S>=45` assumption.

## The two candidates

If `i<m`, inequality (4) and integrality force the unique possibility

```text
q_1 = floor(X) = (7*10^L) // H.
```

If `i>=m`, the integer `10^i/25` is a multiple of `K`. Equation (2)
therefore implies `A*q+1=0 (mod K)`. Since `0<q<K` and `A` is invertible
modulo `K`, there is at most one possibility:

```text
q_2 = the least nonnegative residue of -A^(-1) modulo K.
```

The inverse exists by the coprimality proof. In this domain `K>1`, so
`q_2` is actually positive. It still has to satisfy `q_2<X`; merely
computing the inverse does not certify a candidate.

Both candidates are functions of `L` alone. Computing them does not
require enumerating the positions.

## Recover and verify the position

For each positive candidate `q`, put `B=A*q+1`. In equation (2) the factor

```text
D_g = 7*10^g-18
```

has `v_5(D_g)=0` and `v_2(D_g)=1`: modulo 5 it is 2, and modulo 4 it
is 2 because `g>=2`. Hence every witness necessarily has

```text
v_5(B)=i-2,     v_2(B)=i+1.
```

An exact algorithm is consequently:

1. Compute `q_1,q_2` by integer division and modular inversion. Discard
   nonpositive candidates and those not satisfying `H*q<7*10^L`.
2. For each remaining candidate, compute `i=v_5(A*q+1)+2`.
3. Check `v_2(A*q+1)=i+1`, the residual position and gap restrictions,
   the appropriate split `i<m` or `i>=m`, and any inherited filters.
4. Check the **full equality**
   `H*q = 7*10^L-18*10^i-25`.
5. For a reported witness, independently construct the decimal digits,
   recompute their product and sum, and verify the exact integer quotient
   and zero remainder.

Steps 1--4 are equivalent to existence of a full witness at this length
on the residual domain. Necessity follows above. Conversely, an accepted
position gives the actual two-five decimal word `n=F/9`, with digit
product `P=25*7^(L-2)` and sum `S`; the equality says `n=P*S*q`.
The independent last step protects the reported certificate from an
implementation error. Valuation or congruence checks alone are not a
replacement for the equality.

The implementation in [checks.py](checks.py) uses the weaker original
residual position restrictions so it can be compared with small direct
enumerations. It omits the split and additional filters as redundant once
the full equality is checked: an equality with either computed quotient
is already sufficient, regardless of which split supplied that quotient.
The `5 | S` exclusion is applied before taking the modular inverse.
Witness output gives the digit rule, length, position and a SHA-256 of the
positive quotient's minimal unsigned big-endian bytes; these permit exact
reconstruction without printing a potentially enormous quotient.

## What is still unproved

There are infinitely many odd lengths to which this decision procedure
can be applied. No uniform obstruction for `q_1` or `q_2` is proved here.
For the first candidate one would need to exclude the requisite exact
remainder `7*10^L-H*floor(X)=18*10^i+25` at every remaining length, or
derive a global effective cutoff. For the second, one must exclude the
small inverse residue with its required valuations and full equality.
A positive inverse residue can be much smaller than its modulus; the
bound `q<X<K` alone is no contradiction.

The variable factor `S=7L-4` is retained in both candidates. Thus this is
an exact way to pursue the varying digit sum, but the fact that only two
candidates remain at each length does not exclude infinitely many lengths.
