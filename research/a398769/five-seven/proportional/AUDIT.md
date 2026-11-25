# Independent audit of the five proposed proportional exclusions

25 November 2026. The submission is the attached *A398769 proportional
position bounds* note. The inherited algebraic and edge reductions are
those merged in PR #10, commit
`2aea8ff77232225a68f5ebe694b812bc3a9438b8`.

**Verdict: all five proposed inequalities are valid necessary conditions
for a witness.** The all-length midpoint exclusion extends from
`|L-2i| <= 47` to `|L-2i| <= 165`. These are ordinary mathematical proofs
using a published explicit theorem, combined with the inherited exact
certificate through 10,000,000. They do not settle the full subclass or
extend complete length coverage.

Let `L >= 5` be odd, `3 <= i < L`, and retain the inherited necessary
congruence `i = 3 (mod 6)`. Write

```text
F = 7*10^L - 18*10^i - 25,   t = v_7(F),   N = 10,000,000.
n = F/9,   P = 25*7^(L-2),   S = 7L-4.
```

A full witness requires `225*7^(L-2)*(7L-4) | F`, hence `t >= L-2`.
The separate digit-sum condition is `9*S | F`. None of the arguments
below replaces it by `S | F` or treats a bounded modular survivor as a
full witness.

| Proposed necessary inequality | Verdict | Exclusion proved for `L >= N` |
|---|---|---|
| `i > L/25,000` | Pass | `i <= L/25,000` contradicts `t >= L-2` |
| `L-i > L/25,000` | Pass | `L-i <= L/25,000` contradicts `t >= L-2` |
| `abs(L-2i) > L/60,000` | Pass | `abs(L-2i) <= L/60,000` contradicts `t >= L-2` |
| `abs(L-3i) > L/300,000` | Pass | `abs(L-3i) <= L/300,000` contradicts `t >= L-2` |
| `abs(2L-3i) > L/300,000` | Pass | `abs(2L-3i) <= L/300,000` contradicts `t >= L-2` |

The closed endpoints are excluded: each final estimate is strictly below
`L-2`, even at the allowed offset equality. The certificate covers all
smaller lengths, so each strict necessary inequality holds for every
possible witness.

A further refinement proved at the end of this audit excludes the
larger fixed strip `abs(L-2i) <= 179` at every length.

## Primary-source theorem and parameter audit

Bugeaud and Laurent, *Minoration effective de la distance p-adique entre
puissances de nombres algébriques*, Corollary 1, printed p. 4, and the
definitions on printed pp. 2–3 were checked directly against the
[primary paper](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf).
For multiplicatively independent unit bases, positive exponents, and
`log A_j >= max(h(alpha_j), log p/D)`, its parameters include

```text
D = [Q(alpha_1,alpha_2):Q]/f,
b' = b_1/(D*log A_2) + b_2/(D*log A_1).
```

Here the selected root belongs to `Q_7`, so the local extension has
`e=f=1`. Its global degree `D` need not equal the local degree. Taking
`alpha_1=10`, `alpha_2=alpha`, `(b_1,b_2)=(k,1)`, and

```text
log A_1 = log 10,
log A_2 = H*log 10/D,
H*log 10 >= max(D*h(alpha), log 7)
```

gives exactly

```text
b' = (k/H + 1/D)/log 10,

v_7(10^k-alpha)
 <= 63*D^3*H
    * max(log b' + log log 7 + 0.4, 10*log 7/D, 10)^2.       (A)
```

Indeed the source coefficient becomes
`168*D^4*log A_1*log A_2/(log 7)^4`, and
`168*(log 10)^2/(log 7)^4 < 63`. The `D^4` term is retained before
substitution. The denominator `log 10` in `b'` is essential for the
numerical bounds used below. Enlarging `H` is permitted because it is
an upper height parameter; the theorem does not require a fixed `H`
for all pairs.

## Both ends

For `i <= L/25,000`, put `alpha=(18*10^i+25)/7` and `k=L`.
The inherited congruence makes `alpha` an integer. If `7 | alpha`,
then `t=1`. Otherwise `alpha` and 10 are 7-adic units,

```text
t = 1 + v_7(10^L-alpha),
h(alpha) < (i+1)*log 10.
```

Independence follows from `v_2(alpha)=0` and `v_5(alpha)=2`: the 2- and
5-adic valuations of `10^r*alpha^s=1` force `r=s=0`.

For `g=L-i <= L/25,000`, put `B=7*10^g-18`, `alpha=25/B`, and `k=i`.
Since `g` is even and at least two, `v_2(B)=1`, `v_5(B)=0`, and
`v_7(B)=0`. Both bases are units, `h(alpha)=log B<(g+1)*log 10`, and
`t=v_7(10^i-alpha)`. Independence follows because the 2- and 5-adic
valuations of a relation give `r-s=0` and `r+2s=0`.

