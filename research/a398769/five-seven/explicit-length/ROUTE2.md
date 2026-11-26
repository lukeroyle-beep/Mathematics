# Full-witness route: exact obstruction and an effective moving-centre subfamily

26 November 2026. This note starts from `main` at
`aab83fc4ed706cd4aca4d51dc6e533d60cb87477`. The decimal-height argument was
read at PR #23's reviewed commit
`c977422826ce674d4068c0517afb1f75fc368893`; it is not present on this base.
There is no unconditional global upper bound for all witnesses established
here. The subfamily bound at the end is unconditional **on membership of
its explicitly defined subfamily**, not on an unproved analytic estimate.

## Exact premise at the same position

For odd `L>=5`, `3<=i<L`, set

```text
S=7L-4, F=7*10^L-18*10^i-25,
n=7*(1+10+...+10^(L-1))-2-2*10^i=F/9,
P=25*7^(L-2), t=v7(F).
```

Thus the original predicate is exactly
`PS|n` if and only if `225S*7^(L-2)|F`. Since `F=-25 mod125`, its
five-adic valuation is two. A witness has `5` not dividing S. Also
`S=3 mod7`. On the eligible domain `5` not dividing S and `9S|F`, the
integer `H=F/(225S)` exists and satisfies `v7(H)=t`, because
`gcd(25,9S)=1` and `7` does not divide `225S`. This proof combines
the coprime factors 25 and **9S**; it never cancels nine modulo S.
Consequently, including when S is composite or divisible by three,

```text
PS|n  iff  t>=L-2.
```

These hypotheses must refer to the same actual position i. A sum pass
at one position and a high seven-adic valuation at another do not help.

## Lift deadline, with all endpoints retained

Let `T_k=6*7^(k-1)` and `K=min{k>=1:T_k>L}`. Order six modulo seven
and `v7(10^6-1)=1` prove `ord_(7^k)(10)=T_k`. Thus ten generates every
unit modulo `7^k`; the unit `(7*10^L-25)/18` determines exactly one
`r_k` in `[0,T_k)`. At depth K, any actual position with `t>=K`
must be `i=r_K`, since `i<L<T_K`. In particular every witness is
covered: `T_(L-2)>L` for `L>=5`, so `K<=L-2`.

The lifts have the exact form

```text
r_(j+1)=r_j+a_j*T_j, 0<=a_j<=6,
a_j=5*(F(L,r_j)/7^j) mod7.
```

Indeed `10^T_j=1+7^j*c_j` with `c_j=1 mod7`, while
`r_j=3 mod6` and `18*10^r_j=3 mod7`. The coefficient inverse is five.
Once `j>=K`, a nonzero digit takes the representative beyond L and
later lifts never decrease it. If the first nonzero digit is `a_t`,
then all earlier representatives equal i and the valuation of the
actual positive integer F is exactly t. Positivity proves that this
digit eventually exists, without bounding its index.

Therefore a sum-compatible actual `r_K` is a witness exactly when

```text
a_K=a_(K+1)=...=a_(L-3)=0.
```

To exclude it one must prove a nonzero digit at an index in the
**inclusive** interval `[K,L-3]`. A first nonzero digit at `L-2`
still gives a witness. The first unproved global implication in this
route is that exact sum compatibility forces such an index.

## What the sum contributes, and what it does not

During the constant-representative portion, `225S=3 mod7` gives

```text
a_j=H/7^j mod7, K<=j<=t.
```

Extracting the exact sum divisor therefore preserves the trailing
seven-adic zeros. It does not give a shorter run of zeros. The strongest
positive-size estimate is `7^t<=H`; replacing seven by ten requires an
additional theorem for this particular cofactor. The abstract integers
`H=7^m` illustrate the logical deficiency of that replacement, but are
not claimed to come from actual pairs.

There is also a precise obstruction to a later CRT incompatibility.
Put `o=ord_S(10)`, which exists because S is odd and five-free, and
`e=v7(o)`. For any two sum-compatible positions, subtracting the
original n values gives `S|2*(10^i-10^s)`. Only two is inverted.
Thus all such positions form one class `s mod o` when any exist.

If `e>=1`, a prime p dividing S has `7^e|p-1`. Write
`p=1+c*7^e`; c is positive even. The value c=2 would make p a
multiple of three larger than three, so `p>=4*7^e+1`. As `p=1 mod7`,
the positive odd integer `S/p` is `3 mod7`, hence is at least three.
It follows that

```text
L>=12*7^(e-1)+1=2T_e+1, and hence e<=K-1.
```

For every `j>=K`, therefore,

```text
gcd(o,T_j)=gcd(o,6)*7^e
```

is constant. A sum-compatible `r_K` implies compatibility of the
**unbounded exponent** congruences at every later depth. This rules
out a later incompatibility proof based solely on this gcd. It does
not rule out a future bound for their least common representative
in `[3,L)`, which is the remaining issue. No primality assumption on
S has entered this argument.

Assuming a witness from the start gives

```text
F=225S*7^(L-2)*q, q a positive integer.
```

The integer q can have unrestricted prime factors. The exact magnitude
bounds `5*10^L<F<7*10^L` give

```text
(245/(225S))*(10/7)^L < q < (343/(225S))*(10/7)^L.
```

The cofactor can therefore have logarithmic height proportional to L;
it has not become a fixed algebraic base or an S-unit for a fixed set
of primes. An explicit theorem requiring either hypothesis cannot be
applied merely because the factor `225S` was separated.

## PR #23's decimal-height assertion is not a weaker known input

For integral H let d be its number of decimal digits. Exact integer
comparisons give

```text
10^t<=10^12 H  iff  t<=d+11;
its failure              iff  t>=d+12.
```

