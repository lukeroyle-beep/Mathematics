# Effective valuation bounds: a central strip and the remaining obstruction

25 November 2026. Base: merged PR #9,
`4dc97536a57d1b216f79e4856c333ea2c8e6d1ae`.

**New partial result.** Every residual pair with
`|L-2i| <= 47` is excluded at every length. Both `i` and `L-i` can grow
without bound in this region, so this is an interior exclusion, additional
to the previously established edge regions. It does **not** exclude the
whole remaining family and gives no global maximum length. The exhaustive
interval remains all lengths through 10,000,000 inclusive.

The proof below establishes an explicit variable-offset valuation bound
using an algebraic factorization of degree at most two and a fully
explicit published two-logarithm estimate. The inherited ten-million
certificate completes the strip consequence. Checks of 48 polynomial
discriminants provide separate arithmetic controls. These are
ordinary mathematics and exact finite arithmetic, not Lean formalizations.

## Statement and precise domain

Throughout, logarithms are natural, `v_7(7)=1`, and

```text
F(L,i) = 7*10^L - 18*10^i - 25,
M(L) = max(log L+2,20).
```

For every pair of integers `L>=5`, `3<=i<L`, with `L` odd, put
`d=L-2i`. Then

```text
v_7(F(L,i)) <= 504*(|d|+2)*M(L)^2.                    (1)
```

The number 504 is absolute for this family; the dependence on the changing
offset is displayed explicitly. In particular, if `|d|<=47` then the
right side is at most `24696*M(L)^2`. The estimate needs neither
`i=3 (mod 6)` nor the digit-sum condition. For a potential
witness the latter remains exactly `9*(7L-4) | F`, and full divisibility
remains `225*7^(L-2)*(7L-4) | F`.

Combining (1) with the already proved comparison in
[EDGE_BOUNDS.md](../settlement/EDGE_BOUNDS.md) shows that for `L>=10,000,000`
there is no pair in this strip satisfying even `v_7(F)>=L-2`. The inherited
exact certificate covers the lower lengths. Consequently there is no full
witness anywhere in this strip. No digit-sum weakening occurs: the proof
excludes a necessary condition for full divisibility.

## Fixed algebraic bases supplied by the offset

Write `x=10^i`. For each nonzero odd `d` define a primitive integer
quadratic as follows:

```text
d>0:  P_d(X) = 7*10^d*X^2 - 18*X - 25,
       F(L,i) = P_d(x).

d<0:  e=-d,
       P_d(X) = 7*X^2 - 18*10^e*X - 25*10^e,
       F(L,i) = P_d(x)/10^e.                          (2)
```

The denominator in the second identity is a 7-adic unit. Both polynomials
are primitive: their three integer coefficients have common gcd one.
Their leading coefficients have valuation one and their middle and
constant coefficients are 7-adic units. Modulo 7, each polynomial is a
nonzero scalar times `3X+3`; its root `6` is simple. Hensel's lemma
therefore gives a unique unit root `alpha_d` in `Q_7`.

Put `D=[Q(alpha_d):Q]`, which is either one or two. We do not assume that
all these polynomials are irreducible. If `beta_d` is the other root,
the product of the roots has valuation `-1`, so `v_7(beta_d)=-1`.
It follows for the unit `x=10^i` that

```text
v_7(x-beta_d) = -1,
v_7(F(L,i)) = v_7(x-alpha_d).                         (3)
```

Indeed the valuation one from the leading coefficient cancels the
valuation minus one from `x-beta_d`; (2)'s denominator contributes zero.
This is an exact factorization of the additive three-term expression,
not an application of a multiplicative logarithm theorem to the original
sum without a reduction.

For multiplicative independence in the degree-two case, suppose
`10^r*alpha_d^s=1` for integers `r,s`. Taking the norm gives

```text
100^r * N(alpha_d)^s = 1,
N(alpha_d) = -25/(7*10^d)  if d>0,
N(alpha_d) = -25*10^(-d)/7 if d<0.
```

In both cases `v_7(N(alpha_d))=-1`, so `s=0`, then `r=0`.

For negative odd `d=-e`, the degree is always two: the discriminant is
`4*10^e*(81*10^e+175)`, whose 2-adic valuation `e+2` is odd. Thus it
cannot be a rational square.

It remains to establish independence if `d>0` and `alpha_d` is rational.
A nontrivial multiplicative relation with 10 would force
`alpha_d=epsilon*10^k` with `epsilon` equal to 1 or -1 and `k` an integer:
prime valuations outside 2 and 5 vanish, and its 2- and 5-adic valuations
are equal integers. For `k>0`, the rational-root theorem is impossible
because the numerator `10^k` does not divide 25. For `k=0`, neither 1 nor
-1 is a root. For `k=-u<0`, multiplying the root equation by `10^(2u)`
gives

