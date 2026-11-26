# Witness investigation above a trillion digits

**NO WITNESS IN THE STATED SEARCH.** Neither a full witness nor a proof
of absence at every length above `10^12` was obtained. No counterexample
to the stronger early-rejection implication (E) was found. The
`{5,7}` subclass and the wider A398769 digit-1 conjecture remain open.

26 November 2026. Starting main:
`0c8a8f2dd1c8340cc6fb7c2485ad206cba72bdd7`, freshly cloned from
`lukeroyle-beep/Mathematics`. This is the merge of
[PR #20](https://github.com/lukeroyle-beep/Mathematics/pull/20), whose
audited head is `37bd10a930d6dc7c9a7bcfd8db7588451dc26da2`.
The merged reduction, early-rejection results, fixed-depth constructions,
and PR #20's lift/analytic analysis were read. Existing checkouts were
preserved in a separate clone and branch. There was no applicable
`AGENTS.md`. These are ordinary proofs and exact finite computations;
no Lean theorem was added and no Lean build was run.

## Starting evidence and unavailable attachments

Neither `A398769-Trillion-Length-Investigation.md` nor
`A398769-Trillion-Length-Evidence.zip` was available in the repository,
the Mathematics workspace, or Downloads. No archive control was silently
substituted or claimed inspected. The user's reported complete exclusion
through **`10^12` inclusive**, and reported (E) coverage through odd
**`1,694,851,493`**, remain distinct, reported results whose certificates
were unavailable here. Current main/PR #20 retain the older complete
exclusion through 10,000,000 and broad (E) through odd 9,999,999.
Those large inherited searches were not rerun. Thus this work does not
certify one combined interval starting at length one and ending above
a trillion.

[STRUCTURE.md](STRUCTURE.md) and [archive-audit.json](archive-audit.json)
record the precise evidence boundary and freshly run retained repository
controls: a nonzero sum-compatible giant pair of exact depth four, the
five-zero-lift control, the PR #19 exceptions at depths 44, 56, 85 and
92, and a factor-nine negative control. They use original decimal blocks.

## Exact criterion and complete per-length rejection

For units-indexed positions, the candidate is

```
repeat("7", L-i-1) + "5" + repeat("7", i-1) + "5".
```

The merged reduction proves that every possible `{5,7}` witness has
this form, with odd L and `3<=i<L`. It has

```
S=7L-4, P=25*7^(L-2), F=7*10^L-18*10^i-25, n=F/9.
P*S | n  iff  225*S*7^(L-2) | F.
```

Its suffix 775 gives `v5(n)=2`, so `5|S` excludes a witness. Since
`7` does not divide S, the remaining exact conditions are `9S|F`
and `v7(F)>=L-2`. The extra nine is retained even when `3|S`.

Ten has order six modulo seven and `v7(10^6-1)=1`; the lifting lemma
therefore gives exact order `T_k=6*7^(k-1)` at every depth. It generates
all units modulo `7^k`. The target `(7*10^L-25)/18` is a unit, so there
is a unique representative `0<=r_k<T_k`. At
`K=min{k:T_k>L}`, at most one position in `[3,L)` can have depth K.
Every full witness must use that position. Rejecting it, or proving it
is outside the interval, excludes **every position at that length**.

The primary scanner uses a complete low-depth power cycle followed by
linearized seven-adic lifts, with exact divisibility checks. No (E),
heuristic density, unproved global bound, prime filter, or position-strip
conjecture is used to prune lengths. A resource guard raises an error;
it cannot return an exclusion when the required test is unfinished.

The independently written verifier receives the length/position records
and the original digit specification. It imports no discovery program.
It checks the exact order and unique-representative congruence for every
row. For actual positions it derives S, the factored P and five positions
from the four decimal runs, then concatenates those runs modulo S and
the first failed seven power. Outside representatives are checked only
as the algebraic replacement of digits in the all-seven word; they are
not described as decimal candidates. See [independent/DESIGN.md](independent/DESIGN.md).

## Gap-free search immediately above a trillion

Exactly **1,000,000 odd lengths**, from `1,000,000,000,001` through
`1,000,001,999,999` inclusive, were scanned. Every has K=15.
Together with the parity exclusion, this excludes the entire interval
`10^12 < L <= 10^12+2,000,000` for the subclass, independently of the
unavailable preceding trillion-length certificate.

| Partition of the million odd lengths | Count |
| --- | ---: |
| Unique r_K outside `[3,L)` | 753,853 |
| Actual r_K with `5|S` | 48,801 |
| Actual r_K, five-free S, fails `9S|F` | 197,346 |
| Actual r_K, five-free S, passes `9S|F` | **0** |

All 246,147 actual representatives were also lifted to their first
failure, including those already rejected by the sum/five conditions.
In fact **none** passes the digit sum, including the five-filter rows.

| Exact v7(F) | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Actual representatives | 210,817 | 30,155 | 4,404 | 660 | 96 | 14 | 1 |

The unique depth-21 pair is

```
(L,i)=(1000001665855,567539735319), K=15,
S=7000011660981,
F mod(9S)=17261071696710,
F mod(7^22)=1117091728166568014=2*7^21.
```

The independent original-word check obtains
`n mod S=1917896855190` and `n mod(7^22)=558545864083284007=7^21`.
Its zero lift digits are a15 through a20; a21=3. This pair is
definitively rejected, not awaiting enormous-modulus verification.

Every row, including exact next-power and full-sum residues and the first
nonzero lift digit, is retained in [evidence/contiguous.tsv.gz](evidence/contiguous.tsv.gz).
The uncompressed ordered stream SHA-256 is
`7cbc3e734b1123ad3cdfdeb28a40e1af2e86e0b370c9b0b94d0083858428652a`.
[The primary summary](evidence/contiguous.json) and
[the independent full-stream receipt](independent/contiguous_stream.json)
agree. The latter checks every row and all seven possible first-failure
lifts; the hash alone is not the verification.

## Two additional finite directions

**High-valuation direction.** [bands.py](bands.py) searches sixteen
explicit odd lengths in each order band K=16 through 128: **1,808
lengths**. Their exact formula is in [scope.json](scope.json); every
one exceeds `10^12`. Counts are 782 outside, 175 actual with `5|S`,
851 actual five-free sum failures, and zero joint passes. All 1,026
actual positions were independently checked from decimal blocks.
The greatest exact depth is 128. Every sampled length is completely
excluded using its unique r_K, but the lengths between samples are
**not** covered. Exact pairs and residues are in
[evidence/bands.json](evidence/bands.json) and the independent audit in
[independent/bands_check.json](independent/bands_check.json).

**Digit-sum-first direction.** The [family investigation](families/README.md)
enlarges an inherited progression to

```
S=898129*3^(193+210t), L=(S+4)/7, t=0,1,...,31.
```

For each of these **32 selected lengths**, it establishes the complete
class of actual positions passing `9S|F`, then intersects that class
with every seven-adic lift until no positions remain. It covers all
**479,894** actual sum-compatible positions. All have five-free S;
K ranges from 116 to 3,791. The exact depth distribution is:

| Depth | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Positions | 239,950 | 0 | 205,666 | 29,382 | 4,198 | 597 | 85 | 13 | 3 |

The depth-eight positions occur at t=13,24,26. None reaches K.
Each entire selected length is excluded, not just a preferred position.
The complete class, period, count at every depth, and every deepest
pair's nonzero rejection residue are in [families/results.json](families/results.json).
The [independent family audit](review-family.py) reconstructs the joint
classes by extending the previous class, without importing the discovery
logarithm or CRT solver. It verifies each full-sum class using original
decimal blocks and independently recovers every count; its receipt is
[review-family.json](review-family.json).
These are sparse length samples; t outside 0..31 and intervening lengths
are omitted. The t=0 length was already excluded in earlier repository
work; this is a fresh check, not a claim that all 32 exclusions are new.

## Structural outcome and precise remaining obligation

The [structural note](STRUCTURE.md) gives a useful all-parameter count
for the inherited subfamily `a=193+1470t`: at most 154 sum-compatible
positions can reach depth four, 22
depth five, four depth six and one depth seven. **At most one still
allows a witness.** The infinite family compatibility theorem is not an
infinite rejection theorem.

PR #20 proves that unrestricted exponent CRT compatibility stabilizes
by K. It therefore cannot supply a later incompatibility contradiction.
Its size and polynomial-root estimates do not give a uniform failed-lift
bound on all sum-compatible actual positions. Qualitative finiteness,
spacing and fixed-depth constructions do not determine whether there is
an isolated solution beyond these tests.

For every unsearched odd L above a trillion with five-free S, the
remaining problem is still: does the actual r_K pass `9S|F`, and, if
so, can **every lift digit a_K through a_(L-3) be zero**? To prove
absence it suffices to force a nonzero digit in that interval at every
such pair, or establish and discharge an effective global cutoff.
No such theorem was obtained. No apparent witness survives to require
a compact certificate through L-2. Modular samples and hashes have not
been promoted to certificates of those untested depths.

## Reproduction

Run from the repository root with Python 3.14 and a C++17 compiler
supporting unsigned 128-bit products. The code uses only the Python
standard library. Compiler/Python versions and fresh check identities
are recorded in the final verification receipt.

```sh
clang++ -O3 -std=c++17 research/a398769/five-seven/trillion-witness/scan.cpp -o /tmp/trillion-scan
/tmp/trillion-scan 1000000000001 1000000 > /tmp/trillion.tsv
python3 research/a398769/five-seven/trillion-witness/summarize.py /tmp/trillion.tsv --output /tmp/trillion-evidence
cmp /tmp/trillion-evidence/contiguous.json research/a398769/five-seven/trillion-witness/evidence/contiguous.json
python3 research/a398769/five-seven/trillion-witness/independent/verify_stream.py /tmp/trillion.tsv --start 1000000000001 --stop 1000001999999 > /tmp/trillion-independent.json
cmp /tmp/trillion-independent.json research/a398769/five-seven/trillion-witness/independent/contiguous_stream.json
python3 research/a398769/five-seven/trillion-witness/independent/verify_stream.py research/a398769/five-seven/trillion-witness/evidence/small.tsv.gz --start 5 --stop 5003 > /tmp/trillion-small-independent.json
cmp /tmp/trillion-small-independent.json research/a398769/five-seven/trillion-witness/independent/small_stream.json
python3 research/a398769/five-seven/trillion-witness/bands.py > /tmp/trillion-bands.json
cmp /tmp/trillion-bands.json research/a398769/five-seven/trillion-witness/evidence/bands.json
python3 research/a398769/five-seven/trillion-witness/families/search_families.py --first-t 0 --last-t 31 > /tmp/trillion-families.json
cmp /tmp/trillion-families.json research/a398769/five-seven/trillion-witness/families/results.json
python3 research/a398769/five-seven/trillion-witness/review-family.py > /tmp/trillion-family-independent.json
cmp /tmp/trillion-family-independent.json research/a398769/five-seven/trillion-witness/review-family.json
```

[Independent reproduction and controls](independent/README.md) include
the original-word CLI, the 2,500-length small stream, literal decimal
tests, order boundaries, and deliberate corruption rejection.
[STRUCTURE.md](STRUCTURE.md) has the retained-control commands.
No full trillion-length run or giant `7^(L-2)` calculation was performed.
All files are preserved on a dedicated draft review branch; merging is
left to the repository owner.
