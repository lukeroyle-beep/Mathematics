# Investigation of `10^t <= 10^12 H`

**Global verdict: unresolved.** No counterexample to the inequality and
no full `{5,7}` witness was found. The [proof and obstruction](PROOF.md)
verify the exact domain, decimal threshold, cutoff and lift indexing,
and state the first unsupported global assertion.

Starting current main was **`aab83fc4ed706cd4aca4d51dc6e533d60cb87477`**,
exactly the merge of [PR #22](https://github.com/lukeroyle-beep/Mathematics/pull/22).
Both Git ancestry and live GitHub merged metadata were checked. The work
uses the isolated branch `research/a398769-decimal-height-bound`.
[baseline.json](baseline.json) records parents, reference hashes and
the precise inherited evidence that was checked.

Proved results include:

- `H=F/(225S)` is positive integral and `v7(H)=t`, including `3|S`.
- The target is exactly `t<=digits(H)+11`; failure is exactly
  `7^(digits(H)+12)|F` at that same position.
- Its conditional full-witness cutoff is `L<=444444444445<B`.
- `t<K` implies the stronger `10^t<H`; when `t>=K`, the actual position
  is `r_K`. The missing nonzero lift must occur in `[K,d+11]`, whose
  upper endpoint is at most `L-3` above B.
- The target holds in the closed strip `|L-2i|<=L/60000` for
  sum-compatible odd `L>=10000000`, with explicit constants and no gap.
  A separate exact integer criterion covers additional positions.
- Inherited finite valuation certificates also imply the target for
  every sum-compatible odd `5<=L<=B`. Qualitatively it holds at all
  sufficiently large lengths, but no effective starting length is known.

The exact sum divisor and the stabilized exponent CRT do not force the
required nonzero lift. The first unproved assertion remains its existence
for **every actual sum-compatible `r_K` above B**, including composite S.
Neither generic integers failing the analogous inequality nor high-depth
positions failing the sum premise are counterexamples to the target.

## Computation and exact coverage

The new [checker](checks.py) and its [receipt](verification.json) contain:

| Check | Exact scope and result |
| --- | --- |
| Sparse decimal sign | 10,030 comparisons, including exact cancellation and enormous exponents |
| Decimal digit endpoint | 1,500 exact comparisons at and adjacent to powers of ten |
| Literal original words | All 22,350 pairs with odd `5<=L<=301`, `3<=i<L`; 46 five-free sum-compatible pairs, 34 with `3|S`; all satisfy the target |
| Actual high-depth representative | 201 scattered five-free lengths above B; 74 actual `r_K`, none passing the full sum; greatest exact t is 64 |
| Giant sum-positive controls | Six individual positions from three inherited lengths; exact depths 4,7,0,6,6,6; all have `3|S`, pass the target and fail the full witness condition |
| Nonzero lift control | `(69489,40323)`: five zero digits at indices 6--10, first nonzero digit 4 at index 11; sum fails |
| Factor-nine negative control | `(313,51)`: `S|F` but `F mod(9S)=17496`; not in the target domain |

The exact scattered set is the five-free members above B of

```
{B+1+2u^2 : 0<=u<=127}
  union {6*7^(k-2)+1, 6*7^(k-1)-1 : 16<=k<=64}.
```

All those lengths are odd. At each one, the proved `t<K` bound and the
unique representative check together cover **every** sum-compatible
position. The hard case has no positive instance among these 201 lengths:
every actual r_K fails the full sum. The six giant positive examples all
have `t<K`; they test nonvacuous integrality and exact arithmetic without
supplying evidence of the unresolved high-depth joint premise. All six
original decimal words were separately evaluated modulo `25S` and
`7^(t+1)` by run concatenation. No modulus of size `7^(L-2)` was needed:
the exact valuation below `L-2` decisively rejects the full divisor.

These are scattered length and individual-position results. There is no
claim to have searched the intervening lengths or to extend the certified
consecutive endpoint B. The two first sampled odd lengths happen to be
adjacent to B; this investigation retains the named baseline endpoint
and reports its complete sample list instead of announcing a new range.

[proof_checks.py](proof_checks.py) separately checks rational logarithm
enclosures for the published bound, its exact affine margin
`8712828/25` at `L=10^7`, and 44,550 two-candidate decimal thresholds
(all integer lengths 5--301, both parities, all positions). See
[proof-checks.json](proof-checks.json).

The inherited archive checker was freshly run in its default
`not_rerun` enumeration mode: it authenticated the archive and all
27 internal hashes, recomputed all 74,601 retained candidates by original
decimal concatenation, and matched the retained arithmetic receipt.
All 35 PR #21 artifact bindings were also checked. The two full archive
enumerators, PR #21 million-length arithmetic scan, broad early-rejection
searches and Lean build were **not** rerun. Density claims were not audited.

## Reproduction

From the repository root, using Python's standard library:

```sh
python3 research/a398769/five-seven/decimal-height/checks.py > /tmp/height-checks.json
python3 -O research/a398769/five-seven/decimal-height/checks.py > /tmp/height-checks-O.json
cmp /tmp/height-checks.json /tmp/height-checks-O.json
cmp /tmp/height-checks.json research/a398769/five-seven/decimal-height/verification.json
python3 research/a398769/five-seven/decimal-height/proof_checks.py > /tmp/height-proof.json
python3 -O research/a398769/five-seven/decimal-height/proof_checks.py > /tmp/height-proof-O.json
cmp /tmp/height-proof.json /tmp/height-proof-O.json
cmp /tmp/height-proof.json research/a398769/five-seven/decimal-height/proof-checks.json
python3 research/a398769/five-seven/prime-sum/archive_audit.py --output /tmp/height-archive.json
```

The last command verifies retained candidates and archive integrity; it
does not rerun the exhaustive enumerators. No new assertion about global
coverage follows from its successful exit. The new checker raises if its
valuation guard `K+32` is exhausted; it never silently treats that guard
as an exact valuation or a witness exclusion.

Fresh independent review is recorded in [REVIEW.md](REVIEW.md). The draft
PR is for owner review and must remain unmerged by this investigation.

**Separate verdicts:** the proposed inequality remains open on its full
requested domain; the `{5,7}` subclass remains open; the wider A398769
digit-1 conjecture remains open. Even a proof of this inequality would
settle only this subclass.
