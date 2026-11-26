# Prime digit-sum audit and the remaining global obstruction

**PARTIAL THEOREMS; GLOBAL TARGET UNRESOLVED.** Both proposed prime-density
claims are proved. The recovered trillion-length archive is independently
certified. An explicit effective bound for the signed expression is proved,
but its exponent is insufficient to exclude all remaining witnesses. No
fully verified counterexample or all-length proof was found.

26 November 2026. Starting main is
`b991c97a3d3e91b8339e25c8932ae8072f8c4a09`, exactly the merge of
[PR #21](https://github.com/lukeroyle-beep/Mathematics/pull/21).
See [BASELINE.md](BASELINE.md) for source and coverage boundaries.
All new mathematics is ordinary proof and exact computation; no Lean theorem
or build is claimed.

## Proved prime-sum exclusions

For prime `p=S=7L-4`, Fermat gives `(10^L)^7=10^5 mod p`. Every witness
has `i=3 mod6`. The necessary polynomial

```
H(X)=(180X^2+25)^7-7^7*10^5
```

has no root for **exactly one half**, in relative natural density, of primes
`p=3 mod7`. Each excludes the entire length `(p+4)/7`.
Using the position class fully, `(7Y-25)/18000` must be a sixth power for
the unique `Y^7=10^5 modp`. This excludes **exactly two thirds** of the same
prime population. The sixth-power exclusion is `5/6` within `p=1 mod3`
and `1/2` within `p=2 mod3`; averaging these equally frequent classes is
essential. The corresponding densities among all primes are `1/12` and
`1/9`, respectively. They are not proportions among all integer lengths.

[PRIME_DENSITY.md](PRIME_DENSITY.md) proves the affine Galois action,
good reduction, conjugation alignment and balanced kernel characters using
31/59 and 199/283. It counts Frobenius elements that fix a root, not roots
with multiplicity. Passing a root test is only necessary. Independent
literal polynomial checks and original decimal sum-compatible controls
confirm this distinction.

## Finite coverage and the separate density-one theorem

The archive's exact SHA-256 matches the handoff:
`b657f158d6362c77c570b87c3c193fe54c6f3c385889379edf5bf79b71f05c0a`.
Both full enumerators were freshly run and agree on all **74,601** pairs
with `7^22|F`. Independent original-decimal concatenation proves that their
maximum exact valuation is **27**, with none reaching 28. Completeness and
all 182 small words were audited, proving exclusion through **10^12**.

Together with the inherited PR #21 certificate for
`10^12<L<=1,000,002,000,000`, the documented consecutive exclusion now runs
from **1 through 1,000,002,000,000 inclusive**. PR #21's 35 artifact bindings
were checked here; its million-length arithmetic scan was not rerun.
The fresh trillion-length audit and the inherited adjacent interval retain
separate provenance. Neither implies broader early rejection `(E)`.

[ARCHIVE_AUDIT.md](ARCHIVE_AUDIT.md) also audits the Space proof that
lengths allowing even `S|F(L,i)` for some unbounded exponent have natural
density zero among all lengths. That stronger density denominator is
compatible with the prime-sum result and with exceptional lengths. It gives
no final exception or effective witness cutoff.

## Effective analytic progress and the exact gap

[GLOBAL.md](GLOBAL.md) derives, for every integer `L>=5, 3<=i<L`,

```
7^v7(F) < 25*F^(1-1/(3*10^16)).
```

This is a proved signed-coefficient adaptation using Bugeaud's stated
real and p-adic logarithm estimates, with explicit constants and starting
length. Its exponent is greater than `log(7)/log(10)`, so it supplies no
closing cutoff. The ordinary sparse-digit Theorem 1.2 is not directly
applicable to F, and does not furnish the desired exponent `5/6`.

If the stronger bound `7^t<=C*F^(5/6)` were proved from an explicit start,
a witness would satisfy

```
(117649/100000)^L < C^6*7^17.
```

The implication is correct; conditional exact cutoffs are 204 for C=1,
323 for C=25 and 714 for C=10^6. These are **not established witness
cutoffs**, because the required bound is unproved. Any finite gap up to
the effective starting length would still need to be discharged.

The first unsupported global step is forcing a nonzero lift digit at
some `K<=j<=L-3` for **every** actual `i=r_K` passing `9S|F`, including
composite S. Prime exclusions, stabilized CRT compatibility, and uniform
qualitative `t=o(L)` do not supply that assertion. A nonzero digit first
at `L-2` is too late to reject a witness.

The `{5,7}` subclass and wider digit-1 conjecture remain open. These results
settle no other residual digit family. A verified `{5,7}` witness would
refute the wider conjecture; a proof excluding this subclass alone would
leave the other families.

## Reproduction and review

Run from the repository root with Python 3 and a C++17 compiler supporting
unsigned 128-bit products for the two full archive enumerations:

```sh
python3 research/a398769/five-seven/prime-sum/verify.py
python3 research/a398769/five-seven/prime-sum/archive_audit.py --rerun-enumerations --output /tmp/trillion-rerun.json
```

The first command checks artifact bindings, finite controls, and every
archived candidate; it does not rerun either exhaustive enumeration. The
second runs both complete enumerators and compares every candidate.
All new Python checks remain active under `-O`; normal/optimized outputs
were compared. [verification.json](verification.json) records the scope;
[REVIEW.md](REVIEW.md) records the fresh independent mathematical review.

Work is preserved on `research/a398769-prime-sum-audit` for a draft PR.
Merging is left to the repository owner.
