# Closed seven-twelfths strip: independent audit

**Verdict: PASS.** For every odd `L>=5` and `3<=i<L`, every full
witness satisfies

```
|12i-7L| > L/10^9.
```

The simple-root step from the inherited five-twelfths proof cannot be
copied: here the derivative always has a factor seven. Strong Hensel
lifting supplies an exact loss of one valuation unit. Both root branches
below retain this loss. The proof uses the necessary full-witness
threshold `v7(F)>=L-2`, never the depth test `v7(F)>=K(L)` or the separate
digit-sum test `9S|F`. In particular this is a position exclusion, not an
extension of consecutive whole-length coverage or broad statement (E).

## Domain, small lengths, and clearing the coefficients

Write `N=10^9`, `F=7*10^L-18*10^i-25`, `S=7L-4`, and
`delta=12i-7L`. The exact full-witness condition is
`225*S*7^(L-2)|F`. The integer F is positive, since
`F>=52*10^i-25>0` when `L>=i+1`; its valuation is finite.

Odd L makes delta odd. If `L<N`, then `|delta|>=1>L/N`, so the closed
strip is empty without using a finite computation. For the remaining
proof suppose `L>=N` and `|delta|<=L/N`, and write uniquely

```
L=12q+r, 0<=r<12, i=7q+s, x=10^q,
m=min(0,s), w=max(0,r,s)-m, delta=12s-7r.
```

Here `q>=1`, while s is an unrestricted integer. The polynomial

```
Q(X)=7*10^(r-m)*X^12-18*10^(s-m)*X^7-25*10^(-m)
```

has integral coefficients, also for negative s. Direct substitution gives

```
Q(x)=10^(-m)*F,
x*Q'(x)=7*10^(-m)*(12*10^L-18*10^i)
        =7*10^(-m)*(F+5*10^L+25).                     (1)
```

Thus `v7(Q(x))=t:=v7(F)`. If `t<=2`, then already `t<L-2` for
`L>=N`; no root lifting is needed in that case.

## Derivative and the precise strong Hensel conclusion

If `t>=1`, the bracket on the right of (1), reduced modulo seven, is
`5*(10^L+5)`. For odd L the possible residues of `10^L` are `3,6,5`,
so the bracket is never zero modulo seven. Since both x and ten are
seven-adic units, **`v7(Q'(x))=1`**. This is where odd L enters the
lifting argument; omitting it is invalid (the checker rejects the
would-be assertion at `L=8,i=3`).

