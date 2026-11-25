# Independent review record

**PASS. Submitted theorem verified as written; all submitted numerical
examples verified as supplied.** No mathematical repair is required.

The audit began from `main` at PR #12 merge
`2505f83c98fff9d11971c83f6a833740f7afadf6`, after reading the attached
submission, repository README and merged bounded-depth note. No applicable
AGENTS.md or CI workflow was present in the audited checkout. Existing
research notes and standalone exact-arithmetic checkers provide the relevant
validation pattern. The pinned Lean project is unchanged.

## Review independence

Two separate agent contexts reviewed the submitted proof adversarially:
one concentrated on decimal reduction, orders, CRT and compatibility; the
other on the joint-tail set, finite-set contradiction, published theorem
and actual positions. A third context wrote the primary exact checker.
The parent independently reconstructed and integrated the proof, inspected
the code, reran validation, and assembled the deliverable. The arithmetic
reviewer then checked the checker using a different logarithm-lifting and
CRT implementation, without importing it. The topology reviewer reread
the integrated proof and its scope statements.

These are separate computational-agent reviews of ordinary mathematics,
not external human peer review or Lean kernel certification.

## Findings and resolution

- The factor nine is correctly retained at `3^(a+2)` before division.
- All prime-power subgroup, order and CRT overlap claims pass, including k=1.
- Multiplication shifts points down an index; shifting up supplies preimages.
- Finite E gives proximity on a whole tail quadrant, legitimizing a fixed row.
- The signed-error recurrence gives one integer C for unbounded a; all signs
  of C, including zero, work in the two fixed integer polynomials.
- A fixed Bezout identity rules out coprimality even if modular roots vary.
- The degree-seven field argument and strict conjugate modulus inequality pass.
- BLMV §1.1, p.1705 supplies precisely the required published closed-set
  theorem. No inference from irrational-orbit density alone is used.
- The bounded positive limit of W/L at fixed k yields actual positions,
  including in intervals near 0 or 1. The least representative suffices.
- Both appendix examples pass on independent formula and word paths. The
  four grid representatives exceed L and are correctly labelled as controls.
- Fixed depth, the same-length threshold L-2, inherited consecutive coverage,
  the isolated PR #12 length, and the full conjecture remain clearly separated.

Two precision edits were requested in the integrated exposition and applied:
use “both indices tending to infinity,” and explicitly require
`0<t-eta<t+eta<1`. The submitted proof already had the required stronger
premises; these clarify the audit's exposition rather than repair the
submitted theorem. Final readback of PROOF.md passed at SHA-256
`270d03d76a083c98e168a9f96db7507563eb5576e3ce2e13cfd8701a15b0bee8`.

## Reproduced evidence

- Primary checker normal and optimized runs are identical to checks.json.
- The independent reviewer recomputed all four representatives using
  linearized prime-adic lifting and CRT idempotents, then used recursive
  geometric sums for the decimal words; results agree with the primary path.
- Exact literal positions match SUBMISSION.txt. All interval tests use integers.
- The primary block routine passes 6,240 literal-word comparisons.
- Both inherited ten-million programs reproduce their retained receipts
  (only the lifting elapsed time differs).
- The isolated-length checker exactly reproduces PR #12's receipt: 14,997
  full-sum positions, maximum depth six.
- `git diff --check` passes. No new Lean formalization or build was performed.

File fingerprints, commands and receipt comparisons are in
[verification.json](verification.json). The reproducible independent review
code and output are linked from [README.md](README.md).

No mathematical blocker remains for this fixed-depth theorem. The requested
delivery state is an unmerged draft pull request for owner review, not an
all-length proof or an approval to merge.
