# Five-adic lower bound for the exact seven-free quotient

26 November 2026. All logarithms are natural. The proposed deductions
pass audit with their stated constants. These are ordinary mathematical
proofs using the published Bugeaud--Laurent corollary, not Lean theorems.

## 1. Exact identity and hypotheses

The inherited elementary reduction leaves only odd lengths L, with
fives in positions 0 and i from the units end, `3<=i<L`, and sevens
elsewhere. Put

```
S=7L-4, P=25*7^(L-2), F=7*10^L-18*10^i-25, n=F/9.
```

The exact predicate is `PS|n`, equivalently
`225*S*7^(L-2)|F`. In particular **9S divides F**. This remains the
condition when `3|S`; no cancellation of nine modulo S is used.
Because `L>i>=3`, `F=-25 mod125`, so `v5(F)=v5(n)=2`.
Also `S=3 mod7`. A full witness consequently has `5∤S`, and its
positive integer quotient

```
q=n/(PS), q0=q/7^v7(q), t=v7(F), A=9S*q0
```

satisfies

```
t=L-2+v7(q), F=225S*q0*7^t=25A*7^t,
5∤q0, 5∤A, 7∤A, 9|A (in particular 3|A).
```

Here q0 retains every prime factor of q except seven: it is not assumed
to have bounded prime support. Rearranging the exact equality gives

```
25*(A*7^t+1)=10^i*(7*10^(L-i)-18).
```

The parenthesis on the right is `2 mod5`; thus
**`v5(A*7^t+1)=i-2` exactly**. Both bases used below are five-adic units.

Finally `7^t<=F/25<(7/25)*10^L<49^L`, since `A>=1`, `7<25`
and `10<49`. Taking logarithms base seven proves **t<2L**.
The witness assumption gives `t>=L-2>0`, so both exponents below
are positive integers.

## 2. Audit of the inherited strict position bound

The necessary strict inequality **i>L/25000** is proved in
[proportional/AUDIT.md](../proportional/AUDIT.md), section "Both ends".
Here is a replay of the portion used in this proof, valid for `L>=10^7`.
If `i<=L/25000`, the inherited `i=3 mod6` makes
`alpha=(18*10^i+25)/7` a positive integer. If `7|alpha`, then t=1.
Otherwise `t=1+v7(10^L-alpha)`. Independence follows by taking the
2- and 5-adic valuations of a relation: `v2(alpha)=0` and `v5(alpha)=2`.
Both global and local degrees equal one. Its height is less than
`(i+1)ln10`. In the corollary use heights `ln10` and `H_e ln10`,
where `H_e=L/25000+1`; the height floors are satisfied.

The coefficient `168*(ln10)^2/(ln7)^4` is less than 63, using the
fresh rational enclosures `389/200<ln7<39/20` and
`23/10<ln10<2303/1000`. Moreover
`b'<25001/ln10`, so the first maximum entry is less than 11,
and the other entries are below 19.5 or equal to ten. Hence

```
t <= 1+(95823/4)*(L/25000+1) < L-2.
```

The affine slope is `95823/100000<1`; the margin at `L=10^7`
is `1574965/4>0`, and increases thereafter. This contradicts a
witness. The inherited finite certificates handle the smaller lengths.
Only the already analytic range `L>B=1,000,002,000,000` is needed here.

## 3. Primary theorem and five-adic substitution

Source: Y. Bugeaud and M. Laurent, *Minoration effective de la distance
p-adique entre puissances de nombres algébriques*,
[Corollary 1, printed p.4](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf),
with the definitions on printed pp.2--3. The formula page was inspected
visually in this audit. Source SHA-256:
`554bb384df62538fa11fcf6ab74976e772156c9d3ca4022e2128d48e3632128d`
(271382 bytes), matching the inherited [source record](../uniform-bound/SOURCES.md).

For multiplicatively independent algebraic p-adic units, positive
integers b1,b2, and `Lambda=alpha1^b1-alpha2^b2`, the source uses

```
f = residue degree of Q_p(alpha1,alpha2),
D = [Q(alpha1,alpha2):Q]/f,
log A_j >= max(h(alpha_j),log(p)/D),
b' = b1/(D*log A2)+b2/(D*log A1).
```

Corollary 1 states

```
v_p(Lambda) <= 24*p*(p^f-1)*D^4*log A1*log A2
              / ((p-1)*(log p)^4)
              * max(log b'+log log p+2/5, 10*log p/D, 10)^2.
```

