# Fresh independent review

25 November 2026. **Mathematical verdict: verified as written for all three
claims. Computational verdict: verified as written. No substantive defect
or required correction was found.**

The review context `/root/fresh_review` is distinct from report/proof author
`/root` and arithmetic implementer `/root/exact_checker`. The reviewer read
the proof, inherited early-rejection report, checker, certificate generator,
all certificates, both result receipts, and final audit report/computation
documents. The reviewer did not edit those implementation files. The only
files authored by this reviewer are this review, `review_check.py`, and
`review_results.json`. This is independent reasoning and implementation in
a separate agent context, not external human review or Lean verification.

## Mathematical findings

| Proposed claim | Classification | Independent finding |
| --- | --- | --- |
| General prime-factor obstruction and three bounds | Verified as written | The common root forces p to divide R; R is nonzero; the product bound, its coarse version, and the fixed-line length bound follow. |
| Composite D extension | Verified as written | The integer adjugate identity implies D divides R, including every prime-power multiplicity. |
| Exact conditional line exclusion | Verified as written | The complete forced divisor set contains one Fermat survivor, which fails even S divides F. |

No claim requires the classification "verified after correction", "refuted",
or "unresolved". There is no unsupported step within these stated claims.
The broader open problems are outside those verdicts.

Specific checks of the proof:

- The definition of n and its full witness divisor retain the factor nine:
  `225*S*7^(L-2) | F`; the required digit-sum test is `9S | F`. The audit
  consistently uses a necessary condition and does not claim equivalence
  between `S | F` and the full digit-sum condition.
- For every prime p dividing S, p is coprime to ten. The identity
  `7L=cp+4` gives the P congruence using Fermat's theorem. The Q congruence
  uses the exact exponent equality `bi+h_minus=aL+h_plus` and does not
  divide by 18 or any other quantity that might vanish modulo p. In
  particular p=3 is valid. Both parities of i are included.
- In the nonzero argument, `m=y^(7b)=18^(7b)*10^e` is a nonzero rational
  algebraic integer, hence an integer. Crucially, the quotient
  `B^(7b)/m=z^(7b)` is also rational and an algebraic integer. Thus integer
  divisibility is justified, rather than inferred merely from divisibility
  in an extension ring. B is odd; therefore m is odd, forcing `e=-7b`
  and the impossible integer value `(9/5)^(7b)`. This does not use a
  degree-seven minimal polynomial or irreducibility of P.
- Negative and zero h, a=0, a=b, and `7 | c+4` introduce no failure in
  that reasoning. Extra exact controls use c=3, so P has the rational
  root 10, with actual parameters L=13, i=3, S=87, p=29 and the choices
  `(a,b,h)=(0,1,3),(1,1,-10),(3,13,0)`. Their nonzero norms are in the
  review receipt; these are controls, not the proof of the general claim.
- Each root has modulus t, so `|Q(x)| <= 10^|h|*C` and the product has
  seven factors. The logarithmic and coarse bounds follow with the stated
  constants. A widening logarithmic strip requires fixed a,b,c (or
  sufficient uniform control); a fixed finite length bound also fixes h.
  An arbitrary prime divisor with uncontrolled c does not give a cutoff.
- The rank-seven quotient over Z is free because P is monic. The
  multiplication matrix and adjugate have integer entries, giving
  `V*P+U*Q=R` over Z[X]. Evaluation modulo D proves divisibility by D
  itself, not merely by its radical. This is adequate when D is composite
  and has repeated factors. The Fermat condition gives D=S.
- Solving the line gives exactly `L=12u+5,i=5u+2,S=84u+31`, with the
  actual-position domain exactly u>=1. The u=0 case has i=2 and is
  excluded. On this line S is coprime to 2,3,7; the Fermat condition
  excludes 5. The full multiplicity theorem then makes every possible S
  a subset product of the fifteen remaining distinct prime factors.

The line theorem quantifies over all u>=1 for which S passes the base-ten
Fermat test, including passing composite S. It excludes one position at
each such length. It neither proves broad all-length (E), excludes all
positions at those lengths, nor supplies a consecutive interval beyond
the inherited bounds. The report correctly preserves broad E only for
odd lengths 5..9,999,999 and consecutive full-witness exclusion only for
lengths 1..10,000,000. The all-length `{5,7}` subclass and wider digit-1
conjecture remain open.

## Independent exact calculation

`review_check.py` imports neither the primary checker nor SymPy. It
constructs Q directly by the binomial theorem and forms the 7 by 7 matrix
of multiplication by Q in `Q[X]/(X^7-100000)`. Ordinary Gaussian
elimination over exact `fractions.Fraction` gives a third resultant route,
separate from both the 19 by 19 Sylvester/Bareiss computation and SymPy's
symbolic resultant. It recovers the same signed nonzero resultant.

The reviewer separately verifies all 66 Lucas certificates in increasing
numeric order, requiring every factor prime of n-1 to have already been
proved. The mathematical justification is complete: each prime divisor r
of n has multiplicative order n-1 for the certificate witness, since the
gcd tests retain every prime-power exponent in n-1. Hence n-1 divides r-1
and r>=n, which forces primality. This includes all nineteen resultant
factor primes and both factors beyond 64 bits. The exact product and every
multiplicity agree with the computed norm.

