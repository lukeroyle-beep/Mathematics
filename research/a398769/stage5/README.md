# A398769 Stage 5: no-7 reduction and the 23-digit search

Reproduced on an arm64 Mac on 24 November 2026, from the supplied
`A398769-Stage5-checkpoint.zip`, based on merged revision
`0c13017980679832e6f03b31e6a304da7749dc4f` (PR #5).
For a positive odd integer with no decimal digit 1, write `P` for its digit
product and `S` for its digit sum. A counterexample satisfies `P*S | n`.

This checkpoint establishes two distinct results:

- **All lengths:** if a counterexample contains no 7, its digits are all 3 or 9.
- **Finite computation:** two exhaustive searches find no 23-digit
  counterexample over the full alphabet `{3,5,7,9}`. Combined with the
  [earlier bound below 10^22](../stage3/README.md) and the
  [all-length parity theorem](../stage2/README.md), this excludes every
  counterexample with `0 < n < 10^24`.

The no-7 theorem also combines with the retained
[Stage 4 search through 75 digits](../stage4/search/RESULTS.md) to exclude
no-7 candidates through 75 digits. Those earlier finite results are reused;
the complete Stage 3 and Stage 4 searches were not rerun for this checkpoint.
The computations are not Lean kernel certificates. None of these results
settles the unrestricted conjecture.

## The no-7 theorem

[`A398769.Stage5.digitsThreeOrNine_of_noSeven`](../../../A398769/Stage5.lean)
uses the actual decimal digits of `n` and the Stage 2 restrictions. With no 7,
all digits belong to `{3,5,9}`. No number with these digits is divisible by
25, as its last two digits cannot be 00, 25, 50 or 75. Thus there can be at
most one 5. If there is exactly one, the number is 2 modulo 3; no 3 or 9 can
occur, since each digit divides `P` and hence `n`. But for an all-5 digit
list, both `P` and `S` are divisible by 5, again forcing `25 | n`.

The supplied `NoSeven.lean` is included byte-for-byte as `A398769/Stage5.lean`
and imported by the root library. A clean project build with pinned Lean
4.24.0 passed (806 jobs). Upstream dependency artifacts were reused from
copies of checkouts whose revisions match `lake-manifest.json`; the original
checkout was preserved. The final theorem's complete [axiom report](axioms.txt)
is `[propext, Classical.choice, Quot.sound]`. There is no `sorry`, custom axiom
or `native_decide` in the proof.

## Exhaustive 23-digit computations

| Method | Multisets | Enumeration work | Hits |
|---|---:|---|---:|
| C++ prefix and derived tail | 2,600 | 2,546 viable multisets; 3,161,494 prefixes; 1,001,382 tails in range | 0 |
| Python quotient and suffix congruences | 2,600 | 5,115,601 candidate integers checked | 0 |

Both methods enumerate every multiset of 23 digits in `{3,5,7,9}`, including
more than eight 5s and repeated blocks. They share the mathematical condition,
but use different enumeration procedures and integer representations.

For each multiset, the C++ program chooses a power of ten `B <= D = P*S`.
For each permissible prefix `h`, at most one tail `0 <= r < B` satisfies
`h*B+r = 0 (mod D)`. It derives that tail and checks the exact remaining
digit counts, including fixed-width leading zeros. The largest possible
divisor is `207*9^23 < 2^128`; decimal values are below `10^23`. The counters
are bounded by `5^23 < 2^64`, even when 1 is allowed for controls.

Python bounds the quotient `q` using the smallest and largest arrangements
of each multiset. Each compatible suffix gives a congruence for `D*q` modulo
`10^width`; the digit sum gives another modulo 9. Dividing out the relevant
greatest common divisors leaves invertible factors and coprime moduli. The
program enumerates every compatible quotient in range and checks its complete
digit multiset. Python integers have arbitrary precision.

The prior bound covers through length 21; length 22 is impossible by parity.
The new computation covers length 23. Thus all lengths below 24 are covered.
Length 24 is also impossible by parity; the next unchecked length is 25.

## Controls and review

For a 23-place positive control, take 21 ones and two threes. Direct arithmetic
on all `binomial(23,2) = 253` placements finds ten hits, and both programs return
exactly those ten integers. Their values exceed 64-bit unsigned capacity.
The C++ control visits 232 prefixes and 96 tails in range; Python checks 27
candidate integers with suffix width 21.

[`check_controls.py`](check_controls.py) compares both programs against direct
decimal arithmetic on small complete alphabets and odd-digit multisets,
checks the full-width control, and rejects malformed commands. The existing
Stage 3 controls also pass against this C++ source at lengths 1 through 9,
with and without digit 1, and on the 21-digit positive control.
See [independent review](REVIEW.md) and [Mac run receipt](run-receipt.json).

The original archive was reproduced before any changes to its search code.
The integrated Python program additionally rejects invalid lengths, suffix
widths and multisets, and displays `NOT_CHECKED` in count-only mode. Its search
algorithm is unchanged. The C++ header's filename was corrected.

## Reproduce

Use the pinned Lean toolchain, Python 3.8 or newer, and a C++17 compiler with
unsigned 128-bit integers. From the repository root:

```sh
lake clean mathematics
lake build
lake env lean A398769/Stage5.lean
c++ -O3 -std=c++17 -Wall -Wextra -pedantic research/a398769/stage5/prefix23.cpp -o /tmp/a398769-stage5-prefix
/tmp/a398769-stage5-prefix 23
python3 research/a398769/stage5/quotient23.py 23 5 --run
/tmp/a398769-stage5-prefix 23 --multiset 11111111111111111111133
python3 research/a398769/stage5/quotient23.py 23 21 --multiset=11111111111111111111133 --run
python3 research/a398769/stage5/check_controls.py /tmp/a398769-stage5-prefix
python3 research/a398769/stage3/check_controls.py /tmp/a398769-stage5-prefix
```

`lake clean mathematics` removes this project's build products while preserving
compiled dependencies. The Python output fields are length, suffix width,
multisets, candidate count and hits. **Without `--run`, candidates are counted
but not checked**, and the last field is `NOT_CHECKED`. Both programs accept
lengths 1 through 23; Python requires `1 <= width <= length`.

On the reproduction Mac the matching toolchain was already installed at
`/private/tmp/lean-4.24.0-darwin_aarch64/bin`; that directory was prepended to
`PATH` for the Lean commands. Standard Elan installations use the repository's
`lean-toolchain` file.

## Next research target

Investigate the all-length subclass whose digits are only 5 and 7. This is a
separate proof problem; no all-length exclusion of that subclass is claimed
by this checkpoint.
