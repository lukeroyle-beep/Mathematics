# Rational centres: two new strips and a quantitative coverage obstruction

This note uses the independently audited Bugeaud--Laurent parameterization
in `AUDIT.md`. It proves additional exclusions with offsets growing
linearly in the length. It does not prove that the full decimal `{5,7}`
subclass is empty. The final section identifies an explicit failure of a
specified uniform degree-and-height estimate, not an impossibility theorem
for every refinement of the method.

Put `N=10,000,000` and `x=i/L`. The five submitted, verified exclusions
leave exactly these open ratio regions before the other discrete filters
are imposed:

```text
(1/25000,       299999/900000)
(300001/900000, 59999/120000)
(60001/120000,  599999/900000)
(600001/900000, 24999/25000).
```

Every displayed endpoint is excluded. In particular the radius of the
one-third strip is `1/900000`, not `1/300000`; the midpoint radius is
`1/120000`. These describe what the inequalities leave open, not ratios
known to occur in witnesses.

## A positive-width exclusion near 2/5, also valid near 3/5

For each `a` in `{2,3}`, no witness can have

```text
|5i-aL| <= L/2,000,000.                              (1)
```

Equivalently the two closed ratio strips have radius `1/10,000,000`
about `2/5` and `3/5`. These exclusions hold at every length: the proof
below treats every `L>=N`, and the inherited exact certificate and
elementary reductions treat all smaller lengths. There is no unchecked
finite interval between the analytic and computational parts.

Write

```text
L=5k+r, 0<=r<=4,       i=ak+s,
delta=5i-aL=5s-ar,     X=10^k.
```

Here `s` is allowed to be negative and to grow with `L`; it is not a
fixed-offset argument. Let `m=min(0,r,s)=min(0,s)` and use the integral
polynomial

```text
P(X)=7*10^(r-m)*X^5 - 18*10^(s-m)*X^a - 25*10^(-m).
P(10^k)=10^(-m)*F(L,i).
```

Multiplication by this power of 10 leaves the 7-adic valuation unchanged.
Set `w=max(0,r,s)-min(0,r,s)`. Since
`s=delta/5+ar/5` and `0<=a<=5`, considering `s<0`, `0<=s<=r`, and `s>r`
gives

```text
w <= |delta|/5 + 4.
```

The sum of the absolute coefficients of `P` is at most `50*10^w`.
The Mahler measure of `P` is at most that sum. The primitive minimal
polynomial of any root divides `P` over the integers, and the other
integral factor has Mahler measure at least one. Thus every root `alpha`
of global degree `D` satisfies

```text
D*h(alpha) <= log(50*10^w) < (w+2)*log 10
           <= (|delta|/5+6)*log 10.                 (2)
```

Suppose `t=v_7(F)>0`. Modulo 7 the leading term vanishes, the remaining
coefficient and constant are nonzero, and

```text
P'(10^k) = -18*a*10^(s-m)*(10^k)^(a-1) != 0 (mod 7).
```

This uses `a=2` or `a=3`. Hensel's lemma gives a unit root `alpha` in
`Q_7`, congruent to `10^k` modulo 7, of global degree `1<=D<=5`. The
difference quotient of `P` at these two congruent arguments is a unit,
so `t=v_7(10^k-alpha)`. Also `F>0` when `L>i>=3`, hence `10^k!=alpha`.
If `t=0`, exclusion is already immediate.

Under (1), choose the enlarged height

```text
H=7L/10,000,000.
```

For every `L>=N`,

```text
|delta|/5+6 <= L/10,000,000+6 <= H.
```

In particular `H>=7`, so all logarithmic height conditions hold. If the
bases `10,alpha` are multiplicatively independent, use

```text
log A1=log 10, log A2=H*log 10/D,
b'=(k/H+1/D)/log 10,
k/H <= 2,000,000/7.
```

The retained denominator gives

