# Audit of the five-twelfths strip and exact line

25 November 2026. The strip deduction passes as stated. The separate
modular certificate and its exhaustive computations are documented in
[COMPUTATION.md](COMPUTATION.md). Given that independently reproduced
certificate, the all-length line conclusion below also passes.

## Domain and necessary divisor

Let L be odd, L >= 5, and 3 <= i < L. Set

```
S = 7L-4,  F = 7*10^L-18*10^i-25,  delta = 12i-5L.
```

The corresponding decimal number is n=F/9, with digit product
25*7^(L-2) and digit sum S. Thus a full witness requires exactly
225*S*7^(L-2) to divide F. In particular t=v_7(F) must be at least
L-2. The argument below excludes that last necessary condition;
it assumes neither a Fermat test for S nor 9S dividing F. It does
not impose i=3 modulo 6 in advance. Also F>0: since L>=i+1,
F>=52*10^i-25>0.

Put N=10^9. Since 12i is even and 5L is odd, delta is odd.
For L<N, therefore, |delta|>=1>L/N. The proposed closed strip
contains no admissible positions in this range. This is a parity
argument, not an invocation of a finite length certificate.

Now assume L>=N and |delta|<=L/N. Write uniquely

```
L=12q+r, 0<=r<=11,  i=5q+s,  delta=12s-5r,
m=min(0,s),  w=max(0,r,s)-m,  x=10^q.
```

Here q>=1. The integer s may have either sign and is not fixed as
L varies. Use the integral polynomial

```
Q(X)=7*10^(r-m)*X^12-18*10^(s-m)*X^5-25*10^(-m).
Q(x)=10^(-m)*F.
```

All three exponents in its coefficients are nonnegative, including
when s<0. Multiplication by a power of ten preserves v_7.

## Coefficient span, height, and the simple root

The identity s=delta/12+5r/12 gives the required span bound in all
three cases:

* If s<0, then delta<0 and
  w=r-s=7r/12+|delta|/12<=11+|delta|/12.
* If 0<=s<=r, then w=r<=11<=11+|delta|/12.
* If s>r, then delta>0 and
  w=s=5r/12+|delta|/12<=11+|delta|/12.

Consequently w+2<=|delta|/12+13. The sum of the absolute
coefficients of Q is at most (7+18+25)*10^w=50*10^w. The Mahler
measure is at most this sum. An integral primitive minimal polynomial
of any root alpha divides Q over Z; the integral cofactor has Mahler
measure at least one. Thus, for its global degree D,

```
1<=D<=12,
D*h(alpha)<=log(50*10^w)<(w+2)*log10.
```

This allows reducible Q and nontrivial content. All logarithms here
and below are natural. Choose the enlarged real height parameter

```
H=14L/N.
```

Indeed

```
w+2 <= L/(12N)+13 <= H,
H-[L/(12N)+13]=(167/12)*(L/N)-13 >= 11/12>0.
```

Also H>=14, so H*log10>log7 as required for the logarithmic theorem.

If t=0, exclusion is immediate. If t>0, x is a nonzero root of
Q modulo seven and

```
Q'(x) = -90*10^(s-m)*x^4 != 0 (mod7).
```

The leading derivative term has a factor seven. The displayed term
is a unit because 7 does not divide 90, 10, or x. In particular,
negative s causes no loss of the simple-root hypothesis. Hensel's
lemma gives alpha in Z_7, congruent to x modulo seven, with Q(alpha)=0.
The polynomial difference quotient at x and alpha is a unit, since
its reduction is Q'(x). Therefore

```
t=v_7(Q(x))=v_7(x-alpha).
```

The root alpha is a 7-adic unit, and x!=alpha follows from F>0.

## Multiplicatively independent root

The [primary Bugeaud--Laurent paper](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf),
printed pp. 2--4, was checked directly. Corollary 1 applies to
multiplicatively independent unit bases, positive exponents, and
log A_j >= max(h(alpha_j),log p/D), where D is global degree divided
by local residue degree. Here Q_7(10,alpha)=Q_7, so e=f=1 and D
is the global degree. Substituting p=7, bases (10,alpha), exponents
(q,1), log A_1=log10, and log A_2=H*log10/D gives

```
b'=(q/H+1/D)/log10,
t <= [168*(log10)^2/(log7)^4]*D^3*H
     *max(log b'+log log7+0.4, 10*log7/D, 10)^2.
```

The source's D^4 and its factor 24p(p^f-1)/(p-1) become D^3*H
and 168 after this substitution. The rational logarithm enclosure
in [strip_check.py](strip_check.py) proves the square-bracketed
coefficient is less than 63.

Since q=(L-r)/12<=L/12,

```
q/H <= N/168,
b' <= (N/168+1)/log10.
```

The exact rational series calculation gives

```
log((N/168+1)/log10)+log log7+0.4
    < 15.830999390874 < 16 < 20,
10*log7/D <= 10*log7 < 20,  and 10<20.
```

Thus the actual maximum is bounded by 20; in the uniform envelope
which already includes a floor of 20, T is exactly 20. No entry in
the theorem's maximum has been dropped. With D<=12,

```
t <= 63*12^3*H*20^2
   = (63*1728*14*400/1,000,000,000)*L
   = (609638400/1,000,000,000)*L
   = (47628/78125)*L = 0.6096384L < L-2.
```

The last strict margin at L=N is
(1-0.6096384)*N-2=390361598>0, and increases with L. This proves
the comparison even at the conservative real threshold N, although
N is even and the first admissible odd length above it is N+1.
Allowed equality |delta|=L/N is covered throughout.

## Multiplicatively dependent root, including D=7

