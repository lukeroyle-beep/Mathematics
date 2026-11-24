# A398769 · The odd digit conjecture

Chai Wah Wu asks whether every odd positive integer divisible by its decimal digit sum times its decimal digit product contains a 1. Write S(n) for the sum and P(n) for the product. The exact hypothesis is P(n)S(n) | n. A counterexample would settle both Wu's question and its equivalent formulation in A398768, which says every qualifying integer without a 1 is even. [A398769](https://oeis.org/A398769/internal) · [A398768](https://oeis.org/A398768/internal)

## Result on 24 November 2026

Two exhaustive implementations found **zero counterexamples for all positive integers below 10²⁰**. This is a finite computational result. The unrestricted conjecture remains open in the sources checked. The check gives a lower bound on the size of any counterexample.

Every digit in a counterexample must belong to {3,5,7,9}. A zero makes the putative divisor zero, an even digit makes it even, and a 1 would satisfy the conclusion. The digit sum must also be odd. A sum of odd digits is odd precisely when their count is odd. The programs therefore need to check odd lengths through 19 to cover every integer of up to 20 digits. The first outstanding length is 21.

| Check | Result |
|---|---|
| Independently generated full A049102 table for 0 < n < 10^14 | 19,637 terms, 52 odd, every odd term contains a 1 |
| Published table comparison | All 384,483 bytes reproduced, verified against the official SHA-256 (Secure Hash Algorithm 256-bit) digest |
| Exhaustive check by digit lengths 15, 17 and 19 | Zero counterexamples at each length in both implementations |
| Regression case | 357937935933375 is divisible separately by 81 and 22785532875. On division by 22785532875 its quotient is 15709, which leaves remainder 76 on division by 81. |

The published comparison is David Corneth's table, with the first 100 terms credited to Vincenzo Librandi. The repository verifier checks the digest of the complete indexed table, using the published single line-feed character at each row ending. [Parent sequence and table](https://oeis.org/A049102) · [Pinned official digest](https://github.com/oeis/oeisdata/blob/1ebf49cffb4038214cb8afb0d86c310c9aad7dcb/files/A049/b049102.txt)

## Reproduce

Run from the repository root with Python 3.8 or newer and a C++17 compiler available as `c++`. The run uses the Python standard library and a temporary build directory.

```sh
python3 research/a398769/verify.py
```

The verifier rebuilds the parent table, compares its digest, checks every generated term by direct digit arithmetic and compares against a brute-force scan below 10^6. It runs a positive control for the quotient search by allowing the digit 1 and comparing against the published odd terms at lengths 1, 3 and 5. It then runs both finite searches. A mismatch stops the run. Per-length counts from the suffix method are recorded in [suffix_check_19.csv](suffix_check_19.csv).

### Why the searches cover the range

1. **Parent table.** In [parent.cpp](parent.cpp), enumerate every multiset of nonzero decimal digits through length 14. Its sum S and product P are fixed. The number must be a multiple of SP and congruent to S modulo 9. Compatible constraints specify one residue modulo the least common multiple of SP and 9. For each possible prefix, take a suffix width whose number of possibilities is at most that modulus. There is at most one possible number in each prefix interval. Check its complete digit counts before emitting it.
2. **Search by suffix.** [suffix_check.cpp](suffix_check.cpp) prepends one admissible digit at a time. If a suffix of length j already contains f fives, then 5^f must divide the completed number. Since f ≤ j, adding a prefix cannot change that residue modulo 5^f. A failing suffix can be discarded permanently. All remaining odd-length words are tested by first checking P | n and then S | (n/P). Unsigned 64-bit arithmetic suffices for n and P through length 19. The program never forms SP.
3. **Independent search by quotient.** [by_multiset.py](by_multiset.py) enumerates each possible multiset on {3,5,7,9} and computes SP in arbitrary-precision arithmetic. Sorting its digits ascending and descending bounds every arrangement, hence also its possible integer quotient q = n/(SP). The units digit and digit sum modulo 9 restrict q to residue classes. Checking the digits of every remaining multiple SPq for exact equality with the multiset completes the search. This method uses no suffix pruning or fixed-width arithmetic.

