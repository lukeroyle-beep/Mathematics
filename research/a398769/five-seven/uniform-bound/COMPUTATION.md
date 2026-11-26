# Exact checks and reproduction

Observed environment: CPython **3.14.4**, standard library only, Darwin
arm64; Git **2.54.0 (Apple Git-157)**. The checker sources and complete
deterministic outputs are committed. Every receipt contains its source
SHA-256; the aggregate binds source and receipt hashes and the baseline.
These are exact finite computations supporting ordinary proofs. They do
not formalize the proofs in Lean or certify an all-length search.

## Primary checks

[`exact_checks.py`](exact_checks.py) produces
[`exact_results.json`](exact_results.json). No assertion is used for an
essential check; explicit exceptions remain active under `python3 -O`.

| Check | Exact scope and result |
| --- | --- |
| Quadratic sufficiency | Exact K=9 and K=10 base margins are 1,899,999 and 24,588,805. Algebraic induction proves all larger K; finite controls K=9--200 check the implemented arithmetic only. |
| Uniform derivative comparisons | At the least remaining odd lengths, `L-2-2B_K` is 9,495,997 for K=9 and 33,917,979 for K=10. The dependent-root margins are 9,747,988 and 34,253,381. |
| Logarithmic constants | A 60-term rational atanh series with explicit remainder and reduction to [1,2] certifies `168(log10)^2/(log7)^4<63`, `log7<2`, and `log10>2`. |
| Exponent lifts | All 149 odd lengths 5--301, digit indices 1--8: 1,192 comparisons of the linearized digit with exhaustive testing of all seven lifts, including 187 zero and 1,005 nonzero digits. All actual positions are also directly enumerated at their own K. |
| Polynomial identities | Every odd L=5--61, every `3<=i<L`, every reduced `0<a<b<=min(L,16)`: 67,410 identities, including both derivative formulas, all three derivative branches, content and span. There are 11,925 positive-depth cases, 1,352 singular positive-depth cases, and 25,953 negative-s cases. |
| Hensel loss | 1,564 transformed-polynomial root checks in the declared subdomain (`t>2d`, and `L<=25` or `d>0`), plus separate degree-50 and derivative-two controls. The latter has `(L,i,a,b)=(233,183,7,9)`, `t=5,d=2`, exact root distance 3. |
| Degree correction | Twenty exact rational LTE controls, degree factors 1,2,7,14,49 and signed exponents -7,-1,1,7. These test the algebraic valuation correction, not the existence of roots of every listed global degree. |
| Stabilization sharpening | Direct order enumeration at all 199 five-free odd lengths 5--501; equality controls `(L,S,order,e)=(13,87,28,1)` and `(85,591,98,2)`. |
| Size-method obstruction | Exact difference `A_12-B_12=115445517975`; the proof uses growth comparison to cover every L>=12. |

The polynomial and lift loops are exhaustive on their **finite declared
domains**: they iterate every integer index, rejecting only unreduced
centres or the explicitly stated root-check subdomain. Root lifting starts
from all seven residues of the transformed polynomial and tests all seven
lifts at each step. Completeness of the all-length mathematics is supplied
by the proofs, not by extrapolating these loops.

Meaningful nonzero controls include `(L,i)=(61,57)`, where `9S|F` and
`v7(F)=1<K=3`; the exact cofactor lift identity is checked. The inherited
zero-run position `(69489,40323)` has `K=6,t=11` and digits
`a_6,...,a_11=(0,0,0,0,0,4)`, but fails `9S|F`. Its depth is certified
modulo `7^12`, without constructing F. The depth-44 example is likewise
certified modulo `7^45` and `9S`, and its first escape digit is `a_44=1`.

Six deliberate failures are rejected: valuation of zero, an unreduced
centre, the non-strict Hensel boundary `t=2d`, a false guard, cancelling
nine when `(L,i,S)=(151,8,1053)`, and mislabelling the depth-44 example as
a counterexample to (E). In the factor-nine control, `S|F` but
`F mod9S=8424`. The `q=0` control uses `b>L` and is explicitly outside
the positive-exponent theorem application.

## Independently structured verification

