# Uniformity audit of the polynomial-root route

This note proves a uniform bound on the **derivative valuation**, hence
removes the singular-Hensel issue for possible full witnesses. It does
not prove the proposed bound on `v7(F)`. The remaining independent-root
estimate retains its actual degree and height. A quantified obstruction
below concerns a specified degree-and-coefficient-span estimate, even
after optimizing all ten published Bugeaud–Laurent table entries.

The domain throughout is odd `L>=5`, `3<=i<L`,
`F=7*10^L-18*10^i-25>0`, and `t=v7(F)`. A full witness requires
`t>=L-2` and `9*(7L-4)|F`, with `5` not dividing `7L-4`.
Most arguments here use only the valuation requirement; no digit-sum
condition is silently dropped from a claimed equivalence.

## 1. Integral polynomial, variable parameters, and height

For any reduced `0<a<b` with **`b<=L`**, write

```
L=bq+r,  0<=r<b,  i=aq+s,  delta=bi-aL=bs-ar,
m=min(0,s),  w=max(0,r,s)-m,  x=10^q,
Q(X)=7*10^(r-m)*X^b-18*10^(s-m)*X^a-25*10^(-m).
```

Then `q>=1`, every coefficient is integral, and direct substitution gives

```
Q(x)=10^(-m)*F,
x*Q'(x)=10^(-m)*(7b*10^L-18a*10^i)
       =10^(-m)*(aF+7(b-a)*10^L+25a).               (1)
```

No constancy of `a,b,s,delta` as L varies has been assumed. The span
satisfies

```
|delta|/b = L*|i/L-a/b| <= w <= |delta|/b+b-1.       (2)
```

For the lower bound, `ar/b` lies between 0 and r, within the interval
spanned by `0,r,s`. For the upper bound, if `s<0` then
`w=r-s=(b-a)r/b+|delta|/b`; if `0<=s<=r`, `w=r`; and if `s>r`,
`w=s=ar/b+delta/b`. Each gives (2). Also

```
0<=w<=L-1.                                         (3)
```

Indeed when `s>=0`, `r<=L-1` and `s=i-aq<=L-2`; when `s<0`,
`w=r-s=L-i-(b-a)q<=L-4`.

For any algebraic root alpha of Q with actual global degree
`D=[Q(alpha):Q]`, its primitive integral minimal polynomial divides Q
over the integers. The Mahler measure is multiplicative; the integral
cofactor has measure at least one, even if Q has content. Also
`M(Q)<=sum |coefficient|<=50*10^w`. One elementary justification for the
first inequality is the identity
`log M(Q)=(1/2pi)*integral log|Q(exp(i theta))| d theta`, obtained
factor by factor from the power series for `log(1-z)` and continuity;
the triangle inequality then bounds the integrand by the logarithm of
the coefficient sum. Thus reducibility and content are both allowed:

```
1<=D<=b,  D*h(alpha)<=log(50*10^w)<(w+2)*log10.
H:=w+2 <= L+1.                                     (4)
```

`D<=b` is an upper bound, not a proof that the selected root has degree b.
Factoring Q or proving a better root-specific height can improve (4),
but such an improvement must be established for the chosen root.
The content is explicit: it is 2 if `s<0`, and
`5^min(2,r,s)` if `s>=0`. In the first case the middle coefficient is
`-18`, the others are divisible by 2, and the leading coefficient has
no factor 3; in the second case the constant is `-25` and the common
five-part is exactly the stated minimum. Thus content is at most 25.
Dividing it out improves the logarithmic coefficient bound by at most
`log25`; it does not remove growing degree or coefficient span.

If `b>L`, then `q=0,r=L,s=i,w=L`; this positive-exponent application
does not apply. Such a choice is not used to exclude any pair here.
There is no omitted witness domain: every admissible pair permits, for
example, `a/b=1/2` with `b<=L`. What is missing is a sufficiently strong
estimate for some allowed centre at each pair, not the existence of a
parameterization. Denominators larger than the actual length cannot be
inserted into the proof while pretending `q>=1`.

## 2. The derivative, including every case with seven dividing a

Because ten and x are seven-adic units, (1) gives the exact finite integer

```
d:=v7(Q'(x))=v7(7b*10^L-18a*10^i).                 (5)
```

The expression is positive: `7b*10^(L-i)>=70b>18a`. Since `gcd(a,b)=1`,
comparison of the two summand valuations proves

```
7 does not divide a:  d=0;
v7(a)>=2:             d=1;
a=7c, 7 does not divide c:
                      d=1+v7(b*10^(L-i)-18c).      (6)
```