In both cases `D=1`. Choose `H=L/25,000+1`; then
`b' < 25,001/log 10`. The first entry in (A)'s maximum is below 11,
while `10*log 7 < 19.5`. Thus both cases are covered by

```text
t <= 1 + (95823/4)*(L/25000+1) < L-2,   L >= N.        (B)
```

The extra 1 in (B) is unnecessary for the leading-end case but harmless.

## Midpoint

Put `d=L-2i` and `x=10^i`. As `L` is odd, `d` is a nonzero odd integer.
The integral quadratic is

```text
d>0:  7*10^d*X^2 - 18*X - 25,
d<0:  7*X^2 - 18*10^(-d)*X - 25*10^(-d).
```

Its value at `x` is respectively `F` or `10^(-d)*F`; the extra factor
is a 7-adic unit. The reduction modulo 7 has a simple unit root.
The other root has valuation -1, canceling the leading coefficient's
valuation 1. Consequently the selected `alpha` in `Q_7` satisfies

```text
t = v_7(10^i-alpha),
D <= 2,
D*h(alpha) < (abs(d)+2)*log 10.
```

The inherited argument handles independence for both possible degrees.
For degree two, the root norm has 7-adic valuation -1 and a norm of
any multiplicative relation forces its exponent to vanish. The optional
irreducibility argument below in fact proves that `D=2` for every
applicable offset, but the bound does not need that improvement.

Assume `abs(d) <= L/60,000`, and choose `H=L/60,000+2`.
Since `i=(L-d)/2`,

```text
b' < 30001.5/log 10.
```

The first maximum entry is below `10.6`. For `D=2`, the other entries
are at most 10; for `D=1`, the entire maximum is below 20. Hence

```text
t <= max(504*(10.6)^2, 63*20^2)*H
   = (1415736/25)*(L/60000+2) < L-2,   L >= N.         (C)
```

For all `L >= N`, `165 < N/60,000 <= L/60,000`, so (C) excludes
every offset `abs(d) <= 165`. The inherited certificate covers
`L < N`. Thus this strip is excluded at every length, with no residual
finite interval left to compute. Odd parity makes 167 the next possible
absolute offset, without asserting that such an offset is feasible.

## Both cubic centres, including both signs of the offset

The two parameterizations are

| Centre | `k` | `d` | Polynomial before clearing denominators |
|---|---|---|---|
| `1/3` | `i` | `L-3i` | `7*10^d*X^3-18*X-25` |
| `2/3` | `L-i` | `L-3(L-i)=3i-2L` | `7*10^d*X^3-18*10^d*X^2-25` |

Multiply by `10^max(0,-d)` to obtain an integral polynomial `Q`.
At `x=10^k`, its value is this same 7-adic unit times `F`.
Modulo 7, `Q` has the form `c*X^j+c_0` with `j=1` or 2 and both
coefficients nonzero. For `t>0`, `x` is a unit root and
`Q'(x)=j*c*x^(j-1)` is nonzero modulo 7. This argument is unaffected
by a negative or zero `d`.

Hensel lifting gives a root `alpha` in `Q_7` with `alpha=x (mod 7)`.
The difference quotient `(Q(x)-Q(alpha))/(x-alpha)` is a unit, so

```text
t = v_7(x-alpha),   D=[Q(alpha):Q] <= 3.
```

Here `F>0` for `L>i>=3` ensures `x != alpha`. If `t=0`, the required
exclusion is immediate and no root is needed.

For both parameterizations and both signs of `d`, the sum of absolute
coefficients is at most `50*10^abs(d)`. The Mahler measure of `Q` is
at most this sum. The primitive integral minimal polynomial of `alpha`
divides `Q` over the integers, and its cofactor has Mahler measure at
least one. Therefore

```text
D*h(alpha) <= log(50*10^abs(d)) < (abs(d)+2)*log 10.
```

This reasoning does not assume that `Q` itself is primitive or
irreducible; in particular the second polynomial can have nontrivial
content. It does account for a reducible cubic and any selected factor.

If `abs(d) <= L/300,000`, choose `H=L/300,000+2`. Since
`k=(L-d)/3`, `b' < 100,002/log 10`. The first maximum entry in (A)
is below 12. For `D=2,3` the entire maximum is at most 12; for `D=1`
it is below 20. In the multiplicatively independent case,

```text
t <= max(63*27*12^2,63*20^2)*H
   = 244944*(L/300000+2) < L-2,   L >= N.             (D)
```

For completeness, dependence is also excluded without using (A).
Write `alpha^s=10^r` for integers `s>0` and `r`, allowing `r=0`.
Taking the norm and its 2-adic valuation shows that `a=Dr/s` is an
integer. Height gives `abs(a)=D*h(alpha)/log 10 < H`, and
`alpha^D/10^a` has finite order in `Q_7`. Such an order divides six:
reduction modulo 7 is injective on torsion, because `1+7*Z_7` is
torsion-free.

