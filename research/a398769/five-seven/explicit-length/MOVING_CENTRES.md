# An explicit bound with a growing rational denominator

This is a new consequence of the fully parameterized estimate in
[`uniform-bound/ANALYTIC.md`](../uniform-bound/ANALYTIC.md), not a bound
for every pair. It allows the rational centre to change with the length.
All statements are ordinary mathematics, not new Lean formalizations.

## Precisely defined subfamily and bound

Use the residual domain in [README.md](README.md), and put
`K=min{k>=1:6*7^(k-1)>L}`. Suppose a full witness has integers

```
0<a<b<=4K, gcd(a,b)=1, |bi-aL|<=K^2.                 (1)
```

Then, unconditionally,

```
L <= U_moving = 902265864195 < B=1000002000000.       (2)
```

The inherited consecutive certificate through B therefore excludes this
entire subfamily. In particular, every still-possible full witness above B
must satisfy `|bi-aL|>K^2` for **every** reduced `0<a<b<=4K`.
The denominator is unbounded as L grows; no fixed-centre constants are
silently reused. There is no assertion that (1) covers all witnesses or
even all rational ratios `i/L`.

## Effective estimate with every parameter retained

It suffices to consider `L>10000000`; earlier lengths already satisfy (2)
without invoking a certificate. Then `K>=9`, and `4K<=L` (check K=9,
then use `L>=6*7^(K-2)` for K>=10 and induction). Thus every centre
in (1) has `b<=L` and a positive quotient `q=floor(L/b)`.

Write `L=bq+r`, `i=aq+s`, `0<=r<b`, and `m=min(0,s)`. The integral
polynomial and its coefficient span are

```
Q(X)=7*10^(r-m)*X^b-18*10^(s-m)*X^a-25*10^(-m),
w=max(0,r,s)-m <= |bi-aL|/b+b-1,
H=w+2 <= H0:=K^2/b+b+1.
```

At `x=10^q`, `v7(Q(x))=t`. The inherited uniform derivative theorem
gives `d=v7(Q'(x))<=1+252(K+1)^3`. A hypothetical full witness has
`t>=L-2>2d`, so strong Hensel supplies a unit root alpha with
`v7(x-alpha)=t-d`. The dependent-root case is already excluded in
ANALYTIC sections 2–3, including degrees divisible by seven.

For an independent root its actual degree satisfies `D<=b` and
`D*h(alpha)<H0*log10`. Bugeaud–Laurent, Corollary 1, printed p.4
([primary PDF](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf)),
has parameters `p=7`, local degree one, bases `10,alpha`, exponents
`q,1`, and `log A1=log10`, `log A2=H0*log10/D`. Both bases are units,
both exponents positive, and the height floors hold because `H0>=2`.
The global degree remains D; it is not replaced by the local degree.
The polynomial identity handles the signed sum before the theorem is used.

The exact instantiated inequality is

```
t <= d + C0*D^3*H0*M^2,
C0=168*(log10)^2/(log7)^4 < 63,
M=max(log((q/H0+1/D)/log10)+log log7+0.4,
      10*log7/D,10) <= 2K+2.                       (3)
```

For the last comparison, `q/H0+1/D<L`, `L<7^K`, `log7<2`,
and `log(log7/log10)+0.4<1` bound the first branch by `2K+1`;
the other branches are below 20 and equal to 10, and `K>=9`.
The rational logarithm certificate for `C0<63` is reproduced by
`python3 research/a398769/five-seven/explicit-length/checks.py`.
These are exactly the hypotheses and normalization recorded in
[`uniform-bound/SOURCES.md`](../uniform-bound/SOURCES.md).

Since all coefficients below are nonnegative and `b<=4K`,

```
b^3*H0 = K^2*b^2+b^4+b^3 <= 272K^4+64K^3,
t <= R(K):=1+252(K+1)^2*((K+1)+272K^4+64K^3).       (4)
```

This estimate is used under the full-witness hypothesis; it does not
claim an unconditional valuation bound for unrelated small-valuation pairs.
The non-7 digit-sum factor remains part of that hypothesis, although this
particular contradiction uses its necessary high-valuation condition only.

## Integer endpoints and persistence

For `K<=14`, `L<T_14=581334062442<U_moving`. For `K=15`, (4) gives

```
L-2 <= t <= R(15)=902265864193,
L <= 902265864195.
```

For `K=16`, exact arithmetic gives

```
R(16)+1=1317309441086 < 4069338437094=6*7^14.
```

The polynomial `R(k)+1` has nonnegative coefficients and degree six.
For every `k>=16`, therefore,

```
(R(k+1)+1)/(R(k)+1) <= ((k+1)/k)^6
                         <= (17/16)^6 < 2 < 7.
```

The final strict inequality is the integer comparison
`17^6=24137569<33554432=2*16^6`. Induction now proves
`R(K)+1<6*7^(K-2)` for every `K>=16`.
Minimality of K and odd L imply `L>=6*7^(K-2)+1`, hence

```
t <= R(K) < 6*7^(K-2)-1 <= L-2,
```

a contradiction. This proves (2), including its allowed endpoint.
There is no new whole-length interval: (1) is a position restriction.
The computational checks in `checks.py` audit the exact endpoints and
polynomial induction; they do not replace the cited logarithm theorem.