Independence is not assumed without proof: the complementary case
has a separate argument. Write alpha^v=10^a with integer v>0 and
integer a (including a=0). Taking the global norm and then its
2-adic valuation gives

```
v*v_2(Norm(alpha))=aD,  j=aD/v in Z.
```

The norm is a nonzero rational number, whose 2-adic valuation is an
integer. Heights give D*h(alpha)=|j|*log10, so |j|<H. Further,
zeta=alpha^D/10^j satisfies zeta^v=1. It belongs to Q_7, whose
torsion units have order dividing six: reduction modulo seven is
injective on torsion, since 1+7Z_7 is torsion-free. Hence zeta^6=1.

Put y=x/alpha in 1+7Z_7. If Dq=j, then y^(6D)=1, so the same
torsion-free property forces y=1, contradicting x!=alpha. Thus
h=Dq-j is a nonzero integer, and

```
y^(6D)=10^(6h).
```

Principal-unit lifting of the exponent yields
v_7(y^(6D)-1)=v_7(y-1)+v_7(D). On the right,
v_7(10^6-1)=1, so v_7(10^(6h)-1)=1+v_7(h). For negative h,
inversion only introduces a 7-adic unit denominator. Since alpha
is a unit, v_7(y-1)=t. The exact identity is therefore

```
t=1+v_7(Dq-j)-v_7(D).
```

In particular the subtraction must remain when D=7, a possible
degree within 1<=D<=12. Also

```
0<|Dq-j| <= Dq+|j| < L+H < 2L < 7^(L-3).
```

Here Dq<=12q=L-r<=L and H/L=14/N<1. The final inequality already
holds at L=5 (10<49); replacing L by L+1 multiplies 2L by less
than seven while multiplying the right side by seven, so it holds
for every integer L>=5. It follows that v_7(Dq-j)<L-3, and the
nonnegative term v_7(D) can only lower t. Thus t<L-2 also in this
branch.

Combining both branches and the empty small strip proves, at every
admissible position,

```
full witness ==> |12i-5L|>L/10^9.
```

Equivalently the closed ratio interval
[5/12-1/(12*10^9), 5/12+1/(12*10^9)] is excluded, including both
endpoints. No finite-search or Fermat hypothesis is used in this
strip theorem.

## Exact line and combination with the separate certificate

The congruence 5L=1 modulo 12 forces L=5 modulo 12, because 5 is
its own inverse modulo 12. The integer solutions of 12i-5L=-1
are consequently

```
L=12u+5, i=5u+2, S=84u+31.
```

L>=5 gives u>=0; u=0 has i=2 and is invalid. Every integer u>=1
has L odd, L>=17, i>=3, and L-i=7u+3>0. This is exactly the
admissible range, with both parities of i retained. Direct substitution
gives

```
F/25=P(10^u),  P(X)=28000X^12-72X^5-1.
```

Since 25 is a seven-adic unit and L-2>=15, a full witness must
satisfy 7^10 dividing P(10^u). The separate exhaustive certificate
establishes

```
P(10^u)=0 mod7^10
  iff u=185987897 mod242121642.
```

Its least positive representative gives L=2231854769. This is the
least admissible length passing this depth-ten necessary condition,
not a witness. In particular every admissible line position with
L<N fails that condition and has v_7(F)<10<L-2. For L>=N the
same line has |delta|=1<=L/N and is excluded by the strip. There
is no length at the split missing from either argument.

Therefore **every integer u>=1 gives v_7(F)<L-2, and no full
witness exists at any admissible position on 12i-5L=-1**, without
a Fermat hypothesis. This is one position at each eligible length;
it does not exclude all positions of those lengths.

This conclusion neither proves 9S never divides F on the line nor
proves broad statement (E), which demands the sharper threshold
v_7(F)<K(L) when 9S divides F. PR #17 separately proves that 9S
fails on this line when S passes the base-10 Fermat test. That
conditional digit-sum result and the present unconditional
full-witness exclusion have different hypotheses and conclusions.

## Exact arithmetic checks and their limits

The strip checker uses exact integers and rational numbers. For
1<=x<=2 it bounds log x by the first 32 terms of
2*sum(z^(2k+1)/(2k+1)), z=(x-1)/(x+1), adding the upper tail
2*z^65/(65*(1-z^2)); powers of two reduce other positive arguments.
Monotonic substitution gives the displayed coefficient and maximum
bounds. No floating-point logarithm certifies an inequality.

Controls cover every odd L from 5 through 241 and every 3<=i<L:
14,280 cleared-polynomial identities, including 5,455 negative s.
All 2,420 positive-depth cases have nonzero derivative, including
959 with negative s and 18 with zero s. Their simple roots are
lifted through 7^6 for 12,100 root-distance congruence comparisons.
There are 42 separate LTE checks, including D=7 and negative
exponents. The nonzero control (L,i)=(23,15) has v_7(F)=2 and
F mod343=245. Four explicit negative controls are rejected.

These bounded controls support the algebra; they do not replace
the all-length proof or create a new length certificate. Essential
checks raise explicit exceptions and survive optimized Python.

From the repository root:

```sh
python3 research/a398769/five-seven/strip-audit/strip_check.py > /tmp/strip-results.json
python3 -O research/a398769/five-seven/strip-audit/strip_check.py > /tmp/strip-results-O.json
cmp /tmp/strip-results.json /tmp/strip-results-O.json
cmp /tmp/strip-results.json research/a398769/five-seven/strip-audit/strip_results.json
```

Both runs pass with byte-identical output. The receipt records the
source hash and exact bounds. This work is ordinary mathematics
with exact arithmetic checks; no new Lean theorem is claimed.
