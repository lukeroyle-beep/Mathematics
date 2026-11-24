# A398769 · The 21-digit search

On 24 November 2026, two exhaustive implementations found **zero 21-digit counterexamples** to Chai Wah Wu's digit conjecture. Together with the reproduced search below 10²⁰ and the exclusion of even lengths, this checks every positive integer below **10²²**. The first unchecked digit length is 23. This is a computational bound. The all-length conjecture remains open in the public sources checked. [Original conjecture](https://oeis.org/A398769/internal) · [Equivalent formulation](https://oeis.org/A398768/internal) · [Earlier work](../README.md)

For a positive integer n, let S be its decimal digit sum and P its digit product. A counterexample is odd, lacks a 1 and satisfies SP | n. Every digit must be among 3, 5, 7 and 9. A zero makes the divisor zero, and any other even digit makes it even. The sum of an even number of those odd digits is even, so all even lengths are excluded. Both implementations checked the full four-digit alphabet, including strings with more than eight 5s and strings that repeat a shorter block.

## Evidence

The existing [Python quotient search](../by_multiset.py) constructs multiples of SP over the range for each digit multiset, then checks their digits. The new [prefix search](prefix_tail.cpp) constructs leading digits and derives the only possible suffix. The methods share the mathematical definition and the four-digit alphabet. They use separate implementations, integer representations and enumeration procedures.

| Digit length | Multisets examined | Prefixes checked | Suffixes within the numerical interval | Prefix search hits | Quotient search hits |
|---:|---:|---:|---:|---:|---:|
| 15 | 816 | 33,270 | 10,754 | 0 | 0 |
| 17 | 1,140 | 104,730 | 33,311 | 0 | 0 |
| 19 | 1,540 | 325,730 | 103,940 | 0 | 0 |
| **21** | **2,024** | **1,016,064** | **323,272** | **0** | **0** |

At length 21 the prefix search discarded 58 multisets because SP exceeded the largest number one could make from their digits. All 1,966 remaining multisets were processed. Each of the 323,272 suffixes in range was checked against the exact digits left over. The 21-digit run took about 81 seconds with the quotient method and 0.02 seconds with the compiled prefix method on the test machine. The output counts are reproducible. Timings depend on the machine.

### Why deriving a suffix is exhaustive

Fix a multiset and put D = SP. Select the largest power of ten B = 10^t with B ≤ D and t at most the number of digits. With that split, each arrangement is uniquely a prefix h and a suffix r of exactly t decimal places. A qualifying number must satisfy hB + r ≡ 0 modulo D. Thus r must be the least nonnegative residue of −hB modulo D, since 0 ≤ r < B ≤ D. Enumerating all permissible prefixes and testing that one residue covers every qualifying arrangement. The fixed-width suffix check also detects leading zeros. The case t = 0 gives an empty suffix and is handled by the same test.

The program uses an unsigned 128-bit integer for all decimal values and products. A 21-digit number is below 10²¹, and D is at most 189 × 9²¹, below 10²³. Each digit multiplicity has a separate counter. The Python quotient search uses arbitrary-precision integers. The Stage 1 64-bit program remains capped at length 19.

### Positive controls

Direct enumeration agreed with the prefix search for every word of lengths 1 to 9 on the odd digits, with and without 1 allowed. At 21 digits, twenty 1s and one 7 give 21 possible placements. Three arrangements pass and both the direct and prefix checks agree on their exact quotients. For example, 111111111111111117111 = 27 × 7 × 587889476778365699. Every arrangement in this control exceeds the largest unsigned 64-bit value.

## Reproduce

Use Python 3.8 or later and a C++17 compiler with an unsigned 128-bit integer type, such as GCC (GNU Compiler Collection) or Clang. Run from the repository root. The first command reproduces the previous range and the official 19,637-term table checksum. The second prints the quotient-search result for each odd length up to and including 21.

```sh
python3 research/a398769/verify.py
python3 research/a398769/by_multiset.py 21
c++ -std=c++17 -O3 -Wall -Wextra -pedantic research/a398769/stage3/prefix_tail.cpp -o /tmp/a398769-prefix
python3 research/a398769/stage3/check_controls.py /tmp/a398769-prefix
for length in 15 17 19 21; do /tmp/a398769-prefix "$length"; done
```

## Next Codex goal

The user reports that local commit `af58ecb` proves `A398769.counterexample_restrictions` in Lean. This finite search is independently reproducible from the Stage 1 files. The next goal is designed for the checkout that contains the Lean proof.

```text
/goal Start from the local Mathematics checkout containing af58ecb. Bring in the Stage 3 results if absent, preserving the existing Lean work. Investigate the infinite subcase of Wu's conjecture where every digit is either 3 or 9. Check prior work on that exact subcase and verify the Stage 2 theorem still builds. For length L and b occurrences of 9, write n=3m: replacing each 3 by 1 and each 9 by 3 gives m without carries. Establish that P(n)S(n) divides n exactly when 3^(L+b)*(L+2*b) divides m. Then seek an all-length exclusion or an exact counterexample, with particular attention to mixed, non-repeating strings. Verify every proposed witness from its digits. If this subcase remains open, formalise any proved reduction in Lean and record the precise remaining obstacle. Distinguish a proof for this subcase from a proof of the full conjecture.
```

The Omega Institute already gave an argument for strings formed by repeating one shorter block exactly. The mixed, non-repeating case has no such restriction on length. The sources checked for this note yielded no general settlement of the two-digit-alphabet subcase. [Omega Institute's argument and scope](https://github.com/the-omega-institute/trureturing/issues/26444#issuecomment-6629067008)
