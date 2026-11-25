# The single high-depth position and the unresolved escape bound

These are elementary ordinary mathematical proofs, not Lean statements.
The starting commit is `b6db8703afd3d32211fd75de9ce1e34440dddfe8`,
the actual merge of PR #14; its audited research parent is
`22ef46d55fa903b54e0b288a1b38ba0a6fa0659a`.
No theorem below proves the all-length exclusion or gives a global cutoff.

## 1. Exact domain and divisor

The inherited reduction leaves a decimal word of length L with two fives,
at positions 0 and i, and sevens elsewhere. Here position 0 is the units
position. On the broader domain used in this note,

```
L >= 5 odd, 3 <= i < L, S=7L-4, 5 does not divide S,
F(L,i)=7*10^L-18*10^i-25,
n=F/9, P=25*7^(L-2).
```

Every actual word has suffix 775, so `v_5(n)=2`. If `5 | S`, the original
condition `PS | n` requires at least three factors of five and is impossible.
This is why that complementary length class is removed before using
coprimality. Also `S=3 mod7`, and S is odd. Thus on the displayed domain
`gcd(25,S)=1`, `gcd(7,9S)=1`, and `25 | n`. Consequently

```
PS | n  <=>  225*S*7^(L-2) | F
        <=>  9S | F and v_7(F) >= L-2.              (1)
```

The factor nine is retained even when `3 | S`. The exact target is to
prove `v_7(F)<=L-3` for every remaining full-sum pair. All the inherited
necessary restrictions and exclusions summarized in [README.md](README.md)
remain in force for potential witnesses. The lemmas here deliberately
apply to a broader domain and therefore do not remove any of them.

## 2. Order, representatives and the uniqueness threshold

Put `T_k=6*7^(k-1)` for `k>=1`. Direct residues give order six for 10
modulo seven, and `10^6=1+7 mod49`. The binomial theorem gives
`v_7(10^(6m)-1)=1+v_7(m)` for positive m: multiplying m by seven raises
the valuation by exactly one, and multiplying it by an integer coprime
to seven preserves it. Hence

```
ord_(7^k)(10) = T_k.
```

This equals the number of units modulo `7^k`, so 10 generates that entire
group. The target `(7*10^L-25)/18` is a unit modulo seven. Division by 18
means multiplication by its modular inverse. There is exactly one exponent
class, with least nonnegative representative `r_k=r_k(L)`, satisfying

```
18*10^r_k = 7*10^L-25 (mod 7^k),  0 <= r_k < T_k.   (2)
```

Define `K=K(L)` to be the least positive integer with `T_K>L`. It exists.
Moreover `K<=L-2` for every integer `L>=5`: at L=5,
`T_(L-2)=294>5`, and increasing L by one multiplies that period by seven,
which preserves its strict excess over the new length. This proves the
bound without a floating-point logarithm or an endpoint convention.

If `v_7(F(L,i))>=K`, then (2) gives `i=r_K mod T_K`. Because
`0<=r_K<T_K` and `3<=i<L<T_K`, necessarily

```
i=r_K, 3<=r_K<L.                                  (3)
```

Thus if r_K is outside this interval, the entire length is excluded from
(1). If it lies inside but `F(L,r_K)` is nonzero modulo **9S**, the whole
length is also excluded: every other position already fails the power
`7^K`, and `K<=L-2`. This is a necessary rejection criterion for each
specified length, not a universal rejection theorem.

At the final threshold one may use the sharper width `L-4`:
`T_(L-2)>L-4` implies at most one actual position. This is consistent with
(3); it does not exclude that position.

## 3. Exact lifts and the required zero run

Reduction from level k+1 to k preserves the exponent class, so there is
a unique `a_k in {0,1,...,6}` with

```
r_(k+1)=r_k+a_k*T_k.                               (4)
```

For an explicit exact computation let `m=7^k`,
`c_k=(10^T_k-1)/m mod7`, and `y=18*10^r_k`.
The order theorem says `c_k!=0 mod7`. Equation (2) makes the integer
`D_k=(7*10^L-25-y)/m` well-defined. Expanding modulo `7m` gives

```
a_k = D_k * (y*c_k)^(-1) mod7.                     (5)
```

All inverses are of units. Negative values of D_k cause no difficulty;
the chosen remainder is in `0..6`. The formula can be evaluated using
modular powers and division of residues whose difference is divisible
by m; it does not require allocating the full decimal word.

Suppose r_K is actual and passes the full digit sum. For every `k>=K`,
`T_k>L`. Therefore the first nonzero a_k gives `r_(k+1)>=T_k>L`.
All later least representatives are at least this large by (4), so no
actual position remains. If instead

```
a_K=a_(K+1)=...=a_(L-3)=0,                         (6)
```

