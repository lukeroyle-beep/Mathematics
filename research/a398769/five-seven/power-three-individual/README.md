# Isolated power-of-three witnesses: common factors and the remaining position

**A full witness must satisfy `q^4>L`, equivalently `gcd(L,s_a)^4<L^3`.**
This holds for every `a=31+6u`, `u>=0`, regardless of either neighbouring
length. The proposed constant and cutoff survive independent audit:
`t<312000*q^3*(a+20)^2`, with `q^4<=L` excluded analytically for a>=100
and all twelve smaller exponents covered by exact certificates.

**The remaining individual family is open.** The fixed-position index
map is a seven-adic isometry after division by 49 and has one surviving
class at every depth. The ternary definition of the actual position does
not currently force that position's index to miss the class before the
inclusive witness threshold. No effective cutoff for all remaining
positions and no counterexample was obtained.

The first two unchecked members are independently excluded:

| a | Unique joint position | Conclusion |
|---:|---|---|
|1573|`s_a>=L`, although `s_a=123 mod126`|Class miss; no actual candidate|
|1579|`3<=s_a<L`, `g=1`, `q=L`, `n mod25S=0`|`n mod49=14`, exact `t=1`|

Exact decimal L and s are in [INDIVIDUAL.md](INDIVIDUAL.md) and both
machine receipts. With inherited certificates, **259 named family lengths**
are excluded: every `a=31+6u`, `0<=u<=258`, through **a=1579**.
There are 85 class misses and 174 actual candidates, with valuation
histogram `{1:152,2:18,3:3,4:1}`. The next unchecked exponent is **1585**.

## Proof and logical scope

- [COMMON_FACTOR.md](COMMON_FACTOR.md): depth-two equivalence, unit
  derivative, exact Hensel and sixth-power valuation, multiplicative
  independence, degree-weighted height, all Corollary 2 branches,
  exact induction and complete finite remainder; comparison with earlier
  rational-centre exclusions.
- [MOVING_POSITION.md](MOVING_POSITION.md): the exact identity
  `v7(F(L_u,s)-F(L_v,s))=2+v7(u-v)`, digit lifting, depth-three control,
  ternary relation `7q*kappa=4p mod d`, its lower-bound direction, and
  the precise missing universal mismatch estimate.
- [INDIVIDUAL.md](INDIVIDUAL.md): two reconstruction methods, full decimal
  representatives, original-word residues and retained positive controls.
- [SOURCES.md](SOURCES.md): authoritative base, theorem source and
  distinction between fresh calculations and inherited coverage.

The exact test throughout is `PS|n`, equivalently
`225*S*7^(L-2)|F`, with **9S|F at the same actual position**. After
the other factors pass, `t=L-2` already qualifies as a witness.

The former rational-centre theorem excludes exact ratios `s/L=p/q`
with `q<=K(L)^2` and also certain nonzero offsets. Here the exact-ratio
range extends to `q<=L^(1/4)` in this family. It does not imply that
every actual position lies in that range. The inherited adjacent-pair
theorem still allows an isolated witness whose neighbours fail.

Consecutive whole-length exclusion remains **1 through 1,000,002,000,000
inclusive**; the first unproved odd whole length is 1,000,002,000,001.
The unrestricted `{5,7}` subclass and the wider digit-1 assertion remain
**open**. No new Lean formalization, Lean build, or historical large
enumeration was performed. The arguments here are ordinary mathematical
proofs supplemented by exact finite computations.

## Reproduce all new arithmetic

From the repository root, using only Python's standard library:

```sh
pt=research/a398769/five-seven/power-three-individual
PYTHONDONTWRITEBYTECODE=1 python3 "$pt/verify.py" --run
PYTHONDONTWRITEBYTECODE=1 python3 -O "$pt/verify.py" --run
```

Each command runs all four arithmetic programs, checks their complete
output against retained bytes, compares every new member across the
two individual methods and four selected rows against a third method,
verifies the base archive and source hashes, reconciles all 259 named
family exponents, and rejects nine corrupted-receipt controls. Checks
raise explicit exceptions and remain active under `-O`.

The individual engines freshly reconstruct the twelve a<100 cases and
a=25,1231,1567,1573,1579. `root_log.py` explicitly reuses the inherited
Newton/logarithm implementation, whose exact source is bound by the base
manifest and receipt; `independent_decimal.py` imports no project code
and uses original decimal blocks and all-three-child ternary lifting.
It includes 2,015 literal-word checks, a complete small-position
enumeration and the lost-factor-nine negative. `index_lift.py` has a
third independent modular-root/ternary calculation and compares digit
lifts to direct exponentiation. The a=1231 **actual** depth-four control
tests the surviving side of the index-class condition.

`verification.json` binds every implementation document, source and
receipt. The independent final reviews are recorded separately against
the immutable implementation commit; their checks can be reproduced with:

```sh
python3 "$pt/review_check.py"
python3 -O "$pt/review_check.py"
```

Starting main was exactly PR #29's merge
`a9edeb0a96bd56d55f3c96767f5154e69cb8ceda`; no later main results were
present. All 1,067 inherited files are hash-bound, and every one except
the root README addition remains byte-identical. PR #29's aggregate and
source-bound review checks were rerun in both Python modes before that
addition. Historical receipt bindings have not been rewritten.

Draft publication only; merging remains with Luke.