The last line permits cancellation. At positive t, its bracket modulo
seven is equivalently `b*10^L+25c`, up to a unit. Odd L alone does not
prevent this bracket from vanishing. For example:

| `(L,i,a,b)` | `q` | `t` | `d` |
| --- | ---: | ---: | ---: |
| `(11,3,7,9)` | 1 | 1 | 2 |
| `(11,9,7,9)` | 1 | 1 | 3 |
| `(15,3,14,15)` | 1 | 2 | 2 |

These are counterexamples only to transferring PR #19's derivative-one
lemma to all reduced ratios. They do not refute broad (E), the quadratic
target, or the subclass. Strong Hensel requires **`t>2d`**, rather than
merely `t>=3`.

### A new uniform derivative bound

Put `K=K(L)`. For every `L>10,000,000` in the stated domain and every
reduced `0<a<b<=L`,

```
d <= B_K:=1+252*(K+1)^3.                            (7)
```

Here `K>=9` and `L<T_K=6*7^(K-1)<7^K`. Only the last case of (6)
needs proof. Put `g=L-i>=1` and `beta=18c/b`. This rational number is
a seven-adic unit, satisfies `0<beta<18/7<3`, and has height

```
h(beta)<=log(max(18c,b))<log(3L)<(K+1)*log10.
```

Suppose first that 10 and beta are multiplicatively independent. In
[Bugeaud–Laurent Corollary 1](SOURCES.md), take bases `(10,beta)`,
exponents `(g,1)`, `p=7`, global and local degrees one,
`log A1=log10`, and `log A2=(K+1)*log10`. All bases are units and both
exponents are positive. Then

```
d-1 <= C0*(K+1)*M^2,
C0=168*(log10)^2/(log7)^4 <63,
M=max(log((g/(K+1)+1)/log10)+log log7+0.4,
      10*log7, 10).
```

All branches are retained. Since `g/(K+1)+1<L`, the first is
`<log L+log(log7/log10)+0.4<2K+1`, using `log7<2`.
The second is below 20 and the third is 10. For `K>=9`, therefore,
`M<=2K+2`, proving `d<=1+63(K+1)(2K+2)^2=B_K`.
The strict coefficient bound is certified by rational logarithm
enclosures in the checker; it is not a floating-point assumption.

If 10 and beta are dependent, positivity and rational prime valuations
give `beta=10^j` for an integer j: a relation forces all prime valuations
other than those at 2 and 5 to vanish, and forces those two to agree.
The height bound gives `|j|<=K`. Moreover `beta<3<=10^g` gives `g-j>0`.
We have `g-j<=L+K<7^K`; the last inequality uses
`L<6*7^(K-1)` and `K<7^(K-1)` for `K>=9`. If six does not divide
`g-j`, the inner valuation in (6) is zero. Otherwise elementary LTE
and `v7(10^6-1)=1` give

```
d=2+v7(g-j)<=K+1<=B_K.
```

This proves (7) without a digit-sum or high-valuation hypothesis.

### Effective Hensel applicability for every possible full witness

At `K=9`,

```
2B_9=504002 < 9999999 <= L-2.
```

For `K>=10`, oddness and minimality of K give
`L-2>=6*7^(K-2)-1`. The comparison at K=10 is

```
2B_10=670826 < 34588805.
```

It persists: for `K>=10`, `(K+2)^3<7(K+1)^3`, so
`2B_(K+1)+1=3+504(K+2)^3 <7(3+504(K+1)^3)=7(2B_K+1)`.
The comparison `2B_K+1<6*7^(K-2)` consequently propagates by induction.
Thus a full witness's `t>=L-2` implies `t>2d` for **every** allowed
centre, including `7|a`.

Conrad's Theorem 4.1 now produces a root `alpha in Z_7` such that

```
Q(alpha)=0, v7(x-alpha)=t-d>d, v7(Q'(alpha))=d.       (8)
```

It is a unit because `alpha=x mod7`, and `alpha!=x` because `F>0`.
This is a uniform repair of the Hensel prerequisite. It is not a bound
of order `K^2` on t.

## 3. Strongest retained root estimate and the dependent branch

For an independent selected root, the parameters are

```
alpha1=10, alpha2=alpha, b1=q>=1, b2=1,
p=7, e=f=1, D=[Q(alpha):Q],
log A1=log10, log A2=H*log10/D,
b'=(q/H+1/D)/log10.
```

The global degree is D even though alpha lies in `Q_7`. Equation (4)
and `H>=2` verify both height floors, including `log7/D`.
Also `g=6` in the source's notation: base 10 itself has order six
modulo seven. The exact Corollary 1 substitution is

