# One member of the power-of-three family

Base: `0a47180b889b392c2323bc1614a473af51f38d78`, PR #27's merge.
All logarithms in real inequalities are natural. These are ordinary
mathematical arguments; no Lean formalization or build is claimed.

**Verdict: the infinite individual-family assertion remains open.** The
3-adic description in the question is correct, including its stated
precision, once division by 18 and by `log(10)` is done at the precisions
below. It does not yet bound the seven-adic valuation below `L_a-2`.
The explicit inequalities here do not give a numerical exponent cutoff.
The new finite certificates and their exact range are in [README.md](README.md).

## 1. The full original predicate

For the decimal word with fives at positions zero and s, and sevens
elsewhere, let `R_L=1+10+...+10^(L-1)`. Directly from its decimal blocks,

```
n=7R_L-2-2*10^s,
P=25*7^(L-2), S=7L-4,
F=9n=7*10^L-18*10^s-25.
```

Hence `PS|n` is exactly `225*S*7^(L-2)|F`. In the present family
`S=3^a`, with `a=31+6u`, `u>=0`, `L=(3^a+4)/7` is odd and five-free.
For `3<=s<L`, `v5(F)=2`, `F>0`, and `7` is coprime to `225S`.
On the **same actual position**, `9S|F` therefore makes the full
predicate equivalent to `t=v7(F)>=L-2`. Equality already suffices.
A first nonzero residue modulo `7^m` excludes it only when `m<=L-2`.

## 2. Existence, domains and exact precision at three

On `1+3 Z_3`, the 3-adic logarithm and exponential are inverse
isometries to and from `3 Z_3`; in particular they restrict to
`1+9 Z_3` and `9 Z_3`. Here `v3(log(10))=2`. Define

```
theta=exp((4/7)*log(10)).
```

The multiplier `4/7` is a 3-adic unit. Thus `theta` belongs to
`1+9 Z_3`, satisfies `theta^7=10^4`, and is the unique such root:
multiplication by seven is invertible on `9 Z_3`. Equivalently, the
polynomial has a unique root in this residue class by Hensel lifting.
For the integer `L=(3^a+4)/7`,

```
10^L/theta = exp((3^a/7)*log(10)),
v3(10^L-theta)=a+2.                                  (1)
```

So the requested congruence modulo `3^(a+2)` holds, and generally
cannot be increased to `3^(a+3)`. This is exact precision, not just a
lower bound. For finite computation to precision `N>=3`, one may also
use `theta=10^e mod3^N`, where `7e=4 mod3^(N-2)`; the exact order of ten
modulo `3^N` is `3^(N-2)`. The new program instead uses Newton lifting.

Set `C=(7theta-25)/18`. Division by 18 costs **two** ternary digits.
A convenient finite calculation is

```
theta=145 mod729,     C=55 mod81,
v3(C-1)=3.
```

Indeed `145=1 mod9` and `145^7=10^4 mod729`; uniqueness identifies this
root. The C congruence follows by the exact division
`(7*145-25)/18=55`. In particular C is in `1+27 Z_3`, so its logarithm
exists, and

```
kappa=log(C)/log(10) is in 3 Z_3,
v3(kappa)=1,         kappa=6 mod9.                    (2)
```

For the last congruence, `log(C)=54 mod81`, while `log(10)/9=1 mod3`.
The logarithm quotient loses another two ternary digits. Thus a theta
known modulo `3^(a+2)` determines C modulo `3^a` and kappa modulo
`d=3^(a-2)`, exactly the precisions required, with no missing factor nine.
To check the equality in (1) numerically, use one additional theta digit.

Define the moving target `C_L=(7*10^L-25)/18` in `Z_3`. Equation (1) gives
`v3(C_L-C)=a`. Consequently

```
9*3^a | F(L,s)
  iff 10^s=C_L mod3^a
  iff 10^s=C mod3^a
  iff s=kappa mod3^(a-2).                            (3)
```

The final equivalence uses
`v3(10^s-C)=2+v3(s-kappa)`, from the logarithm isometry and
`10^kappa=C`. These are statements in `Q_3`, not real logarithms.