```text
7*10^d - 18*epsilon*10^u - 25*10^(2u) = 0.
```

The three 5-adic valuations are `d,u,2+2u`. Their minimum must occur at
least twice, forcing `d=u`. Division by `10^u` would then give
`7-18*epsilon-25*10^u=0`, impossible for either sign and `u>0`.
This handles the rational-root case without assuming any unverified
irreducibility statement. In every case the bases are multiplicatively
independent 7-adic units, and `10^i-alpha_d` is nonzero.

## Heights and all parameters of the logarithm theorem

Let `h_alg` denote absolute logarithmic algebraic height, to distinguish
it from the integer height in the Evertse argument.

For `d>0`, the polynomial takes positive values at `-1` and `1` and a
negative value at zero. Its two real roots lie strictly inside `(-1,1)`.
If `D=2`, primitivity and irreducibility give

```text
h_alg(alpha_d) = (log 7+d*log 10)/2
               < (|d|+2)*log 10/2.
```

If `D=1`, write the root as a reduced rational number `a/b`. The
rational-root theorem gives `|a|<=25` and `b<=7*10^d`, so
`h_alg(alpha_d)<=log(7*10^d)<(|d|+2)*log 10`.

For `d=-e<0`, its values at both `-1` and `1` are negative, so its two
real roots lie respectively below `-1` and above `1`. The product of their
absolute values is `25*10^e/7`. Here `D=2`, as proved above, and hence

```text
h_alg(alpha_d) = (log 25+e*log 10)/2
               < (|d|+2)*log 10/2.
```

Consequently in every case

```text
h_alg(alpha_d) < (|d|+2)*log 10/D,  D in {1,2}.       (4)
```

Use Bugeaud--Laurent, *Minoration effective de la distance p-adique entre
puissances de nombres algebriques*, Corollary 1, printed p. 4, with the
definitions on printed pp. 2--3:
[primary PDF](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf).
The following parameters specify the application completely:

```text
p=7,
alpha_1=10, alpha_2=alpha_d,
b_1=i, b_2=1,
Q_7(alpha_1,alpha_2)=Q_7, hence e=f=1,
D=[Q(alpha_1,alpha_2):Q]/f in {1,2},
log A_1=log 10,
log A_2=(|d|+2)*log 10/D.
```

The height conditions `log A_j >= max(h_alg(alpha_j),log(7)/D)` follow
from (4), `D<=2`, `|d|>=1`, and `log 10>log 7`. The theorem's local
parameters are fixed and its degree is at most two; the auxiliary `g`
of its Theorem 3 has
already been bounded by `7^f-1` in Corollary 1. It is unrelated to our
digit-position gap.

In this application the corollary reads

```text
v_7(10^i-alpha_d)
 <= 168*D^4/(log 7)^4 * log A_1*log A_2
    * max(log b' + log log 7 + 0.4, 10 log 7/D, 10)^2,

b' = i/((|d|+2)*log 10) + 1/(D*log 10) < i.          (5)
```

The strict inequality for `b'` holds already for `i>=1`, since `|d|>=1`
and `log 10>2`. Also `log log 7+0.4<2` and `10 log 7/D<20`, so the maximum
in (5) is at most `M(L)`.

The rational logarithm enclosures already checked by
[log_bounds.py](../log_bounds.py) give

```text
168*(log 10)^2/(log 7)^4 < 63.
```

Substitution of `log A_2` multiplies this exact comparison by
`D^3*(|d|+2)`, at most `8*(|d|+2)`. It therefore bounds the coefficient
in (5) by `504*(|d|+2)`. Equations (3)--(5) prove (1). The smaller degree
in the rational case compensates for its larger allowed root height.
The degree-four factor in the source is included throughout.

For the single ray `d=1`, its nonsquare discriminant gives `D=2`, and
the sharper height `h_alg(alpha_d)<log 10` permits
`A_2=10` and gives

```text
v_7(F(2i+1,i)) <= 1008*max(log i+2,10)^2.
```

This last specialization is not needed for the strip result.

## Numerical cutoff and the exact finite verification obligation

The inherited edge proof establishes, for every real `L>=10,000,000`,

```text
24948*M(L)^2 = 63*396*M(L)^2 < L-3.
```

Since `504*(47+2)=24696<24948`, equation (1) implies
`v_7(F)<L-3<L-2` throughout the stated strip above that boundary.
The remaining integer lengths are `5<=L<10,000,000` in the residual
domain; they are a subset of the already independently certified interval
through 10,000,000. Although (1) does not assume `i=3 (mod 6)`, positions
outside that class have `F!=0 (mod 7)`, because 10 has order 6 modulo 7
and `18*10^i+25=0 (mod 7)` is equivalent to `10^i=6 (mod 7)`.
They therefore cannot satisfy `v_7(F)>=L-2`, and the inherited residual
certificate completes all positions covered by the strip statement.
The old parity and elementary reductions cover the
other original-problem cases. No new exhaustive interval has been run or
claimed, and no intervening unverified finite range remains for this
particular strip.

