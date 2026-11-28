# Independent review record

**Mathematical review: PASS. Computational review: PASS.** Both reviews
apply to implementation commit
`734d1fc12ef149edbd593ce5232454492f9b3727`. Neither reviewer authored the
implementation. There are no unresolved findings. This subsequent
review-artifact commit changes no implementation file.

## Mathematical review

Reviewer `/root/final_math_review` independently checked the original
predicate and factor nine, same-position hypotheses, inclusive threshold,
increment range with a nonactual predecessor, isometry, permutation,
coefficient two and inverse four, and the deadline `r<=L-3`. The three
constant-block sufficient bounds and constants `3528,2268,38304` are
valid with their stated hypotheses. No actual-prefix infinitude or
coverage theorem is claimed. The corollary, both exact inequalities,
strict induction and all 259 smaller certificates pass.

The reviewer separately revalidated all 259 earlier positions using
original repunit arithmetic and the unique representative domain,
obtaining 85 misses and 174 actual positions, with histogram
`{1:152,2:18,3:3,4:1}`. The selected residues and printed decimal triples
also agree. The global carry-bound gap remains explicit. A wording
observation was resolved before the final reviewed commit: CRT solutions
**may** lie outside the actual interval; no distribution assertion is made.

Exact reviewed document SHA-256 values:

```text
ONE_STEP.md          f29d06108f6ffb4ed760ff580d1894cf371edc8f390fd68b9ea34e7aeea5837c
MOVING_BOUND.md      b0cf0b95ef35ac0619d8e2ceb67644f262e08035f5666523bf6960dbc95b5a91
COROLLARY.md        7c817365605dc82311ccd9befe0ca09280ff83d1d8c37b4fcb735b688a68cbeb
README.md           ee3fb13616384e6695859ccef03d57bf925961ad7ee3326ed11fcb957de2b467
EXACT_CERTIFICATES.md b0c69d72476bb5d27b3c4fb97dcc24e5f624842d9108a13400ca927f7bbedc8c
```

This review uses the merged analytic estimates. It does not claim a new
audit of their external theorem source or any Lean verification.

## Computational review

Reviewer `/root/computational_review` implemented
[`independent_review.py`](independent_review.py) without importing project
arithmetic. It uses a modular-inverse seventh root and quotient-derived
ternary digits, then original repunits modulo `9m` followed by exact
division. It freshly recovers all **262** representatives and original-word
exclusions, rather than merely comparing the retained summaries.

The reviewer enumerates all 2,401 classes at depth five for each of the
five selected members (12,005 classes total), chooses lift digits by
exhaustive child testing, and checks all 245 child residues through depth
eight. Exact k, K, j_5, gcd, other factors, valuations and first nonzero
residues agree. It checks 18 printed exact integers, all five printed
summary rows, the factor-nine negative control and nonzero positive
controls. Thirteen corrupted certificates, including a coordinated
plausible wrong valuation and an omitted finite base, are rejected.

The source-bound [receipt](independent-review.json) binds all fifteen
implementation files at the reviewed commit. Its SHA-256 is
`f565530a46363b0be9f9cab50b714bb92140b55c7b008037b039928a55021a6f`.
Normal and optimized runs give identical bytes. The aggregate also
passed both modes; the subsequent wording-only edit changed no arithmetic
or arithmetic receipt, and the updated manifest passed both modes.

From the repository root:

```sh
pt=research/a398769/five-seven/power-three-carry
PYTHONDONTWRITEBYTECODE=1 python3 "$pt/independent_review.py" \
  --commit 734d1fc12ef149edbd593ce5232454492f9b3727 \
  --check "$pt/independent-review.json" > /tmp/power-three-carry-review.json
PYTHONDONTWRITEBYTECODE=1 python3 -O "$pt/independent_review.py" \
  --commit 734d1fc12ef149edbd593ce5232454492f9b3727 \
  --check "$pt/independent-review.json" > /tmp/power-three-carry-review-O.json
cmp /tmp/power-three-carry-review.json /tmp/power-three-carry-review-O.json
```

The reviewed implementation remains byte-identical at the later review
commit. The working tree's inherited research files remain byte-identical
to the PR #30 merge; only the additive root README entry is excepted.
Final main refresh was still exactly
`61a6fdfd7f4093b77be36ed0a55fbd3ebf798b7c`, with no later coverage.

Review certifies the stated proofs, finite exclusions and open scope. It
does not turn the unproved universal moving-position bound into a theorem.
