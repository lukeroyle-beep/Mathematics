# Independent mathematical and computational review

**PASS: no unresolved findings in the stated partial results.**

Reviewed implementation commit:
`8d56670602fe57280b10ab7a5221941438f28f2c`.
Base main and refreshed publication-time main:
`0a47180b889b392c2323bc1614a473af51f38d78`, the requested PR #27 merge.
No later main commits were present at either fetch. The implementation
is an ancestor of the review revision; merging remains Luke's decision.

The reviewer `/root/independent_transitions` independently authored the
residue-class lifting method, then reviewed the separately authored
direct full-period implementation, individual root/logarithm program,
original-word adapter, proofs and aggregate verifier. The individual
mathematical specialist separately reviewed the root/logarithm program.
This record distinguishes an independent implementation from review of
one's own method; the two transition methods share no arithmetic imports.

## Mathematical findings

- The original decimal blocks give `F=9n`, `S=7L-4` and
  `P=25*7^(L-2)`. The complete predicate is
  `225*S*7^(L-2)|F`; the digit-sum predicate retains `9S`.
  Equality `v7(F)=L-2` already suffices at an eligible sum-compatible
  position. Every finite exclusion fails at a depth `m<=L-2`.
- The root exists uniquely in `1+9 Z_3`. The exponential isometry gives
  **exactly** `v3(10^L-theta)=a+2`. Division by 18 costs two digits;
  the logarithm quotient costs another two. The resulting congruence
  `s=kappa mod3^(a-2)` and the odd representative modulo `2*3^(a-2)`
  are valid. Newton precision and the modular-logarithm implementation
  supply all the required digits, including the last exponent.
- The joint size inequality has leading coefficient `log(10)/log(7)>1`
  and cannot exclude the individual witness threshold. The algebraic
  norm has exact seven-adic valuation **seven**, independent of a large
  `v7(F)`; its calculation does not transport the desired large valuation.
  The norm and independence calculations were independently recalculated.
- The reviewer reopened the [Bugeaud--Laurent primary PDF](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf),
  checking the definitions on printed pp.2--4 and Corollary 2 on p.5.
  The application uses principal units, `p=3`, `e=f=1`, `D=7`,
  height parameters 3 and 4, and the stated `b'`. Its constant
  `1037232` and inequality direction are correct. It constrains the
  size of s from below and supplies no upper cutoff for a. No fresh
  raw-byte hash of this web-opened PDF is claimed.
- The transition identity is necessary whenever two successive actual
  positions survive. `7|F` forces `i=3 mod6`, so using the joint class
  does not omit any depth-nine survivor. The period proof retains the
  leading factor seven in U. It establishes `R_m=7^(m-2)` for `(U,G)`
  for every `m>=2`, including wraparound; minimality is unnecessary.
- Both enumerations allow every increment in `[0,728]`. The direct
  method's shallow filter is complete, its recurrence is correct, and
  its last-to-first edge pair is checked. The independent method tests
  all seven lifts of every surviving start, beginning with a complete
  depth-two period. Reduction preserves bounded increments, so no
  higher-depth survivor is omitted.

One explanatory improvement was requested and incorporated: the
three-length proof now explicitly derives `i=3 mod6` from `7|F`.
No substantive mathematical or computational repair was required.

## Computational evidence and source binding

The direct and lifting methods agree on **every** start and increment
list at depths 5--9, with counts `35,14,14,7,0`. At depth eight, all
seven starts are `14984+16807j`, `0<=j<=6`, with increments `(189,42)`.
The independent method checks all 49 possible depth-nine lifts and
finds none; the direct method visits the complete 823,543-start period.
The five direct periods together contain **960,743** starts.

The individual implementations agree on all **256** specified exponents
`31+6u`, `0<=u<256`, through 1561. There are **84** class misses and
**172** actual positions, with exact valuation histogram
`{1:150,2:18,3:3,4:1}`. The first 128 rows are identical to PR #27's
retained rows. The previously unchecked `a=799` is actual, has valuation
one, and has original-word residue `n mod49=35`. The next unchecked
exponent is 1567.

[`review_checks.py`](review_checks.py) adds a third arithmetic calculation:
it computes the decimal repunit modulo `9m`, divides the integer residue
by nine, and subtracts the two changed digit contributions. It imports
no implementation arithmetic. This checks every reported sum class,
all 172 actual non-seven divisors and exact first failing seven powers,
the a=25 positive control, and the `(313,51)` lost-nine negative.
It separately reads back theta, C and kappa at their declared precisions.

The review program also compares `baseline.json` with the bytes of an
actual `git archive` of the base commit: all **1,028** paths and hashes
agree. Exactly **1,027** inherited files remain unchanged; only the
reviewed root README addition differs. The archive and adjacent interval
certificates are retained evidence; historical large searches were not
rerun by this review. The aggregate verifier pins the adapter's inherited
arithmetic source to this baseline.

[`review-checks.json`](review-checks.json) binds the reviewed implementation
commit, all final proof/source/receipt files, root README, relevant inherited
sources and the review program itself. The checker compares every bound
implementation file directly with its bytes at the reviewed commit.
Both final review runs, normal and `python3 -O`, produce byte-identical
receipts. The implementation's four arithmetic programs and aggregate
verifier also passed in both modes, with deterministic receipt equality.
No check relies on removable Python assertions.

The independent transition checker rejected three corrupted receipts in
both modes: changed source hash, a fabricated depth-nine count, and an
omitted depth-eight control. The review comparison also rejected changed
source hash, fabricated a=799 valuation, and fabricated depth-nine count
in both modes. The aggregate verifier's nine recorded corruption controls
all pass.

Reproduce the frozen review from the repository root:

```sh
pt=research/a398769/five-seven/power-three
python3 "$pt/review_checks.py" --check "$pt/review-checks.json"
python3 -O "$pt/review_checks.py" --check "$pt/review-checks.json"
python3 "$pt/verify.py" --run
python3 -O "$pt/verify.py" --run
git diff --check
```

## Scope retained after review

The three-length theorem is proved for all `u>=0`; an isolated full
witness remains logically possible. The universal individual-family
assertion, unrestricted `{5,7}` subclass and wider digit-1 conjecture
remain open. No individual exponent cutoff or full witness is claimed.
Consecutive whole-length coverage remains **1--1,000,002,000,000**
inclusive; the named family lengths do not extend it. The first missing
individual inference remains a valuation bound below `L_a-2` for every
remaining actual candidate. No new Lean theorem or Lean build was
performed. These are ordinary proofs and exact finite computations.