then `r_(L-2)=r_K`, and (1) gives a full witness. Thus (6), together with
the actual-position and full-sum checks, is an exact witness criterion.
For a starting position of exact depth `t>=K`, the first nonzero lift is
`a_t`; it has exactly `t-K` preceding zero lift digits. The required
exclusion is `t<=L-3`, equivalently a nonzero lift with
`K<=k<=L-3`. Finiteness of t follows from `F>0`, but does not prove this
upper bound. Rewriting the valuation as (6) does not settle it.

## 4. A sharper stabilization lemma for the digit-sum order

The following refinement uses the special relation `S=7L-4`. It explains
what the varying digit sum can and cannot contribute through exponent
CRT compatibility. It is not a valuation bound.

Let `d=ord_S(10)` and `e=v_7(d)`. Then

```
e <= K(L)-1.                                      (7)
```

**Proof.** When e=0 this is immediate because K>=1. Suppose e>=1.
Factor S into odd prime powers `q^b`. None has q=7. By the ordinary CRT,
d is the least common multiple of the orders modulo these prime powers.
Hence for some q the order modulo `q^b` has 7-adic valuation e. Euler's
theorem bounds that order by a divisor of `q^(b-1)*(q-1)`. Since q is
not seven, `7^e | q-1`. The odd prime q therefore satisfies
`q>=2*7^e+1`. Also `S/q` is a positive odd integer congruent to 3 modulo
seven, because S is 3 modulo seven and q is 1 modulo seven. In particular
`S/q>=3`. These facts imply

```
7L-4=S >= 3q >= 6*7^e+3,
6*7^(e-1) <= L-1.                                 (8)
```

If e>=K, (8) would give `T_K=6*7^(K-1)<=L-1`, contradicting
`T_K>L`. This proves (7). No hypothesis about a prescribed prime
factorization of S or about 10 generating its unit group was used.

Now define the full-sum exponent class carefully. With
`R_L=(10^L-1)/9`, the identity

```
n=7R_L-2-2*10^i
```

gives `S | n` if and only if
`10^i=u mod S`, where `u=(7R_L-2)*2^(-1) mod S`. Only 2 is inverted;
9 is not cancelled modulo S. If u is not in the subgroup generated by
10 modulo S, there is no full-sum position. Otherwise exactly one
exponent class `s mod d` gives all full-sum positions, including both
parities. This is the class proved in the PR #14
[whole-length audit](../whole-length/PROOF.md).

The simultaneous exponent congruences at depth k are

```
i=s mod d,  i=r_k mod T_k.
```

They have an integer solution, with no upper bound on i, precisely when
`s=r_k mod g_k`, where

```
g_k=gcd(d,T_k)=gcd(d,6)*7^min(e,k-1).
```

By (7), `g_k=gcd(d,6)*7^e` for **every k>=K**. Also each lift changes
r_k by a multiple of T_k and therefore by a multiple of this stabilized
gcd. Consequently compatibility at depth K implies compatibility at
every later depth. In particular, if the actual r_K passes the full sum,
no later level can reject it merely by a new incompatibility in this
unrestricted exponent CRT system.

This does **not** say that the lifted least representative remains
sum-compatible or actual. A compatible exponent may be r_k plus a huge
multiple of T_k. The complete joint class has period `lcm(d,T_k)`; its
least representative may exceed L. The theorem isolates the issue:
after the initial full-sum check, a successful global argument still has
to force bounded-position escape, or otherwise rule out the exact value
of F. Compatibility stabilization supplies no bound for that escape.

## 5. Why the available size bound misses the target

For an actual full-sum position, `225S | F` and `7` divides none of
225S. Thus, with `t=v_7(F)`,

```
225*S*7^t <= F < 7*10^L,
t < (L*log(10)+log(7)-log(225S))/log(7).            (9)
```

The leading coefficient `log(10)/log(7)` exceeds one. Since `S=7L-4`
contributes only a logarithmic subtraction, (9) eventually exceeds the
required threshold L-2. It cannot force a nonzero lift in the interval
in section 3. The known effective edge, midpoint and rational-centre
bounds give stronger results on their named regions, but their
complement remains as stated in [README.md](README.md).

The inherited uniform `v_7(F)=o(L)` proves that (6) eventually fails;
it does not provide an effective starting length, locate all exceptions,
or show their absence above the consecutive certificate. The sharper
stabilization lemma does not change that effectivity boundary.

The missing additional arithmetic ingredient is a **uniform, effective
bound for the valuation at the bounded sum-compatible r_K**, or an
independently proved reason that this position cannot exist for every
remaining length. A lower bound on the nonzero p-adic distance in (2)
with enough strength and constants independent of L and i would suffice.
No such bound is proved here. There is no new numerical cutoff and no
unchecked finite interval presented as a completed exclusion.
