# Baseline and dependency boundary

The starting commit is **`ecac4f73be7c19daff5ac931f0b7b9e2cd78b119`**,
freshly fetched from `origin/main` on 25 November 2026. GitHub identifies
this as [PR #19](https://github.com/lukeroyle-beep/Mathematics/pull/19)'s
merge commit. Both required commits are ancestors of the branch:

```
PR #19 merge: ecac4f73be7c19daff5ac931f0b7b9e2cd78b119
audited head: 47f1939a4f14f774cfbc0daa1e1f8e33e9c402ea
```

The merge tree equals the audited head's tree. Main had no later commits
at startup, so there were no intervening changes to reconcile.
Work uses a separate clone, `five-seven-uniform-bound`, and branch
`research/a398769-uniform-bound`. Existing research checkouts and their
branches were not changed. No applicable `AGENTS.md` was found in the
repository, the enclosing Mathematics directory, or its directory
ancestors. No GitHub Actions workflows were present at this baseline.

The following were read before preparing the research record:

- [Subclass reduction and navigation](../README.md).
- [Finite pairs](../FINITE_PAIRS.md), with the original Evertse source
  checked in [SOURCES.md](SOURCES.md), and
  [qualitative uniform bound](../effective/QUALITATIVE.md).
- [Early-rejection record](../early-rejection/README.md) and
  [proof](../early-rejection/PROOF.md).
- [Proportional audit](../proportional/AUDIT.md) and
  [coverage](../proportional/COVERAGE.md).
- [Five-twelfths strip proof](../strip-audit/PROOF.md).
- [PR #19 audit record](../three-deductions-audit/README.md),
  [depth proof](../three-deductions-audit/DEPTH.md), and
  [seven-twelfths proof](../three-deductions-audit/SEVEN_TWELFTHS.md).

Further dependencies followed include the
[settlement certificate](../settlement/README.md),
[exact full divisor](../settlement/FULL_DIVISOR.md),
[high-depth representative and stabilization proof](../high-depth/PROOF.md),
[its computational controls](../high-depth/COMPUTATION.md), and the
[whole-length proof](../whole-length/PROOF.md). The linked records retain
their historical dates, scopes and outcomes.

The initial reduction excludes zero, one, and at least three fives; it
also excludes even lengths. The remaining odd lengths and positions
satisfy the exact setup in [LIFTS.md](LIFTS.md). On `5` not dividing S,
the full test is **`9S|F` and `v7(F)>=L-2`**. Multiplication by nine is
not invertibility of nine modulo S; the nine cannot be dropped.

The following inherited facts are retained, not newly broadened:

| Inherited result | Scope |
| --- | --- |
| Consecutive subclass exclusion | All lengths 1--10,000,000 inclusive |
| Broad (E) finite certificate | Every odd L=5--9,999,999, all actual positions, five-free S |
| PR #19 depth-44 exception | Counterexample to unconditional `v7(F)<K`; digit-sum premise fails |
| Qualifying minus-line depths through 100 | 44, 56, 85, 92; all four exact gcds are one |
| Restricted minus-line (E) | Every admissible position on `12i-5L=-1` with `L<6*7^99` |
| Strips and opposite line | Their stated position-level exclusions only |
| Isolated and infinite whole-length exclusions | Each original named domain, without a consecutive-range extension |
| Evertse finiteness / qualitative `o(L)` | No numerical global cutoff |
| All-length (E), subclass, wider digit-1 conjecture | Open |

The verifier compares every baseline tracked file except root `README.md`
navigation byte for byte against this starting commit. It checks the
retained early-rejection source-bound receipts and their 100 matching,
gap-free blocks, plus the inherited certificate hash chain. It also
cross-checks the two retained PR #19 depth tables and all four exceptions.
The depth-44 and zero-run modular controls are freshly recomputed.
**Neither ten-million search is freshly rerun.** No retained certificate
is represented as a new execution or new coverage.