For example, the suffix program visited 3,177,637,371 admissible suffixes at length 19 after its divisibility-by-powers-of-five filter. A zero in the last column means no full-product witness. The other columns distinguish the weaker divisibility tests.

## Prior results and credit

- Corneth's 2019 argument shows that the number consisting of 3^k ones is a term for every nonnegative k. This supplies infinitely many positive examples. [A049102](https://oeis.org/A049102)
- The Omega Institute's 4 November 2026 attempt gave an argument excluding any counterexample made by repeating a shorter decimal block two or more times. Its attempt on the full conjecture ended unresolved. The finite searches here include repeated strings. [Argument and scope](https://github.com/the-omega-institute/trureturing/issues/26444#issuecomment-6629067008)
- A classical suffix result gives an all-length restriction. Any counterexample with nine or more 5s would be a multiple of 5^9. Its final nine digits would be odd and would form a multiple of 5^9, since 5^9 divides 10^9. The unique such nine-digit block is 193359375, which contains a 1. Thus any counterexample contains **at most eight 5s**. This is an application of an existing result. [A151752 and uniqueness argument](https://oeis.org/A151752) · [2003 United States of America Mathematical Olympiad, Problem 1](https://f.hubspotusercontent30.net/hubfs/981338/Math%20Competition%20Problems_PDFS/2003USAMO-solutions.pdf)

## Staged Codex goals

**Stage 1 is complete.** Its evidence is the matched parent table and independently reproduced finite range above. The later stages have distinct completion criteria.

### Stage 2 · Start here in Codex

```text
/goal In lukeroyle-beep/Mathematics, start from the branch containing research/a398769/README.md. Read that file and set up a minimal pinned Lean 4 and Mathlib project. Define the exact base-ten A398769 counterexample predicate on positive natural numbers. Prove that every counterexample has only digits 3, 5, 7 and 9, has odd digit length, and contains at most eight occurrences of 5. For the last conclusion, connect the last nine decimal digits to the residue modulo 10^9 and prove the required uniqueness of 193359375 as an all-odd nine-digit multiple of 5^9. A kernel-checked finite proof for the 512 possible multiples below 10^9 is acceptable. Include the general bridge from nine or more occurrences to this suffix. Account for Lean's least-significant-digit-first convention. Credit A151752 and the 2003 Olympiad result. Finish with a successful clean lake build and an axiom report for the final theorem. Use no sorry, custom axioms or native_decide. Update the research note with theorem names and reproduction commands. Report any remaining proof gap precisely. The deliverable is this all-length restriction on hypothetical counterexamples.
```

### Stage 3 · Target 21 digits

```text
/goal Extend the A398769 counterexample search in lukeroyle-beep/Mathematics to exactly 21 digits. Read research/a398769/README.md and reproduce the existing checks. Start with the arbitrary-precision quotient method. Obtain a second exhaustive enumerator with independently justified pruning and arithmetic safe at 21 digits. Benchmark its cost on prior lengths before running to completion. Do not raise the capacity of the existing 64-bit verifier without replacing its unsafe operations. Record the commands, coverage argument and two outputs. Verify any witness directly from its decimal digits and report its exact quotient. If both methods complete with zero witnesses, the resulting range is 0 < n < 10^22 by parity. If the independent run is impractical, record the exact coverage achieved and estimated remaining work. Credit older results and make no claim of priority from a finite search.
```

### Stage 4 · Seek a general argument

Use the earlier results to select one infinite class that remains unresolved, for example counterexamples with no digit 5. Before starting, check for prior proofs of that exact subcase. Record the quantifiers and attempt a general exclusion or produce an exact witness. Retain any proved intermediate lemma and identify the unclosed cases. The full problem requires a contradiction covering every admissible length and digit string, or a verified counterexample.