The version used is Keith Conrad, *Hensel's Lemma*, Theorem 4.1, printed
p. 6, in the [author's notes](https://kconrad.math.uconn.edu/blurbs/gradnumthy/hensel.pdf),
read on 25 November 2026. For an integral polynomial over `Z_p` at
`a in Z_p`, its hypothesis is `v_p(f(a))>2*v_p(f'(a))`. Its conclusion
includes a unique root in `v_p(alpha-a)>v_p(f'(a))` and the equality
`v_p(alpha-a)=v_p(f(a))-v_p(f'(a))`.

For `t>=3` this hypothesis is precisely `t>2`. Therefore a root
`alpha in Z_7` exists with

```
Q(alpha)=0, v7(x-alpha)=t-1>=2, v7(Q'(alpha))=1.       (2)
```

It is a unit because `alpha=x (mod49)`. It is algebraic over Q because
Q is a nonzero integral polynomial; `alpha!=x` follows from `F>0`.
The uniqueness statement is local in `x+49Z_7`. It does not assert
that Q has only one root modulo every power of seven.

For an elementary check of the reduction, put
`R(Y)=Q(x+49Y)/343`. Its constant coefficient is integral by `t>=3`,
its linear coefficient is `Q'(x)/7`, a unit, and coefficients of degree
at least two are integral and divisible by seven. Consequently R has
one simple root modulo seven and one compatible lift at every depth;
it gives the same root `alpha=x+49Y`. The checker uses this transformed
polynomial rather than assuming a false unique-lift rule for Q itself.

## Coefficient span and root height, with either sign of s

The three cases in the span estimate are

```
s<0:       w=r-s=5r/12+|delta|/12 <=11+|delta|/12;
0<=s<=r:  w=r                      <=11+|delta|/12;
s>r:      w=s=7r/12+|delta|/12     <=11+|delta|/12.
```

Hence `w+2<=|delta|/12+13`. The coefficient sum is at most
`(7+18+25)*10^w=50*10^w`, bounding the Mahler measure of Q. The
primitive integral minimal polynomial of alpha divides Q over Z;
the remaining nonzero integral factor has Mahler measure at least one.
Therefore, with `D=[Q(alpha):Q]`,

```
1<=D<=12, D*h(alpha)<=log(50*10^w)<(w+2)*log10.       (3)
```

This argument permits reducible Q and nontrivial content. All logarithms
are natural. Set `H=14L/N`. Since

```
H-[L/(12N)+13]=(167/12)*(L/N)-13>=11/12>0,
```

the strip assumption and (3) give `D*h(alpha)<H*log10`.
Also `H>=14`, so `H*log10>log7`. These are the required height
hypotheses; the height parameter has not been held fixed as L varies.

## Multiplicatively independent root

Use Bugeaud--Laurent, *Minoration effective de la distance p-adique
entre puissances de nombres algebriques*, Corollary 1, printed p. 4,
with the definitions on printed pp. 2--3 of the
[primary paper](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf),
rechecked on 25 November 2026. The explicit corollary applies to
multiplicatively independent unit bases and positive exponents, with
`log A_j>=max(h(alpha_j),log p/D)`. Here both bases `10,alpha` lie
in `Q_7`, so the local residue and ramification degrees are `f=e=1`;
the theorem's D is the global degree in (3), not the local degree.

Take `(b1,b2)=(q,1)`, `p=7`, `log A1=log10`, and
`log A2=H*log10/D`. They satisfy all stated hypotheses by (2), (3),
and `q>=1`. Substitution in that corollary gives

```
b'=(q/H+1/D)/log10,
t-1 <= [168*(log10)^2/(log7)^4]*D^3*H
       *max(log b'+log log7+0.4, 10*log7/D, 10)^2.    (4)
```

In particular the corollary's original `D^4` is retained before the
height substitution, and `24p(p^f-1)/(p-1)=168`. The left side is
`t-1`, not t, by the strong-Hensel distance (2).

Since `q<=L/12`, `q/H<=N/168`. Exact rational logarithm enclosures in
[seven_twelfths.py](seven_twelfths.py) certify

```
168*(log10)^2/(log7)^4 <63,
log((N/168+1)/log10)+log log7+0.4 <15.830999390874<16,
10*log7/D<=10*log7<20, and 10<20.
```

Every entry of the maximum in (4) is accounted for. Taking the
upper envelope 20 and `D<=12` gives exactly

```
t <= 1+63*12^3*(14L/N)*20^2
  = 1+(47628/78125)*L
  = 1+0.6096384L < L-2.                             (5)
```

Indeed the margin `(L-2)-(1+0.6096384L)` at `L=N` is the positive
integer **390361597**, and its slope is `1-47628/78125>0`.
This certifies the strict comparison for all real `L>=N`, hence for
all admissible odd lengths. The t<=2 branch also satisfies (5).

## Multiplicatively dependent root, including degree seven

In the complementary case write `alpha^v=10^a`, with integers `v>0`
and a, which can be zero or negative. Taking global norms and then
the 2-adic valuation proves

```
j=aD/v=v2(Norm(alpha)) in Z.
```

The height identity `v*h(alpha)=|a|*log10` gives
`D*h(alpha)=|j|*log10`, and thus `|j|<H`. Further,
`zeta=alpha^D/10^j` has `zeta^v=1` and belongs to `Q_7`.
The torsion units of `Q_7` have order dividing six: their reduction
is injective because `1+7Z_7` is torsion-free. Thus `zeta^6=1`.

Put `y=x/alpha in 1+49Z_7`, using (2), and `h=Dq-j in Z`.
If h were zero, then `y^(6D)=1`, and torsion-freeness would force
`y=1`, contrary to `x!=alpha`. Hence h is nonzero and

```
y^(6D)=10^(6h).
```

Odd-prime LTE on the left gives `v7(y^(6D)-1)=t-1+v7(D)`.
Since `v7(10^6-1)=1`, LTE on the right gives `1+v7(h)`;
for negative h, inversion changes only a unit factor. Therefore

```
t=2+v7(Dq-j)-v7(D).                                (6)
```

Both the extra unit loss and the subtraction are essential in this
identity. In particular D can equal seven, and then `v7(D)=1`.
The proof does not discard that subtraction or assume degree coprime
to seven.

Finally `Dq<=12q<=L`, `|j|<H`, and `H/L=14/N<1` show

```
0<|Dq-j|<L+H<2L<7^(L-4), for L>=N.
```

For the last inequality, `2*6<7^(6-4)` is a valid induction base;
at the next integer L the left side grows by a factor less than seven
while the right side grows by seven. Thus it holds for all `L>=6`,
which includes this domain. It follows that `v7(h)<L-4`. Substituting
in (6), and using `v7(D)>=0`, yields `t<L-2` as required.

## Endpoints, coverage, and reproducibility

The proof assumed the closed inequality `|delta|<=L/N` and obtained
the strict contradiction `t<L-2`; it therefore excludes both strip
endpoints as stated. In fact exact equality would imply
`L=N*|delta|`, impossible for odd L because N is even. No gap is left
at the transition `L=N`, also even; the estimates cover it anyway.

The newly excluded closed ratio interval is

```
[6999999999/12000000000, 7000000001/12000000000].
```

It lies inside the inherited open interval
`(60001/120000,5999999/10000000)` and splits that interval at the two
displayed endpoints. It excludes positions in this interval for every
length; it does not exclude every position of any new whole length.
The all-length subclass, broad (E), and the wider digit-1 conjecture
remain open.

From the repository root:

```sh
python3 research/a398769/five-seven/three-deductions-audit/seven_twelfths.py > /tmp/seven-twelfths.json
python3 -O research/a398769/five-seven/three-deductions-audit/seven_twelfths.py > /tmp/seven-twelfths-O.json
cmp /tmp/seven-twelfths.json /tmp/seven-twelfths-O.json
cmp /tmp/seven-twelfths.json research/a398769/five-seven/three-deductions-audit/seven_twelfths.json
```

Both modes passed with byte-identical results. All essential guards are
explicit exceptions. The rational logarithm enclosure uses 36 terms of
`2*sum(z^(2j+1)/(2j+1))`, `z=(x-1)/(x+1)`, for `1<=x<=2`, with
upper omitted tail `2*z^73/(73*(1-z^2))`; scaling by powers of two
covers larger arguments. No floating-point value certifies a bound.

Bounded controls check 2,412 spans with both signs of s, and all
14,280 admissible pairs at odd lengths 5 through 241. There are 2,420
positive-depth cases with derivative valuation exactly one, including
negative, zero, and positive s. Fifty cases have `t>=3`, with 300
transformed-root lift comparisons. Three retained positive controls
have depths 3, 4, and 5 and exact distances 2, 3, and 4 respectively.
Forty-four LTE checks include the degree-seven subtraction algebra
and negative exponents; five deliberate negative controls are rejected.
The receipt describes those finite controls, not an all-length search.
The all-length conclusion is the proof above, not a new Lean theorem.
