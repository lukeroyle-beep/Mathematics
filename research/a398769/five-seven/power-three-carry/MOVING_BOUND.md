# The first nonzero carry: proved bounds and the remaining gap

**The moving-position family remains open.** The one-step theorem
provides an exact test independent of both neighbours. It does not
prove that the first nonzero carry at a depth-five survivor occurs by
`L-3`. No universal exponent cutoff is obtained, and no full witness
is found. The explicit bounds below separate termination of a lift
calculation from a mismatch soon enough to exclude a witness.

## Bounds on a surviving actual position

Suppose the independently reconstructed position is actual and
`j_5=k`. In [ONE_STEP.md](ONE_STEP.md)'s notation its first nonzero
carry index is exactly `r=t=v7(F)>=5`. Positivity of the original
word gives `F>0`, so r is finite. The merged PR #30 theorem gives

```
q=L/gcd(L,s_a),
r < B(a,q)=312000*q^3*(a+20)^2.                    (1)
```

Since B is an integer, `r+1<=B`. Thus a completely explicit sufficient
inequality for failure by the required depth is

```
312000*q^3*(a+20)^2 <= L-2.                       (2)
```

This is a corollary of the merged bound, not a new logarithm estimate.
The stronger necessary condition `q^61>L^20` follows from (1) and
the finite certificates by the separate corollary in this directory.
It still permits `q=L`; then the right side of (1) is much larger
than L, and (2) fails. No gcd hypothesis is concealed in the one-step
theorem; it is the usefulness of (1) that deteriorates in this case.

The elementary size bound retains the full digit-sum factor:

```
25*3^(a+2)*7^r <= F < 7*10^L,
r < [L*log(10)-(a+2)*log(3)-log(25/7)]/log(7).     (3)
```

Its leading coefficient is `log(10)/log(7)>1`; the ternary saving
is linear in a while L grows exponentially in a. This proves an
effective upper bound on r, including when `gcd(L,s_a)=1`, but does
not prove `r<=L-3`. Merely running a lift to a fixed cap below the
first nonzero carry leaves that candidate unresolved.

## What several blocks can prove

There is a rigorous sufficient test using several consecutive blocks
of kappa and the inherited position bound. It is useful to state its
scope exactly; no theorem here says that all remaining candidates, or
infinitely many actual kappa prefixes, satisfy it.

Let `h>=1`, `A=a-6h>=31`, `T=3^(A-2)`, and `R=729^h`.
Repeated use of the odd-representative recurrence gives

```
s_a=s_A+2T*J, 0<=J<R,
L=(9RT+4)/7.                                       (4)
```

Suppose **all h intervening increments vanish**, equivalently `J=0`,
so `s_a=s_A`. Nonnegativity of the weighted increments proves this
equivalence without assumptions about valuations at intervening lengths.
The odd-representative range gives `s_A+1<=2T`.

The inherited [edge estimate](../settlement/EDGE_BOUNDS.md) proves
`t<=1+63*(s_a+1)*M(L)^2`, where `M(L)=max(log(L)+2,20)`.
For `a>=31`, `L<3^a` and `log3<2` give `M(L)<2(a+20)`. Hence

```
t < 1+252*(s_a+1)*(a+20)^2
  <= 1+504*T*(a+20)^2.                             (5)
```

The explicit integer condition

```
9*729^h >= 3528*(a+20)^2+1                         (6)
```

implies `(9R-3528*(a+20)^2)*T>17`, since `T>=3^29>17`.
Rearranging gives

```
1+504*T*(a+20)^2 < (9RT-10)/7 = L-2.               (7)
```

Equations (5)--(7) force `t<L-2`, and therefore the first nonzero
carry, if `j_5=k`, satisfies `r<=L-3`. This conditional block test
applies even for gcd one and when both neighbours fail. Its assumptions
are the exact zero-block condition in (4) and inequality (6), not
merely a count of inspected blocks. It is a sufficient test at every
admissible exponent where those assumptions hold, with no small-exponent
exceptions; it proposes no universal cutoff.

Two other constant runs preserve small geometric quantities. Write
`delta_a=L_a-s_a` and `e_a=L_a-2s_a`. At any one step, with previous
ternary modulus d, the exact identities are

```
delta_(v+6)-delta_v=2d*(468-k),
e_(v+6)-e_v=4d*(234-k).
```

Thus h consecutive increments equal to 468 preserve the gap,
`delta_a=delta_A`; h increments equal to 234 preserve the central
offset, `e_a=e_A`. Again these identities make no assumption on the
seven-adic valuation at an intervening length. In the 468 case,
current actuality implies `delta_A>0` as well. The representative
lower bound `s_A>=3` gives

