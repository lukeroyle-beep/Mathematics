# Independent audit and validation record

24 November 2026. Base: main at
`214cd49e660f31aaee0aaecd48d36a8ec3624653`, containing merged PR #6.
This is an agent review record, not an external peer-review endorsement.

## Review coverage

Three separate reviewers independently checked the elementary setup/Lean
scope, the Bugeaud–Laurent application, and the Evertse application.
The two analytic reviewers then cross-reviewed the other deduction.
A final reviewer inspected the assembled reports and scripts. No unresolved
mathematical or code-correctness finding remained.

- Re-derived the decimal formula and exact divisor, without a coprimality
  shortcut or dropping the factor 9.
- Read Bugeaud–Laurent's definitions and Corollary 1 in the supplied PDF,
  pp. 2–4; checked independence, units, field degrees, heights, positive
  exponents, all substitutions, and the rational bound on the prefactor.
- Checked both intervals of the large-length inequality, including the
  transition at `exp(18)`.
- Independently reproduced the modular lifts and orders, the complete
  below-cutoff coverage, and the restricted meaning of the `i=15` result.
- Visually checked Evertse's original printed pp. 226–228, including
  equations (9)–(12). Checked integrality, common gcd 1, every proper
  subsum, height, injection, and the uniform outside-prime estimate.
- Reran both Python scripts, independently recomputed the exact rational
  fraction in the fixed-position report, checked the preservation hashes,
  and verified the stated Lean boundary.

Both deductions pass independently. The Evertse proof remains valid
without the fixed-position exclusion, and does not depend on the first
deduction's cutoff or constants.

## Fresh validation

[verification.json](verification.json) contains exact commands, outputs,
source hashes, and original-note hashes. The pinned Lean 4.24.0 project was
cleaned and rebuilt in the new checkout (807 build jobs), reusing copied
upstream dependency artifacts. This is a clean build of the project,
not a rebuild of Mathlib from source.

An initial dependency-copy warning came from dereferencing the Batteries
documentation symlink `docs/README.md`. It changed no Lean source. The
original symlink was restored in the isolated copy, all dependency Git
statuses were checked clean, and the clean project build and axiom check
were repeated successfully. The receipt retains both runs.

All three preserved public Lean theorems report exactly
`[propext, Classical.choice, Quot.sound]`. Both certificate scripts and
`git diff --check` pass. The original local notes and existing research
checkouts were preserved. The old Stage 5 searches were not rerun.

## Changed files

- `A398769.lean`: imports the preserved proof.
- `A398769/FiveSeven.lean`: byte-identical copy of the unpublished proof.
- Root `README.md`: links the audit and states its limited conclusions.
- `research/a398769/five-seven/README.md`: verdicts, setup, formal boundary,
  reproduction, and open questions.
- `research/a398769/five-seven/FIXED_POSITION.md`: first deduction.
- `research/a398769/five-seven/FINITE_PAIRS.md`: second deduction.
- `research/a398769/five-seven/certificates.py`: modular certificates.
- `research/a398769/five-seven/log_bounds.py`: exact rational log bounds.
- `research/a398769/five-seven/verification.json`: fresh evidence receipt.
- `research/a398769/five-seven/REVIEW.md`: this review record.
- `research/a398769/five-seven/prior-notes/{README.md,REVIEW.md,FiveSeven.lean,axioms.txt,verification.json}`:
  all five original files, unchanged and explicitly historical.

## Open conclusions

The finite set of remaining pairs has not been enumerated or proved empty;
no numerical maximum length is obtained. Position 15 is merely compatible
with the earlier modulo-49 restrictions. The all-length `{5,7}` exclusion
and the unrestricted A398769 conjecture remain open. Neither paper's
theorem or its application is formalized here. No merge is authorized or
performed by this audit.