In particular any still-possible full witness inherits all earlier
restrictions and must additionally satisfy both

```text
|L-2i| >= 49.
L-2 <= 504*(|L-2i|+2)*M(L)^2.
```

This does not say that arbitrary offsets at least 49 are feasible.

## Exact discriminant certificate and its limited coverage

The computational question was whether each of the 48 fixed quadratics
for odd `-47<=d<=47` is irreducible over `Q`. Its exact coverage is those
48 polynomials, **not** a range of lengths or candidate witnesses. These
checks verify the degree-two specialization on the strip. The general
proof above covers rational roots separately and does not depend on this
finite irreducibility list. None of these 48 discriminants is a square.

For `d=-e<0`, there is also a symbolic check valid for every odd `e>0`:

```text
disc(P_d) = 4*10^e*(81*10^e+175),
v_2(disc(P_d)) = e+2,
```

which is odd. For the 24 positive offsets the following table supplies a
small prime `p` and the nonsquare residue of the discriminant modulo `p`.
These provide a second verification independent of integer square roots.

| d | p | discriminant mod p | d | p | discriminant mod p |
|---:|---:|---:|---:|---:|---:|
| 1 | 13 | 5 | 25 | 13 | 5 |
| 3 | 19 | 3 | 27 | 17 | 10 |
| 5 | 29 | 8 | 29 | 31 | 22 |
| 7 | 13 | 5 | 31 | 13 | 5 |
| 9 | 17 | 5 | 33 | 17 | 14 |
| 11 | 17 | 10 | 35 | 19 | 14 |
| 13 | 13 | 5 | 37 | 13 | 5 |
| 15 | 17 | 3 | 39 | 19 | 3 |
| 17 | 17 | 14 | 41 | 17 | 5 |
| 19 | 13 | 5 | 43 | 13 | 5 |
| 21 | 19 | 3 | 45 | 23 | 10 |
| 23 | 23 | 10 | 47 | 17 | 3 |

Reproduce both checks from any Python 3.8+ interpreter. Explicit exceptions
keep checks enabled under `python3 -O`:

```python
from math import isqrt

certs = [
    (1,13,5), (3,19,3), (5,29,8), (7,13,5), (9,17,5), (11,17,10),
    (13,13,5), (15,17,3), (17,17,14), (19,13,5), (21,19,3), (23,23,10),
    (25,13,5), (27,17,10), (29,31,22), (31,13,5), (33,17,14), (35,19,14),
    (37,13,5), (39,19,3), (41,17,5), (43,13,5), (45,23,10), (47,17,3),
]
for d in range(-47,48,2):
    if d>0:
        a,b,c=7*10**d,-18,-25
    else:
        a,b,c=7,-18*10**(-d),-25*10**(-d)
    disc=b*b-4*a*c
    t=isqrt(disc)
    if not t*t < disc < (t+1)*(t+1):
        raise ArithmeticError((d,"not certified nonsquare"))
for d,p,r in certs:
    if any(p%q==0 for q in range(2,isqrt(p)+1)):
        raise ArithmeticError((p,"not prime"))
    if (324+700*pow(10,d,p))%p != r:
        raise ArithmeticError((d,"wrong residue"))
    if r in {x*x%p for x in range(p)}:
        raise ArithmeticError((d,"square residue"))
print("48 discriminants and 24 modular nonsquare certificates passed")
```

The primary workstream ran exact integer square-root enclosures for all 48
discriminants and exhaustively enumerated squares modulo each listed prime.
The independent review record identifies its separate checks. Neither test
uses original-problem witnesses as positive controls; these are finite
polynomial-hypothesis certificates.

## Where the attempted global routes stop

1. **Let the offset vary without a bound.** The degree remains at most
   two, but the allowed root height in (4) grows proportionally to
   `|L-2i|`. The proved estimate (1) is of size
   `O((|L-2i|+1)*(log L)^2)`, rather than a uniform sublinear estimate.
   The first unproved step is a uniform improvement that removes this
   growing height, or a proved restriction forcing the offset into a
   controllably narrow band. No general irreducibility claim is needed
   or made outside the proved negative-offset case and finite list.

2. **Combine all three explicit bounds.** The existing fixed-position
   and fixed-gap estimates have factors `i+1` and `L-i+1`. The new
   factorization adds an offset factor. When, for example, `i` is near
   `L/3`, all three quantities are proportional to `L`. Taking their
   minimum still allows upper bounds of order `L*(log L)^2`, which do
   not contradict `v_7(F)>=L-2`. No global cutoff follows.

