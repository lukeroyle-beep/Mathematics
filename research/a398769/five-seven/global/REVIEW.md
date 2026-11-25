# Independent mathematical and computational review

Reviewed 24 November 2026 by the separate `certificate_audit` agent, against
the files identified by SHA-256 in [review.json](review.json). The starting
commit is merged PR #8, `7b0151105c481b227b26c6198186500ba63a2bd9`.
The reviewer did not write the primary proof notes or `checks.py`.

**Assessment: the stated partial results are supported; the subclass remains
open.** No must-fix mathematical or implementation finding remains. This is
not approval to merge or a proof of all-length exclusion.

## Proof checks

- The fixed-modulus theorem has the correct universal length quantifier.
  The central interval contains every exponent class, the primitive-root
  argument covers all units, and odd multiples of the odd radical give
  `gcd(S,M)=1`. The suffix and constructed seven-power divisibility imply
  exactly the gcd condition for a modular quotient, including `M=1`.
  Enlarging the fixed modulus incorporates all inherited finite filters,
  without claiming the actual varying divisors.
- The two-quotient reduction retains the factor 9 and requires `5` not
  to divide `S` before inversion. Independent cancellation gives
  `X/K=49/(9S)*(10/49)^r` and the bound
  `301/(225S)*(10/49)^r` for the low-position correction. Both literal
  attachment bounds fail at the documented length 9. The corrected bounds
  prove the intended conclusion for all odd lengths at least 5.
- The valuation recovery is necessary, and the final equality is sufficient.
  Omitting redundant split and residue filters in the implementation is
  sound because the complete equality still proves `n=P*S*q`. The direct
  digit check protects a reported witness. Synthetic positive controls are
  clearly separated from original-problem witnesses.
- The spacing lemma correctly separates equal low valuations from the
  case where both valuations exceed the fixed threshold. Its same-position,
  same-length and same-gap consequences follow with the stated powers.
  It cannot bound the first possible solution. The conditional cutoff
  calculation is valid only after proving the missing uniform estimate.
- The reviewer independently opened Evertse--Ferretti's
  [primary paper](https://math.leidenuniv.nl/reports/files/2010-17.pdf),
  printed pages 4--5. The interval endpoints in Theorem 1.2 are explicitly
  ineffective. A bound on the number of subspaces or intervals does not
  supply a maximum length in this application.

## Executed checks

Both unchanged PR #8 ten-million programs were rerun. Their deterministic
receipts match the merged records exactly; only the observed lifting-run
time changed. The source hashes and commands are in
[pr8-audit.json](pr8-audit.json). The earlier modular and rational-log checks
also passed, as did the weak positive control retaining `(23,15)`.

The final primary checker was rerun normally and with `python3 -O` and
matched [checks.json](checks.json). It compares 3,775 actual digit pairs at
149 odd lengths, tests 386 fixed-modulus examples, exercises both quotient
branches with synthetic successes, and preserves the required regression.
The spacing checker also passed both ways, matching
[spacing.json](spacing.json) with nonempty congruence controls.

The reviewer added [independent_checks.py](independent_checks.py), importing
none of the primary implementations. Its normal and optimized executions
match [independent.json](independent.json):

- 3,020 actual decimal words at 119 odd lengths passing the 5-filter agree
  with independently computed quotient candidates and exact division;
- 18,120 direct modular comparisons validate a separately implemented
  decimal-block composition;
- three synthetic positive controls exercise accepted recovery, including
  two high-position cases where the second quotient differs from the first;
- the huge sum-only pair is independently checked from its actual digit
  blocks, obtaining `n mod S=0`, `n mod49=0`, and `n mod343=294`.

Reproduce the independent checks with:

```sh
python3 -O research/a398769/five-seven/global/independent_checks.py > /tmp/a398769-independent-global.json
cmp /tmp/a398769-independent-global.json research/a398769/five-seven/global/independent.json
git diff --check
```

## Scope and remaining limitation

The inherited exhaustive exclusion remains every length through 10,000,000
inclusive. **No new exhaustive interval of odd lengths above 10,000,000 is
certified**, and no global cutoff or full witness is claimed. The very large
sum-only example rejects one pair because its seven-adic valuation is 2;
it does not exclude all positions at that length. The old parity, residue
and edge exclusions retain their earlier all-length scope.

The precise missing step is uniform exclusion of the two quotient candidates
at all remaining lengths, or a uniform effective valuation bound or other
global argument, followed by any required finite verification. The current
proofs and executed checks supply none of those conclusions.

No Lean source changed, and no new Lean theorem or fresh Lean build was
checked. The additions are ordinary proofs and exact finite arithmetic.
Review hashes identify the inspected content; branch publication and the
owner's merge decision are separate actions.
