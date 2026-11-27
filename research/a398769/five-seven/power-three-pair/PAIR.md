# No two adjacent power-of-three members are full witnesses

**Theorem.** For every integer `u>=0`, put `a=31+6u`. The two lengths
`L_a=(3^a+4)/7` and `L_(a+6)` cannot both contain a full witness in the
residual two-five `{5,7}` family. This is an ordinary mathematical proof
with independently reproduced finite arithmetic, not a Lean theorem.

## 1. Exact predicate and elimination of the actual position

The word has fives at positions zero and `s` from the units end, and
sevens elsewhere. Direct decimal summation gives

```
n=7*(10^L-1)/9-2-2*10^s,
S=7L-4=3^a, P=25*7^(L-2),
F(L,s)=7*10^L-18*10^s-25=9n,
PS|n  iff  225*S*7^(L-2)|F.
```

At every actual position `3<=s<L`, `v5(F)=2`. Thus after **9S|F** and
the five factor pass at this same position, the witness condition is
`v7(F)>=L-2`: equality suffices. Any witness also satisfies `s=3 mod6`,
since `7|F` forces `10^s=-1 mod7`.

Put `d=3^(a-2)`. The inherited [sum-class proof](../power-three/INDIVIDUAL.md)
gives the unique joint representative `s` in `[0,2d)`. In more detail,
`theta=10^(4/7)` in `1+9 Z_3`, `C=(7theta-25)/18`, and
`kappa=log(C)/log(10)` give `9S|F iff s=kappa mod d`. This equivalence
retains both divisions costing two ternary digits each. The odd lift is
`3 mod6`; because `2d>L`, it is the only possible actual witness position.
For the successor use primes. Its representative reduces to the same
odd class modulo `2d`, so

```
d'=729d, L=(9d+4)/7, L'-L=936d,
s'=s+2dk, 0<=k<=728.
```

Actuality sharpens this to `k<=468`: from `s'>=3+2dk` and
`s'<L'=(6561d+4)/7` one obtains
`k<6561/14-17/(14d)<469`. No negative increment is possible, since
`s` is the least nonnegative representative modulo `2d` and `s'` is
nonnegative in the same class. Both endpoints zero and 468 are retained.

For depth three put `U_u=7*10^L-25` and `G_u=10^(2d)` modulo 343.
Any pair requires `U_u*G_u^k=U_(u+1)`. The complete period in `u` is
seven: `v7(729^7-1)=2`, so the length changes by a multiple of 42 and
`2d` changes by a multiple of 294. The factor seven in `U` means that
period 42 suffices for its exponent; ten has order 294 modulo 343.
This follows from `ord_7(10)=6` and `v7(10^6-1)=1` by binomial lifting.

Both exact programs enumerate **all seven starts and all 469 increments**.
For each start the result is exactly

```
K={42,91,140,189,238,287,336,385,434}.
```

Equivalently `k=42 mod49` in the actual range. Periodicity, necessity,
and complete enumeration certify completeness; no pilot value is used
as a filter. These are projected necessary transitions, not assertions
that the actual ternary position sequence realizes any listed increment.

Since `a-2=29+6u`, `d=5 mod7` and `d=3 mod6`. Write `d=7w+5`.
It follows that `w` is a positive integer and `w=4 mod6`. Set `x=10^w`.
Then `L=9w+7`, `L'=6561w+4687`, and `2dk=14kw+10k`. Cancellation of
the two position terms proves the **exact integer identity**

```
F(L',s')-10^(2dk)*F(L,s)=H_k(10^w),
H_k(X)=7*10^4687*X^6561-25
       -10^(10k)*X^(14k)*(7*10^7*X^9-25).
```

There is no zero-value exception. Indeed for every `0<=k<=468`,

```
H_k(10^w)=7*10^(L+2dk)*(10^(2d*(468-k))-1)
          +25*(10^(2dk)-1)>0.
```

Both summands are nonnegative, the first is positive unless `k=468`,
and the second is positive unless `k=0`. A pair of full witnesses
therefore forces `7^(L-2)|H_k(10^w)`, using the **smaller** threshold.
An isolated witness supplies only one divisible F and imposes no such
divisibility on H.

## 2. Uniform bound on the eliminant

For each of the nine k, the polynomial has degree 6561. Differentiation
at the 49 eligible `w mod294` gives **H'_k(10^w)=49 mod343** in every
case, hence exact derivative valuation two. The two implementations use
respectively automatic differentiation of the factored expression and
an independent finite difference of the expanded polynomial modulo `343^2`.
Periodicity of `10^w`
modulo 343 certifies all possible w, not just small exponents.

The complete analytic details and exact numerical inequalities are in
[LOGARITHMS.md](LOGARITHMS.md). In summary, if `t=v7(H_k(x))>=5`, strong
Hensel lifting supplies an algebraic root `alpha in Q_7` with

```
v7(x-alpha)=t-2>2, v7(H'_k(alpha))=2,
t=2+v7(x-alpha).
```

This is an equality, not a lower estimate. Taylor expansion at x shows
the linear term has valuation `2+v7(x-alpha)` strictly below every
quadratic and higher term. Positivity above ensures `x!=alpha`.

The degree and height bounds are uniform in all nine polynomials:
`[Q(alpha):Q]<=6561`, `||H_k||_1<10^4688`, and
`h(alpha)<=log||H_k||_1`. When 10 and alpha are multiplicatively
independent, apply Bugeaud--Laurent Corollary 2 to `10^6,alpha^6`,
exponents `(w,1)`, `p=7`, and height parameters `log A1=15`,
`log A2=70000`. Both bases are principal units; sixth powers preserve
the distance valuation. The local field is Q_7, and the global degree
parameter is at most 6561.

In the dependent case take an integer-normalized place above two,
`e=v(2)`, `r=v(alpha)`. The polynomial gives
`-4687e<=r<0`, `e<=6561`. Dependence gives
`alpha^(6e)=10^(6r)`, since the roots of unity in Q_7 have order
dividing six. In particular `ew-r>0`, so the resulting difference
does not vanish. Lifting the exponent yields
`v7(10^w-alpha)<=1+v7(ew-r)` (the proof records a slightly sharper form).

Both cases, as well as the elementary case `t<=4`, prove

```
v7(H_k(10^w)) <= 10^30*(a+20)^2.
```

Exact integer inequalities show this is **strictly less than L-2**
for all integers `a>=100`. The base comparison is
`7*10^30*120^2+10<3^100`; induction works because
`3*(a+20)^2>(a+21)^2`. Thus no adjacent pair can start at an
admissible exponent at least 100.

## 3. Every remaining start, including the cutoff-crossing pair

The admissible starts below 100 are exactly
`31,37,43,49,55,61,67,73,79,85,91,97`.
All are among PR #28's 256 individually excluded members. The new
independent original-word checker recomputes their unique joint classes
and exclusion residues and compares them with those inherited rows.
At a class miss there is no actual candidate; otherwise a nonzero residue
at depth at most `L-2` excludes the original decimal word.
In particular a=97 itself fails, so the pair **97,103** crossing the
cutoff is covered without assuming a=103 is below 100. This completes
the theorem for every `u>=0`.

## 4. Logical boundary

This strengthens the inherited three-successive-member theorem to a pair
obstruction. It permits isolated full witnesses whose two neighbours fail.
There is no implication here from an individual full witness to a second
one, nor to `7^(L-2)|H_k(10^w)` when its neighbour fails. Therefore the
universal individual-family conclusion remains open. The separate
[a=1567 calculation](INDIVIDUAL.md) is one more excluded length, not an
extension of consecutive whole-length coverage.
