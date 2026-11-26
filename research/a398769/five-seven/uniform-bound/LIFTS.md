# Sufficiency, exact lifts, and the digit-sum route

These are ordinary mathematical proofs, with exact finite controls described
in this directory's reproduction record. They are not Lean formalizations.
The quadratic valuation bound is a research target, not an assumption of
any unconditional conclusion below.

## 1. Exact setup and reduction to the actual representative

Let `L>=5` be odd, `3<=i<L`, and

```
S=7L-4, F(L,i)=7*10^L-18*10^i-25,
n=F/9, P=25*7^(L-2), T_k=6*7^(k-1),
K=K(L)=min{k>=1:T_k>L}.
```

The [initial reduction](../README.md) proves that every possible `{5,7}`
full witness has this form; the other numbers of fives are excluded there.
The exact condition is

```
P*S | n  iff 225*S*7^(L-2) | F.                 (1)
```

The suffix 775 gives `v_5(n)=2`, so a full witness must have `5` not
dividing `S`. For the rest of this note impose this five-free hypothesis
whenever using `ord_S(10)` or separating the divisor. Since `S` is odd
and `S=3 mod7`, the integers `25,S,7^(L-2)` are pairwise coprime.
Consequently (1) is equivalent on this domain to

```
9S | F and v_7(F)>=L-2.                         (2)
```

The nine has not been cancelled modulo S. In particular (2) retains its
meaning when `3|S`. The [early-rejection proof](../early-rejection/PROOF.md)
and [whole-length proof](../whole-length/PROOF.md), section 1, explain
this distinction independently.

For completeness, the unit order and actual-position argument can be
checked directly. The powers of ten modulo seven have order six, and

```
10^6=1+7*c_1, c_1=142857=1 mod7.
```

Binomial expansion shows inductively that

```
10^T_j=1+7^j*c_j, c_j=1 mod7,                   (3)
ord_(7^j)(10)=T_j.
```

Indeed, replacing an element `1+7^j*c_j` by its seventh power raises
the valuation by exactly one and leaves the leading coefficient unchanged
modulo seven. Raising such an element to an exponent coprime to seven
preserves its valuation. Every exponent yielding one must first be a
multiple of six. These facts prove the asserted exact order, not just
an upper bound.

The order is the entire size of the unit group modulo `7^j`. The unit
`(7*10^L-25)*18^(-1)` therefore has exactly one exponent representative
`r_j` in `[0,T_j)`. Modulo seven, its exponent satisfies
`10^r_j=-1`, hence `r_j=3 mod6`.

For all integers `L>=5`, `T_(L-2)>L`: at L=5 the period is 294;
increasing L by one multiplies this period by seven, preserving the
strict inequality. Thus `K<=L-2`. If an actual i has valuation at least K,
then `i=r_K mod T_K`. Both i and `r_K` lie in `[0,T_K)`, so

```
i=r_K, 3<=r_K<L.                               (4)
```

Every possible full witness has valuation at least `L-2>=K`, and is
therefore covered by (4). No full witness is discarded by examining only
this actual representative. This reduction alone does not reject it.

## 2. Exact sufficiency of the proposed quadratic bound

Suppose the following additional statement could be proved:

> For every odd `L>10000000`, if `5` does not divide S,
> `3<=r_K(L)<L`, and `9S|F(L,r_K(L))`, then
> `v_7(F(L,r_K(L)))<=100000*K(L)^2`.

This would settle the `{5,7}` subclass together with the inherited
consecutive exclusion through 10,000,000. Here is an exact proof of the
cutoff comparison, without a floating-point logarithm.

First,

```
T_8=4941258 < 10000000 < T_9=34588806.
```

For `10000000<L<T_9`, K is exactly nine. Since L is odd, the least
possible L is 10,000,001, and

```
100000*9^2=8100000 < 9999999 <= L-2.             (5)
```

For `K>=10`, minimality of K gives `T_(K-1)<=L`; that period is even,
so oddness improves this to

```
L>=6*7^(K-2)+1.
```

Let `M_K=6*7^(K-2)-1-100000*K^2`. At K=10,

```
100000*10^2=10000000 < 34588805=6*7^8-1,
M_10=24588805>0.
```

For every integer `K>=10`, direct algebra gives

```
M_(K+1)=7*M_K+6+100000*(6K^2-2K-1).             (6)
```

The last polynomial is positive for K>=1: it equals
`3+2*(K-1)*(3K+2)`. Hence positivity of `M_10` propagates to every
larger K. Equations (5) and (6) prove

```
100000*K(L)^2 < L-2 for every odd L>10000000.    (7)
```

A full witness would satisfy (2) and (4), so the proposed bound and
(7) would contradict its required valuation. The finite certificate
then covers all earlier lengths. No finite interval remains between
that certificate and the conditional argument. This is a proof of
**sufficiency**, not a proof of the proposed estimate. It would not by
itself prove broad (E), whose strict bound is K rather than `100000K^2`.
It would not settle other digit sets in the wider digit-1 conjecture.

