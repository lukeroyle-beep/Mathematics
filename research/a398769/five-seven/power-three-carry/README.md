# One-step moving-position audit

**The individual moving-position family remains open.** The one-step
seven-adic lift is proved, but no bound has been obtained that forces a
nonzero carry by index `L-3` for every actual ternary position. In
particular, the remaining case includes `gcd(L,s_a)=1` with both
neighbours failing. No universal cutoff or full witness is claimed.

For `a>=37`, writing `s_a=s_(a-6)+2*3^(a-8)*k` gives `0<=k<=728`;
an actual position requires `k<=K<=468`. At the current length,
`W(j)=F(L,s_(a-6)+2*3^(a-8)*j)` has exactly one zero class modulo
`7^(m-1)` at depth m, with next digit `c=-4*(W(j_m)/7^m) mod7`.
The preceding representative is used even if it exceeds its own length;
no preceding-length valuation hypothesis occurs. At depth five a
survivor must have `j_5=k<=K`. It then needs every digit indexed
`5,...,L-3` to vanish. The mathematical investigation identifies the
precise missing bound, and gives a sufficient bound for specified runs
of zero ternary blocks without claiming that they cover all positions.

The corollary **`q^61>L^20`**, where `q=L/gcd(L,s_a)`, holds for every
full family witness. It follows from PR #30's merged valuation bound
and the 259 certified earlier members. Both exact crossover inequalities
at a=1585 pass, and the finite remainder is completely accounted for.
The condition leaves `q=L` possible.

| a | k | K | j_5 | Exact t | First nonzero original n residue |
|---:|---:|---:|---:|---:|---|
|1585|450|468|922|1|28 modulo 49|
|1591|191|468|780|1|42 modulo 49|
|1597|92|468|2255|2|294 modulo 343|

All three positions are actual and satisfy `n mod25S=0`. Independent
ternary reconstruction and original decimal-block reconstruction agree.
The controls include `a=1579` (in-range root `j_5=119`, actual `k=205`),
`a=1231` (actual `k=377` survives through depth four, then `j_5=720>K`),
the inherited base a=31, a nonzero sum-positive a=25 control, and the
literal `(L,s)=(313,51)` lost-factor-nine control.

There are **262 excluded family lengths**, exactly `a=31+6u` for
`0<=u<=261`, through **a=1597**, with **a=1603 next**. They comprise
85 class misses and 177 actual positions, with exact valuation histogram
`{1:154,2:19,3:3,4:1}`. Coverage through a=1579 originated in inherited
paired certificates; this audit revalidates all 259 rows' arithmetic
and recovers them from a fresh high-precision kappa. The second original
ternary reconstruction is rerun for the explicitly listed selected
exponents, not for all 259.

Consecutive whole-length coverage remains **1 through 1,000,002,000,000
inclusive**. The unrestricted `{5,7}` subclass and wider digit-1
assertion both remain **open**. No Lean formalization or Lean build was
performed. No historical large length enumeration was rerun.

## Evidence and reproduction

- [ONE_STEP.md](ONE_STEP.md): exact increment theorem and inclusive carry deadline.
- [MOVING_BOUND.md](MOVING_BOUND.md): attempted ternary/block bounds and precise unresolved candidates.
- [COROLLARY.md](COROLLARY.md): stronger denominator bound and complete finite remainder.
- [EXACT_CERTIFICATES.md](EXACT_CERTIFICATES.md): full decimal L, s_b, s_a and exact certificates.
- [SOURCES.md](SOURCES.md): current-main reconciliation, implementation independence and evidence scope.
- [REVIEW.md](REVIEW.md): independent reviews bound to the implementation commit.

From the repository root, using the Python standard library:

```sh
pt=research/a398769/five-seven/power-three-carry
PYTHONDONTWRITEBYTECODE=1 python3 "$pt/verify.py" --run
PYTHONDONTWRITEBYTECODE=1 python3 -O "$pt/verify.py" --run
```

These commands reproduce all three new arithmetic receipts byte-for-byte,
check source/document hashes and inherited-tree preservation, reconcile
the finite ranges, and reject corrupted-certificate controls. All checks
remain active under `-O`. Individual receipts can also be reproduced by
running `certificates.py`, `corollary_checks.py`, and `one_step_checks.py`;
their stdout is the corresponding JSON receipt.

The exact predicate is always `PS|n`, equivalently
`225*S*7^(L-2)|F`. Both actuality and `9S|F` are required at the same
position; after the other factors pass, `t=L-2` already qualifies.
A program stopped at a depth cap raises an unresolved error and certifies
no exclusion. Draft publication only; merging remains with Luke.