It has no unspecified large-exponent threshold. We apply this explicit
corollary, not the separate asymptotic theorem. The source's `A1,A2`
are height parameters; they must not be confused with the integer A.

Set `p=5, alpha1=7, alpha2=-1/A, (b1,b2)=(t,1)`.
These rational bases have global degree one and local field Q_5, so
`e=f=D=1`. Their heights are `ln7` and `ln A`. Negative rational
bases are allowed; there is no positive-real-base hypothesis.
For any integer relation `7^u*(-1/A)^v=1`, taking v3 gives
`-v*v3(A)=0`. Since `3|A`, v=0, then u=0. This proves
multiplicative independence, including relations with negative exponents.
Also

```
Lambda=7^t+1/A=(A*7^t+1)/A != 0,
v5(Lambda)=i-2.
```

Assume for contradiction `ln A<=H=L/10^9`. Choose
`log A1=ln7` and `log A2=H`. Since `L>B>10^12`, `H>1000>ln5`;
also `ln7>ln5`. All height floors are met. The exponent bound implies

```
b'=t/H+1/ln7 < 2*10^9+1,
i-2 <= [120*ln7/(ln5)^4] * H
       * max(ln b'+ln ln5+2/5, 10 ln5, 10)^2.
```

## 4. Strict rational margins at every relevant length

No floating-point approximation is needed. The two independent checkers
certify the logarithm bounds with rational series and rigorous tails.
For the coefficient, `ln7<2` and `ln5>8/5` give

```
120*ln7/(ln5)^4 < 240/(8/5)^4=9375/256 < 48.
```

For the first branch, `b'<3*10^9`, `ln3<11/10`,
`ln10<2303/1000`, and `ln ln5<ln2<7/10` give

```
ln b'+ln ln5+2/5
 < 11/10+9*(2303/1000)+7/10+2/5
 = 22927/1000 < 24.
```

The second branch is below 20 because `ln5<2`; the third is ten.
Thus **every branch is strictly below 24**, and

```
i-2 < (48*24^2/10^9)*L = (27648/10^9)*L.
```

But `i>L/25000` gives `i-2>L/25000-2`. Their slope difference is

```
1/25000-27648/10^9=193/15625000.
```

At `L=10^12`, this difference times L, minus two, is
**12,351,998>0**, and it increases with L. The strict inequalities
are incompatible throughout `L>B`. We have proved

> Every full residual witness with L>B satisfies **ln A>L/10^9**.

The quantitative quotient conclusion is

```
q0 > exp(L/10^9)/(9*(7L-4)) > exp(L/10^9)/(63L).
```

## 5. Polynomial consequence and all-length exclusion

Let `g(L)=L/10^9-ln63-36 ln L`. At `L=10^12`, the exact
enclosures `ln10<2303/1000` and `ln63<21/5` give

```
g(10^12) > 1000-21/5-432*(2303/1000)=113/125>0.
```

For every real `L>=10^12`,
`g'(L)=1/10^9-36/L>=1/10^9-36/10^12>0`.
Consequently `ln63+36 ln L<L/10^9` throughout this range.
If a full witness above B had `q0<=L^35`, then

```
A=9(7L-4)q0 < 63L^36,
ln A < ln63+36 ln L < L/10^9,
```

contradicting section 4. Combining with the inherited complete exclusion
for `1<=L<=B` proves:

> **There is no full {5,7} witness with q0<=L^35 at any length.**

This conclusion has no restriction on the second-five position. The
stronger functional lower bound above B is retained as part of the result;
the constants have not been optimized.

PR #24's [ROUTE1.md](../explicit-length/ROUTE1.md), section 4, proves
`q0<=L^d => L<=10^18*(d+1)^2-1`. For d=35 its cutoff is
`1,295,999,999,999,999,999,999`, leaving the odd lengths
`B<L<=U_35` unchecked. The present analytic bound starts before B
and closes that entire subfamily without enumerating that remainder.
The older statement for arbitrary fixed d remains useful and is preserved.
Neither proof supplies an upper bound `q0<=L^35` for all witnesses.

The whole-length endpoint remains **B=1,000,002,000,000 inclusive**.
The unrestricted {5,7} subclass and wider A398769 digit-1 conjecture
both remain open. The exact remaining implication and numerical gap are
given in [OBSTRUCTION.md](OBSTRUCTION.md).
