# Exact reduction to the three finite bands

26 November 2026. This note audits the analytic reduction independently of
the finite enumerators. Its conclusions about all lengths use the inherited
whole-length certificate through **B=1,000,002,000,000**, the inherited
`b<=4K` theorem, and the explicitly identified finite computations below.
The ZIP named in the request was unavailable; no claim is credited merely
because it was reported in that unmerged archive. No new Lean formalization
is performed.

Write `t=v7(F)`, where `F=7*10^L-18*10^i-25`, and let
`K=min{k>=1:6*7^(k-1)>L}`. A full witness requires `t>=L-2` together
with `5∤S` and **`9S|F`** at that same position, `S=7L-4`. This note
uses the high-valuation necessary condition to exclude specified centres;
it does not replace the full witness predicate by that condition.

## Nearest rounding and the selected root

Fix coprime `0<a<b`, `|h|=|bi-aL|<=K^2`, and `4K<b<=c<=K^2`.
In the ranges at issue `L>B`, so `b<L` and rounding `q` to the nearest
integer to `L/b` gives `q>=1`. Either choice at a tie is valid. Set

```
r=L-bq, s=i-aq, u=min(0,r,s), w=max(0,r,s)-u,
Q_q(Z)=7*10^(r-u)*Z^b-18*10^(s-u)*Z^a-25*10^(-u),
x=10^q.
```

All coefficients are integers, `Q_q(x)=10^(-u)F`, and
`s=(a/b)r+h/b`. Each of `|r|,|s|,|r-s|` is at most
`|r|+|h|/b`; their maximum is the span w. Hence

```
w <= b/2+K^2/b,
w+2 <= H:=c/2+K^2/c+2.                                      (1)
```

The last comparison follows because the derivative of `z/2+K^2/z`
is positive for `z>4K`. Negative r must be included in the minimum u.

The inherited polynomial uses `q0=floor(L/b)` and `u0=min(0,r0,s0)`.
Nearest rounding changes q by zero or one. In the latter case

```
r1=r0-b, s1=s0-a,
Q_(q0+1)(Z)=10^(u0-u1) Q_q0(Z/10).                          (2)
```

Thus a selected root transforms as `alpha1=10 alpha0`, and
`x1=10 x0`. Multiplication by a nonzero rational preserves the exact
global degree `D=[Q(alpha):Q]`. The derivative is multiplied by the
seven-adic unit `10^(u0-u1-1)`, so its valuation is unchanged;
`v7(x1-alpha1)=v7(x0-alpha0)` as well. Multiplicative dependence of
`10,alpha1` is equivalent to that of `10,alpha0`: multiply a purported
relation by the corresponding integer power of ten. This checks the
root change before applying any inherited root exclusion.

In particular the exact derivative identity remains

```
d=v7(Q_q'(x))=v7(7b*10^L-18a*10^i).
```

When `7∤a`, `d=0`; when `v7(a)>=2`, `d=1`; when `a=7v` with
`7∤v`, `d=1+v7(b*10^(L-i)-18v)`. The last case can exceed one.
The audited [uniform derivative theorem](../uniform-bound/ANALYTIC.md)
gives, with all its singular cases retained,

```
d<=B_K:=1+252(K+1)^3,       2B_K<L-2.                       (3)
```

Its proof uses the rational base `18v/b`; the independent case is
Bugeaud–Laurent Corollary 1 with the coefficient `<63`, and the
dependent case is elementary LTE. The exact constant check is repeated
here. Under a full-witness hypothesis `t>=L-2>2d`, strong Hensel gives
a unit root with `v7(x-alpha)=t-d` and `v7(Q_q'(alpha))=d`.

For completeness, the inherited floor-root dependent branch writes
`alpha0^v=10^u`, uses the integer `j=uD/v` obtained from the global
norm, and gives

```
t=d+1+v7(Dq0-j)-v7(D).                                    (4)
```