If this assertion held at every witness, then `F<7*10^L` would give
`1575L<700000000000900`. The largest allowable integer is
`444444444445`: the products at this integer and its successor are
respectively `700000000000875` and `700000000002450`. This is only
a conditional cutoff.

For `B=1000002000000` and `B<L<=M=3301587301587`, put
`D=225S=1575L-900`. The upper bound gives `H<10^(L-14)` because
`D>7*10^14`. At M, `52*10^14-D=1375`; at M+1 it is `-200`.
Throughout the band the lower bound
`F>=52*10^(L-1)-25` gives `H>=10^(L-15)` (in fact strictly greater).
Thus `d=L-14` there. Failure is exactly `t>=L-2`, hence exactly the
original witness condition on the eligible domain. Proving that
inequality throughout this band would already resolve its witnesses;
it is not an independent established exclusion for the band.

At all larger L the missing digit deadline for that stronger assertion
is `[K,d+11]`, which may end before `L-3`. Neither that deadline nor
the witness deadline follows from the lift identities alone.

The fixed-depth theorem in [`fixed-depth/PROOF.md`](../fixed-depth/PROOF.md)
gives infinitely many sum-compatible pairs of **each fixed positive
valuation** in every open ratio interval. Its quantifier fixes t before
L tends to infinity. It forbids promoting the finite archive's absence
of sum passes at depths at least 22 to a constant global ceiling of 21.
It also cannot be specialized by setting its fixed depth equal to `L-2`.

## A computable upper bound for a family with growing denominators

Here is an additional effective consequence of the independently
established polynomial-root estimates in
[`uniform-bound/ANALYTIC.md`](../uniform-bound/ANALYTIC.md), sections 1--3.
It uses the published Bugeaud--Laurent Corollary 1, printed p.4, through
those fully parameterized estimates; no new theorem for unrestricted
three-term sums is asserted.

Define the subfamily by requiring the existence of coprime integers
`0<a<b` such that, at the actual length and position,

```text
b<=K(L)^2,  |bi-aL|<=K(L)^2.                         (A)
```

Every full witness in this subfamily has the explicit integer bound

```text
L<=U_square=1721427606158403.                         (B)
```

This is a bound for (A), not a global bound. The denominators in (A)
are permitted to grow with L; no single centre or constant offset is
silently fixed.

To prove it, suppose `K>=20`. Then `L>=T_(K-1)=6*7^(K-2)` and
`K^2<=L`, so every selected b is permitted in the polynomial-root
parameterization. For a possible witness with `L>10000000`, its
derivative valuation is at most

```text
B_K=1+252*(K+1)^3.
```

Strong Hensel applies since `t>=L-2>2B_K`. The selected root is
multiplicatively independent of ten: the dependent branch of that
same proof already gives `t<L-2`. If D is its actual global degree
and H a valid normalized height, the proof gives `D<=b` and permits

```text
H=K^2/b+b+1.
```

This follows from `H_actual<=|bi-aL|/b+b+1`; increasing the height
parameter is allowed. Every entry in the logarithm estimate's maximum
is at most `2K+2`: the first is below `log L+1<2K+1`, the second is
below twenty, and the third equals ten. Consequently

```text
t<=B_K+252*b^3*H*(K+1)^2
 <=R(K):=1+252*(K+1)^2*((K+1)+K^8+2K^6),            (C)
```

because `b^3 H=K^2 b^2+b^4+b^3<=K^8+2K^6`.

All boundary arithmetic is integral:

```text
R(20)=2859204098333773,
6*7^18=9770481587462694,
R(20)+1 < 6*7^18.
```

The inequality persists. The polynomial `R(k)+1` has nonnegative
coefficients and degree ten. For `k>=20`, its increase is bounded
above by `(6/5)^10<7`, since `(k+1)/k<6/5` and
`6^10=60466176<68359375=7*5^10`. The comparison `6*7^(k-2)` grows
by exactly seven. Thus for every `K>=20`,

```text
t<=R(K)<6*7^(K-2)-1<=L-2
```

using odd L for the last inequality: `L>=6*7^(K-2)+1`.
This contradicts a witness. Hence a witness in (A) has `K<=19`.
For `K<=18`, `L<T_18=6*7^17=1395783083923242<U_square`. At `K=19`,
the same valid estimate (C) gives

```text
L-2<=t<=R(19)=1721427606158401,
L<=R(19)+2=1721427606158403=U_square.
```

This proves (B), including its allowed odd endpoint. For `K=19`,
the preconditions `L>10000000`, `b<=K^2<=L`, and `t>2d` hold
just as above; twenty was needed for the final exponential comparison,
not for (C).

Combining (B) with the inherited certificates through B leaves only
odd lengths in `(1000002000000,1721427606158403]` to examine for
subfamily (A), subject to all earlier restrictions. This note does not
exhaust that interval, nor claim additional consecutive coverage.
Failure of (A) remains an unbounded class. The proof uses only a
necessary valuation condition, so it covers both prime and composite
S and does not discard the digit-sum condition from any equivalence.

Reproduce the endpoint and persistence constants with ordinary Python:

```sh
python3 - <<'PY'
R = lambda k: 1+252*(k+1)**2*((k+1)+k**8+2*k**6)
if not R(20)+1 < 6*7**18:
    raise ArithmeticError('initial comparison')
if not 6**10 < 7*5**10:
    raise ArithmeticError('growth comparison')
if not 6*7**17 < R(19)+2:
    raise ArithmeticError('preceding band endpoint')
print(R(19)+2, R(20), 6*7**18)
PY
```

The global first unproved implication remains the universal escape of
the actual sum-compatible representative by `L-3`. Effective moving-
centre estimates prove that implication on their stated subfamilies;
no coverage theorem places every possible witness in those subfamilies.