A third full divisor enumeration uses `itertools.combinations` by subset
size. Decimal-Horner modular exponentiation independently tests the
Fermat condition for all 1,360 eligible products and computes the final
residues. Results:

| Check | Independently observed result |
| --- | --- |
| Distinct subset products | 32,768 |
| Products congruent to 31 modulo 84 | 1,360 |
| Minimum eligible S | 17,251 (u=205) |
| Fermat survivors | Exactly S=555700252411 |
| Survivor L, i | 79385750345, 33077395977 |
| Survivor F mod S | 333668527919 |
| Survivor F mod 9S | 889368780330 |
| Composite Fermat control S=451 | L=65, i=27, F mod9S=2241 |

Both complete sorted-list SHA-256 values agree with the primary receipts.
All twelve power and F residues for the survivor and control agree exactly.

The reviewer directly executed these checks with CPython 3.14.4 and
SymPy 1.14.0 in `/private/tmp/a398769-audit-venv`:

```sh
/private/tmp/a398769-audit-venv/bin/python research/a398769/five-seven/prime-factor-audit/checker.py --sympy > /private/tmp/fresh-review-normal.json
/private/tmp/a398769-audit-venv/bin/python -O research/a398769/five-seven/prime-factor-audit/checker.py --sympy > /private/tmp/fresh-review-optimized.json
cmp /private/tmp/fresh-review-normal.json /private/tmp/fresh-review-optimized.json
cmp /private/tmp/fresh-review-normal.json research/a398769/five-seven/prime-factor-audit/results-sympy.json
/private/tmp/a398769-audit-venv/bin/python research/a398769/five-seven/prime-factor-audit/generate_certificates.py > /private/tmp/fresh-review-certificates.json
cmp /private/tmp/fresh-review-certificates.json research/a398769/five-seven/prime-factor-audit/primality_certificates.json
/private/tmp/a398769-audit-venv/bin/python research/a398769/five-seven/prime-factor-audit/review_check.py > research/a398769/five-seven/prime-factor-audit/review_results.json
/private/tmp/a398769-audit-venv/bin/python -O research/a398769/five-seven/prime-factor-audit/review_check.py > /private/tmp/a398769-review-check-optimized.json
cmp research/a398769/five-seven/prime-factor-audit/review_results.json /private/tmp/a398769-review-check-optimized.json
```

Every command and comparison succeeded. The primary negative checks ran
in both modes and rejected the invalid Lucas witness, incomplete n-1
factorization, missing multiplicity and perturbed resultant. No new Lean
theorem or Lean build is part of this review.

## Reviewed artifact identity and delivery boundary

The reviewer directly checked baseline commit
`43da3bfcd17f53dc26925b00175042c8d16db78d` and confirmed that
`a75b08e1e21561fc1877e312f5fca0cf25174a18` is its second parent. The only
tracked-file change at review time was the declared navigation paragraph
in the inherited early-rejection README; all implementation additions are
under this new audit directory. Baseline coverage is read from repository
evidence, not inferred from a new bounded computation.

The final `verification.json` was also reviewed. The reviewer independently
compared all 240 listed inherited files byte for byte against that baseline
and checked each retained SHA-256, then removed the exact five-line
navigation addition in memory and recovered the original early-rejection
README exactly. All comparisons passed. Its command/receipt records agree
with the independently reproduced arithmetic. Its explicit
`fresh_full_runs=[]` correctly preserves the inherited large-run limitation.

These SHA-256 values bind this precommit review to its substantive inputs:

| File | SHA-256 |
| --- | --- |
| PROOF.md | `8ca5e280f0be7f920cb5d81e765e9228839d1f832314c0ce73b26ab978c20b52` |
| README.md | `cdd40236b4a0730d9959d65003b1e3620249d00b9a58b063190a7234f4a4921e` |
| COMPUTATION.md | `5ffbdd87ecacb8aa96d08a1b21d199d0f2d4ae1669b5c6c3372874d222cfec3c` |
| checker.py | `1128c4fc807589d5c29d9fa93deb0b878d540b8de330d613dd03ea35374df553` |
| generate_certificates.py | `6aff19fef30b515e1d8ba73a8763328297e6619f393fe18e42643ace76477c80` |
| primality_certificates.json | `cbae2508bdf6ae19f2aba2c91609ad9654f05abf716dfa644add7e263499fe6f` |
| results.json | `e4ad7dd8acbebace41b8e3475af95ca1001db43bfa8497172f408a89c7340fd7` |
| results-sympy.json | `ca51c584bfeac2662b8cf4070369c965387fbd0bbf83e14c0238fa363835813c` |
| review_check.py | `a1e9c2d83d3eb8cf59fea6ef5255299dc8ad4a95652da3c608fce0d0639bc894` |
| review_results.json | `80c04f8bb8d71f0ca0bb49fba9156b070775628f97cb8b80fcf076765f78e7a0` |
| verification.json | `6475b4fefe3b5b787a27651335ee8a450775f71a5aead5c5c8768c8bda7a3ab8` |

This review approves the mathematical/computational artifacts for draft
delivery. It does not itself attest that a remote PR already exists,
authorize a merge, or claim a final commit before one has been created.
The final acceptance check must bind these reviewed bytes to the actual
draft PR head. Owner merge remains outside the task's completion gate.
