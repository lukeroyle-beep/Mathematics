# Exact computation and reproducibility

The computational verdict is **verified as written**: every submitted factor,
multiplicity, count, survivor parameter and residue reproduces. The full
residue omitted from the submission is F mod (9S) = **889368780330** for
the sole survivor. All arithmetic supporting the theorem is exact integer
arithmetic. No floating-point logarithm or probable-prime result is used
to certify the finite exclusion.

## Independent resultant calculations

[checker.py](checker.py) constructs P in ascending coefficient order and
constructs Q by twelve integer polynomial convolutions with [-25,7],
scaling by ten and subtracting 18^12 from its coefficient of X^5. It builds
the 19 by 19 Sylvester matrix (twelve shifted P rows followed by seven
shifted Q rows, in descending coefficient order), then evaluates its
determinant with a plain-Python fraction-free Bareiss algorithm. Every
division is explicitly checked to have zero remainder, and row swaps
update the sign.

With `--sympy`, a separately constructed symbolic expression is supplied
directly to SymPy's `resultant`, without sharing the convolution's
coefficient lists or its determinant routine. SymPy documents its
[resultant and subresultant implementation](https://docs.sympy.org/latest/modules/polys/internals.html).
The two signed results agree:

```
-250661191576198393222089099629904823989413273206227655149385621244521493970768146119991156593887577503584037549226391126286277770996093750000000
```

A fresh reviewer additionally reproduced this value as the determinant of
the 7 by 7 multiplication matrix for Q modulo P, using binomial coefficients
and ordinary Gaussian elimination over exact rational numbers. This third
route imports neither the main checker nor SymPy. It also rechecks all 66
prime certificates in increasing order, enumerates subsets by combinations,
and uses decimal-Horner exponentiation for every Fermat test and residue.

The submitted **absolute** factorization is correct:

```
|R| = 2^7 * 3^24 * 5^25 * 7 *
      13 * 23 * 211 * 1237 * 1289 * 1327 * 2609 * 7043 * 11399 * 11831 *
      903649 * 555700252411 * 4920652182747643 *
      958850750886621892231 * 4240701096684867281569789303.
```

The checker verifies the full product against the computed determinant,
then repeatedly divides out each prime and checks its exact multiplicity.
The residual cofactor must be one. All fifteen factors after 7 are distinct
and occur to exponent one. No factorization oracle is trusted by this
verification.

## Deterministic primality certificates

[primality_certificates.json](primality_certificates.json) contains 66
recursive full n-1 Lucas certificates. Its roots are all nineteen distinct
factors of |R|, including 2,3,5,7. The only terminal case is 2. Each other
record specifies n, the complete prime factorization of n-1, and an integer
witness a. For every distinct certified prime q dividing n-1 the verifier
checks

```
a^(n-1) = 1 (mod n),
gcd(a^((n-1)/q)-1,n) = 1.
```

These conditions prove primality, not just probable primality. For any
prime r dividing n, the order of a modulo r divides n-1, but cannot divide
(n-1)/q for any q. Thus it contains every full prime power in n-1, and
equals n-1. Since that order divides r-1, r>=n, forcing n to be prime.
Every factorization product, exponent, recursive certificate, witness
power and gcd is checked using only Python's standard library. Duplicate
records, cycles, missing factors and unused certificates are rejected.

[generate_certificates.py](generate_certificates.py) uses SymPy's `factorint`
only to discover factorizations of n-1 and scans integer witnesses from
two upward. Its output is not trusted until the standalone verifier passes.
The generator is retained to reproduce the entire certificate file; the
verifier does not require regenerating it or installing SymPy.

## Complete independent enumerations

The first enumeration forms products by iterating all fifteen-bit masks.
The second recursively includes/excludes each of the fifteen certified
primes. Both generate complete lists independently, sort them numerically,
and compare every entry. Uniqueness is checked separately. The congruence
filter is S mod 84 = 31. Its minimum is S=17251, u=205, so all its entries
are actual positions; u=0 would have i=2 and is not eligible.

The first Fermat filter uses Python's modular `pow`; the second uses a
separate square-and-multiply implementation. Their complete survivor lists
agree. Counts are measured first, then compared with the supplied claims:

| Stage | Exact count |
| --- | ---: |
| Distinct subset products, including the empty product | 32,768 |
| Products congruent to 31 modulo 84 | 1,360 |
| Those passing 10^(S-1)=1 modulo S | 1 |

To make complete enumeration reproducible without storing two large lists,
the receipts hash the sorted decimal integers, each followed by a single
ASCII LF (including the last), encoded as ASCII:

```
All products: aa16b558c719f9fe39a29f04d0bb1677263368ed8ea771eb487a38f054746529
S=31 mod84:   73b38df684d89e130858ade5b79af15f5b07af482adf1c40f2f57c8e06ff130c
```

The one survivor is fully recovered, rather than supplied to the filters:

| Quantity | Value |
| --- | ---: |
| S | 555700252411 |
| u | 6615479195 |
| L | 79385750345 |
| i | 33077395977 |
| 10^L mod S | 79923024499 |
| 10^i mod S | 166905216978 |
| F mod S | 333668527919 |
| 9S | 5001302271699 |
| 10^L mod 9S | 3414124538965 |
| 10^i mod 9S | 2389706226622 |
| F mod 9S | 889368780330 |

Both power implementations agree. A separate digit/repunit computation
uses n=7*(1+10+...+10^(L-1))-2-2*10^i modulo S, computing the repunit by
binary concatenation without division by nine, and checks that 9*(n mod S)
equals the least nonnegative F mod 9S. Thus a mistaken cancellation of
nine cannot pass this comparison.

The composite control S=451=11*41 has u=5, L=65 and i=27. Trial division
certifies 11 and 41, and the Fermat residue is one. Its residues are

```
mod 451: 10^L=329,  10^i=428,  F=437;
mod4059: 10^L=2584, 10^i=2683, F=2241.
```

The checker also confirms that the line contains both position parities,
and that u=0 has the invalid position i=2. The line theorem uses neither
the seven-adic congruence i=3 mod6 nor any stronger full-witness filter.

## Commands and environment

Observed on Darwin arm64, CPython 3.14.4 (Clang 21.0.0), Git 2.54.0
(Apple Git-157). The isolated symbolic environment has SymPy 1.14.0 and
mpmath 1.3.0. mpmath is an installed dependency; its numerical arithmetic
is not part of the verification. From the repository root, the exact
standard-library commands are:

```sh
python3 research/a398769/five-seven/prime-factor-audit/checker.py > /tmp/prime-audit.json
python3 -O research/a398769/five-seven/prime-factor-audit/checker.py > /tmp/prime-audit-O.json
cmp /tmp/prime-audit.json /tmp/prime-audit-O.json
cmp /tmp/prime-audit.json research/a398769/five-seven/prime-factor-audit/results.json
```

For the symbolic cross-check and certificate regeneration, this audit used:

```sh
python3 -m venv /private/tmp/a398769-audit-venv
/private/tmp/a398769-audit-venv/bin/python -m pip install sympy==1.14.0 mpmath==1.3.0
/private/tmp/a398769-audit-venv/bin/python research/a398769/five-seven/prime-factor-audit/checker.py --sympy > /tmp/prime-audit-sympy.json
/private/tmp/a398769-audit-venv/bin/python -O research/a398769/five-seven/prime-factor-audit/checker.py --sympy > /tmp/prime-audit-sympy-O.json
cmp /tmp/prime-audit-sympy.json /tmp/prime-audit-sympy-O.json
cmp /tmp/prime-audit-sympy.json research/a398769/five-seven/prime-factor-audit/results-sympy.json
/private/tmp/a398769-audit-venv/bin/python research/a398769/five-seven/prime-factor-audit/generate_certificates.py > /tmp/prime-certificates.json
/private/tmp/a398769-audit-venv/bin/python -O research/a398769/five-seven/prime-factor-audit/generate_certificates.py > /tmp/prime-certificates-O.json
cmp /tmp/prime-certificates.json /tmp/prime-certificates-O.json
cmp /tmp/prime-certificates.json research/a398769/five-seven/prime-factor-audit/primality_certificates.json
python3 research/a398769/five-seven/prime-factor-audit/review_check.py > /tmp/prime-review.json
python3 -O research/a398769/five-seven/prime-factor-audit/review_check.py > /tmp/prime-review-O.json
cmp /tmp/prime-review.json /tmp/prime-review-O.json
cmp /tmp/prime-review.json research/a398769/five-seven/prime-factor-audit/review_results.json
```

The installation initially requested `sympy` and resolved exactly the
versions pinned above. The explicit pins reproduce that observed environment.
All listed checker runs and comparisons passed. Receipts include the
checker source SHA-256, certificate SHA-256, Python version, full signed
resultant and all survivor/control residues. A different Python version
changes its reported version field, so byte comparisons with the committed
receipt require the recorded version; the arithmetic still checks directly.

Essential checks call an explicit `require` function raising `ValueError`;
there are no `assert` statements. Built-in negative controls verify rejection
of a failed Lucas gcd, an incomplete n-1 factorization, a missing resultant
multiplicity and a perturbed resultant in
both normal and optimized execution. Positive determinant controls exercise
row swapping, a singular matrix and the sign convention. Independent review
and its additional computation are recorded in [REVIEW.md](REVIEW.md).

The inherited `early-rejection/verify.py` was also run without `--recompute`.
It passed its source/receipt integrity and small controls, compared all 100
stored blocks, and reported `fresh_full_runs=[]`. This does **not** claim
a fresh ten-million-length run; the unchanged large certificates are reused.
