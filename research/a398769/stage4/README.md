# A398769 Stage 4: independent Lean reconstruction

For a positive natural number `n` whose decimal digits all belong to `{3, 9}`,
let `L` be its digit length, `b` its number of 9s, `P` its digit product and `S`
its digit sum. The theorem proved here is exactly

```text
P * S ∣ n  ↔  3^(L+b) * (L+2*b) ∣ n/3.
```

The Lean source is [A398769/Stage4.lean](../../../A398769/Stage4.lean).
`A398769.stage4_reduction` quantifies over `n : ℕ`, assumes `0 < n` and
`A398769.DigitsThreeOrNine n`, and uses natural-number divisibility and division.
Every quantity is defined from `Nat.digits 10 n`: `digitLength` is its length,
`numberOfNines` counts 9s, `digitProduct` takes its product, and `digitSum` takes
its sum. The product and sum formulas are proved, not hypotheses.

## Proof

Induction on a list of digits in `{3, 9}` gives
`P = 3^(L+b)` and `S = 3*(L+2*b)`. A separate list induction proves that its
base-ten reconstruction is divisible by 3. Applying that fact to the actual
digits and the identity `Nat.ofDigits 10 (Nat.digits 10 n) = n` gives `3 ∣ n`,
so `n = 3*(n/3)` exactly. Substituting the formulas and cancelling the common
factor 3 proves both implications. In particular, the reverse implication
does not assume divisibility by `P*S` when justifying the division by 3.

Mathlib lists digits least significant first. The count, length, product and
sum are insensitive to this order, and the reconstruction uses Mathlib's
matching `ofDigits` convention. The proof also works for zero; the public
theorem retains positivity to match the requested statement.

This is a fresh reconstruction from the stated theorem, using standard Lean
and Mathlib lemmas, without an earlier Stage 4 proof. It proves a reduction for
all admissible lengths, not an exclusion of every `{3, 9}` number. It makes no
claim to resolve the full A398769 conjecture. No 75-digit search is included.

## Reproduce

Install [elan](https://github.com/leanprover/elan), then run from the repository
root:

```sh
MATHLIB_NO_CACHE_ON_UPDATE=1 lake update
lake env lean --version
lake clean
lake build
lake env lean A398769/Stage4.lean
```

`lean-toolchain` pins Lean to `leanprover/lean4:v4.24.0`; `lakefile.toml` pins
Mathlib to release `v4.24.0`. The committed `lake-manifest.json` fixes the exact
Mathlib and transitive dependency commits. On an existing clone the lockfile
is sufficient for `lake build`; `lake update` resolves the same pinned release.
The environment variable skips the optional upstream cache download. `lake clean`
removes the build directories of every package in the Lake workspace; `lake build`
then rebuilds this project and the dependency modules it imports. Unrelated
Mathlib modules are not build targets. Lean itself uses the pinned release binary.

The final command elaborates the proof again and prints the axioms of
`digit_formulas_of_three_or_nine`, `three_dvd_of_three_or_nine`, and
`stage4_reduction`, via the source's `#print axioms` commands.

## Validation record

Validated on the Mac mini on 24 November 2026, in
`/Users/lukesmacminim41/Projects/Mathematics`, on branch
`research/a398769-stage4-reconstruction`. The checkout was initially clean and
the branch was created directly from the freshly fetched `origin/main` at
`6f67bb8db338d8877b8d9f601e49384e39043eaa`. Existing `main` was preserved.

- Lean: 4.24.0, `arm64-apple-darwin23.6.0`, release compiler commit
  `797c613eb9b6d4ec95db23e3e00af9ac6657f24b`.
- Mathlib: `f897ebcf72cd16f89ab4577d0c826cd14afaafc7` (`v4.24.0`).
- `lake clean` followed by `lake build`: **passed**, 796 jobs, no warnings.
- `lake env lean A398769/Stage4.lean`: **passed**; its complete axiom output is
  retained in [axioms.txt](axioms.txt).
- All three printed declarations depend only on
  `[propext, Classical.choice, Quot.sound]`, the standard axioms used here by
  Lean/Mathlib. No `sorry`, custom axiom, or `native_decide` occurs in the proof.
- Independent source review found no remaining statement or proof gap.

On this Mac, the release toolchain was downloaded from Lean's official GitHub
release archive and extracted under `/private/tmp`; the commands above used
`/private/tmp/lean-4.24.0-darwin_aarch64/bin` at the front of `PATH`. Elan provides
the same pinned version for subsequent reproductions. The initial dependency
setup fetched upstream caches, which the final workspace-wide `lake clean`
removed before the recorded build.
