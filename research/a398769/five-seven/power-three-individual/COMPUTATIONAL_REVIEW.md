# Independent computational review

**Verdict: PASS.** No unresolved computational findings at implementation
commit `561cd96effccc9362255ac6c766445fafaec3145`, based on
`a9edeb0a96bd56d55f3c96767f5154e69cb8ceda` (PR #29's merge).
Builder context: `/root`. Independent reviewer context:
`/root/final_computational_review`. The reviewer authored none of the
17 implementation paths. The separate mathematical verdict is in
[MATH_REVIEW.md](MATH_REVIEW.md).

## Methods and precision

The reviewer inspected all four arithmetic programs and the explicitly
reused inherited Newton/logarithm source. Newton doubling uses a unit
seventh-root derivative. The division by 18 retains two ternary digits,
and dividing the logarithms retains two more. The logarithm tail and
all skipped terms vanish at the stated precision. Precision 1580 supplies
theta modulo 3^1582, sufficient for the last a=1579 exact-valuation test,
and kappa modulo 3^1578, exceeding the required 3^1577. Precision 1586
provides a separate stability check.

The decimal-block implementation has no project arithmetic imports and
checks every ternary child. It reconstructs the original decimal word
modulo each required factor. In the index engine, division by seven is
performed after obtaining the numerator modulo seven times the exponent
modulus. The coefficient seven in F correctly lowers the power-of-ten
precision needed. Every range and deadline is inclusive where required:
first failure at depth m excludes only when m<=L-2; valuation t=L-2
would already qualify. Both valuation resource guards raise errors and
are never credited as exclusions.

All four programs freshly reproduced their retained receipt bytes in
ordinary Python and under `python3 -O`. The aggregate additionally checks
complete source/base bindings, method agreement, inherited finite coverage
and nine corruptions. It was rerun in both modes at the reviewed commit.
The review checker binds every implementation path to `git show` of that
immutable commit; later review-only files do not relax those bindings.

## Independent additional arithmetic

`review_check.py` imports no submitted arithmetic for its original-word
or fixed-position calculations. It independently:

- compares the 17 ordered member rows and checks exact L,S,d, range,
  ternary order, digit-sum class and reduced gcd data;
- computes each actual original word as seven times a repunit minus the
  two digit changes, retaining modulus 9M before dividing by nine;
- verifies n modulo 25S and every residue through the first failure;
- reconstructs the literal 313-digit control, its product and sum, and
  both full divisibility predicates, detecting the lost factor nine;
- checks the entire depth-six permutation over all 2,401 indices for
  each of seven positions, using L_(u+1)=729L_u-416, then independently
  checks every child by direct exponentiation through depth six;
- rejects two coordinated corruptions to both individual receipts in
  addition to the aggregate's nine corrupted-evidence controls.

The complete depth-six zero classes are:

| Fixed s | Unique u modulo 2401 |
|---:|---:|
|39|1530|
|81|954|
|123|2380|
|165|1839|
|207|1193|
|249|932|
|291|174|

These are bounded independent checks of the proved fixed-s statement;
they supply no theorem that the moving ternary position must escape.

The new a=1573 row is correctly classified as a range miss despite
s mod126=123; no original word is evaluated outside its length.
The a=1579 row is actual with g=1, q=L, n mod25S=0 and n mod49=14,
so exact t=1 excludes it. The actual a=1231 control has t=4 and first
nonzero original-word residue 14406 modulo 16807. The a=25 sum-positive
and a=1567 inherited controls reproduce.

## Reproduction and limits

From the repository root:

```sh
pt=research/a398769/five-seven/power-three-individual
python3 "$pt/review_check.py"
python3 -O "$pt/review_check.py"
```

Both commands recompute the independent checks, rerun the aggregate's
four engines and compare the review receipt and source bindings. The
retained JSON binds this note, the separate mathematical note and the
review checker as well as the immutable implementation.

The accepted finite family coverage is 259 named exponents through a=1579;
next unchecked a=1585. Most historical family rows are inherited and
cross-compared, not newly reconstructed by this review. Consecutive
whole-length exclusion remains 1 through 1,000,002,000,000 inclusive.
The remaining individual family, unrestricted {5,7} subclass and wider
digit-1 assertion remain open. No historical large enumeration or Lean
formalization/build was performed by this review.