## 3. The lift digits and their exact indexing

Reducing a depth-`j+1` exponent modulo `T_j` gives the depth-j exponent.
Thus for each `j>=1` there is a unique digit `a_j` in `{0,...,6}` with

```
r_(j+1)=r_j+a_j*T_j.                            (8)
```

Write `D_j=F(L,r_j)/7^j`, an integer, possibly negative if `r_j` is
no longer an actual position. Using (3) in the defining congruence at
the next depth gives

```
0 = D_j-18*10^r_j*a_j*c_j mod7.
```

Since `r_j=3 mod6`, `18*10^r_j=3 mod7`, and `c_j=1 mod7`. Therefore
the lift formula simplifies to

```
a_j = 5*D_j mod7, with the representative in {0,...,6}.   (9)
```

This can be checked without constructing F: compute `F mod7^(j+1)`,
which is a multiple of `7^j`, divide that residue by `7^j`, multiply
by five, and reduce modulo seven. Equivalently one can test all seven
possible lifts of (8); the order proof makes precisely one successful.

Now suppose `r_K` is actual. For all `j>=K`, `T_j>L`, so any nonzero
`a_j` sends the next representative above L. Formula (8) shows that
representatives never decrease; no subsequent lift can restore an actual
position. Until the first nonzero digit, all representatives equal `r_K`.
If that first nonzero digit is `a_t`, then

```
v_7(F(L,r_K))=t,
a_K=...=a_(t-1)=0, a_t!=0.                     (10)
```

In particular there are `t-K` zero digits, not `t-K+1`. The first
nonzero digit exists because actual `F>0`. For a full-sum-compatible
actual representative, the full witness criterion is exactly

```
a_K=a_(K+1)=...=a_(L-3)=0.                      (11)
```

There are `L-2-K` digits in (11); an empty range has its usual vacuous
meaning. If the first nonzero digit is `a_(L-2)`, the valuation is
`L-2`, which still meets the witness threshold. Exclusion therefore
requires a nonzero digit at some index at most `L-3`.

For the proposed benchmark put `B=100000*K^2`. The estimate `t<=B`
is equivalent to a nonzero digit at an index in `[K,B]`, **including B**.
In the target length range (7) gives the integer inequality `B<=L-3`.
This checks both endpoints of the required escape argument.

The inherited five-free control `(L,i)=(69489,40323)` has `K=6`, exact
valuation 11, five consecutive zero digits `a_6,...,a_10`, and `a_11=4`.
It fails the digit-sum test: `F mod(9S)=2218743`. This is a positive
control for the lift arithmetic, not a counterexample to (E) or to the
quadratic bound. Its compact next-depth certificate is
`F mod7^12=9886633715=5*7^11`, consistent with (9).
See [the inherited control record](../high-depth/COMPUTATION.md).

## 4. A strengthened, sharp order-stabilization inequality

Let `d=ord_S(10)` and `e=v_7(d)`. The inherited result is `e<=K-1`.
The same method gives the stronger explicit inequality

```
e>=1  ==>  L>=12*7^(e-1)+1=2*T_e+1.             (12)
```

To prove it, factor S into odd prime powers. The order d is the least
common multiple of their orders. Because `7` does not divide S, some
prime `p|S` must satisfy `7^e | p-1`. Write `p=1+c*7^e`. The integer
c is positive and even. The possibility c=2 would give
`p=2*7^e+1=0 mod3`, with p>3, impossible for a prime. Thus c>=4 and

```
p>=4*7^e+1.
```

Also `S/p` is positive, odd, and `3 mod7`, so `S/p>=3`. Consequently

```
7L-4=S>=3p>=12*7^e+3,
L>=12*7^(e-1)+1,
```

as asserted. This argument uses only ordinary prime factorization,
Euler's theorem, and exact congruences. No factorization of a varying S
has to be computed to apply the inequality.

The inequality is sharp as a general statement: the exact controls

```
(L,S,d,e,K)=(13,87,28,1,2), (85,591,98,2,3)
```

satisfy equality. Their orders can be checked by direct modular powering
and rejection of each order divided by its distinct prime factors.
They also show that the integral bound `e<=K-1` cannot be uniformly
replaced by `e<=K-2` on this full domain. They are order controls, not
sum-compatible depth-K positions.

For K>=2, (12) does imply the more precise band statement

```
L<=2*T_(K-1)  ==>  e<=K-2.                      (13)
```

If `e>=K-1`, (12) would instead force `L>=2*T_(K-1)+1`.
Thus the seven-part of the sum order stabilizes even earlier in the
lower part of a K band. This sharpens the diagnosis of the CRT route;
it does not supply a new position or whole-length exclusion.

To see the obstruction explicitly, when full-sum positions exist they
are one class `s mod d`. This follows from
`n=7R_L-2-2*10^i`, reducing modulo S and inverting only two; alternatively
subtract two F values and divide the integer divisibility by nine before
cancelling a unit. The full-sum and depth-j classes are simultaneously
solvable in an **unbounded integer exponent** exactly when