```
t <= d+C0*D^3*H
       *max(log((q/H+1/D)/log10)+log log7+0.4,
            10*log7/D,10)^2.                       (9)
```

One may improve (9) by taking the minimum with **all ten** bounds
from Theorem 4:

```
t <= d+A*c(mu,nu)*D^3*H
       *max(log((q/H+1/D)/log10)+log log7+0.4,
            mu*log7/D,nu)^2,
A=7*(log10)^2/(log7)^4=C0/24.                       (10)
```

The constants are in [SOURCES.md](SOURCES.md). This retains the actual
root degree, exponent, coefficient span, derivative loss, and every
maximum branch before any coverage envelope is considered. Any better
verified height parameter may replace H, provided both height floors
remain satisfied. Neither the displayed H nor D is held constant as L
and its chosen rational approximation vary.

If the selected root is dependent with 10, write `alpha^v=10^u` with
integers `v>0,u`. Taking the global norm and its 2-adic valuation gives
the integer `j=uD/v`. Heights give `|j|=D*h(alpha)/log10<H`.
Furthermore `zeta=alpha^D/10^j` is torsion in `Q_7`, so `zeta^6=1`.
Indeed reduction modulo seven injects on torsion: for `y in 1+7Z_7`,
the binomial expansion proves `v7(y^h-1)=v7(y-1)+v7(h)` for nonzero
integers h (negative h by inversion), ruling out nontrivial torsion.

Set `y=x/alpha`. Equation (8) puts y in `1+7Z_7`. If `Dq=j`, then
`y^(6D)=1` would force x=alpha, impossible. Applying the same LTE
identity to `y^(6D)=10^(6(Dq-j))` yields the exact formula

```
t=d+1+v7(Dq-j)-v7(D).                              (11)
```

This includes degrees divisible by seven. Discarding the subtracted
term is permissible only in an upper bound, not in the identity.
By (3)–(4), the integer j satisfies `|j|<=L`; also `Dq<=bq<=L`.
Consequently

```
0<|Dq-j|<=2L<7^(K+1),
t<=d+K+1<=B_K+K+1<=2B_K<L-2                       (12)
```

for `L>10,000,000`, contradicting a full witness. Thus in the remaining
full-witness domain **every selected Hensel root at every allowed centre
is multiplicatively independent**. This uniform branch elimination
does not prove that any of the independent estimates is small enough.

## 4. The denominator and height obstruction, with explicit thresholds

A convenient bound using only `D<=b` is

```
U=63*b^3*H*max(log((q/H+1)/log10)+log log7+0.4,20)^2,
t<=d+U.                                            (13)
```

An exclusion at an actual length must prove `d+U<L-2`, or the sharper
actual-root analogue of that comparison using (9)–(10). It is not enough
that some fixed centre will work eventually. For fixed a,b,offset s,
the height is constant and the source estimate is logarithmic squared
in q (with d separately controlled). Allowing s or b to change with L
does not preserve that constant.

### Complete parameterwise effective thresholds

The following thresholds are executable using integers and rationals;
they expose, rather than suppress, the parameter dependence. They are
conditional position exclusions above their stated start, not additional
all-length or whole-length coverage claims.

For a fixed reduced centre a/b and fixed integer `Delta>=0`, restrict
to `|delta|<=Delta` and set

```
H0=Delta/b+b+1,
R_b,Delta(k)=1+252*(k+1)^2*((k+1)+b^3*H0).
```

Equation (2) permits replacing H by H0. For `K>=9` all branches in
(9) are at most `2K+2`: its first branch is below `2K+1`, since
`q/H0+1<=L/4+1<L`, and its other branches are below 20 and equal
to 10. Together with (7), this gives `t<=R_b,Delta(K)` in the
independent-root branch of a possible witness. The dependent branch
is already excluded. Choose the first integer `k0>=10` such that

```
6*7^(k0-2)>=b,
R_b,Delta(k0)+1 < 6*7^(k0-2).                       (13a)
```

Every admissible position with `|delta|<=Delta` and
`L>=6*7^(k0-2)` is then excluded. Indeed odd L with `K>=k0`
satisfies `L-2>=6*7^(K-2)-1`. The polynomial `R(k)+1` grows by
less than a factor two at each step `k>=10`:
`(k+2)^3<2(k+1)^3` and the corresponding degree-zero and degree-two
terms obey the same bound. Its comparator grows by seven. This proves
both termination of the exact search (13a) and persistence thereafter.
The threshold depends explicitly on **b and Delta**; allowing either
to vary with L invalidates a single fixed cutoff obtained this way.
Lengths between the inherited coverage and this parameterwise start
are an undischarged finite obligation unless separately covered.