```text
b' <= (2,000,000/7+1)/log 10 < 125,000,
log b' + log log 7 + 0.4 < 13.
```

For example, the last two comparisons follow from `log 10>2.30`,
`log log 7+0.4<1.1`, and the rational Taylor-series certificate
`exp(11.9)>125,000`. For `D>=2` the full maximum in the corollary is
at most 13; for `D=1` it is at most 20. Therefore

```text
t <= max(63*5^3*13^2, 63*20^2)*H
   = 1,330,875*H
   = (74529/80000)*L < L-2,                         (3)
```

where the strict margin at `L=N` is exactly `683873`, and the margin
increases linearly thereafter.

For completeness, multiplicative dependence also excludes the pair.
Write `alpha^v=10^u`, with `v>0` and integer `u`. Taking the global norm
and then its 2-adic valuation shows `j=D*u/v` is an integer. Heights give
`|j|<H`. The element `alpha^D/10^j` is a root of unity in `Q_7`, hence
its order divides six. Since `10^k/alpha` belongs to `1+7 Z_7`, the case
`Dk=j` would force `10^k=alpha`, a contradiction. Otherwise, because
`D<=5` and `v_7(10^6-1)=1`, lifting the exponent gives

```text
t = 1+v_7(Dk-j).
```

This identity also allows a negative `Dk-j`, by inversion. Now
`0<|Dk-j|<L+H<2L<7^(L-3)` for `L>=N` (the last inequality already holds
at `L=5` and persists). Hence `t<L-2` in this branch as well. This handles
reducible quintics, rational roots, and both signs of `s` and `delta`.

## Exact remaining intervals after all seven exclusions

Adding (1) leaves these six open ratio intervals:

```text
(1/25000,        299999/900000)
(300001/900000,  3999999/10000000)
(4000001/10000000, 59999/120000)
(60001/120000,   5999999/10000000)
(6000001/10000000, 599999/900000)
(600001/900000,  24999/25000).
```

These are the exact complements of the seven named proportional strips.
The additional fixed midpoint exclusion `abs(L-2i)<=179` from `AUDIT.md`
replaces the midpoint radius, at a specified length, by
`max(1/120000,179/(2L))`. Equivalently, replace the two midpoint endpoints
above by `1/2` minus and plus that radius. The fixed exclusion is stronger
only when `L<10,740,000`. Discrete congruences, the old nonproportional
valuation bounds, and the full divisor impose further conditions.

In particular the entire interval `(41/100,42/100)` survives all seven
named proportional exclusions and the fixed midpoint exclusion for
`L>N`. It is a specific gap in their coverage.
No finite extension of the length certificate, full digit-sum test, or
witness is asserted by this interval calculation.

## General rational centres and their actual length thresholds

For a reduced `a/b` with `0<a<b`, write

```text
L=bk+r, 0<=r<b,       i=ak+s,
delta=bi-aL,          w=max(0,r,s)-min(0,r,s).
```

Clearing denominators in
`7*10^r X^b-18*10^s X^a-25` gives the same polynomial construction.
Its coefficient span satisfies both

```text
w >= |s-ar/b| = L*|i/L-a/b|,
w <= L*|i/L-a/b|+b-1.
```

The first inequality follows because `ar/b` lies in `[0,r]`, and all
of `0,r,s` lie in an interval of width `w`. Consequently `H=w+2` is a
valid height parameter, with

```text
D*h(alpha) < H*log 10,       D<=b.
```

When `7` does not divide `a`, the same simple-root proof applies to any
pair with `t>0`. The value of `b` modulo 7 causes no problem in that
argument. When `7` divides `a`, the displayed derivative is zero modulo
7; this particular simple-root reduction is not established and may not
be silently applied.

For an independent root, a uniform envelope that uses only `D<=b` is

```text
U_b(L,i) = 63*b^3*H*T^2,
T = max(log((k/H+1)/log 10)+log log 7+0.4, 20).
                                                               (4)
```

