# Independent computational review of implementation B

Reviewer context: `/root/checker_a`, separate from `/root/checker_b`.
Date: 25 November 2026. This reviewer independently wrote implementation A
before reading B's implementation. Neither checker imports the other.

Reviewed B source SHA-256:
`8e697625fa29102dee4a4edc8d900e0aa810825c32f8f1b4a8298d0474e98125`.

**Verdict: no must-fix findings in the reviewed source.** This is review of
an exact finite computation, not a proof of the all-length statement.

## Arithmetic and coverage

* A enumerates the complete multiplicative power cycle modulo `7^k`, then
  looks up the discrete logarithm. B computes successive linearized lifts.
  B's memoization indexes odd lengths modulo `T_(k-1)` at depth k because
  the length-dependent term is multiplied by seven. The initial length
  period two and indexing by `(L mod period)//2` cover every odd length.
* At a lift, the incoming difference is checked divisible by `7^k`.
  The binomial coefficient `(10^T mod 7^(k+1)-1)/7^k` is nonzero modulo
  seven. Multiplication by its unit inverse gives the unique next digit;
  the outgoing congruence and representative bounds are checked explicitly.
* Every audited length receives a separately recalculated defining
  congruence check using modular exponentiation, independently of the cached
  recovery step. The main loop includes every odd length in the requested
  inclusive interval and partitions all four categories without witness
  filters or a parity filter on possible full-sum positions.
* B uses division-free binary concatenation for the repunit. Doubling
  a block uses `(p,r) -> (p*p,r*(p+1))`; appending a digit one sends it to
  `(10*p,10*r+1)`. Hence B evaluates `n mod S` without inverting nine,
  and `9*(n mod S)` is exactly `F mod 9S`, also when `3 | S`.
* B's arithmetic uses unbounded Python integers. Its explicit CLI length
  cap bounds resource consumption, and is not a mathematical exclusion.
  Essential failures use explicit exceptions and remain active under `-O`.
* The literal tests contain all 9,900 pairs at odd lengths 5 through 201,
  with 4,950 positions of each parity. Strict period equality is correctly
  assigned to the next depth, including even boundary lengths. Required
  controls distinguish a shallow full-sum success, loss of nine, and exact
  depth two at `(23,15)`.

## Observed checks

The reviewer independently completed A's full run normally and under
`python3 -O`; its two receipts were byte-identical. After B completed its
ordinary full run, the reviewer checked B's receipt against its current
source hash and compared both receipts' full digest, the prefix digest,
and all **100** block first/last/count/hash tuples. All agreed:

```
full:   037a7a03e48eceea6893641af0459885380975e2234aa11b6820a0d2a6c5f08f
prefix: 26f81c8c6d9f43786390b9aea1974965afe5906b280d30225a658bdb2e28c374
```

The reviewer additionally ran B's controls under `python3 -O`, and 2,267
independent targeted probes: repunits for lengths 0 through 201 versus
literal `(10^L-1)//9`, modulo each of `1,3,9,27,81,87,1053,7L+1`; then
cached versus uncached lifts at depths 1 through 8. The latter probes use
`random.seed(398769)` and, for `T=6*7^(k-1)`, the sorted distinct odd
lengths from `1,3,T-1,T+1` and `2*random.randrange(T)+1` repeated 100
times per depth. Every representative's defining congruence was also
rechecked in those probes. All passed. The checked source's mandatory
controls provide permanent reproduction. B's author separately reported
byte-identical full ordinary and optimized receipts at this same source
hash; the repository reproduction verifier checks those claims again.

Matching aggregate counts alone was not used as the agreement criterion.
The canonical records are ordered and contain length, exact integer K,
representative, category and the normalized full-sum residue; every
50,000-length block has an independent digest. `--min-length`,
`--max-length`, and `--records` allow a mismatching block to be isolated.

The finite result does not extend consecutive full-witness exclusion
beyond the inherited lengths 1 through 10,000,000 inclusive. It gives no
all-length valuation bound, effective cutoff, or Lean verification.
