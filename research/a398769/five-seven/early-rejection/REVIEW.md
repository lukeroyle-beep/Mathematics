# Independent review and evidence ledger

Date: 25 November 2026. Builder/coordinator context: `/root`.
The investigation follows the explicit user contract for all three objectives
and one draft PR. The owner retains the merge decision. There is no claim of
GitHub approval, a new Lean proof, or completion of either conjecture.

## Separate contexts

| Context | Independent work | Record |
|---|---|---|
| `/root/checker_a` | Built complete-cycle/direct-F implementation A before reading B; reviewed B and cross-compared all blocks | [Review A](COMPUTATIONAL_REVIEW_A.md) |
| `/root/checker_b` | Built linearized-lift/repunit implementation B before reading A; reviewed A and the integration verifier | [Review B](COMPUTATIONAL_REVIEW_B.md) |
| `/root/arithmetic_search` | Reconstructed arithmetic, declared and completed falsification scope, recorded proof obstructions | [Proof](PROOF.md), [routes](ROUTES.md), [scope](search_scope.json) |
| `/root/adversarial_review` | Fresh adversarial mathematical/computational review; independently recovered representatives and rechecked all smooth-family lengths | [Adversarial review](ADVERSARIAL_REVIEW.md) |
| `/root` | Checked inherited evidence and ancestry; inspected all new sources; integrated and reran verification; reviewed claims and delivery | This record and [verification](verification.json) |

The two required checkers share only the mathematical specification and
comparison format. They import neither one another nor inherited checker
arithmetic. Different digit-sum algorithms and representative recovery paths
are reviewed in the linked records. Source hashes identify exactly what was
checked; [artifacts.json](artifacts.json) binds the final report artifacts.

## Findings and resolution

One must-fix integration defect was identified in the first verifier draft:
implementation B's coverage fields live in its `audit` object, but the initial
verifier read them at the receipt root. It raised `KeyError: 'counts'` after
the checker runs, rather than yielding a false pass. The verifier now selects
that object explicitly. A fresh corrected `--recompute` invocation completed
all four full runs and every comparison successfully. The exact same receipt
checks also pass with the verifier itself run under `python3 -O`. The defect
never changed either checker, a count, a residue or an ordered digest.

A control-label improvement was also made before B's final runs: the shallow
positive control now computes and checks its depth zero and K=2, and the
`(23,15)` regression explicitly checks both residues modulo 49 and 343.
The final B receipt and both independent code reviews pin the corrected
source hash. No findings remain unresolved in the reviewed artifacts.

## Observed validation

* Both complete audits reproduce both reported count rows, with every odd
  length included. Full and prefix ordered hashes and all 100 block hashes
  agree. A and B each give identical ordinary/optimized receipts.
* Literal controls include both position parities, strict period equality,
  full-nine positive/negative tests, and the valuation regression. Unsupported
  inputs are rejected under normal and optimized Python.
* The corrected integration verifier freshly executed A and B normally and
  under `-O`, with byte-for-byte comparison against committed receipts.
  It verified 110 inherited proof/source/receipt/formalization/dependency files
  unchanged against the actual starting commit, and checked the prior receipt
  manifest's hashes. The inherited large computations were not rerun.
* The predetermined search completed normally and under `-O` with identical
  receipts. No factorization, logarithm or resource interruption is counted
  as exclusion. A fresh reviewer independently tried the seven possible
  lift digits at every step for all 2,731 smooth-family lengths and used a
  separate exact integer-quotient full-sum calculation; its ordered digest
  agrees with the search receipt.
* Local validation used Python 3.14.4 on Darwin arm64. Arithmetic uses Python
  integers; A's checked fixed-width array stores bounded exponents only.
  Markdown links, the scoped diff, generated evidence and whitespace were
  checked before publication. No secrets or unrelated changes were included.

## Mathematical assessment and completion boundary

The reviewers verified the exact full divisor, the necessity of retaining
nine, the broad-domain equivalence of E, uniqueness, `K<=L-2`, and the
inherited CRT stabilization argument. They checked that the main computation
uses none of the narrower witness filters and that all search claims match
their finite scopes.

**Primary verdict: no structural advance; finite evidence audited.**
The finite implication is certified for odd lengths 5 through 9,999,999.
No full-sum-compatible actual `r_K` with five-free S was found in the audited
interval or declared searches. Broad E has been neither proved nor refuted.
No new useful all-length restricted valuation theorem or effective cutoff
has been established. The subclass and wider digit-1 conjecture remain open.

The exact unresolved obligation is a uniform rejection of `9S|F` at actual
`r_K` for E, or the weaker bound `v_7(F)<=L-3` on the remaining full-witness
domain for subclass closure. Consecutive full-witness exclusion remains
**1 through 10,000,000 inclusive**. Sparse checked lengths and inherited
isolated/infinite families are kept separate. Ordinary proof, finite exact
computation and the unchanged Lean results are not conflated.
