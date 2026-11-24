# Effective bounds when either position or gap is small

This is an **ordinary mathematical proof**, conditional only on the cited
published logarithm estimate. It is not a Lean formalization. The finite
arithmetic used with the proof is identified separately below.

Let `L >= 5` be odd, `3 <= i < L`, `i = 3 (mod 6)`, and set

```text
F = 7*10^L - 18*10^i - 25,
g = L-i,
M(L) = max(log L + 2, 20).
```

Here `g` is an even integer at least 2; logarithms are natural. Every pair
satisfying even the weaker condition `7^(L-2) | F` satisfies both

```text
L-3 <= 63*(i+1)*M(L)^2,
L-2 <= 63*(g+1)*M(L)^2.                 (1)
```

These bounds track the dependence on the changing position and gap. Their
right sides are not constants independent of the pair.

## Source and hypotheses

Use Bugeaud–Laurent, *Minoration effective de la distance p-adique entre
puissances de nombres algébriques*, Corollary 1, printed p. 4, with the
definitions on printed pp. 2–3:
[original 29-page PDF](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf).
The source was opened and its statement checked on 24 November 2026.
The same corollary is reproduced in [the merged audit](../FIXED_POSITION.md).

For rational, multiplicatively independent 7-adic units `alpha_1,alpha_2`,
positive integer exponents `b_1,b_2`, and
`log A_j >= max(h(alpha_j),log 7)`, it gives

```text
v_7(alpha_1^b_1-alpha_2^b_2)
 <= 168/(log 7)^4 * log A_1 * log A_2
    * max(log b' + log log 7 + 0.4, 10 log 7, 10)^2,
b' = b_1/log A_2 + b_2/log A_1.
```

Both rational numbers lie in `Q_7`, so the source parameters are
`e=f=D=1`; Corollary 1 has already replaced its auxiliary `g` by
`7-1`. That auxiliary parameter is unrelated to our gap `g`.
For a reduced rational number `a/b`, its height here is
`log max(|a|,|b|)`; the source does not require `alpha_2 > 1` in the real
absolute value.

## Position-dependent estimate

Put `C_i=(18*10^i+25)/7`. Since `i=3 (mod 6)`, this is a positive integer,
and `F=7*(10^L-C_i)`. If `7 | C_i`, then `v_7(F)=1`, immediately excluding
the weaker condition. Otherwise use

```text
alpha_1=10, alpha_2=C_i, b_1=L, b_2=1,
A_1=10, A_2=10^(i+1).
```

Both numbers are 7-adic units. Also `C_i` is odd and `v_5(C_i)=2`: after
factoring 25 from its numerator, the remaining factor is 1 modulo 5.
If `10^r*C_i^s=1` for integers `r,s`, its 2-adic valuation gives `r=0`,
and its 5-adic valuation then gives `s=0`. This proves multiplicative
independence and in particular excludes a zero logarithmic difference.

The height conditions follow from `C_i < 10^(i+1)` and `10 > 7`.
Since `log 10 > 2`,

```text
b' = L/((i+1)*log 10) + 1/log 10 < L/8 + 1/2 < L.
```

The certified logarithm enclosures in [log_bounds.py](../log_bounds.py)
give the exact rational comparison

```text
168*(2.30258510)^2/(1.94591014)^4 < 63.     (2)
```

Further, `log log 7+0.4 < 2` and `10 log 7 < 20`. Thus the corollary
implies `v_7(F)-1 <= 63*(i+1)*M(L)^2`. The necessary lower bound
`v_7(F) >= L-2` proves the first inequality in (1).

## Gap-dependent estimate

Put `D_g=7*10^g-18`; then `F=D_g*(10^i-25/D_g)`. Use

```text
alpha_1=10, alpha_2=25/D_g, b_1=i, b_2=1,
A_1=10, A_2=10^(g+1).
```

We have `D_g >= 682`, `7` does not divide `D_g`, and
`gcd(25,D_g)=1`. Both rational numbers are 7-adic units. Since `g>=2`,
`v_2(D_g)=1` and `v_5(D_g)=0`. Consequently the 2- and 5-adic
valuations of `10^r*(25/D_g)^s=1` give respectively `r-s=0` and
`r+2s=0`. Hence `r=s=0`, verifying multiplicative independence.

The reduced fraction `25/D_g` has height `log D_g`, and
`D_g < 10^(g+1)`, so the height conditions hold. Moreover

```text
b' = i/((g+1)*log 10) + 1/log 10 < i/6 + 1/2 < L.
```

Using (2) and the same maximum bound gives
`v_7(F) <= 63*(g+1)*M(L)^2`, since `v_7(D_g)=0`. This proves the
second inequality in (1).

## An explicit all-length edge consequence

Set `N=10,000,000`. If either `i+1 <= 396` or `g+1 <= 396`, its
corresponding right side in (1) is at most

```text
B(x) = 63*396*max(log x+2,20)^2.
```

We prove `B(x) < x-3` for every real `x >= N`, including the switch of
the maximum. Write `x_0=exp(18)`. Since
`log N=7 log 10 < 18`, we have `x_0>N`.

For `N <= x <= x_0`,

```text
B(x)=63*396*400=9,979,200 < 9,999,997 <= x-3.
```

For `x >= x_0`, put
`H(x)=x-3-63*396*(log x+2)^2`. Then

```text
H'(x)=1-126*396*(log x+2)/x.
```

The ratio `(log x+2)/x` has derivative `-(log x+1)/x^2<0` there.
It follows that

```text
H'(x) >= 1-997,920/x_0 > 1-997,920/N > 0,
H(x_0)=x_0-3-9,979,200 > 0.
```

This proves the strict inequality on the second branch as well.
Therefore no weaker-condition pair with `L >= N` can have `i <= 395`
or `L-i <= 395`.

Combining this analytic result with a certified exclusion of all residual
pairs at odd lengths `5 <= L <= N` proves an all-length exclusion for
each of those two edge regions. The finite search and its independent
checks are recorded in this directory; this paragraph uses their stated
coverage, rather than deriving it from the analytic estimate. The largest
admissible position in the first region is `393` (positions are 3 modulo
6); the largest admissible gap in the second is `394` (gaps are even).

## What remains

After that finite exclusion and these edge bounds, any weaker-condition
survivor must have

```text
L > 10,000,000, i >= 399, L-i >= 396,
```

as well as the original odd-length, position, and modulo-49 restrictions.
In fact the modulo-49 table sharpens the position bound to `i >= 417`:
the first three positions `399,405,411` have residues `21,27,33` modulo
42, none of which appears in the table. Position `417` has residue 39
and remains compatible when `L=1 (mod 6)`.
The full problem imposes the further conditions in
[FULL_DIVISOR.md](FULL_DIVISOR.md).

Neither (1) nor the edge consequence bounds `L` when both `i` and `L-i`
grow proportionally to `L`: the displayed upper bounds can then exceed
the necessary valuation. The merged Evertse argument still gives
finiteness without a numerical maximum. No all-length exclusion of the
whole subclass, or verified witness, follows from these results.