```
delta_A+1 <= (9T-10)/7 < 9T/7.
```

The inherited gap estimate consequently gives
`t<324*T*(a+20)^2`. The exact sufficient condition

```
9*729^h >= 2268*(a+20)^2+1                         (8)
```

forces `t<L-2`, since `(9R-2268*(a+20)^2)*T>10`.

In the 234 case, `3<=s_A<=2T-1` gives, by checking both signs,

```
abs(e_A)+2 < 19T/7.
```

The inherited [central-offset estimate](../effective/ROUTE_A.md)
`t<=504*(abs(e_a)+2)*M(L)^2` therefore gives
`t<5472*T*(a+20)^2`. The sufficient condition is

```
9*729^h >= 38304*(a+20)^2+1.                        (9)
```

It again forces `t<L-2`, using `T>10`. These are three precisely
specified constant-block tests. They do not require gcd greater than
one, adjacency survival, or a cutoff with unchecked smaller exponents.

For arbitrary blocks, (4) allows `s_a`, `L-s_a`, and `abs(L-2s_a)`
all proportional to L. Their inherited bounds can then exceed L.
No covering theorem says every remaining prefix has one of the three
runs long enough for (6), (8), or (9). In particular, irrationality of
kappa neither ensures such runs nor says that the remaining prefixes
obey (2). None of these conditional tests is labelled an infinite
subfamily of *actual* prefixes without an infinitude proof.

## Why the defining ternary congruence has not closed the last case

For `g=gcd(L,s_a)`, `p=s_a/g`, `q=L/g`, the exact identity
`qs_a=pL` and `7L=9*3^(a-2)+4` imply

```
7q*kappa=4p mod3^(a-2).                            (10)
```

The inherited effective three-adic logarithm bound gives only

```
a < 1037232*max(log(q)+1,10)^2.                    (11)
```

It constrains q from below. It is compatible with `q=L`, and contains
no seven-adic carry. The same issue persists when several blocks are
recovered exactly: they determine the specific integer k, or J in
(4), but do not establish a bound on the seven-adic agreement of that
integer with the root in [ONE_STEP.md](ONE_STEP.md).

There is also no local-congruence inconsistency to exploit by merely
combining moduli. For fixed L and finite depth m, the seven-adic
position equation has one class `s=3 mod6` modulo `6*7^(m-1)`:
divide `18*10^s+25=7*10^L mod7^m` by the unit 18 and use
`ord_(7^m)(10)=6*7^(m-1)`. The target reduces to `-1 mod7`, so
its root exponent is `3 mod6`. Its congruence with the ternary class
modulo `d=3^(a-2)` is compatible modulo their gcd three, since
`kappa=0 mod3`. The generalized Chinese remainder theorem therefore
has an integer solution modulo `2d*7^(m-1)`. Such a solution usually
lies outside `[3,L)`; that is why the actual least representative,
not mere solvability of both congruences, matters. This observation
does not show that the actual representative survives, nor disprove
the possibility of a future effective bound.

An attempted elimination using the fixed algebraic relation has a
specific valuation loss. Put `U=18*10^s+25` and
`Z=U^7-7^7*10^4`. At an actual candidate the ternary relation gives
`v3(Z)>=a+2`. If `t>=2`, then `U/7=10^L=3 mod7` because `L=1 mod6`.
Consequently

```
Z/7^7=(U/7)^7-10^4=3-4=-1 mod7,
v7(Z)=7,                                          (12)
```

independent of how large t is. Thus this algebraic norm does not
transport the large seven-power valuation. Replacing the fixed seven
in (12) by t would be invalid.

Finally, the adjacent-pair theorem is a statement about two divisible
values of F. Its eliminant needs both. When the neighbours fail, no
large seven-power divisibility of that eliminant follows from the
single surviving value. Using the representative `s_b` in W is valid;
using its predecessor as a full witness is not.

The exact candidate set left by the new tests consists of the admissible
exponents beyond the certified finite endpoint for which the unique
position is actual, `q^61>L^20`, `j_5=k<=K`, inequality (2) fails,
and there is no h with `a-6h>=31` satisfying one of the three matched
run-and-size conditions (6), (8), or (9). All inherited additional
necessary conditions still apply. Defining this residual set does
not claim that it is nonempty or infinite.

The first unproved assertion is therefore explicit: for every such
remaining candidate, prove a nonzero `c_m` for some `5<=m<=L-3`, or
supply a universal exponent cutoff and fully certify every smaller
admissible member. Neither (10), (11), finite block recovery, the CRT,
nor the pair obstruction proves that assertion. The retained finite
exclusions do not turn this gap into a theorem. No Lean verification
is claimed.
