# An effective bound for the pair eliminant

This note proves the analytic part of the adjacent-pair argument. It does
not infer eliminant divisibility from one isolated witness. Throughout,
`a=31+6u`, `u>=0`, `d=3^(a-2)=7w+5`, `x=10^w`, and
`k in {42,91,140,189,238,287,336,385,434}`. Put

```
H(X)=7*10^4687*X^6561
     -7*10^(10k+7)*X^(14k+9)+25*10^(10k)*X^(14k)-25.
```

The position elimination and positivity of `H(x)` are proved in the
pair proof. In particular `H(x)` is nonzero. All logarithms of positive
real numbers below are natural; `v7(7)=1`.

## 1. The derivative, Hensel root, and exact valuation loss

Since `d=3^(29+6u)=33 mod42`, division of `d-5` by seven gives
`w=4 mod6`. The exponent of ten modulo 343 is 294: its order modulo
seven is six and `v7(10^6-1)=1`. Thus `H'(10^w) mod343` depends only
on `w mod294`. Independently evaluating all **49** residues
`4,10,...,292`, for all nine k, gives in every one of the **441** cases

```
H'(10^w)=49 mod343, hence v7(H'(x))=2.                 (1)
```

The complete table and its unfiltered construction are in
`logarithm_checks.py` and its receipt. This is a finite universal
verification of (1), not a sampling of family exponents.

Let `t=v7(H(x))`. If `t<=4`, the proposed pair is already impossible
because its smaller threshold `L-2` exceeds four. If `t>=5`, then
`t>2*v7(H'(x))`, the strict strong-Hensel condition. There is a root
`alpha in Z_7` with `q=v7(alpha-x)>2`. Here is also a direct reduction
to simple Hensel, keeping the exact precision: the polynomial

```
G(Y)=H(x+7^3*Y)/7^5
```

