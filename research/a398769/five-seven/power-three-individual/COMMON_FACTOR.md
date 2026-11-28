# Common-factor exclusion for one actual position

**Theorem.** For every `a=31+6u`, `u>=0`, a full witness in the
`S=3^a` family must have

```
q^4>L, equivalently gcd(L,s_a)^4<L^3,
q=L/gcd(L,s_a), L=(3^a+4)/7.
```

This excludes every specified position with `q^4<=L` at every
admissible exponent, independently of both neighbouring lengths. It does
not assert that the unique actual position always satisfies `q^4<=L`.
The proposed constant **312000** and the cutoff **a=100** are valid.

## Exact predicate and depth two

The original decimal word satisfies

```
n=7(1+10+...+10^(L-1))-2-2*10^s,
P=25*7^(L-2), F=9n=7*10^L-18*10^s-25,
PS|n iff 225*S*7^(L-2)|F.
```

The inherited [ternary proof](../power-three/INDIVIDUAL.md) gives the
unique odd representative `s_a` of `kappa mod d`, `d=3^(a-2)`, in
`[0,2d)`. A full witness needs `3<=s_a<L` and **9S|F at this same s**.
For an actual candidate `v5(F)=2`, so it is a full witness exactly when
`t=v7(F)>=L-2`; equality already qualifies.

Here `L=1 mod6`: `3^a=3 mod42`, and `7L=3^a+4=7 mod42`.
Modulo 49, the term `7*10^L` is therefore 21. Hence

```
49|F iff 18*10^s=-4 mod49 iff 10^s=27 mod49
     iff s=39 mod42.                                      (1)
```

The last equivalence uses `ord_49(10)=42` and `10^39=27 mod49`.
The order follows from `ord_7(10)=6` and `v7(10^6-1)=1`.
Thus `t>=2` gives `7∤s` (indeed `s=4 mod7`). Put

```
g=gcd(L,s), p=s/g, q=L/g, X=10^g,
f(T)=7T^q-18T^p-25, F=f(X).
```

We have `0<p<q`, `gcd(p,q)=1`, `q` odd because L is odd, and
`7∤p`. Consequently

```
f'(X)=-18pX^(p-1) mod7
```

is a seven-adic unit. If `t<=1`, the candidate is already excluded.
For `t>=2`, simple Hensel lifting gives a root `alpha in Z_7` with
`alpha=X mod7`. In particular alpha is nonzero and is a unit. Factoring
`f(X)-f(alpha)` shows that its cofactor is `f'(alpha) mod7`, a unit;
therefore

```
t=v7(X-alpha).                                           (2)
```

Nonvanishing is established before any valuation estimate:
`F>=52*10^(L-1)-25>0`, since `s<=L-1`. Hence `X!=alpha`.
The cofactor of `X^6-alpha^6` reduces to `6*alpha^5 mod7`, also a unit.
It follows, with no valuation loss and no zero exception, that

```
v7(10^(6g)-alpha^6)=t.                                   (3)
```

## Multiplicative independence

At any place above two in `Q(alpha)`, write its integer-normalized
valuation as v and `r=v(alpha)`. The leading and constant coefficients
of f are odd. If `r>0`, the constant term has uniquely minimal valuation
zero. If `r<0`, the leading term has uniquely minimal valuation `qr`:
the middle term has valuation `v(18)+pr>qr`, and the constant has
valuation zero. Both possibilities contradict `f(alpha)=0`. Thus `r=0`.

A relation `alpha^m*10^n=1` with integers `(m,n)!=(0,0)` must have
`m!=0`. Applying v gives `n*v(2)=0`, so `n=0`, and alpha would be a
root of unity. At a complex embedding put `z=alpha`; then `|z|=1` and

```
7z^q-18z^p=25,
|7z^q-18z^p|<=7+18=25.
```

Equality in the triangle inequality forces the two nonzero summands to
have the same argument. Their sum is the positive real number 25, so
each summand is positive real: **z^q=1 and z^p=-1**. But then
`z^(pq)=1` and `z^(pq)=(-1)^q=-1`, since q is odd. This is impossible.
Therefore 10 and alpha, and also their sixth powers, are multiplicatively
independent. No assumption that alpha is rational or real was made.

## Degree, height and every corollary hypothesis

Let `E=[Q(alpha):Q]` and `D=[Q(alpha^6):Q]`. Then `1<=D<=E<=q`.
The primitive minimal polynomial of alpha divides f in `Z[T]`.
Multiplicativity of Mahler measure and the fact that a nonzero integer
polynomial has measure at least one give

```
E*h(alpha)<=log M(f)<=log(||f||_1)=log50.
D*h(alpha^6)=6D*h(alpha)<=6log50<25.                     (4)
```

In particular the degree in the height bound need not equal q.

Apply [Bugeaud--Laurent, Corollary 2, printed page 5](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf)
to `beta1=10^6`, `beta2=alpha^6`, prime seven, and positive exponents
`(b1,b2)=(g,1)`. The primary text's definitions on printed pages 2--4
were reopened together with the corollary during this audit. The selected
roots lie in `Q_7`, so the local ramification index and residue degree
are both one; the paper's degree parameter is exactly D as defined above.
Both bases lie in `1+7 Z_7`, and independence was proved above.

Choose the real height parameters

```
log A1=15, log A2=25/D.
```

