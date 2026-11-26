# The remaining global obstruction

This note proves a deliberately conservative, effective power saving for the
signed three-term expression. Its exponent is **insufficient** to exclude a
witness. Neither the desired `5/6` bound nor an all-length exclusion is proved.
The results are ordinary mathematics, not Lean formalization.

## Exact reduction and the first missing step

For odd `L>=5`, `3<=i<L`, put

```
F=7*10^L-18*10^i-25, S=7L-4, n=F/9, P=25*7^(L-2).
```

The original decimal word is a run of `L-i-1` sevens, a five, a run of
`i-1` sevens and a five. Direct concatenation gives the displayed F, and
the digit counts give P and S. Its suffix 775 gives `v5(n)=2`. Since
`7` does not divide S, the exact full condition is

```
5 does not divide S, 9*S divides F, and v7(F)>=L-2.
```

The order of ten modulo `7^k` is exactly `T_k=6*7^(k-1)`:
`v7(10^6-1)=1`, followed by binomial lifting, proves the claim. Ten
therefore generates the whole unit group. The target `(7*10^L-25)/18`
is a unit and determines one exponent `r_k in [0,T_k)`. Modulo seven
that exponent is `3 mod6`. At `K=min{k:T_k>L}`, any witness necessarily
has the **actual** position `i=r_K in [3,L)`. The exact lift is

```
r_(j+1)=r_j+a_j*T_j, 0<=a_j<=6,
a_j = 5*(F(L,r_j)/7^j) mod7.
```

If `r_K` is actual, a nonzero digit at index j sends `r_(j+1)` above L
permanently. If the first such index is t, the actual pair has exact
valuation t. Consequently exclusion requires a nonzero digit at some
index in **`[K,L-3]`**, including both endpoints. Index `L-2` is too
late. A full-sum test and a depth test at different positions do not
establish or refute the joint condition.

The first unsupported assertion in a proposed global closing argument is:

> Every full-sum-compatible actual `r_K`, including those with composite S,
> has a nonzero lift digit at some index at most `L-3`.

Neither prime-sum density theorem addresses composite S, nor does it
reject every prime S. The known inequality `v7(ord_S(10))<=K-1` makes
the gcd in the unbounded-exponent CRT condition constant from depth K
onward. Later compatibility remains possible. The required extra theorem
must control the bounded actual representative or its valuation. See
[the exact lift analysis](../uniform-bound/LIFTS.md) and
[the retained structural analysis](../trillion-witness/STRUCTURE.md).

## The proposed `5/6` bound and its exact conditional cutoff

Suppose, on a stated domain beginning at a specified integer `L0`, one
could prove

```
7^t <= C*F^(5/6), C>=1.
```

For a witness, positivity and `F<7*10^L` give

```
7^(6L-12) <= C^6*F^5 < C^6*7^5*10^(5L),
(117649/100000)^L < C^6*7^17.                 (1)
```

Thus the constants and strict inequality in the proposed implication are
correct. Let N(C) be the least nonnegative integer satisfying

```
117649^N >= 100000^N*C^6*7^17.                (2)
```

Since `117649>100000`, (2) persists for every larger exponent. The
hypothetical bound excludes every `L>=max(L0,N(C))` on its stated
domain. For rational C, this is an exact integer comparison after clearing
denominators; floating logarithms are unnecessary. Examples, **conditional
only**, are `N(1)=204`, `N(25)=323`, and `N(10^6)=714`.

Any lengths below `max(L0,N(C))` must still be covered by a finite theorem
or direct checks. A starting length cannot be omitted merely because
the numerical value N(C) is small. There is no established C or L0 for
the `5/6` bound in this investigation, so these examples add no coverage.

More generally `7^t<=C*F^alpha` gives a finite cutoff by this argument
only when `alpha<log(7)/log(10)`. At or above that threshold, comparing
exponential sizes gives no eventual contradiction.

## What Bugeaud's Theorem 1.2 does and does not supply

