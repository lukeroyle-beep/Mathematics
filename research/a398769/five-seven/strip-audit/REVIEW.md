# Fresh independent review

25 November 2026. **PASS, with no must-fix findings.** This was a separate
agent context (`/root/fresh_review`) started without the builders' working
conversation. It received the task, baseline and claims, independently
reconstructed the arithmetic, then examined the delivered proof, code,
receipts and coverage wording. This is an independent model review,
not a claimed human or Lean review.

The proof and arithmetic builders were `/root/strip_proof` and
`/root/modular_audit`; `/root` integrated and checked the deliverables.
The fresh reviewer did not author either primary proof or either primary
modular implementation. It authored the additional `review_check.py`.

## Mathematical review

The reviewer freshly opened Bugeaud--Laurent Corollary 1 and checked its
parameter substitutions, including the global degree, local degree one,
height floors, positive exponents, prefactor, and all logarithmic maximum
entries. It verified the signed coefficient-span construction, strict
height margin, simple-root difference quotient, and both root branches.
The dependent-root norm/torsion argument and the subtraction `-v_7(D)`
were retained, including degree seven and negative `Dq-j`. The small
strip is empty by parity; no inherited finite search is needed there.
The closed endpoints and the even analytic threshold `10^9` cause no gap.

Independent arithmetic recovered all ten exponent classes and the final
root. The reviewer checked root and exponent exhaustiveness, exact order,
least positive exponent and length, and the distinction between a
modular survivor and a full witness. The combined theorem proves
`v_7(F)<L-2` at every integer `u>=1` on the line. It does not prove
unconditional failure of `9S|F` or broad (E).

## Additional independent arithmetic

[review_check.py](review_check.py) uses rational **exponential** series
with explicit tails for coarse logarithmic bounds, independently of the
strip checker's rational logarithm series. It proves the source
coefficient is below 63 and the maximum below 20, then checks the exact
slope `47628/78125` and threshold margin `390361598`.

It fully scans all 16,807 polynomial residues and all 14,406 exponent
classes modulo `7^5`, obtaining sole root 4044 and sole exponent 6437.
This complete small scan supplies a third computational route. It also
runs both depth-ten implementations normally and with `-O`, checks their
receipt/source hashes and agreement, projects to the independently
scanned depth, and checks nonzero exact-depth-one and exact-depth-ten
controls. All essential failures are explicit exceptions.

The reviewer separately ran the strip checker normally and with `-O`;
its outputs match the stored receipt. The independent review checker
also passes both modes with byte-identical results. Its receipt is
[review_results.json](review_results.json).

## Coverage and delivery review

The new closed ratio interval lies in exactly one of the previous six
open intervals and splits it at the two reported rational endpoints.
The other intervals and discrete restrictions remain in place. These
are position exclusions; no new whole length, consecutive broad interval or
all-length (E) result is claimed. The prior consecutive ranges, isolated
lengths and infinite whole-length families are preserved. The stronger
PR #17 digit-sum result keeps its Fermat hypothesis. The subclass and
wider digit-1 conjecture remain open; there is no new Lean claim.

The review checked the required baseline and ancestor. Root README
navigation is the only inherited modification, and the aggregate verifier
checks every other tracked baseline file byte for byte. The inherited
receipt verifier is reused without its optional full search. Final
publication includes an exact-commit check of this reviewed file set,
recorded in the pull request description; no merge is authorized.

The review identified one scope wording refinement: the modular lifts do
imply a bounded stronger conclusion at the line positions, so an unqualified
statement of "no new (E) coverage" would obscure that fact. The final
README and computation note explicitly record `v_7(F)<K(L)` at every
admissible line position with `L<2231854769`; the aggregate checker verifies
the supporting depth/period comparisons. This refinement adds no
whole-length or broad all-position interval. It does not alter any of the
three requested verdicts.

Reproduce the reviewer arithmetic from the repository root:

```sh
python3 research/a398769/five-seven/strip-audit/review_check.py > /tmp/strip-review.json
python3 -O research/a398769/five-seven/strip-audit/review_check.py > /tmp/strip-review-O.json
cmp /tmp/strip-review.json /tmp/strip-review-O.json
cmp /tmp/strip-review.json research/a398769/five-seven/strip-audit/review_results.json
```
