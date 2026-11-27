# Adjacent power-of-three members cannot both be witnesses

**For every u>=0, the lengths for a=31+6u and a+6 cannot both contain
a full witness.** The proposed pair argument is valid, including both
logarithm cases and the suggested cutoff. No false inference remains in
the pair proof. The universal individual-family assertion remains open:
the theorem supplies no condition on an isolated witness whose neighbours
fail. These are ordinary proofs and independently checked exact arithmetic.

## Proof and audit results

The [pair proof](PAIR.md) retains `PS|n`, equivalently
`225*S*7^(L-2)|F`, with **9S|F at the same actual position**. Equality
`v7(F)=L-2` already suffices for a witness.

- Actuality gives `0<=k<=468`. Complete depth-three tests visit every
  one of seven u classes and every increment, **3,283 comparisons** per
  implementation. The only possibilities are
  `42,91,140,189,238,287,336,385,434`.
- The exact positive eliminant H has degree 6561. A full pair forces
  `7^(L-2)|H(10^w)`, using the smaller threshold. One witness alone does
  not force this divisibility.
- All **441 derivative cases** give `H'(10^w)=49 mod343`. Three methods
  agree: automatic differentiation, finite differences, and expanded
  differentiation. The period and `w=4 mod6` restriction prove completeness.
- [Strong Hensel and both logarithm cases](LOGARITHMS.md) give
  `v7(H(10^w))<10^30*(a+20)^2<L-2` for every integer `a>=100`.
  Bugeaud--Laurent Corollary 2 was read from the primary source; the height
  parameters 15 and 70000 pass. Dependence is treated separately, including
  nonvanishing. The cutoff uses exact integers and induction.
- All twelve admissible starts below 100 are individually excluded by
  inherited certificates and a fresh original-decimal-block reproduction.
  The crossing pair **97,103** is covered.

The independently classified **a=1567** has its unique joint representative
inside the actual range, with `n modS=n mod25S=0` but **n mod49=7**.
Thus `v7(F)=1` and it is not a witness. The full exact representative,
length, sum and moduli are in [individual.json](individual.json), with
the representative also printed in [INDIVIDUAL.md](INDIVIDUAL.md).
The inherited Newton/root/log method, evaluated afresh at precisions
1568 and 1569, independently agrees with the newly authored ternary-lift
and original-block calculation. This adapter explicitly reuses inherited
arithmetic; it is not claimed to be a third newly written engine.

Together with the inherited enumeration, **257 specified lengths**
`a=31+6u`, `0<=u<=256`, through a=1567 are excluded. There are 84 class
misses and 173 actual candidates, with valuation histogram
`{1:151,2:18,3:3,4:1}`. The next unchecked individual exponent is **1573**.
This is sparse family coverage, not a consecutive interval of lengths.

## Reproduction, sources and inherited evidence

The task started from freshly fetched main
**42e6a151c5279905a3e02b859c6fae737178fd7d**, the requested PR #28 merge.
Its first parent is the supplied
`0a47180b889b392c2323bc1614a473af51f38d78`. No later main commits were
present. Work is on isolated branch `research/a398769-power-three-pair`.
[baseline.json](baseline.json) binds all **1,045** inherited files to
the exact Git archive. All 1,044 inherited files other than the root
README remain byte-identical; that README only gains the new entry.

From the repository root, using only standard-library Python:

```sh
pp=research/a398769/five-seven/power-three-pair
PYTHONDONTWRITEBYTECODE=1 python3 "$pp/verify.py" --run
PYTHONDONTWRITEBYTECODE=1 python3 -O "$pp/verify.py" --run
git diff --check
```

The aggregate verifier reruns all five programs in the invoking interpreter's
optimization mode, compares complete deterministic receipt bytes, compares
every independent modular row, validates the finite and new individual
cases, rejects nine corrupted-receipt controls, and binds all proof,
source, receipt and baseline files. No check uses removable assertions.
Without `--run` it checks retained receipts and bindings only.
The exact receipts are [pair-checks.json](pair-checks.json),
[independent-modular.json](independent-modular.json),
[logarithm-checks.json](logarithm-checks.json),
[individual.json](individual.json), and [root-log.json](root-log.json).

The a=25 sum-positive control and the literal `(L,s)=(313,51)`
lost-factor-nine negative are retained and freshly checked. Nine nonzero
strong-Hensel controls exercise exact valuation loss, including valuation
seven. They are synthetic permitted w values, not claimed family witnesses.
The primary PDF was downloaded afresh and hash-checked; the exact source
and acquisition commands are recorded in [SOURCES.md](SOURCES.md).

Before the root README addition, PR #28's aggregate `verify.py --run`
and source-bound `review_checks.py --check review-checks.json` were also
rerun normally and under `python3 -O`; all passed, including all 256
individual rows, the complete three-length computations, and 25,440
literal-word controls. Historical receipts bind their original root
README, so reproduce them at their original commit, rather than rewriting
their hashes to match this later entry. A fresh detached worktree is one
way to reproduce that exact state:

```sh
git worktree add --detach /tmp/a398769-pr28-repro 42e6a151c5279905a3e02b859c6fae737178fd7d
cd /tmp/a398769-pr28-repro
pt=research/a398769/five-seven/power-three
PYTHONDONTWRITEBYTECODE=1 python3 "$pt/verify.py" --run
PYTHONDONTWRITEBYTECODE=1 python3 -O "$pt/verify.py" --run
python3 "$pt/review_checks.py" --check "$pt/review-checks.json"
python3 -O "$pt/review_checks.py" --check "$pt/review-checks.json"
```

The trillion archive and adjacent interval remain inherited evidence;
their large enumerations were not rerun. See [REVIEW.md](REVIEW.md) for
independent mathematical review and the reviewed implementation commit.

## Separate verdicts

| Target | Verdict and remaining obligation |
|---|---|
| Adjacent pair, a and a+6 | **Proved for every u>=0**; no unresolved pair step |
| Every individual S=3^a member | **Open**; exclude an isolated actual candidate without assuming a neighbour survives; next unchecked a=1573 |
| Consecutive whole-length coverage | **1–1,000,002,000,000 inclusive**, unchanged; first unproved odd whole length 1,000,002,000,001 |
| Unrestricted `{5,7}` subclass | **Open**; reject every remaining actual position's full divisor, or exhibit a verified witness |
| Wider A398769 digit-1 assertion | **Open**; close all remaining no-digit-1 cases, including unrestricted `{5,7}` |
| Lean | **No new theorem, formalization, or Lean build performed** |

The inherited ineffective finiteness result does not locate or eliminate
isolated exceptions. Neither pair exclusion nor finitely many tested
members proves universal individual emptiness. The PR is a draft; merging
is left to Luke.