A similar complete threshold can be stated for a rational strip
`|delta|<=epsilon*L`, with fixed rational `epsilon>=0`. Choose rational
`h>epsilon/b` and rational M such that

```
M>=20,
M>=log((1/(b*h)+1)/log10)+log log7+0.4,
lambda=63*b^3*h*M^2 <1.                            (13b)
```

The logarithmic comparison must be certified, for example by the
rational-series method in the checker. Put

```
L0=max(b,10000001,ceil((b+1)/(h-epsilon/b))).
```

Then `H=hL` is valid for every `L>=L0`, `q/H<=1/(bh)`, and the
independent-root estimate is `t<=B_K+lambda*L`. Choose the first
integer `k0>=10` with

```
6*7^(k0-2)>=L0,
B_k0+2 < (1-lambda)*6*7^(k0-2).                    (13c)
```

For the same polynomial-versus-exponential reason, this exact search
terminates and the inequality persists, excluding the stated strip
for `L>=6*7^(k0-2)`. This is an explicit dependence on
`b,epsilon,h,M,lambda`, not an unspecified eventual threshold.
The choice (13b) is substantive: this particular envelope needs
`25200*b^2*epsilon<1`, since `M>=20` and `h>epsilon/b`.
Failure of that necessary comparison cannot be repaired just by
raising the length threshold. Sharper (9)–(10) parameters may help,
but must be proved. A cover would have to cover each actual admissible
pair by strips whose own (13c), or sharper certified thresholds, have
already been reached.

To quantify this even after numerical improvements, consider the class
of degree-b/coefficient-span bounds which replace D by b and keep
`H=w+2`, using any of (9)–(10). A safe such envelope is obtained by
maximizing the actual-D expression over `1<=D<=b`; consequently it is
at least its value at `D=b`. Even granting an optimal treatment of
the logarithmic branch, every member has

```
U_table >= A*b^3*H*min_(mu,nu)(c(mu,nu)*nu^2)
        =465*A*b^3*H > 800*b^3*H.                   (14)
```

The minimum 465 occurs at `(mu,nu,c)=(15,5,18.6)`.
The elementary bounds `log10>2`, `log7<2` give `A>7/4`, hence
`465*A>3255/4>800`. Corollary 1 has the still larger corresponding
product `24*10^2=2400`. Adding the nonnegative d only worsens this
necessary comparison. Therefore use of **any** such envelope requires

```
b^3 < L/1600,
|i/L-a/b| < 1/(800*b^3).                            (15)
```

Both conclusions follow from (2), `H>=2`, and `U_table<L-2<L`.
They hold even if H is enlarged. They are restrictions on this chosen
envelope, not lower bounds on the true valuation or on the actual
degree of a proper factor of Q.

The exact-centre choice makes the trade-off particularly clear. Put
`h=gcd(L,i)`, `a=i/h`, `b=L/h`. Then `q=h`, `r=s=delta=w=0`,
`Q=7X^b-18X^a-25`, and `H=2`. Equation (14) already gives

```
U_table>1600*(L/h)^3,
U_table<L-2  ==>  h^3>1600*L^2.                    (16)
```

Thus when `gcd(L,i)=1`, even zero offset leaves an envelope exceeding
`1600L^3`. A small selected factor or a special height relation could
change this; reduced ratio and zero offset alone do not.

### Actual rational pairs missed by every envelope in this class

The inherited family in [proportional/COVERAGE.md](../proportional/COVERAGE.md)
has

```
xi=sqrt(2)-1, M=16031730,
L=1+M*z, z>=1,
i=39+42*((isqrt(2*L*L)-L-18)//42).
```

It has `|i/L-xi|<=21/L`, consists of actual odd integer lengths and
positions, and passes the listed elementary congruence filters. Its
ratios lie between `0.414` and `0.415`: the exact square comparisons
`(14142/10000)^2<2<(14143/10000)^2` put xi between `.4142` and
`.4143`, while `21/L<21/10000000=.0000021`. In particular they avoid
both later `5/12` and `7/12` strips and both exact lines at `5/12`.
It has **not** been proved to satisfy either `i=r_K(L)` or `9S|F`.
Those missing conditions are essential, not cosmetic qualifications.

For every rational `0<a/b<1`, the nonzero integer
`(a+b)^2-2b^2` proves

```
|xi-a/b|>1/(4b^2).                                 (17)
```

If a bound in the class (14) excluded one of these pairs, (15) would
give `L>1600b^3>168b^2`. Hence `21/L<1/(8b^2)`, and (17) yields