The source is Yann Bugeaud, *On the digital representation of integers
with bounded prime factors*, [arXiv:1609.07926v1](https://arxiv.org/pdf/1609.07926),
Theorems 1.2, 2.2 and 2.3 and the proof on printed pages 6–8. The
downloaded PDF has SHA-256
`eb88ba3dcecf7e56066a11124368f8f2013ee6def488785729b6fdef85212ab7`.

Theorem 1.2 concerns ordinary base-b expansions with at most three
nonzero digits and no factor b. Its effective exponent is `1-c4` for
some positive effective c4, without a displayed numerical c4; the paper
explicitly describes the admissible saving as very small. F has signed
coefficients 7, -18 and -25, so it is not directly an instance of that
ordinary-digit theorem. Borrowing in decimal notation creates long runs,
rather than at most three nonzero digits. A change of base also requires
a proof; it cannot erase arbitrary L and i.

The following separate derivation uses the paper's two stated logarithm
estimates with signed rational input where permitted. It establishes an
actual, though weak, exponent instead of presuming `c4>=1/6`.

## An explicit signed bound, with insufficient exponent

For **all integers** `L>=5`, `3<=i<L`, with no primality or sum hypothesis,

```
7^v7(F) < 25*F^(1-1/(3*10^16)).               (3)
```

Here is a full constants check. Write `F=7^t*M`, where M is a positive
integer prime to seven, and set

```
A=max(M,25), a=log A, x=L/a.
```

The elementary size bounds are

```
10^L < F < 7*10^L, 2L<log F<3L, t<2L.        (4)
```

For the lower bound take the largest allowed i, obtaining
`F>=52*10^(L-1)-25>10^L`. The logarithm inequalities follow from
`2<log10<5/2`, `3/2<log7<2`, and `L>=5`; in particular
`t*log7<=log F<3L` gives `t<2L`. If `t<L/2`, then
`t*log7<L<(log F)/2`, which already proves (3). Otherwise `t>=L/2`,
so `t>=3`; all logarithm-form exponents below are nonzero.

### Case `i<=L/2`: real logarithms

Apply the source's Theorem 2.2 with three positive rational numbers
`7,10,M/7`, exponents `t,-L,1`, and height bounds `7,10,A`. The
nonzero form is

```
Lambda = 7^t*10^(-L)*(M/7)-1
       = -(18*10^i+25)/(7*10^L).
```

Its absolute value is less than `3*10^(-L/2)`, and hence
`log|Lambda|<-L/2` for `L>=5`. The normalized exponent bound in that
theorem is at most `max(1,4L/a)`: indeed
`t*log7<log F<3L` and `L*log10<3L`.

The theorem's numerical coefficient is
`8*30^6*3^(9/2)<10^12`, and `log7*log10<6`. Therefore

```
L/2 < 6*10^12*a*log(e*max(1,4L/a)).           (5)
```

If `x<1` there is nothing to prove. Otherwise (5) implies

```
x < 12*10^12*(1+log(4x)).                    (6)
```

The function `x/(1+log(4x))` is increasing for `x>=1`. At `x=10^16`,
`log(4x)<40`, so the right side of (6) is less than
`492*10^12<10^16`. Thus `x<10^16`.

### Case `i>=L/2`: two-adic logarithms

Use Theorem 2.3 with `p=2`, two nonzero rational numbers `7,-M/25`,
exponents `t,1`, and height bounds `7,A`. Negative rational input is
explicitly allowed in this theorem. Both rational numbers are two-adic
units because F and M are odd. The form is

```
Lambda = 7^t*(-M/25)-1
       = -10^i*(7*10^(L-i)-18)/25.
```

It is nonzero, and `v2(Lambda)>=i>=L/2`. In fact it is `i+2` when
`L-i=1`, and `i+1` when `L-i>=2`. The last exponent is one, so its
two-adic valuation is minimal as required by the theorem. Take `B=t`
and `B_n=1`; then `L/2<=B<2L`.

If `a/B>1/2`, then `a>L/4` directly. Otherwise use the permitted
parameter `delta=a/B in (0,1/2]`. The source's auxiliary quantity is

```
T=16*e^51*log7*(B/a),
log T < 60+log(2L/a).
```

The leading coefficient satisfies

```
(16e)^6*2^(3/2)*(log4)^2*2/(log2)^2
 < 48^6*3*4*8 < 2*10^12.
```

Both entries of the source's maximum are at most `2*a*log T`, since
they are `(log7)*a*log T` and `delta*B=a`. Consequently

```
L/2 < 4*10^12*a*(60+log(2L/a)),
x < 8*10^12*(60+log(2x)).                    (7)
```

For `x>=1`, the function `x/(60+log(2x))` is increasing. At
`x=10^16`, its right side in (7) is below
`800*10^12<10^16`, using `log(2*10^16)<40`. Hence again `x<10^16`.

### Combining the cases

We have proved `a>L/10^16` whenever `t>=L/2`. Since `A<=25M`, (4)
gives

```
log M >= a-log25 > (log F)/(3*10^16)-log25.
```

Exponentiating proves (3). Every constant is explicit; the stated
starting length is five. This addresses the signed coefficients without
appealing to a hypothetical extension of the ordinary-digit theorem.

The exponent in (3) is greater than `9/10`, while
`log7/log10<9/10` follows exactly from `7^10<10^9`. Thus (3) fails the
necessary exponent comparison for a closing cutoff. The much stronger
`5/6` exponent is **not** obtained. Existence of an effective saving
cannot be upgraded to a prescribed saving by enlarging a constant C.

## Qualitative finiteness and final mathematical status

The inherited [qualitative theorem](../effective/QUALITATIVE.md) proves
uniform `t=o(L)` using a Subspace-Theorem consequence. Its unspecified
exceptional heights supply no effective start for the exponent needed
here. The effective estimate (3) and the qualitative small-o estimate
cannot be combined into an effective small-o estimate: the missing
exceptional-height information remains missing.

No fully verified witness or all-length proof emerges. The new
prime-sum theorem is a whole-length exclusion on an infinite subclass;
the effective signed bound is a partial theorem that does not close
the complement. No implication for the other residual digit families
of A398769 follows from these exclusions. A genuine `{5,7}` witness
would refute the wider digit-1 conjecture, but proving this subclass
empty would leave the other digit families to settle separately.
