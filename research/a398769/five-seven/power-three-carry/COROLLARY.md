# A stronger denominator consequence of PR #30

**Corollary.** Every full witness in the family `a=31+6u`, `u>=0`,
with its actual position `s=s_a`, satisfies

```
q^61 > L^20,       q = L/gcd(L,s_a).
```

This is a corollary of the valuation bound merged in PR #30 and the
259 certified earlier members, not a new general logarithm estimate.
It excludes the specified infinite range `q^61<=L^20` even when both
neighbours fail. It leaves `gcd(L,s_a)=1`, hence `q=L`, possible.

## Large exponents: strict comparison with the witness threshold

The merged [common-factor theorem](../power-three-individual/COMMON_FACTOR.md)
proves, at every actual sum-compatible position,

```
t = v7(F(L,s_a)) < 312000*q^3*(a+20)^2.               (1)
```

Suppose `q^61<=L^20`. Raising to the third power and taking positive
61st roots gives `q^3<=L^(60/61)`. Thus (1) yields

```
t < 312000*(a+20)^2*L^(60/61) < L/2 < L-2,            (2)
```

provided `L>(624000*(a+20)^2)^61`. The last inequality is strict because
every family length is greater than four. Thus (2) excludes the inclusive
witness threshold `t>=L-2`; it does not mistakenly demand `t>L-2`.

At `a=1585` the exact integer checks are

```
3^1585 > 7*(624000*1605^2)^61,
3*1605^122 > 1606^122.                               (3)
```

Their full integer sides and positive differences are retained in
[`corollary-checks.json`](corollary-checks.json). No logarithm or floating
point comparison controls these tests. For every integer `a>=1585`,

```
(a+21)/(a+20) <= 1606/1605,
((a+21)/(a+20))^122 < 3.
```

Set `R_a=7*624000^61*(a+20)^122`. The second line gives
`R_(a+1)<3R_a`. Inducting from the first check in (3) proves
`3^a>R_a` for every integer `a>=1585`, including every admissible family
exponent. Since `7L=3^a+4`, this implies the required strict length
inequality and therefore (2).

## All smaller admissible exponents

The exponents below 1585 are exactly

```
31, 37, ..., 1579:  a=31+6u, 0<=u<=258,
(1579-31)/6 + 1 = 259.
```

Their certificates are the 256 paired rows from PR #28, the paired
`a=1567` row from PR #29, and the paired `a=1573,1579` rows from PR #30.
The checker compares each retained pair of independently generated
certificates, verifies exact ordered coverage without duplicates, and
then freshly checks every retained representative against `9S|F` and
the odd representative interval `[0,2*3^(a-2))`. The proved ternary
uniqueness theorem identifies those representatives; a new reconstruction
of all their ternary digits is not claimed.

There are 85 class misses and 174 actual positions. For each actual
position the checker reconstructs the original decimal blocks modulo
`25S` and successive powers of seven, using binary concatenation of
repeated sevens, and independently compares with sparse evaluation of
`F=9n`. All have `n mod25S=0`. Their exact valuation histogram is
`{1:152, 2:18, 3:3, 4:1}`, and every first nonzero residue occurs at
depth `t+1<=L-2`. In particular `a=1231` reaches exact `t=4`; this is a
nonzero control for the deeper calculation. The base `a=31` has `t=1`
and first nonzero residue `35 mod49`.

All 259 lengths therefore fail unconditionally. This completes every
finite case below the analytic cutoff, including ones outside the
specified denominator range. No depth-capped survivor is counted as
excluded, and no historical large length enumeration is rerun.

## What the bound does and does not say about a carry

At an actual position the first failed seven-power divisibility test is
at depth `t+1`. Equation (1) supplies an effective bound depending on
`q`, but it beats the witness deadline only when its numerical right
side is small enough. In the range proved above, `t<L-2` forces a
failure by depth `L-2`, independently of any preceding-length valuation.
When the increment root already equals the actual increment at depth
five, the first nonzero lift digit is indexed by `m=t`; thus it occurs
by `m=L-3` in this range.

For `q=L`, (1) is of order `L^3*(a+20)^2`, greater than the required
linear threshold. This corollary supplies no bound forcing a mismatch
in the remaining range `q^61>L^20`; in particular it does not close the
individual moving-position problem. These denominator ranges describe
an infinite domain of the exclusion theorem, not a claim that the
actual ternary representatives populate that domain infinitely often.

## Reproduction

From the repository root:

```sh
pt=research/a398769/five-seven/power-three-carry
PYTHONDONTWRITEBYTECODE=1 python3 "$pt/corollary_checks.py" --check "$pt/corollary-checks.json"
PYTHONDONTWRITEBYTECODE=1 python3 -O "$pt/corollary_checks.py" --check "$pt/corollary-checks.json"
```

The deterministic receipt binds this proof, its checker, the merged
valuation proof, and all six inherited certificate inputs. It records
fresh finite validations separately from inherited representative
construction. All checks use explicit exceptions and remain active
under `python3 -O`. No Lean proof or build is claimed.