Let `r_a` be kappa's representative in `[0,d)`. Exactly one of `r_a`
and `r_a+d` is odd, since d is odd; call it `s_a`. Since `3|r_a` and
`3|d`, this representative is `3 mod6`, and therefore at least three.
It is the unique joint representative in `[0,2d)`. Also

```
2d-L=(5d-4)/7>0.
```

Thus `s_a>=L` excludes the entire length. Otherwise it is its sole
actual sum-compatible position meeting the necessary seven-adic
residue condition. Equation (3) also proves

```
s_(a+6)=s_a+2d*k_a,       0<=k_a<=728.               (4)
```

Both representatives reduce to the same odd class modulo `2d`, while
the new modulus is `729*(2d)`. This recurrence supplies no requirement
that the true increment `k_a` pass a seven-adic transition.

## 3. An explicit inequality joining three and seven

For every actual sum-compatible position let `t=v7(F)`. The positive
integer F is divisible by `25*3^(a+2)*7^t`. Therefore

```
25*3^(a+2)*7^t <= F < 7*10^L,
(a+2)*log(3)+t*log(7)+log(25) < L*log(10)+log(7),
t < (log(10)/log(7))*L
       - ((a+2)*log(3)+log(25/7))/log(7).            (5)
```

This is an unconditional cross-prime bound with all constants. Its
leading coefficient `log(10)/log(7)>1` is too large for the desired
`t<=L-3`. Substituting `L=(3^a+4)/7` does not repair this: the improvement
from the three-adic factor is linear in a, whereas L is exponential in a.
A full witness would merely satisfy the compatible necessary inequality

```
L*log(10/7) > (a+2)*log(3)+log(25/343).
```

The inherited explicit estimates also remain applicable at this one
position, with `M=max(log(L)+2,20)`:

```
t <= 1+63*(s+1)*M^2,
t <= 63*(L-s+1)*M^2,
t <= 504*(abs(L-2s)+2)*M^2.                          (6)
```

See [edge bounds](../settlement/EDGE_BOUNDS.md) and
[the quadratic estimate](../effective/ROUTE_A.md). They exclude their
specified regions but do not cover an arbitrary residue of kappa: if
s, L-s and `abs(L-2s)` are all proportional to L, their right sides
can exceed L. Neither (2) nor (3) forces membership in the inherited
rational-centre or small-seven-free-quotient subfamilies.

## 4. Why an algebraic norm does not transport the large seven power

The fixed algebraic target makes a natural resultant attempt possible.
For an integer s put

```
A_s=18*10^s+25,
Z_s=A_s^7-7^7*10^4.
```

The algebraic relation `theta^7=10^4` and the unit derivative at three
give, for a sum-compatible s,

```
v3(Z_s)=v3(A_s-7theta)=4+v3(s-kappa)>=a+2.           (7)
```

But if `t=v7(F)>=2`, then `A_s/7` is an integer and
`A_s/7=10^L mod7`. In this family `L=1 mod6` (because
`3^a=3 mod42`), so `10^L=3 mod7`, whereas `10^4=4 mod7`.
Thus

```
Z_s/7^7=(A_s/7)^7-10^4=3-4=-1 mod7,
v7(Z_s)=7,                                         (8)
```

**independently of how large t is**. The large seven-adic agreement
with `10^L` has disappeared from this norm. Since `s>=3`,
`0<Z_s<(19*10^s)^7`; (7)--(8) yield only

```
(a+2)*log(3)+7*log(7) < 7*s*log(10)+7*log(19).
```

It contains the fixed number seven, not t. Replacing it by t would be
an unsupported inference. A 3-adic root cannot simply be regarded as
simultaneously close to `10^L` at seven.

## 5. An effective logarithm estimate at three, and its direction

Even an explicit irrationality estimate for the fixed C is insufficient
in the needed direction. Here is one fully parameterized example.
The degree of theta, and hence of C, is seven: `theta^2/10` is a root
of `X^7-10`, Eisenstein at two. The norm of C is

```
N(C)=(7^7*10^4-25^7)/18^7=236879375/68024448,
v2(N(C))=-7,             v5(N(C))=4.
```