They are positive, and satisfy every height floor:
`h(10^6)=6log10<15`, equation (4) gives `h(alpha^6)<25/D`,
and `log7/D<2/D` is below both chosen parameters. The explicit
corollary has no lower threshold on g. Its stated numerical upper bound
208 gives, using (3),

```
b'=g/(D log A2)+1/(D log A1)=g/25+1/(15D),
M=max(log(b')+log(log7)+2/5, 10log7/D, 10),
t<=208*D^4*M^2*15*(25/D)=78000*D^3*M^2.                (5)
```

All three entries of the maximum are bounded before substituting `D<=q`.
For `g>=1`, `b'<g`. Also `g<=L<3^a`, `log3<2`,
`log7<2`, and `log(log7)<1`. Hence the first entry is less than
`2a+7/5<2(a+20)`. The second is less than 20, since `D>=1`;
the third is 10. Thus the maximum is positive and
`M<2(a+20)` without squaring a possibly negative upper estimate.
Equation (5) proves

```
t<312000*D^3*(a+20)^2<=312000*q^3*(a+20)^2.            (6)
```

The same final bound trivially holds for `t<=1`.
The strict elementary logarithm bounds used here follow from rational
positive-term exponential sums checked in `math_checks.py`; in particular
`exp(5/2)>10`, `exp(25/6)>50`, and `exp(2)>7`. Also `2<e<3`, so
`log(log7)<log2<1`. No floating-point comparison controls the result.

## Exact crossover and all twelve smaller exponents

Suppose `q^4<=L`. By (6),

```
t<312000*L^(3/4)*(a+20)^2<L/2
```

whenever `L>(624000*(a+20)^2)^4`. At a=100 the sufficient exact
integer comparison is

```
3^100=515377520732011331036461129765621272702107522001
 >7*(624000*120^2)^4
 =45633771886553019187200000000000000000000.             (7)
```

Set `R_a=7*624000^4*(a+20)^8`. For every integer `a>=0`,
`(a+21)/(a+20)<=21/20` and
`3*20^8-21^8=38977140639>0`. Thus `R_(a+1)<3R_a`.
Exact induction from (7) proves `3^a>R_a` for every integer `a>=100`.
As `7L=3^a+4`, the needed strict length inequality follows.
Finally `L/2<L-2` because `L>4`. Therefore `t<L-2`, contradicting
the inclusive witness threshold.

The remaining admissible exponents are precisely the twelve below.
They are inherited from the two PR #28 receipts and were independently
recovered in PR #29's original-decimal checker. The new math checker
verifies their odd representatives, ranges and complete `9S` congruences
afresh from those exact integers, and recomputes each displayed residue.

| a | Unique joint class | Exact t | First nonzero n residue |
|---:|---|---:|---|
|31|Actual|1|35 modulo 49|
|37|Actual|1|35 modulo 49|
|43|Misses `[3,L)`|—|—|
|49|Actual|1|21 modulo 49|
|55|Actual|1|14 modulo 49|
|61|Misses `[3,L)`|—|—|
|67|Misses `[3,L)`|—|—|
|73|Actual|1|42 modulo 49|
|79|Actual|1|35 modulo 49|
|85|Actual|1|21 modulo 49|
|91|Actual|1|42 modulo 49|
|97|Actual|3|2058 modulo 2401|

Every actual failure depth is at most `L-2`. These twelve unconditional
individual exclusions cover the small range even when `q^4>L`; none
is assumed merely from the common-factor bound. Thus the theorem has no
unchecked finite remainder.

## Relation to rational centres and the surviving individual question

For the reduced exact ratio `s/L=p/q`, the earlier rational-centre
condition has zero offset `qs-pL=0`. Its all-length theorem covers such
ratios when `q<=K(L)^2`, and also covers specified **nonzero** offsets
with other centres. The present theorem excludes the exact-centre range
`q<=L^(1/4)` in this power-of-three family. This grows much faster than
the earlier logarithmic-square range; it is not a claim to replace the
earlier nonzero-offset results.

Indeed in this family `K>=17`; `17^8<6*7^15`, and
`(18/17)^8<7` propagates `K^8<6*7^(K-2)<=L` for all `K>=17`.
Thus all earlier exact ratios with `q<=K^2` are included, and the new
exact-centre denominator range is larger. These inequalities are checked
by exact integers in the math receipt.

For an individual full witness the new necessary condition is precisely
`q^4>L`, or `g^4<L^3`, in addition to actuality, the same-position sum
condition, and the full seven-power threshold. Failure of both neighbours
does not weaken this exclusion; conversely it supplies no exclusion in
the remaining range. No effective bound for all of that moving-position
range, no family-wide cutoff, and no counterexample is proved here.
No Lean formalization or Lean build was performed for this argument.

## Reproduction

From the repository root:

```sh
pt=research/a398769/five-seven/power-three-individual
python3 "$pt/math_checks.py" --check "$pt/math-checks.json"
python3 -O "$pt/math_checks.py" --check "$pt/math-checks.json"
```

The deterministic receipt binds the source and inherited inputs. It
checks the entire depth-two residue period, exact rational constants and
crossover arithmetic, the twelve inherited exclusions, and synthetic
nonzero simple-Hensel controls. Those controls test the algebra and
valuation transport; they are not asserted to be actual family members.
