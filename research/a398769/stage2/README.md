# Restrictions on a counterexample to A398769

Let $n$ be a positive odd integer with no decimal digit 1. Write $P(n)$ for the
product and $S(n)$ for the sum of its decimal digits. If $P(n)S(n)\mid n$, then

1. every digit of $n$ is 3, 5, 7 or 9,
2. the number of digits is odd, and
3. the digit 5 occurs at most eight times.

[`A398769.counterexample_restrictions`](../../../A398769/Stage2.lean) proves
these necessary conditions at every length. It uses the actual base-ten digits
`Nat.digits 10 n`. This is a fresh reconstruction of the theorem previously
reported at local commit `af58ecb`. The [conjecture](https://oeis.org/A398769)
also requires ruling out all remaining candidates.

## Proof

Each digit divides the product, and both the product and the sum divide $n$.
Since $n$ is odd, every digit is odd. Excluding 1 leaves 3, 5, 7 and 9. The
sum of these odd digits has the same parity as their count. The sum divides
an odd number, so the count is odd too.

If there are $c$ fives, then $5^c$ divides the product. Nine or more fives
would give at least nine digits and force $5^9\mid n$. The last nine decimal
places represent $n\bmod 10^9$. Since $10^9=512\cdot5^9$, this residue
must be $5^9 j$ for some $0\le j<512$. Lean checks all 512 possibilities
by kernel reduction. It inspects exactly nine places, including any leading
zeros in the residue. Every possibility has a digit outside the allowed four.

The underlying odd-digit suffix result appears in the *On-Line Encyclopedia of
Integer Sequences* [A151752](https://oeis.org/A151752) and in the [2003 United
States of America Mathematical Olympiad, problem 1](https://artofproblemsolving.com/wiki/index.php/2003_USAMO_Problems/Problem_1).
The unique nine-place all-odd multiple is 193359375, whose first digit is 1.
The Lean proof checks the exclusion directly.

## Reproduce

From the repository root, using the Lean release in `lean-toolchain` and the
Mathlib revision in `lake-manifest.json`, run

```sh
lake clean mathematics
lake build
lake env lean A398769/Stage2.lean
```

The clean command removes this project's build products and retains compiled
dependencies. The final command elaborates the source and prints the axioms
of the public theorem. The verified output is

```text
'A398769.counterexample_restrictions' depends on axioms: [propext, Classical.choice, Quot.sound]
```