Here `k>=1` is required. The factor 20 bounds `10 log 7/D` and the
fixed entry 10 for every possible `D`. Sharper degree-specific maxima
were used in the quintic proof. They still have the necessary floor
`T>=10`. The height may be enlarged, but doing so cannot defeat the
lower bounds below. To exclude a pair using (4), one must verify the
**actual-pair** comparison `U_b(L,i)<L-2`; the existence of some later
threshold for each fixed rational centre does not suffice.

The dependent-root branch has a separate direct estimate. The same norm
argument gives an integer `j`, `|j|<H`, and `Dk!=j`. For unrestricted
`D`, the exact LTE formula is

```text
t = 1+v_7(Dk-j)-v_7(D).
```

The subtracted term matters when 7 divides `D`. Omitting it is not an
exact identity. This branch, actual proper factors with smaller degrees,
and sharper root-specific heights may give results beyond (4); the
obstruction next concerns the uniform independent-root envelope.

## An infinite admissible family missed by that uniform envelope

Let

```text
xi=sqrt(2)-1,
M=6*5*11*13*37*101=16,031,730,
L=1+M*q,             q any positive integer,
i=39+42*floor((xi*L-39)/42+1/2).
```

The floor is an exact definition using the positive algebraic number
`sqrt(2)`. It is computable using integers alone as
`i=39+42*((isqrt(2*L*L)-L-18)//42)`. The first pair is
`(L,i)=(16031731,6640575)`. Then `|i/L-xi|<=21/L`. The exact inequalities
`(1414/1000)^2<2<(1415/1000)^2`, together with `21/L<=21/N`, put
every pair with `L>=N` in the specific gap `(41/100,42/100)`.
They have `3<=i<L` and satisfy all of:

```text
L odd, i=3 (mod 6),
(L mod 6,i mod 42)=(1,39),
L != 2 (mod 5), 10 (mod 11), 8 (mod 13),
     27 (mod 37), 15 (mod 101).
```

Thus the parity, modulo-49 table, and five inherited digit-sum length
filters pass, as do the seven named proportional inequalities. The
finite certificate does not apply because these lengths exceed `N`.
The growing power `7^(L-2)|F` and the full test `9*(7L-4)|F` have **not**
been established for this family. These are surviving positions for the
specified filters, not witnesses or candidates certified to survive the
full digit-sum test.

For any rational centre `a/b` in `(0,1)`,

```text
|xi-a/b| = |(a+b)^2-2b^2| /
          (b^2*(sqrt(2)+1+a/b)) > 1/(4b^2),         (5)
```

since the numerator is a nonzero integer and the denominator's final
factor is less than four. Suppose the uniform envelope, even with a
sharper maximum having floor 10, could exclude one of these pairs.
From `H=w+2>=2` and `U_b>=6300*b^3*H` we would need

```text
b^3 < L/12600,
|i/L-a/b| < 1/(6300*b^3).                            (6)
```

The first inequality immediately implies
`L>12600*b^3>168*b^2` for every positive integer `b`.
It follows that `21/L<1/(8*b^2)`.
Combining the approximation to `xi` with (5) now gives

```text
|i/L-a/b| > 1/(4*b^2)-21/L > 1/(8*b^2)
          > 1/(6300*b^3),
```

contradicting (6). Thus no denominator that is small enough for this
standard degree-`b`, coefficient-span height estimate to apply with a
contradictory upper bound is close enough to cover this family. This
argument even grants the simple-root reduction at all centres, so centres
with `7|a` cannot repair the numerical gap merely by being added without
a stronger estimate.

The precise obstruction is the `b^3` degree factor together with the
height floor and the distance contribution to `H`. Rational density
ignores both the available width and the length threshold. A claim that
some refined use of proper factors, multiplicative dependence, the full
digit-sum condition, or the two exact quotient candidates covers this
family would require a new argument; none is supplied here. There is no
new effective global cutoff or witness, and no change to complete length
coverage or Lean formalization.
