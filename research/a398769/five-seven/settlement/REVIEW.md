# Independent agent review

Reviewed 24 November 2026 by an independent agent, separately from the
implementing agent and the agent deriving the analytic bounds. This is an
agent review, not a claim of human peer review. The review found no remaining
substantive defect in the recorded finite exclusion or the edge arguments.
The complete subclass remains **open**.

## Mathematical coverage checked

The reviewer checked the unique exponent class at every power of seven,
the coefficient `3c` in the lift, and why a least representative at least
`L` safely rejects every later lift. The implementation retains the whole
class when its period is small. The fixed-modulus implementation has a
separate argument: position keys are injective because the order exceeds
the entire position range. Small lengths for which the fixed power would
be too strong are tested separately at the exact required power.

The inclusive bound 10,000,000 means the last odd length is 9,999,999.
The primary count is 4,999,998 lengths. The independent partition is nine
small lengths with 18 residual pairs, followed by 4,999,989 lengths tested
modulo `7^20`. Positions congruent to 3 modulo 42 are not reduced to the
single position 3; position 45 is retained. Unsigned 64-bit additions and
unsigned 128-bit products are sufficient for all accepted inputs and
power caps in the C++ program.

The reviewer independently opened Bugeaud–Laurent's
[original PDF](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf)
and checked the definitions on printed pages 2–3 and Corollary 1 on page 4.
The two applications use rational 7-adic units, positive exponents,
appropriate heights, and multiplicatively independent bases. The source
permits the rational base `25/D_g`, which is less than 1 in the real
absolute value. Both valuation arguments for independence, the factor
168, the upper constant 63, and the transition at `exp(18)` were checked.

The exact rational constant comparison and the two cutoff comparisons
pass. Combining the finite exclusion with the analytic inequalities
excludes `i <= 395` and `L-i <= 395` at every length. The modulo-49 table
then improves the remaining position bound to 417. This does not bound
the region where both the position and gap grow with the length.

The full-divisor argument keeps the factor 9, uses the 5-adic filter before
claiming coprimality, and correctly proves the 5, 11, 13, 37 and 101 length
filters. The finite search uses the weaker 7-power condition; with no weak
survivors, no full-divisor test on a large survivor is claimed.

## Executed independent arithmetic checks

The reviewer executed the following checks, rather than only inspecting
the implementing agent's outputs:

- Compiled the C++ sieve with undefined-behavior sanitization and ran the
  complete ten-million range: 4,999,998 lengths, zero survivors, and all
  rejections at power 18 or earlier. No sanitizer finding occurred.
- Checked all 4,998 unpruned exponent classes through length 10,000 using
  independently evaluated Python modular powers, including the canonical
  range and the exact period. Repeated this check on the final source.
- Compared 88 C++ runs against decimal-string construction: caps 1 through
  8 and bounds `5,6,7,22,23,24,45,46,47,199,200`. These include nonempty
  truncated-modulus controls and odd/even endpoints.
- Compared the independent fixed-modulus program with direct construction
  at `(limit,exponent)` values `(5,2),(6,2),(7,2),(22,3),(23,3),(24,3),
  (99,4),(100,4),(199,4)`.
- Reconstructed all 9,900 two-five position pairs through odd length 199.
  None passes the growing-power or full-divisor test. The required
  `(23,15)` regression gives `F mod49=0` and `F mod343=245`.
- Ran the final primary runner under Python `-O` through length 301. Its
  3,775 residual pairs, 745 length/power comparisons, 43,690 original
  words through length 15, full-divisor residue tables, and position-45
  control passed with checks still active.
- Reran both final default ten-million commands. The primary receipt
  matched `lifting.json` except for elapsed runtime; the independent
  receipt matched `independent.json` byte for byte. All recorded source
  SHA-256 values matched the files actually reviewed.

Reproducible commands from the repository root include:

```sh
python3 research/a398769/five-seven/settlement/verify.py --output /tmp/a398769-review-lifting.json
python3 research/a398769/five-seven/settlement/verify_fixed.py --output /tmp/a398769-review-independent.json
cmp /tmp/a398769-review-independent.json research/a398769/five-seven/settlement/independent.json
python3 -O research/a398769/five-seven/settlement/verify.py --max-length 301
python3 research/a398769/five-seven/settlement/verify_fixed.py --limit 23 --exponent 2 --direct-limit 23
c++ -std=c++17 -O2 -Wall -Wextra -Wconversion -fsanitize=undefined research/a398769/five-seven/settlement/lift_sieve.cpp -o /tmp/a398769-review-lift
/tmp/a398769-review-lift --max 10000000
/tmp/a398769-review-lift --max 10000 --residues
```

The fixed-modulus positive control intentionally includes `(23,15)` and
does not claim exclusion. The final C++ residues-only output explicitly
labels that mode and omits the survivor field used by the bounded sieve.

## Review corrections and evidence boundary

The initial strict compilation identified a harmless signedness warning
in the small prime initializer and reliance on a transitive include for
`std::min`. The final source uses unsigned literals and includes
`<algorithm>` explicitly; strict compilation is clean. The reviewer also
verified the final separation of residues-only output from exclusion
output. No arithmetic result changed.

These checks support an ordinary mathematical proof of coverage and of
the infinite edge exclusions, plus machine-checked finite arithmetic for
the stated range. They are not Lean proofs. No Lean source was changed,
no new theorem was elaborated in Lean, and this review does not assert a
fresh clean Lean build. The earlier formal theorems retain their existing
scope. Neither abstract finiteness nor this finite certificate establishes
an all-length exclusion of the entire subclass.
