# Independent archive control

The reported **zero digit-sum passes among all 74,601 retained pairs is
confirmed**. This computation tests the exact digit sum at each retained
position. It neither reruns the complete enumeration nor asserts a
valuation ceiling outside the inherited finite interval.

## Fresh arithmetic and controls

[`archive_control.py`](archive_control.py) imports no repository program.
For every retained pair `(L,i)`, it evaluates the original decimal word

```text
repeat("7", L-i-1) + "5" + repeat("7", i-1) + "5"
```

modulo `S=7L-4` by repeated concatenation. A word is represented by its
value and its decimal shift; appending `(b,q)` to `(a,p)` gives
`(a*q+b,p*q)`, modulo the chosen modulus. Binary doubling handles each
run. This path does not form `F` and never divides by nine or inverts
nine, so it is valid when three divides S.

A separate path computes
`F mod(9S)=(7*10^L-18*10^i-25) mod(9S)` using Python's modular powers.
For every pair it checks the exact integer equality

```text
F mod(9S) = 9 * (n mod S).
```

Thus both paths test the same actual position and preserve the entire
factor nine. No primality test or prime-S restriction is used.

The complete results are in [`archive-control.json`](archive-control.json):

| Freshly checked quantity | Result |
| --- | ---: |
| Distinct retained pairs in the stated domain | 74,601 |
| Exact digit-sum passes `S | n`, equivalently `9S | F` | **0** |
| Even the weaker test `S | F` | 0 |
| Pairs with `3 | S` | 24,873 |
| Pairs with `5 | S` | 14,919 |
| Pairs with `5` not dividing `S` | 59,682 |

Every original decimal word is also evaluated modulo `7^28` and compared
with the sparse expression. Each residue is nonzero; repeated exact
integer division of that bounded residue proves the valuation:

| `t=v7(n)=v7(F)` | 22 | 23 | 24 | 25 | 26 | 27 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pairs | 63,974 | 9,161 | 1,272 | 162 | 29 | 3 |

The receipt records both sum residues and both normalized next-seven
residues for the three depth-27 pairs. All have `t<L-2`. The complete
ordered arithmetic stream, consisting of each pair, both sum residues,
exact valuation and normalized next-seven residue, has SHA-256
`51fcd6c2c3c4af80ab68c031b84d6c40654e90cc1584eda6a617325beed73625`.
The checksum summarizes recomputed rows; it does not replace the tests.

The checker also performs 19,600 comparisons with literal decimal words
for every odd `5<=L<=101`, every `3<=i<L`, and eight moduli. It checks
the literal digit sum, product and full-divisor identity. Positive
sum-only controls are `(L,i,S)=(61,57,423)` and `(165,33,1151)`; the first
has composite `S=9*47`. Neither is a full witness. The nonzero original
predicate positive `135` and negative `137` test divisibility by the
literal product times sum; these controls are outside this subclass.

A specific negative control shows why omitting nine is invalid:

```text
L=313, i=51, S=2187=3^7,
F mod S=0, n mod S=1944, F mod(9S)=17496.
```

This pair has five-free S and the admissible position residue, yet fails
the digit sum. The fresh archive result did not rely on the weaker test.

## Exact inheritance boundary

The archive ZIP, all 27 manifested members, CSV SHA-256, CRCs, row arity,
ordering, uniqueness and every pair's domain were freshly checked. The
ZIP is 920,596 bytes with SHA-256
`b657f158d6362c77c570b87c3c193fe54c6f3c385889379edf5bf79b71f05c0a`;
the canonical CSV hash is
`919c091c978ee1e6011f9239fadbba675985714f286d8dcffa1a29ed043cf8e4`.
The retained artifact manifests for PR #22 (`prime-sum`) and PR #21
(`trillion-witness`) are also freshly hash-checked. This binds the
inherited evidence, not a new execution of its searches.

The following mathematical/computational completeness facts are
**inherited**, with their provenance preserved:

1. [PR #22's archive audit](../prime-sum/ARCHIVE_AUDIT.md) proves that the
   two independent complete enumerations include every pair in
   odd `5<=L<=10^12`, `3<=i<L` reaching `t>=22`. Neither enumerator was
   rerun here. The fresh retained-row tests cannot establish that an
   omitted pair has `t<22` without this completeness claim.
2. PR #22 combines this enumeration, small literal checks, and the
   inherited elementary reduction to exclude every original subclass
   length `1<=L<=10^12`. Those small checks and the all-pattern reduction
   are not replaced by this retained-list computation.
3. [PR #21's adjoining interval](../trillion-witness/README.md) excludes
   every odd length from `1,000,000,000,001` to `1,000,001,999,999`;
   parity supplies the even lengths through `B=1,000,002,000,000`.
   That million-length scan was not rerun here.

Therefore the credited consecutive endpoint remains **B**, and this
control certifies **zero new lengths** beyond it. The separate archived
842-million-length early-rejection computation is neither rerun nor
needed here. A zero count on the retained list and a hash match alone
are not independent proofs of complete enumeration.

Combining inherited completeness with the fresh zero count shows
`t<=21` for every digit-sum-compatible pair in the finite domain through
`10^12`; PR #21 provides the adjacent interval. It does **not** show
`t<=21` above B. The inherited
[fixed-depth theorem](../fixed-depth/README.md) supplies infinitely many
actual sum-compatible pairs of exact valuation k for every fixed `k>=1`,
including `k=22`, at unbounded lengths. Its condition `225S | F` also
forces five-free S because `v5(F)=2`. Hence a universal ceiling of 21 is
false. These constructions do not meet the diagonal requirement
`t>=L-2`, so they supply no full witness.

## Reproduction

From the repository root:

```sh
python3 research/a398769/five-seven/explicit-length/archive_control.py > /tmp/a398769-archive-control.json
cmp /tmp/a398769-archive-control.json research/a398769/five-seven/explicit-length/archive-control.json
python3 -O research/a398769/five-seven/explicit-length/archive_control.py > /tmp/a398769-archive-control-opt.json
cmp /tmp/a398769-archive-control.json /tmp/a398769-archive-control-opt.json
```

Normal and optimized execution were both run and their outputs agree
byte-for-byte. All validations use explicit exceptions, so optimization
cannot remove them. The final optimized run takes approximately four
seconds on this machine; runtime is not part of the deterministic receipt.