```
s=r_j mod gcd(d,T_j),
gcd(d,T_j)=gcd(d,6)*7^min(e,j-1).                (14)
```

This gcd is constant for every `j>=e+1`, hence for every `j>=K`.
Every subsequent lift in (8) preserves congruence modulo the stabilized
gcd. Thus if actual `r_K` passes the full sum, the unbounded exponent
system is compatible at every later depth. In the subdomain (13),
stabilization has already occurred by depth `K-1`.

This is a **proved obstruction to a later incompatibility argument using
only (14)**. It is not a general impossibility theorem for using the
digit sum. A common exponent can be outside the actual range; proving
that this necessarily happens soon enough is exactly the missing extra
bounded-position condition. A stronger order bound alone does not
force it, because constant gcd compatibility persists indefinitely.

## 5. The full-sum cofactor and the limit of bare size

If `r_K` is actual and passes the full sum, the five-free hypothesis
and `25|n` give the positive integer

```
C=F(L,r_K)/(225S),   v_7(C)=v_7(F(L,r_K))=t.     (15)
```

Since `225S=3 mod7`, equations (9) and (15) show, for each j during
the constant-representative portion with `j<=t`,

```
a_j = C/7^j mod7.                              (16)
```

Thus the first nonzero lift digit is exactly the first nonzero base-seven
digit of the cofactor C after its trailing zero digits. The digit-sum
divisor contributes a seven-adic unit, so extracting it does not shorten
the zero run. Equation (16) identifies the arithmetic quantity that would
need new control; it does not imply that its trailing-zero count is small.

The strongest bound from positive integer size alone is

```
7^t<=C=F/(225S)<7*10^L/(225S).                  (17)
```

Its failure at the full-witness threshold can be made exact, rather than
described only by the leading coefficient `log(10)/log(7)>1`. For every
position in the actual interval,

```
F(L,i)>=A_L=52*10^(L-1)-25,
B_L=225*(7L-4)*7^(L-2).
```

At L=12,

```
A_12=5199999999975,
B_12=5084554482000,
A_12-B_12=115445517975>0.
```

Moreover `A_(L+1)=10*A_L+225`, and for all L>=3,

```
B_(L+1)/B_L=7*(7L+3)/(7L-4)<10,
```

since the last inequality is exactly `21L>61`. Induction proves

```
F(L,i)>225S*7^(L-2) for every L>=12 and 3<=i<L.  (18)
```

Hence the numerical upper bound on `7^t` furnished by (17) exceeds
`7^(L-2)` everywhere in the remaining research domain, even if the exact
F is used. Its real-valued logarithm and its floor both permit
`t=L-2`. This proves failure of **this size-only inequality** to exclude
the threshold; it does not prove that the divisor in (18) ever divides F.
Any use of divisibility, congruences, or special arithmetic of C beyond
positive size is a further input and is not ruled out by this observation.

## 6. Precise unresolved obligations

| Route | Strongest justified statement | Required next step | First missing input and a sufficient addition |
| --- | --- | --- | --- |
| Actual representative and lift digits | (4), (9), and the exact equivalences (10)--(11) | Force a nonzero digit by `B=100000K^2`, or at least by `L-3` | No bound on the trailing zeros of the actual cofactor (15) is proved. A uniform effective bound `v_7(C)<=B` on this full-sum domain would suffice. |
| Unbounded exponent CRT | (12)--(14), including earlier stabilization in (13) | Show the compatible exponent cannot stay in `[3,L)` through the required depth | Gcd compatibility supplies no bounded representative estimate. A theorem forcing its least nonnegative common exponent outside that interval by a specified depth would suffice. Later incompatibility from this unchanged gcd system is disproved as a mechanism by (14). |
| Bare size after extracting the digit sum | (17), with exact obstruction (18) for all L>=12 | Improve the permitted valuation from an upper bound above `L-2` to at most `L-3` | The allowed cofactor size is exponentially too large. An arithmetic restriction on C strong enough to prevent its divisibility by `7^(L-2)` would suffice; simply extracting 225S does not provide one. |

The inherited [finite-pairs theorem](../FINITE_PAIRS.md) and
[qualitative bound](../effective/QUALITATIVE.md) are not newly reapplied
here. Their ineffective finiteness and `o(L)` conclusions give neither
the proposed quadratic bound nor an executable global starting length.
A numerical effective cutoff would still leave every length between the
existing consecutive certificate and that cutoff to discharge.

This investigation proves no counterexample to broad (E), no counterexample
to the proposed quadratic estimate, and no full witness. The inherited
depth-44 example is only a counterexample to the **unconditional** bound
`v_7(F)<K`: its digit-sum premise fails. The sharp order controls and
zero-lift control above likewise have their individually stated scopes.
No new all-position or whole-length exclusion follows from this note.
