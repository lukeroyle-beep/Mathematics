# Five-twelfths strip and unconditional exact-line audit

25 November 2026. **All three deductions pass:** the closed strip is
excluded for full witnesses, the modular certificate is exhaustive, and
their combination excludes every admissible position on `12i-5L=-1`
without a Fermat hypothesis. These are ordinary mathematical proofs and
exact finite arithmetic, not new Lean formalizations.

| Deduction | Verdict | Exact scope |
| --- | --- | --- |
| Strip | Verified as written | Every full witness has `abs(12i-5L)>L/10^9` |
| Modular certificate | Verified as written | Exactly one exponent class modulo `242121642` passes `7^10` |
| Combined line theorem | Verified as written | No full witness at `(L,i)=(12u+5,5u+2)` for any integer `u>=1` |

For odd `L>=5`, `3<=i<L`, set `S=7L-4` and
`F=7*10^L-18*10^i-25`. The full condition remains
`225*S*7^(L-2) | F`. The new argument uses only its necessary condition
`v_7(F)>=L-2`; neither a Fermat test nor `9S|F` is needed.

## Baseline and preservation

The actual starting commit of this fresh clone and branch
`audit/a398769-five-twelfths-strip` is
`b7659c9c25ef6b339ee3c1de17b1938429b9af9e`, current `main` at startup.
GitHub confirms that it is the merge of
[PR #17](https://github.com/lukeroyle-beep/Mathematics/pull/17), whose head
was `26b79b0fb5c4623e657aca40e34ba95214b5833d`. Both exact commits were
checked as ancestors. There were no later main commits at startup. A fresh GitHub readback
before publication still selected the same main commit; no later change
needed reconciliation.

The audit read the general rational-centre estimate in
[COVERAGE.md](../proportional/COVERAGE.md), its theorem hypotheses in
[AUDIT.md](../proportional/AUDIT.md), the exact divisor and conditional
line result in [PROOF.md](../prime-factor-audit/PROOF.md), and broad (E)
and inherited coverage in [README.md](../early-rejection/README.md).
All inherited research files, Lean files, dependency pins and receipts
are preserved byte for byte. The only inherited edit is root README
navigation. Existing checkouts are untouched; no repository or ancestor
`AGENTS.md` applied. This repository has no GitHub Actions workflows.

## Proof and independent calculations

[PROOF.md](PROOF.md) derives the span and height inequalities, verifies
the simple root for either sign of `s`, checks the actual logarithmic
maximum, and handles multiplicative dependence including degree seven.
It checks both ranges and the closed endpoints. The exact independent
root coefficient is `0.6096384`; its margin below `L-2` at `L=10^9`
is `390361598` and increases thereafter. Below `10^9` the strip contains
no admissible pair, by parity alone.

[COMPUTATION.md](COMPUTATION.md) describes two unseeded, independent routes:
all polynomial roots modulo seven followed by Hensel lifting and discrete
logarithm, and all six exponent classes modulo six followed by lifts
evaluating the original `F` directly. Both recover:

```
7^10 = 282475249
ord_(7^10)(10) = 242121642
u = 185987897 (mod 242121642)
10^185987897 = 213654628 (mod 282475249)
least positive eligible L passing this necessary test = 2231854769
```

The class is exhaustive, not merely a successful substitution. The least
representative has `v_7(F)=10`, a positive control that is far below its
full-witness threshold. The modular test alone excludes line positions
with `17<=L<2231854769`. In particular it covers `L<10^9`; for `L>=10^9`
the line has `abs(delta)=1<=L/10^9` and the strip applies. Thus every
admissible line position is excluded.

## Precisely what changes in coverage

This adds a closed ratio strip of radius `1/(12*10^9)` around `5/12`,
and removes the Fermat restriction from the **full-witness** exclusion
on the exact line. In the previous six open ratio intervals it splits
only `(4000001/10000000,59999/120000)` into

```
(4000001/10000000, 4999999999/12000000000)
(5000000001/12000000000, 59999/120000).
```

All other intervals, fixed strips and discrete filters remain applicable.
Neither statement excludes every position of an eligible length.
No new whole-length exclusion or consecutive interval is claimed.
Consecutive full-witness coverage remains **1 through 10,000,000 inclusive**;
the three separate giant isolated exclusions and the infinite fixed-depth
whole-length families retain their inherited scope.

Broad (E) is the implication `9S|F => v_7(F)<K(L)`, for all positions
and odd five-free lengths, where `K(L)=min{k>=1:6*7^(k-1)>L}`. Its
certified consecutive range remains every odd `L` from **5 through
9,999,999 inclusive**. The new bound `v_7(F)<L-2` is weaker than the
required `v_7(F)<K(L)` and supplies no all-length (E) theorem, even when
restricted to this line. No new consecutive whole-length (E) coverage
is certified here.

There is a bounded, **position-only** stronger consequence of the modular
lift table: every admissible line position with `L<2231854769` satisfies
`v_7(F)<K(L)`, regardless of the digit-sum test. At each depth `k=2..10`,
the first permitted line length exceeds `T_k`; thus `K(L)=k` forces
failure at depth k. For `T_10<=L<2231854769`, `K(L)>=11` and the depth-ten
test already gives `v_7(F)<10`. The aggregate checker verifies all these
finite comparisons. This is no claim about the other positions at those
lengths, nor an all-length (E) theorem on the line.

In particular, the new theorem does **not** establish `9S` never divides
`F` on this line. PR #17 established that stronger digit-sum rejection
under the hypothesis `10^(S-1)=1 (mod S)`; its conditional conclusion
is unchanged. Full witnesses are now excluded on the line regardless of
that hypothesis. Broad all-length (E), the all-length `{5,7}` subclass
and the wider digit-1 conjecture all remain open. No effective global
cutoff or new Lean theorem/build is claimed.

## Reproduction and review

From the repository root, run:

```sh
python3 research/a398769/five-seven/strip-audit/verify.py > /tmp/strip-verification.json
python3 -O research/a398769/five-seven/strip-audit/verify.py > /tmp/strip-verification-O.json
cmp /tmp/strip-verification.json /tmp/strip-verification-O.json
cmp /tmp/strip-verification.json research/a398769/five-seven/strip-audit/verification.json
git diff --check
```

The verifier runs all new arithmetic checkers normally and with `-O`,
compares their complete outputs with the committed receipts, compares the
two modular outcomes, and checks baseline preservation and the inherited
receipt verifier. Essential checks use explicit exceptions. Full commands
and exact results appear in [COMPUTATION.md](COMPUTATION.md) and
[verification.json](verification.json). The inherited large search is
not rerun: its preserved source/receipt integrity and small controls are
checked, with `fresh_full_runs=[]`.

[REVIEW.md](REVIEW.md) records the fresh independent review of the proof,
arithmetic, implementation and coverage. Delivered as a draft pull request;
merging remains with the owner.