The norm and height show `|j|<=L`, while `Dq0<=L`; the nonzero
integer `Dq0-j` has absolute value at most `2L<7^(K+1)`.
Consequently `t<=d+K+1<=2B_K<L-2`. The subtracted `v7(D)` is
retained in the identity, including degrees divisible by seven.
Equation (2) therefore excludes dependence for the nearest-rounding
root as well. No new estimate on a dependent root's height is assumed.

For the nearest polynomial, multiplicativity of Mahler measure and
its coefficient-sum bound give, even for reducible Q or nontrivial
content,

```
1<=D<=b,       D*h(alpha)<=log(50*10^w)<H*log10.             (5)
```

Thus the degree is not asserted to equal b and is not confused with
the local degree, which is one because the selected root lies in Q_7.

## Source substitution, with every logarithm branch

[Bugeaud–Laurent, *Minoration effective de la distance p-adique entre
puissances de nombres algébriques*](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf),
Theorem 4, printed p.5, has the table entry `(mu,nu,c_table)=(15,10,18)`.
The theorem and the height normalization on printed p.4 were checked
directly in the primary PDF on 26 November 2026. The locally retained
271,382-byte PDF has SHA-256
`554bb384df62538fa11fcf6ab74976e772156c9d3ca4022e2128d48e3632128d`,
matching [the inherited source record](../uniform-bound/SOURCES.md).
The source's explicit theorem has no additional large-exponent threshold.

Take bases `10,alpha`, positive exponents `q,1`, and `p=7`.
Both bases are seven-adic units; `e=f=1` and `g=6` (ten itself has
order six modulo seven). Set

```
log A1=log10, log A2=H*log10/D,
b'=(q/H+1/D)/log10.
```

Equation (5) and `H>=2` verify both height floors, including
`log7/D`. The resulting bound is

```
t <= B_K + C D^3 H max(M1, 15 log7/D, 10)^2,
C=126*(log10)^2/(log7)^4 <189/4,
M1=log(q/H+1/D)+log(log7/log10)+2/5.                       (6)
```

These are natural logarithms. `analytic_checks.py` certifies C and

```
log(log7/log10)+2/5 < 1/4                                  (7)
```

using rational atanh-series enclosures. No rounded logarithm enters
any endpoint decision.

## Rational endpoint certificates and propagation

For each row below the checker forms exact H and E and verifies

```
sum_(j=0)^90 (m-1/4)^j/j! > (X/c+1/2)/H+1,
E=3+252(K+1)^3+(189/4)c^3 H m^2 < X.                       (8)
```

Every omitted exponential-series term is positive. The first inequality
therefore proves the requested exponential comparison without an upper
error estimate.

| K | c | X | m | H | Exact X-E |
|---:|---:|---:|---:|---:|---:|
|15|101|1,000,002,000,001|19.30|11055/202|1215725589889/160|
|16|142|4,069,338,437,095|20.04|5311/71|3180559907122/625|
|17|226|28,485,369,059,659|21.10|26279/226|25006562862781/100|
|18|324|199,397,583,417,607|23|165|59123814769696|
|19|361|1,395,783,083,923,243|25|367/2|9126737502881045/8|
|17|289|79,000,000,000,000|21.60|295/2|2567582113763/5|

Fix a row, and consider **every `L>=X` for which `K(L)=K`**, and
every `4K<b<=c`. Put `x=c/b>=1`, `y=L/X>=1`. Since
`q<=L/b+1/2` and `1/D<=1`,

```
(q/H+1/D) <= (L/b+1/2)/H+1
            <= xy*((X/c+1/2)/H+1).
```

Equations (7)–(8) imply `M1<m+log(xy)`. For `z>=1`,
`log z<=2(sqrt(z)-1)` follows by differentiating their difference.
As every row has `m>=2`,

```
m+log(xy) <= m sqrt(xy) <= m x^(3/2) y^(1/2).              (9)
```