has integral coefficients, constant term `H(x)/7^5`, linear coefficient
`H'(x)/7^2`, and every coefficient of degree at least two divisible by
seven. These assertions follow by the integral binomial expansion; the
higher coefficients contain `7^(3j-5)` for `j>=2`. Thus G is an affine
linear polynomial with unit slope modulo seven and has a unique simple
root there. Its Hensel lift gives alpha. This agrees with the strong
form in [Conrad, Theorem 4.1, p.6](https://kconrad.math.uconn.edu/blurbs/gradnumthy/hensel.pdf).

Writing `y=alpha-x`, the integral Taylor expansion is
`0=H(x)+H'(x)y+y^2 R`, `R in Z_7`. The linear term has valuation
`2+q`, whereas `v7(y^2 R)>=2q>2+q`. Therefore cancellation forces

```
t=2+q=2+v7(x-alpha).                                 (2)
```

Also `v7(H'(alpha))=2`, since `H'(alpha)-H'(x)` has valuation at least
q. Positivity of H(x) ensures alpha differs from x. Since q>=3 and x
is a seven-adic unit, alpha is a nonzero seven-adic unit. The elementary
factorization of sixth powers has a unit cofactor modulo seven, giving

```
v7(10^(6w)-alpha^6)=v7(x-alpha)=q.                    (3)
```

In particular taking sixth powers loses no valuation.

## 2. Uniform degree and absolute logarithmic height

All three nonconstant degrees are distinct, with
`14k+9<=6085<6561`. Hence H has degree exactly 6561 and any root has
degree at most 6561. Its coefficient norm is exactly

```
N_k=7*10^4687+7*10^(10k+7)+25*10^(10k)+25 <10^4688.   (4)
```

The last inequality is checked as an exact integer inequality for all
nine k. If the primitive integer minimal polynomial of alpha is m,
Gauss's lemma and multiplicativity of Mahler measure imply
`M(m)<=M(H)`: the integer cofactor and integer content have measure at
least one. Jensen's formula, or the usual coefficient-norm estimate,
gives `M(H)<=||H||_1=N_k`. Thus the **absolute logarithmic** height is

```
h(alpha)=log M(m)/deg(m) <= log N_k.
```

No monicity or irreducibility of H is assumed. The proposed height
parameters are valid, because `log10<7/3` gives

```
h(10^6)=6 log10<14<15,
h(alpha^6)=6h(alpha)<6*4688*(7/3)=65632<70000.         (5)
```

The strict bound `log10<7/3` follows from the positive exponential
series: `sum_{j=0}^{10}(7/3)^j/j! >10`, checked using rational
arithmetic. The other elementary inequalities used below are
`1<log7<2`, `log3<2`, and `log(log7)<1`; for example `e<3<7` and
`e^2>7` prove the first pair. These can all be justified by rational
upper or lower bounds for the exponential series.

## 3. Multiplicatively independent case

Suppose 10 and alpha are multiplicatively independent. Then so are
`beta1=10^6` and `beta2=alpha^6`. Both lie in `1+7 Z_7`. Apply
[Bugeaud--Laurent, Corollary 2, printed p.5](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf)
with exponents `(b1,b2)=(w,1)`, prime 7, and local field `Q_7`.
Its local residue degree is one, so its actual parameter is
`D=[Q(alpha^6):Q]`, with `1<=D<=6561`. Set `log A1=15` and
`log A2=70000`. Equation (5) verifies the height conditions; the
remaining floors `log7/D` are less than two. The source's definitions
and explicit inequality become

```
b'=w/(70000D)+1/(15D),
M=max(log(b')+log(log7)+2/5, 10log7/D, 10),
q <= 208*D^4*M^2*15*70000.                           (6)
```

This uses the source's explicit 208 upper bound, not its separate
asymptotic theorem. The paper has no additional exponent threshold
in this corollary. Keeping the actual D until each maximum entry has
been bounded avoids any unjustified monotonic substitution.

Here w is a positive integer and `b'<w`. Also `w<3^(a-2)`, so

```
log(b')+log(log7)+2/5 < log(w)+2 < 2a-2,
10log7/D<20,                       10<20.
```

Consequently `M<2(a+20)` for every a in this family. Equations (2)
and (6) give

```
t < 2+C*(a+20)^2 <= (C+2)*(a+20)^2,
C=832*6561^4*15*70000
 =1618798436980968297600000,
C+2<10^30.                                           (7)
```

Independence also guarantees the difference in (3) is nonzero.

## 4. Multiplicatively dependent case

Suppose instead that `alpha^m*10^n=1` for integers `(m,n)!=(0,0)`.
Necessarily `m!=0`. Work in `K=Q(alpha)` at any place above two, with
its integer-normalized valuation v, and write `e=v(2)>0`, `r=v(alpha)`.
The ramification index satisfies `e<=[K:Q]<=6561`.

The four coefficient valuations of H are respectively
`4687e`, `(10k+7)e`, `10ke`, and zero. If r>=0, the constant term
is the unique term of minimal valuation, contradicting H(alpha)=0.
If `r<-4687e`, the leading term is uniquely minimal: for every other
nonzero coefficient of degree j<6561 its valuation is at least zero,
and

```
4687e+(6561-j)r <0.
```

Again cancellation is impossible. This proves the proposed bounds

```
-4687e<=r<0,                    1<=e<=6561.           (8)
```

Applying v to the dependence relation gives `mr+ne=0`. Therefore
`zeta=alpha^e/10^r` satisfies `zeta^m=1`. This element belongs to
`Q_7`, whose roots of unity have order dividing six; hence

```
alpha^(6e)=10^(6r).                                 (9)
```

For completeness, reduction modulo seven injects the torsion subgroup
of `Z_7^*` into `F_7^*`: if a principal unit z differs from one, the
binomial identity gives `v7(z^j-1)=v7(z-1)+v7(j)<infinity` for every
positive j, so z cannot be torsion. This proves the needed torsion
claim without assuming the root is rational or real.

Since w>0 and r<0, `ew-r>0`; therefore
`10^(6ew)-10^(6r)` is nonzero. Using (9) and the same binomial
lifting identity gives

```
v7(x^(6e)-alpha^(6e))=1+v7(ew-r),
q+v7(e)=1+v7(ew-r),
q<=1+v7(ew-r).                                      (10)
```

In the second equality `x/alpha in1+7Z_7`, by q>=3. Thus this case
also gives the requested inequality, with the stronger exact loss
`v7(e)` displayed. Nonvanishing is proved before taking any valuation.

From (8), `0<ew-r<=6561(w+4687)<=6561*4688*w<10^8*w`.
Since `log7>1`, `log10<3` and `logw<2(a-2)`, (10) yields

```
t=2+q <=3+v7(ew-r) <27+2a <10^30*(a+20)^2.          (11)
```

The final inequality holds already for every integer a>=0. No
multiplicative-independence assumption was used in this case.

## 5. Exact crossover and finite remainder

Combining t<=4 with (7) and (11) proves the deliberately loose bound

```
v7(H(10^w)) <10^30*(a+20)^2.                         (12)
```

It is strictly below `L-2=(3^a-10)/7` for **every integer a>=100**.
The initial integer comparison is

```
3^100=515377520732011331036461129765621272702107522001
 >7*10^30*120^2+10
 =100800000000000000000000000000000010.
```

To propagate it, set `R_a=7*10^30*(a+20)^2+10`. Then

```
3R_a-R_(a+1)=7*10^30*(2a^2+78a+759)+20>0
```

for a>=0. Induction proves `3^a>R_a` for every integer a>=100.
This establishes the strict comparison with the **smaller** length's
witness threshold. It does not compare against `L'-2`.

The admissible starts below 100 are exactly
`31,37,43,49,55,61,67,73,79,85,91,97`. The inherited individual
certificates exclude each starting member; in particular a=97 is
excluded even though its partner a+6=103 lies above the cutoff. No
assumption about a failing exterior neighbour is needed.

## Source and reproduction record

The logarithm reviewer independently reopened the primary
Bugeaud--Laurent PDF on 27 November 2026, inspected its definitions on
printed pp.2--4 and Corollary 2 on p.5, and downloaded the exact bytes:
**271382 bytes**, SHA-256
`554bb384df62538fa11fcf6ab74976e772156c9d3ca4022e2128d48e3632128d`.
This matches, but is freshly verified independently of, the inherited
source record. The PDF itself is not added to the repository.
Conrad's primary text was also reopened; the proof above supplies its
own simple-Hensel reduction and exact Taylor valuation calculation.

`logarithm_checks.py` independently checks all derivative classes,
the coefficient-norm inequalities, rational exponential lower bounds,
the exact constant and crossover arithmetic, and nine finite Hensel
controls with t>=5. These controls are synthetic points in the
permitted w residue class, not claimed actual family members. Explicit
exceptions preserve every check under optimized Python. From the root:

```sh
pp=research/a398769/five-seven/power-three-pair
python3 "$pp/logarithm_checks.py" --check "$pp/logarithm-checks.json"
python3 -O "$pp/logarithm_checks.py" --check "$pp/logarithm-checks.json"
```

These are ordinary mathematical arguments and exact finite arithmetic.
No Lean verification was performed for this theorem.
