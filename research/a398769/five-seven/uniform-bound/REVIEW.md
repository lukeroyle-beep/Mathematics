# Fresh independent review

Builder context: `/root`, with mathematical contributors `/root/lifts`
and `/root/analytic`. Independent reviewer context: **`/root/review`**.
The reviewer did not write the proofs and used an independently structured
arithmetic checker. This is a fresh AI-agent mathematical/code review,
not external human peer review or Lean formalization.

## Reviewed conclusions

The independent review checked:

- The exact full divisor, retained factor nine, representative reduction,
  and `L-2>=K` whole-length implication.
- The K=9 and K=10 bases, induction persistence, and both endpoints of the
  lift criterion; first nonzero `a_t` means exact valuation t.
- The sharper sum-order bound and its scope, the stable CRT obstruction,
  the full-sum cofactor identity, and the all-L size-method obstruction.
- Both polynomial identities, content, root height and actual degree;
  all derivative branches, including counterexamples to a universal d=1.
- Original Bugeaud--Laurent formula pages, every Corollary 1 and Theorem 4
  hypothesis and constant, the uniform derivative estimate, and the
  strict Hensel hypothesis and valuation loss from Conrad Theorem 4.1.
- Multiplicatively independent and dependent cases, including the
  `-v7(D)` correction and the bound `B_K+K+1<L-2`.
- The effective fixed-offset and rational-strip thresholds, their
  persistence and finite-gap obligations; all-ten-table envelope
  obstruction for actual rational pairs, without assuming those pairs
  meet the digit-sum or bounded-representative premises.
- Source versions, decisive modular certificates, retained baseline
  receipts, computation scopes, coverage and conjecture-status claims.

The reviewer read the original sources independently, checked their PDF
hashes, and inspected the rendered theorem/table pages. The independently
authored [checker](review_check.py) is preserved byte for byte from the
reviewer's file; its complete [receipt](review_results.json) includes the
source hash. See [COMPUTATION.md](COMPUTATION.md) for the exhaustive finite
domains and modular Newton route.

## Findings and resolutions

No must-fix mathematical error was found in the submitted proofs. Three
clarity/scope findings were resolved before final delivery:

1. The sufficiency margin and derivative bound initially reused a symbol.
   The cutoff margin is now `M_K`; the derivative bound is `B_K`.
2. The source height wording now says maximum **absolute** coordinate.
3. The coverage record now explicitly identifies the new parameterwise
   position theorems. It does not say there are literally no new position
   results, and it does not turn them into whole-length exclusions.

During aggregate-checker integration, the parent also corrected a JSON
field lookup (`L` in an exception record versus `representative_L` in a
history row). That checker failure was resolved and the aggregate rerun;
no mathematical result depended on the failed run.

The final review covers the integrated proofs, code, outputs, navigation,
and exact final commit. Its immutable SHA is recorded in the draft PR's
**Reviewed commit** field and final delivery response, after the reviewer
has checked that commit. Keeping that binding outside the commit avoids
a self-referential commit hash in this file. Any substantive later change
requires a new commit review before delivery.

Final verdict: **no must-fix findings**. The strongest overall research
outcome is **no closing advance**, with proved uniform auxiliary bounds
and precisely delimited method obstructions. The quadratic valuation
target, broad all-length (E), the all-length subclass, and the wider
digit-1 conjecture remain unresolved. Merging remains with the owner.
