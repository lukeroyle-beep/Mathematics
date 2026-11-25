# Independent adversarial review

The reviewer worked in a separate agent context from the principal proof
investigator, primary computational implementer, and parent integrator.
This is an ordinary mathematical and code review, not external human peer
review or Lean kernel certification.

## Baseline and mathematical claims

Local Git confirms that the starting commit
`b6db8703afd3d32211fd75de9ce1e34440dddfe8` is the PR #14 merge and has
the audited research commit
`22ef46d55fa903b54e0b288a1b38ba0a6fa0659a` as its second parent.
The inherited depth, fixed-depth, whole-length, edge and proportional
records were read. Their fixed-depth quantifiers, exact sum progression,
separate isolated exclusions and unchanged consecutive interval are
consistent with the new investigation.

The independent proof review checked:

- Every actual word in the stated broader domain ends in 775 and has
  exactly two factors of five. Thus the complement `5|S` is excluded
  before separating the full divisor; `9S` is retained throughout.
- The primitive-root order proves existence as well as uniqueness of
  the exponent class. The strict definition `T_K>L`, including `K(5)=1`,
  and the integer induction proving `K<=L-2` are valid.
- An actual position of depth at least K must equal the least r_K.
  Monotone least-representative lifts justify escape after a nonzero
  digit. These facts alone do not force a nonzero digit before L-2.
- The new order lemma is uniform in the entire displayed domain.
  From a prime-power component attaining `e=v_7(ord_S(10))>=1`, Euler's
  theorem gives `7^e|q-1`. Oddness gives `q>=2*7^e+1`, while the special
  residue `S=3 mod7` gives `S/q>=3`. Thus `T_e<=L-1` and `e<=K-1`.
  This does not assume a particular prime factorization of S or that
  10 generates all units modulo S.
- The full-sum exponent class uses inversion of 2 modulo S, avoiding
  cancellation of nine. Its generalized-CRT compatibility modulus
  stabilizes by K. Later compatibility is an unbounded-exponent claim;
  it does not imply that r_k is actual or itself sum-compatible.
- The elementary size bound has leading coefficient
  `log(10)/log(7)>1`. The inherited qualitative estimate has an
  ineffective starting point. Neither is promoted to the required
  valuation bound.

No defect was found in these claims. The new stabilization lemma diagnoses
an obstruction; it removes no surviving pair from the unresolved domain.
It must not be described as a proof of the direct exclusion target.

The final self-contained README was checked against the inherited six
open ratio intervals, all thirteen forbidden prime divisors, the conditional
43 restriction, analytic edge inequalities, midpoint strip and three
distinct isolated lengths. The route ledger accurately separates known
obstructions from impossibility claims. Two summary precision changes
were requested and applied: explicitly restrict the prime-factor argument
to `e>=1`, and say the quotient upper bound *permits* height proportional
to L rather than asserting an actual lower bound for that height.

## Arithmetic and coverage

The reviewer read both implementations and reran each normally and with
`python3 -O`. The two modes are byte-identical for each implementation;
the primary output matches checks.json. The independent method imports
no primary code: it enumerates complete unit cycles for the exponent
representatives and concatenates decimal blocks for actual-word arithmetic.

The complete ordered digest, total length count, counts by K, actual
representative count, zero-run histogram and full-sum survivor list agree
between implementations. The shared digest is
`a54ad76ea69a6db88927613cfab5da3db41189fbeb5b7b81ebbef6d62247eab7`.
The 49,999 lengths are exactly the odd integers 5 through 100001;
the partition of all their possible depth-K positions is complete.
This window lies inside inherited coverage, so it extends no consecutive
interval. The absent full-sum survivor does not certify any outside length.

Literal-word controls check both position parities. Positive full-sum and
lost-nine controls cover `3|S`. Strict-period endpoint controls include
even boundary lengths. Exact order controls attain `e=K-1`, and the
reviewer separately recomputed `(L,S,d,e,K)=(85,591,98,2,3)`.
The long-zero-run control fails the full sum and is correctly identified
as such. The added control with `5` not dividing S also fails the full
sum; its independent decimal valuation and sum residue agree. All
essential validations use explicit exceptions; a precision
guard fails the computation rather than certifying an exclusion.

The final verifier was inspected. It compares both ordinary and optimized
runs with the committed receipts, checks their common arithmetic and
coverage fields, verifies baseline ancestry, compares 35 inherited files
byte-for-byte with the starting commit, and checks the unchanged tracked
Lean boundary. It deliberately does not rerun the large inherited
certificates. Invalid input is rejected under both Python modes.
The reviewer independently ran this verifier under `python3 -O`; all
four runner invocations, preservation checks and invalid-input checks
passed. The final root summary uses the exact threshold `T_k>L`, without
claiming it is necessarily the earliest depth at which uniqueness holds.

## Completion boundary

The defensible mathematical verdict is **4. No closing advance**.
No uniform bound for the zero-lift run, effective global cutoff, new
finite interval above ten million, or full witness has been established.
There is consequently no finite gap attached to a newly proved cutoff
to discharge; the original residual domain remains unresolved.
Complete consecutive coverage remains 1 through 10,000,000 inclusive,
with the inherited isolated and infinite-family exclusions kept separate.
No new Lean formalization or Lean build is claimed. The full A398769
digit-1 conjecture remains outside the demonstrated results.

The review approves the stated limited research result and reproducible
diagnostics for owner review. It does not approve merging or claim that
the user's primary settlement target has been achieved.
