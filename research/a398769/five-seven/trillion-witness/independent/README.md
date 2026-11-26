# Independent original-digit verifier

`verify_digits.py` receives only `(L,i)` and reconstructs the decimal word
`7^(L-i-1) 5 7^(i-1) 5`, with exponents denoting repetition. It has no imports
from the discovery search. Its modular arithmetic uses original block
concatenation, not the search numerator formula or a supplied residue.
[DESIGN.md](DESIGN.md) states the independently fixed method and its scope.

From the repository root:

```sh
python3 research/a398769/five-seven/trillion-witness/independent/verify_digits.py --self-test
python3 -O research/a398769/five-seven/trillion-witness/independent/verify_digits.py --self-test
python3 research/a398769/five-seven/trillion-witness/independent/verify_digits.py --pair 61 57 --max-depth 256
python3 research/a398769/five-seven/trillion-witness/independent/verify_digits.py --pairs-json pairs.json --max-depth 256
```

The pair file must be a JSON list such as `[[61,57],[313,51]]`; it contains no
claimed residues. All lengths and positions are integers, and positions count
from the units digit starting at zero. The default affordable cap is 256 powers
of seven; the CLI accepts caps 1 through 100,000. No integer of the requested
trillion-digit size or modulus `7^(L-2)` is materialized.

Fresh self-tests cover all legal positions for odd lengths 5 through 65, with
11,904 residue comparisons against explicitly constructed decimal integers.
This includes moduli sharing factors with ten or nine and the original full
divisor `P*S`. `(61,57)` is a nonzero reduced-domain digit-sum positive control:
`S=423`, `5` does not divide `S`, and the exact seven-adic valuation is 1.
With a depth cap of 1 its verdict deliberately remains awaiting full
verification, with exponents 2 through 59 outstanding. `(313,51)` guards the
factor-nine error: `S=2187` divides `9n`, but `n mod S=1944`, so the actual
sum test rejects it. These tests run byte-identically under ordinary and
optimized Python; correctness guards use explicit exceptions, not `assert`.

The merged elementary reduction was read and checked: the eight possible
three-digit suffixes exclude three fives; parity excludes even lengths; zero
and one five are impossible; exactly two fives give the four-block word; and
`7|n` requires `i=3 mod 6`. The suffix 775 has exact five-adic valuation 2.
After excluding `5|S`, the sum and seven-power conditions are coprime and are
sufficient together with `25|n`. This review is ordinary mathematics; no new
Lean proof or Lean build is claimed.

## Complete interval certificate and sampled bands

The stream verifier accepts the discovery's integer representative for every
length, but independently verifies it. It checks the exact multiplicative order
of ten by testing the order and its quotients by every prime factor. Since
`T_K>L`, a canonical representative is the only possible position in `[0,L)`.
For each row it verifies the representative congruence using an independently
constructed all-seven word with the two digit replacements. For an outside
representative this replacement is only a polynomial congruence, never a claim
that it describes an actual decimal word. At every actual position, the sum
residue and first failed seven-power residue are recomputed by the original
four-run concatenation. Every one of the seven possible next lift digits is
also checked. Endpoints and step-two length succession are mandatory; a missing
row, duplicate row or truncated certificate is rejected.

```sh
python3 research/a398769/five-seven/trillion-witness/independent/verify_stream.py research/a398769/five-seven/trillion-witness/evidence/contiguous.tsv.gz --start 1000000000001 --stop 1000001999999
python3 research/a398769/five-seven/trillion-witness/independent/mutation_controls.py research/a398769/five-seven/trillion-witness/evidence/contiguous.tsv.gz
python3 research/a398769/five-seven/trillion-witness/independent/verify_bands.py research/a398769/five-seven/trillion-witness/evidence/bands.json
python3 research/a398769/five-seven/trillion-witness/independent/verify_digits.py --pair 1000001665855 567539735319
```

Fresh audit receipts:

- `contiguous_stream.json`: every one of 1,000,000 odd lengths from
  1,000,000,000,001 through 1,000,001,999,999; all representatives and all 246,147
  actual positions checked independently. The largest exact seven-adic depth
  is 21. No actual position passes the full digit sum, even among rows rejected
  by `5|S`.
- `strongest_contiguous.json`: a separate pair-only verification of the
  depth-21 example `(1000001665855,567539735319)`.
- `small_stream.json`: all 2,500 odd lengths 5 through 5,003 in the small control
  stream, with 935 actual original-digit checks.
- `bands_check.json`: all 1,808 prescribed samples, 16 each at `K=16..128`,
  including 1,026 actual positions. The largest exact depth is 128. This is
  sampled coverage, not a contiguous extension beyond the interval above.
- `mutation_controls.json`: an undamaged 20-row prefix passes, while nine
  corruptions of lengths, representative, K, sum residue, seven residue, depth,
  next lift, category, or completeness are each rejected.

Self-tests, the small stream, band audit and mutation controls were also run
under `python3 -O` with byte-identical receipts. The million-row independent
stream was freshly run once in ordinary Python. Its correctness guards are
explicit exception checks. Hashes identify the inputs and verifier versions;
the exact modular calculations and order argument, not those hashes, establish
finite coverage.

The three family pairs of exact depth eight also received fresh standalone
checks from **pair-only input**, separately from the independent complete-family
audit. `family_depth_eight_pairs.json` contains only the three `(L,i)` pairs;
`family_depth_eight.json` derives their original words, sums, products, positions
and residues. All three pass the full digit sum and have exact `v7(n)=8`, with
`K=1657,2961,3198`. Their original-number residues modulo `7^9` are respectively
`7^8`, `2*7^8`, and `4*7^8`. Therefore each is definitively rejected.

```sh
python3 research/a398769/five-seven/trillion-witness/independent/verify_digits.py --pairs-json research/a398769/five-seven/trillion-witness/independent/family_depth_eight_pairs.json
```