For `D<=b`, the **positive upper bound** on the first logarithm branch
therefore contributes at most `c^3 H m^2 y` after multiplication
by `D^3 H`. If M1 is negative it cannot attain the maximum with 10;
there is no illicit squaring of a negative upper-bound comparison.
The constant branch contributes `100 D^3 H<=c^3 H m^2 y`, since
`m>=10`.

The degree-dependent branch must be treated separately. It contributes

```
D^3 H*(15 log7/D)^2 =225(log7)^2 D H
                    <900 b H <=b^3 H m^2 <=c^3 H m^2 y.    (10)
```

The middle inequality holds for all `b>=4K+1`; it is checked exactly
in every row. In particular **we do not assert `15log7/D<=m` for
every D**. Taking the maximum of the three contributions in (6) now gives

```
t+2 <= B_K+2+(189/4)c^3 H m^2 y
      <= y E < y X=L,
```

contradicting `t>=L-2`. This proves all-length persistence within each
fixed K-band and all denominators in that row; it is not merely a test
at `(b,L)=(c,X)`. Different K values use their own rows or the inherited
large-K induction.

## Exact coverage reduction

The [inherited moving-centre theorem](../explicit-length/MOVING_CENTRES.md)
excludes full witnesses admitting any `b<=4K` at every length: its
upper bound `902265864195` lies below B. The inherited full-family
certificate handles all `L<=B`. For `L>B`, `K>=15`.

For `K>=20`, [ROUTE2](../explicit-length/ROUTE2.md) excludes every
`b<=K^2`: its polynomial bound
`R(K)=1+252(K+1)^2*((K+1)+K^8+2K^6)` obeys
`R(20)+1<6*7^18`. Its degree-ten nonnegative polynomial grows by
less than seven for successive `K>=20`, while `6*7^(K-2)` grows
by seven. The checker repeats the integer base and ratio comparisons.
The K=18 and K=19 rows above use `c=K^2` and begin at the first odd
length in their K-band, closing both bands completely.

For K=15 and K=16 the first two rows leave exactly the first two
finite rectangles in the table below. For K=17, the c=226 row closes
`4K<b<=226` throughout its band; the c=289 row closes all remaining
denominators for `L>=79,000,000,000,000` (the first admissible odd
length there is 79,000,000,000,001). The separately reproduced b=289
control must cover its **original entire odd interval**
`[28,485,369,059,659,199,397,583,417,605]`. Until that control and
the three searches pass, this note proves only the reduction, not the
final exclusion.

| K | Remaining b | Remaining odd L, inclusive |
|---:|---:|---:|
|15|102–225|1,000,002,000,001–4,069,338,437,093|
|16|143–256|4,069,338,437,095–28,485,369,059,657|
|17|227–288|28,485,369,059,659–78,999,999,999,999|

There are 124+114+62=300 denominators. The b=289 control is a
separate fourth obligation and supplies credit only for its own complete
denominator and declared interval. Any earlier 43-centre sample overlaps
that obligation and supplies no whole-denominator credit. Successful
independent exclusion of these four obligations closes the subfamily
admitting **some reduced `0<a<b<=K^2` with `|bi-aL|<=K^2`** at all
lengths. It does not enlarge the whole-length endpoint B, prove that
every residual pair admits such a centre, or settle the unrestricted
`{5,7}` subclass or the wider digit-1 conjecture.

## Reproduce the analytic audit

From the repository root:

```sh
python3 research/a398769/five-seven/rational-centres/analytic_checks.py > /tmp/a398769-centres-analytic.json
python3 -O research/a398769/five-seven/rational-centres/analytic_checks.py > /tmp/a398769-centres-analytic-O.json
cmp /tmp/a398769-centres-analytic.json /tmp/a398769-centres-analytic-O.json
cmp /tmp/a398769-centres-analytic.json research/a398769/five-seven/rational-centres/analytic-checks.json
```

The receipt binds the five required inherited files by SHA-256 and
records exact row margins, nonvacuous negative-remainder, rounding-tie,
and singular-derivative controls. Mathematical persistence and root
degree/independence transport are proved above; finite controls do not
replace those arguments.