If `Dk=a`, then `x/alpha` is torsion and belongs to `1+7*Z_7`, hence
equals one, contradicting `F>0`. Otherwise raising `x/alpha` to the
`6D`-th power preserves its distance valuation because `7` does not
divide `6D`. Thus, using `v_7(10^6-1)=1`,

```text
t = v_7(10^(6*(Dk-a))-1) = 1+v_7(Dk-a).
```

The equality also holds for negative exponents by inversion.
Since `k<L` and `abs(a)<H`,

```text
0 < abs(Dk-a) < 3L+H < 4L < 7^(L-3),   L >= N.
```

The last inequality already holds at `L=5` and persists as `L`
increases. Consequently `v_7(Dk-a)<L-3`, again giving `t<L-2`.
This completes both cubics in every degree and dependence case.

## Exact numerical margins and independent controls

All final upper bounds are affine in `L` with slope below one. The
following exact margins are `(N-2) minus upper_bound(N)`:

| Region | Slope | Margin at `N` |
|---|---:|---:|
| Both ends, including extra 1 | `95823/100000` | `1574965/4` |
| Midpoint | `58989/62500` | `11212478/25` |
| Both independent cubic cases | `5103/6250` | `1345310` |

Therefore no asymptotic-only comparison or unspecified starting length
is being used. A separate rational-series calculation bounded the first
maximum entries above by respectively `10.358368469`, `10.540700025`,
and `11.744642831`. It also checked the coefficient below 63 and
`10*log 7 < 19.5`. These decimal upper bounds denote exact rationals,
not floating-point evidence.

Independent arithmetic controls evaluated both cleared cubic identities
for every odd `5 <= L <= 121` and `3 <= i < L`: 7,080 identities,
including 4,759 negative, 38 zero, and 2,283 positive offsets. The 1,220
instances with `7 | F` had nonzero derivative modulo 7. Their simple
roots were lifted through `7^6`, giving 6,100 comparisons of direct
divisibility with root-distance congruences. These are positive modular
controls, not witnesses or new length certificates. The regression
`(L,i)=(23,15)` gives `v_7(F)=2`, `F mod 49=0`, and
`F mod 343=245`; it fails the full divisor.

## Optional quadratic irreducibility argument

The submitted simplification is valid. For positive integer `d`, a
square discriminant would give an integer `y>9` with

```text
(y-9)*(y+9) = 7*2^d*5^(d+2).
```

The two positive factors differ by 18 and cannot both be divisible by
5. One therefore contains the entire factor `5^(d+2)` and is at least
that large; the other is at most `7*2^d`. Their difference is at least
`5^(d+2)-7*2^d>18` for every `d>=1`, a contradiction. For negative
odd `d=-e`, the discriminant is `4*10^e*(81*10^e+175)` and has odd
2-adic valuation `e+2`. Thus every applicable midpoint quadratic is
irreducible over `Q`. A finite check of 166 discriminants at odd
`-165 <= d <= 165` agrees, but the all-offset conclusion comes from
the proof, not that check.

## Additional verified refinement: fixed midpoint strip through 179

This strengthens the submission's requested 165 consequence. It does
not alter the five proportional constants. The irreducibility proof
above gives `D=2` for every applicable midpoint offset. For
`abs(d) <= 179`, choose the fixed upper height parameter `H=181`.
Since `i=(L-d)/2 <= (L+179)/2`,

```text
b' <= ((L+179)/(2*181)+1/2)/log 10
    = (L+360)/(362*log 10).
```

The same rational logarithm enclosure used in this audit gives

```text
log((N+360)/(362*log 10)) + log log 7 + 0.4 < 10.46.
```

For `L >= N`, `(L+360)/(N+360) <= L/N`; also
`10*log 7/D < 10`. Thus every entry of (A)'s maximum is at most
`10.46+log(L/N)`, and

```text
t <= B(L) = 504*181*(10.46+log(L/N))^2.
B(N) = 6238102374/625 = 9,980,963.7984,
(N-2)-B(N) = 11896376/625 > 0.
```

The derivative is

```text
B'(L) = 1008*181*(10.46+log(L/N))/L.
```

Its derivative has the sign of `1-10.46-log(L/N)`, which is negative
for all `L >= N`. Hence `B'(L) <= B'(N) = 5963769/31250000 < 1`.
The positive margin below `L-2` consequently increases beyond `N`.
This proves `t<L-2` for every `L>=N` in the fixed strip. The inherited
certificate covers every smaller length, with no additional finite
verification obligation. Therefore every possible witness must satisfy
`abs(L-2i) >= 181`, as well as all five proportional inequalities.

This argument does not claim that the fixed width 179 is optimal or
that offset 181 is feasible. It supplies a further all-length exclusion,
not a global cutoff or a new exhaustive length interval.