The independent reviewer authored [`review_check.py`](review_check.py)
without importing the primary checker. Its retained output is
[`review_results.json`](review_results.json). It traverses centres first
and checks all odd `max(5,b)<=L<=101`, `3<=i<L`, and reduced
`0<a<b<=25`: **476,814** identities, 82,331 positive-depth cases, 9,910
singular-centre positive-depth cases, and 1,653 cases with derivative
valuation greater than one.

It uses a separate 120-term rational logarithm enclosure, checks all ten
published table entries and their minimum `c*nu^2=465`, and independently
confirms the two cutoff rows. Four direct modular Newton computations
check the Hensel distance for d=0,1,2, including the degree-50 polynomial;
this differs from the primary transformed-polynomial enumeration. Its
zero-run computation uses direct original-F residues and an independent
repunit calculation for the digit-sum rejection. Four deliberate failure
controls are rejected under both Python modes.

For the specified envelope obstruction, five **actual rational** family
pairs (family parameters 1,2,3,10,100) exhaust every potentially useful
reduced denominator, up to 21,27,31,46,100 respectively: 4,367 centres in
total. The algebraic proof covers every family parameter and every
denominator, while this finite check supports the implementation. These
pairs are not certified as `r_K` or as passing the digit-sum test.

## Effective parameterwise threshold examples

The primary checker executes (13a), starting at k=10 and checking every
successive k, so the returned k0 is the least one permitted by that stated
algorithm. These are **position** thresholds, not global cutoffs:

| b | Delta | First k0 | Inclusive length start `6*7^(k0-2)` |
| ---: | ---: | ---: | ---: |
| 3 | 0 | 10 | 34,588,806 |
| 12 | 1 | 12 | 1,694,851,494 |
| 101 | 0 | 17 | 28,485,369,059,658 |
| 12 | 1,000,000,000 | 21 | 68,393,371,112,238,858 |

Each applies to every reduced numerator `0<a<b` with its specified
`|bi-aL|<=Delta`, above that row's start. No new discharge of the earlier
finite gap is asserted. Some individual domains are already covered more
strongly by inherited results; these rows illustrate parameter growth,
not an optimization or a new consecutive coverage claim. The algorithm's
termination and persistence are proved in [ANALYTIC.md](ANALYTIC.md).

## Commands and retained baseline evidence

Run from the repository root:

```sh
python3 research/a398769/five-seven/uniform-bound/exact_checks.py > /tmp/uniform-exact.json
python3 -O research/a398769/five-seven/uniform-bound/exact_checks.py > /tmp/uniform-exact-O.json
cmp /tmp/uniform-exact.json /tmp/uniform-exact-O.json
cmp /tmp/uniform-exact.json research/a398769/five-seven/uniform-bound/exact_results.json
python3 research/a398769/five-seven/uniform-bound/review_check.py > /tmp/uniform-review.json
python3 -O research/a398769/five-seven/uniform-bound/review_check.py > /tmp/uniform-review-O.json
cmp /tmp/uniform-review.json /tmp/uniform-review-O.json
cmp /tmp/uniform-review.json research/a398769/five-seven/uniform-bound/review_results.json
python3 research/a398769/five-seven/uniform-bound/verify.py > /tmp/uniform-verification.json
python3 -O research/a398769/five-seven/uniform-bound/verify.py > /tmp/uniform-verification-O.json
cmp /tmp/uniform-verification.json /tmp/uniform-verification-O.json
cmp /tmp/uniform-verification.json research/a398769/five-seven/uniform-bound/verification.json
git diff --check
```

The aggregate runs both new checkers in both modes and compares their
complete output to the retained receipts. It compares every inherited
tracked file except root navigation against starting main. It executes
the inherited early-rejection **receipt verifier**, with no `--recompute`:
100 ordered blocks are checked with `fresh_full_runs=[]`. This also checks
the inherited source/receipt hash chain, including the older ten-million
certificates. It cross-checks all 100 retained PR #19 rows between the
independent implementations and freshly recomputes the four exceptional
valuation/digit-sum modular certificates. It does not regenerate that
entire depth table or either ten-million search.

No resource-intensive search beyond the stated bounds was launched.
No generated float is used to certify an inequality. No new whole length
is claimed excluded, and broad (E)'s finite interval is unchanged.