A relation `10^r*C^q=1` would, after taking norms and these valuations,
give `7r-7q=0` and `7r+4q=0`; hence r=q=0. In particular kappa is not
a rational number. Each conjugate of theta has complex absolute value
`10^(4/7)<4`. The polynomial `(18X+25)^7-7^7*10^4`, with leading
coefficient `18^7`, then bounds the absolute logarithmic height by
`h(C)<=log(53)<4`, whether or not its content is divided out.
Also `h(10)=log(10)<3`.

Bugeaud--Laurent's [Corollary 2, printed p.5](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf)
was read afresh, with the definitions on pp.2--4. Its hypotheses hold
with `p=3`, `alpha1=10`, `alpha2=C`, exponents `(s,1)`, local field
`Q_3` (so e=f=1), global parameter D=7, and height parameters
`log A1=3`, `log A2=4`. Both bases are principal units. Here
`b'=s/28+1/21<s`, and the theorem gives

```
v3(10^s-C)
 <= [36*7^4*3*4/(log(3))^4]
    * max(log(b')+log(log(3))+0.4,10*log(3)/7,10)^2
 < 1037232*max(log(s)+1,10)^2.                       (9)
```

The simplifications use `1<log(3)<6/5`,
`log(log(3))<1/5`, and `36*7^4*12=1037232`.
The height bound `log(53)<4` follows, for example, by the rational
positive-term series for `exp(4)`; no floating-point threshold is needed.
At a sum-compatible s, (3) implies only

```
a < 1037232*max(log(s)+1,10)^2.                      (10)
```

This is a lower constraint on the size of s. Together with `s<L<3^a`
it is consistent for arbitrarily large a and does not bound a above.
It also contains no estimate on `v7(F)`. The sharper principal-unit
corollary was used only for this displayed example; none of the finite
certificates or the three-length theorem relies on (9).
The primary PDF's previously retained SHA-256 is recorded in
[the source record](../uniform-bound/SOURCES.md). Its formula was
reopened here through the web tool; no fresh raw-byte download/hash is
claimed (the shell download had a DNS failure).

## 6. Comparison with inherited arguments and the first missing step

The inherited [fixed-depth proof](../fixed-depth/PROOF.md) uses a
**two-parameter** `S=3^a*17^b` grid, two independent circle actions,
and an algebraic contradiction to a finite limiting set. This fixed
algebraic theta is the same three-adic target underlying that proof's
polynomials. Restricting to `S=3^a` removes the independent seventeen
parameter; its density conclusion cannot be imported by setting b=0.
Moreover fixed depth is chosen before length grows. It never permits
substitution of the moving threshold `L-2`. The inherited fixed-depth
result does not, by itself, disprove a constant depth bound for this
pure-power subfamily.

The inherited [qualitative bound](../effective/QUALITATIVE.md) does
imply only finitely many full witnesses here, as a restriction of its
uniform `v7(F)=o(L)` statement. Its starting length is ineffective.
The new three-length theorem excludes three successive survivors; it
does not exclude a single survivor whose neighbours fail. Even a proof
of at most one exception would not locate or eliminate that exception.

The first missing individual inference is therefore an effective bound
forcing `v7(F(L_a,s_a))<=L_a-3` whenever `s_a<L_a`, or a new explicit
cutoff followed by complete checking below it. Equivalently the actual
seven-adic position lift must change by an index at most `L_a-3`.
The exact ternary description, irrationality, (5), (6), (9), and the
three-length obstruction do not establish that inference. No individual
counterexample or full witness has been obtained.

## Implementation inspection

A separate mathematical reviewer inspected `individuals.py`: Newton
precision doubling is valid because `7*x^6` is a unit; reducing the C
numerator modulo `9*3^N` before dividing by nine retains exactly N
digits; dividing both modular logarithms by nine leaves precision N-2
before inverting the unit denominator. The logarithm code separates
`k=3^e*k0` and divides the modular numerator exactly by `3^e`, then
inverts k0. Its omitted tail is valid since `v3(z)>=2` gives
`v3(z^k/k)>=2k-v3(k)>=N` for every `k>=N`. Changing the input unit by
`3^N` changes its logarithm by a multiple of `3^N`. The odd-lift and
exact-theta-valuation checks use sufficient precision, including the
last requested exponent. Explicit exceptions preserve the checks under
`python3 -O`. Independent original-decimal-block arithmetic and its
receipt comparison are recorded separately in the finite audit.