3. **Treat fixed rational slopes as recurrences.** Bugeaud--Evertse,
   *S-parts of terms of integer linear recurrence sequences*, Theorem 1.2,
   printed p. 4 of the [author PDF](https://pub.math.leidenuniv.nl/~evertsejh/16-LinRecBuEv.pdf),
   has an effective conclusion for a fixed nondegenerate recurrence with
   a dominant root. For fixed integers `a>b>0` and fixed offsets `c,d`,
   the sequence `7*10^c*(10^a)^k-18*10^d*(10^b)^k-25` (taking
   nonnegative offsets here) is such a recurrence. Its constants depend
   on the recurrence, including `a,b,c,d`; these cannot be silently made
   uniform over changing slopes or offsets. Moreover a bound
   `7^v <= F^(1-eta)` contradicts `v>=L-2` by exponential rates only
   if `eta > 1-log(7)/log(10)`. Mere positivity of an effective saving
   is insufficient. The first missing step is an applicable estimate
   with the required strength and uniform constants.

4. **Use effective few-digit bounds.** Bugeaud's
   [primary paper](https://arxiv.org/pdf/1609.07926), Theorem 1.2,
   printed p. 3, assumes ordinary nonnegative base digits. The signed
   expression `F` is not in that domain. Its proof on printed pp. 6--8
   explains how a small unrestricted cofactor is treated with a logarithm
   whose height contains that cofactor; this is not a license to regard
   it as a fixed base. The first missing step is a proved signed-coefficient
   adaptation with an explicit saving exceeding the threshold above.
   No such adaptation or sufficient constant is claimed here.

5. **Invoke newer effective multi-term S-unit equations.**
   Bajpai--Bennett, *Effective S-unit equations beyond 3 terms: Newman's
   conjecture*, [2023 primary preprint](https://arxiv.org/pdf/2308.05162),
   Theorem 1, printed p. 2, requires every variable term to be an S-unit
   and at most three places, including infinite places. Writing
   `F=7^t R` does not put the unrestricted integer `R` in a fixed S-unit
   group. Even `{infinity,2,5,7}` already has four places. The theorem
   as stated is inapplicable. An effective treatment of the unrestricted
   cofactor with uniform small height loss is the missing reduction.

6. **Use the digit sum to freeze the cofactor.** Full divisibility gives
   `F=225*7^(L-2)*(7L-4)*q`, where `q` is an unrestricted positive
   integer and

   ```text
   q < 343/(225*(7L-4))*(10/7)^L.
   ```

   The height of this permitted cofactor is still of order `L`, while
   the extra factor `7L-4` has height `log(7L-4)`. A theorem allowing
   constants to depend on either as a fixed coefficient is not uniform
   here. The first unproved step is a new use of the **full** condition
   `9*(7L-4)|F` that restricts the cofactor or the exponents sufficiently.

The original qualitative method loses effectivity before these
special-family reductions: Evertse's 1984 proof uses the unspecified
exceptional subspaces of Theorem 4 (printed pp. 231--232). The induction
constant in Theorem 2 depends on their coefficient tuples, and the height
bound in the proof of Theorem 1 on printed pp. 234--235 uses that constant.
The stronger qualitative corollary does not supply these data. A bound
on the count of subspaces or intervals does not repair their missing
height endpoints.

## Source and reproduction receipts

The original Bugeaud--Laurent PDF was opened, its printed p. 4 rendered
and inspected, and these downloaded bytes were hashed on 25 November 2026:

| Source | SHA-256 |
|---|---|
| `logpadicdef.pdf`, primary theorem | `554bb384df62538fa11fcf6ab74976e772156c9d3ca4022e2128d48e3632128d` |
| `16-LinRecBuEv.pdf`, recurrence route | `a8116b4af8d9fee7c508ab6c905620f8b540b5285b516beb990c1affa63e4860` |
| `arxiv:1609.07926`, few-digit route | `eb88ba3dcecf7e56066a11124368f8f2013ee6def488785729b6fdef85212ab7` |
| `arxiv:2308.05162`, multi-term S-unit route | `be15d92f9e0edd914b2525f4c9c888e3d83859028a03ccba3596b8feba9b91be` |

For example, the primary source check used:

```sh
curl -L --fail https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf -o /tmp/a398769-effective-logpadicdef.pdf
shasum -a 256 /tmp/a398769-effective-logpadicdef.pdf
pdftoppm -f 4 -singlefile -scale-to 1800 -png /tmp/a398769-effective-logpadicdef.pdf /tmp/a398769-effective-logpadicdef-p4
python3 research/a398769/five-seven/log_bounds.py
```

The new effective argument has completely checked finite consequences
only on the displayed strip. It does not provide explicit constants
`c<1,C,L0` for the whole residual family. The `{5,7}` subclass remains
unresolved.
