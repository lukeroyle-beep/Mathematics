# Arbitrary fixed depth: independent proof audit

25 November 2026. **Theorem: verified as written. Numerical examples:
verified as supplied.** No proof repair or corrected example is needed.

Starting revision, freshly fetched from the current default branch `main`:
`2505f83c98fff9d11971c83f6a833740f7afadf6`. GitHub identifies this exact
commit as the merge of [PR #12](https://github.com/lukeroyle-beep/Mathematics/pull/12);
local ancestry was independently checked. Audit branch:
`research/a398769-arbitrary-fixed-depth-audit`.

## Result

For every **fixed** `k>=1` and every nonempty open interval `I` in `(0,1)`,
infinitely many distinct odd lengths L admit a position `3<=i<L` with

```
i/L in I,
225*(7L-4) | 7*10^L-18*10^i-25,
v_7(7*10^L-18*10^i-25)=k.
```

[PROOF.md](PROOF.md) reconstructs every step, including the extra factor
of nine, exact-depth lifts, CRT overlaps, joint-tail surjectivity, finite-set
contradiction, and conversion of density to actual positions. The finite-set
argument is valid because uniform proximity is established on a whole
tail quadrant **before** fixing one row. It produces the same integer C
for unbounded a; negative C and C=0 are both covered. A fixed polynomial
Bezout identity handles varying modular roots.

The external dependency is the published closed-set form of Furstenberg's
theorem in Bourgain–Lindenstrauss–Michel–Venkatesh, *ETDS* 29 (2009),
§1.1, p.1705. The proof checks all its hypotheses and does not substitute
the weaker irrational-orbit statement. [Publisher PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/01225FAD40EEBC38F3AE1A5C119D0267/S0143385708000898a.pdf/some-effective-results-for-ab.pdf).

The period/length ratio tends to `lambda_k=112*7^k/153>1`. Thus the
submission's h is always zero, and the least representative itself
eventually supplies the actual position. This optional simplification
does not repair a gap. It works for `(41/100,42/100)` and intervals
arbitrarily close to either endpoint.

## Numerical results

[checks.py](checks.py) independently recomputes prime-adic discrete logs
and CRT representatives. Its separate decimal-word path concatenates
blocks by binary repetition; it never calls the formula for F or divides
by nine. The routine is validated against literal decimal words for all
`2<=L<=40`, all `1<=i<L`, and eight moduli: **6,240 comparisons**.

[independent_checks.py](independent_checks.py) retains the second reviewer's
different implementation: linearized prime-adic lifting, CRT idempotents,
and recursive geometric sums. It imports no primary checker, reads the
supplied positions from SUBMISSION.txt, and computes its results before
comparing with checks.json. Its deterministic receipt is
[independent_checks.json](independent_checks.json).

At depth one, `A=84,B=42,e=3`, all four grid representatives and all four
adjacent reductions pass. Their exact representatives are:

| (m,j) | Least representative r |
|---|---|
| (0,0) | `6261783` |
| (0,1) | `14911001948157735084662689120339008693462324988026783919719` |
| (1,0) | `59160064997262896473265162460610397096743332663` |
| (1,1) | `321898764289871702573828802697266009495841135756749015442725474562096007168470049568645288692916759` |

Each has `F mod(9S7)=0`, `F mod(225S7)=0`, and `F mod49=28`.
**All four r exceed L**: these are congruence/compatibility controls,
not actual digit positions. The submission makes only the former claim.
The receipt records W and the exact quotient and remainder for each
adjacent reduction, plus finite order/lift controls for k=1 through 8.
Those finite controls are not the proof for arbitrary k.

Both large appendix positions are preserved exactly in
[SUBMISSION.txt](SUBMISSION.txt) and [checks.json](checks.json):

| S | k | F mod(225S7^k) | F mod7^(k+1) | n mod(25S7^k), independent blocks | n mod7^(k+1), independent blocks |
|---|---:|---:|---:|---:|---:|
| `3^164*17^41` | 4 | 0 | 2401 | 0 | 9604 |
| `3^103*898129^21` | 7 | 0 | 1647086 | 0 | 823543 |

Both pass the **integer** inequalities `100i-41L>0` and `42L-100i>0`;
the full positive margins are retained in the JSON. The next residues
are respectively `7^4` and `2*7^7`, so the valuations are exactly 4 and 7.
Multiplying each independent n residue by nine reproduces the F residue.
No floating-point comparison is used. No discrepancies were found.

## Inherited coverage and limits

The complete consecutive exclusion range for the `{5,7}` subclass remains
**all lengths 1 through 10,000,000 inclusive**. Both inherited exact
certificate programs were freshly rerun: the fixed-modulus receipt matches
PR #12 byte for byte, and the lifting receipt differs only in elapsed time.

Separately, the isolated length excluded in PR #12 is

```
L=(898129*3^193+4)/7
 =15582704697570091495948156638491914590405161120787807516829906317314612303918977615165179656913553.
```

Its checker was freshly rerun and reproduces the stored receipt exactly:
all 14,997 full-sum positions, maximum valuation six. This isolated length
is **different** from the appendix's depth-seven length. These new examples
do not exclude their entire lengths, and no new consecutive exclusion
range is certified.

The theorem settles PR #12's fixed-depth existence question. The all-length
`{5,7}` subclass and the full [digit-1 conjecture](https://oeis.org/A398769/internal)
remain unresolved. Indeed `n=F/9`, `P=25*7^(L-2)` and `S=7L-4` give the
full test `225S7^(L-2) | F`, requiring `v_7(F)>=L-2` **at the same L**.
Choosing k first and then growing L does not establish this diagonal
condition. No Lean files changed, and no new Lean formalization or Lean
build is claimed.

## Reproduction

From repository root, use Python 3.9+ and a C++17 compiler for the inherited
lifting certificate:

```sh
python3 research/a398769/five-seven/fixed-depth/checks.py > /tmp/fixed-depth-normal.json
python3 -O research/a398769/five-seven/fixed-depth/checks.py > /tmp/fixed-depth-optimized.json
cmp /tmp/fixed-depth-normal.json /tmp/fixed-depth-optimized.json
cmp /tmp/fixed-depth-normal.json research/a398769/five-seven/fixed-depth/checks.json
python3 research/a398769/five-seven/fixed-depth/independent_checks.py > /tmp/fixed-depth-independent.json
python3 -O research/a398769/five-seven/fixed-depth/independent_checks.py > /tmp/fixed-depth-independent-opt.json
cmp /tmp/fixed-depth-independent.json /tmp/fixed-depth-independent-opt.json
cmp /tmp/fixed-depth-independent.json research/a398769/five-seven/fixed-depth/independent_checks.json
python3 research/a398769/five-seven/settlement/verify.py --output /tmp/fixed-depth-lifting.json
python3 research/a398769/five-seven/settlement/verify_fixed.py --output /tmp/fixed-depth-fixed.json
python3 research/a398769/five-seven/depth/checks_depth_samples.py > /tmp/fixed-depth-isolated.json
cmp /tmp/fixed-depth-fixed.json research/a398769/five-seven/depth/baseline_independent_rerun.json
cmp /tmp/fixed-depth-isolated.json research/a398769/five-seven/depth/depth_samples.json
git diff --check
```

Compare the lifting receipt as parsed JSON while ignoring only
`elapsed_seconds`. The checks use explicit conditionals and exceptions,
so Python optimisation does not remove them. Normal and optimized outputs
were independently rerun and match the committed receipt byte for byte.
[verification.json](verification.json) records exact file hashes, reproduced
coverage and review evidence.

## Submission and sources

The attached Pages file was read by decompressing its IWA document stream;
the body text is retained in SUBMISSION.txt, with Unicode line separators
normalized to newlines. Embedded hyperlink labels remain as supplied;
their resolved targets are linked in this audit. Attachment SHA-256:
`4ec28877d592aaad9745eaa6826b4cd3847d8e9ac8090da7ebbe9ee01f7cddc5`.
Text SHA-256:
`7e77aef5b8b5b3e4b7fff5357c1ef035571e447147f6381082f44909cd9e85ca`.

The merged [bounded-depth note](../depth/BOUNDED_DEPTH.md) was read at the
audited base. Its earlier open-question wording remains a historical
record; this audit supplies the fixed-depth theorem but leaves its global
exclusion obligation open. The original OEIS definition and conjecture
were checked against the indexed OEIS internal entry (direct fetch returned
403). The published circle theorem was read directly in the publisher PDF;
the original Furstenberg paper was also checked in the linked scan.

Separate agent contexts independently reviewed arithmetic and topology
before the parent integrated this proof, then reviewed the integrated proof
and checker. These are ordinary mathematical and code reviews, not a
machine-checked proof or external human peer review. Delivery is a focused
**draft pull request for owner review; merging remains with the owner**.