```
|i/L-a/b| > 1/(8b^2) > 1/(800b^3),
```

contradicting (15). Thus optimizing all ten published constants does
not make this specified family of degree-and-span bounds cover all
these rational pairs at their actual lengths. This strengthens the
inherited obstruction for coefficient 63 and maximum floor 10.

This is a proved method-specific obstruction. It is not an uncovered
irrational point offered as a witness, a proof that the actual degree
equals b, or an impossibility theorem for digit-sum-compatible
representatives, proper factors, better height bounds, or different
analytic methods. Establishing a bound on that smaller arithmetic
domain remains a possible way around it.

## 5. Ineffective finiteness and the exact remaining analytic obligation

The original Evertse statement was rechecked; see [SOURCES.md](SOURCES.md).
The inherited tuple `x=(A,-B,-1,-C)`, where

```
A=7*10^L/25, B=18*10^i/25, C=F/25, A=B+1+C,
S0={2,3,5,7}, height=A,
```

is primitive, has no proper zero subsum, and has outside-prime product
at most `C/7^t<A/7^t`. For any fixed `0<epsilon<log10/log7`, if
`t>=epsilon*L`, choose

```
d_E=1-epsilon*log7/log10 in (0,1), c=1.
```

Since `A<10^L`, we have `A^(1-d_E)<7^(epsilon*L)<=7^t`.
The outside-prime product is therefore below `A^d_E`. Evertse gives
only finitely many such pairs. This proves `t=o(L)` uniformly over
`3<=i<L`, in the sense that each fixed positive epsilon has only
finitely many exceptions to `t<epsilon L`. Large epsilon follows from
any smaller epsilon in the displayed domain.

This yields no computable starting length, no `O(K^2)` estimate, and
no executable terminal search. In particular an abstract sublinear
bound cannot be substituted for the proposed quadratic-logarithmic
bound. Taking `epsilon=1/2` does not tell us where the finite exceptions
are. The inherited finite-pairs conclusion remains correct and
ineffective; no new whole-length coverage follows here.

The analytic route would become sufficient with a theorem saying that
every surviving digit-sum-compatible actual representative admits some
reduced `0<a<b<=L` whose **actual root** parameters make (9), or one
of (10), less than `L-2`, with a common effective threshold and every
earlier length discharged. A direct uniform bound on those degrees and
heights strong enough for that comparison would also suffice. The
present argument supplies the uniform derivative bound, the Hensel
root, and the dependent-root exclusion. It supplies neither that
degree/height theorem nor a finite cover meeting the actual thresholds.

## 6. Route-by-route boundary of the result

| Route | Strongest statement proved here | Required next comparison | First missing step and why the available theorem does not supply it | Additional result sufficient for this route |
| --- | --- | --- | --- | --- |
| Singular derivative and Hensel | `d<=B_K`, `2B_K<L-2`; every possible full witness lifts at every `b<=L` | Bound the selected root distance below `L-2-d` | No unresolved Hensel hypothesis remains in this domain; Hensel gives a distance identity, not a useful upper bound | The independent-root estimate in the next row must be made small enough |
| Multiplicatively dependent root | Exact (11), including `-v7(D)`; uniform contradiction (12) | None within this branch | This branch is resolved; it cannot establish that an independent root is impossible | No additional result needed for this branch |
| Independent polynomial root | Actual-parameter bounds (9)–(10), plus effective fixed-offset and strip thresholds (13a)–(13c) | At each remaining pair, some allowed representation must give upper bound `<L-2` (or `<=100000K^2`) | D, height and offset are uncontrolled across varying centres; the theorem explicitly multiplies them and does not use `9S|F` | A uniform root-degree/height theorem or arithmetic restriction covering every possible full witness and meeting the comparison |
| Optimizing rational-strip envelopes | Even all ten tabulated constants fail the rational family in (17), for the specified degree-b/span envelope | A cover of the actual digit-sum-compatible representatives at their actual lengths | Rational density does not control widths or thresholds; the exhibited rational pairs are not proved to satisfy those arithmetic premises | A smaller proved arithmetic domain, root-specific factors/heights, or a different estimate, together with verified coverage and thresholds |
| Evertse finiteness / `o(L)` | Only finitely many pairs have `t>=epsilon L` for each fixed positive epsilon | A numerical maximum exceptional length, then discharge every remaining finite case | The quoted corollary gives finiteness without an effective height bound | An effective version applicable to these tuples with a usable bound and completed finite remainder |

The method-specific envelope obstruction is a theorem about that
envelope. The absence of a sufficient independent-root estimate in this
investigation is not a general impossibility theorem.
