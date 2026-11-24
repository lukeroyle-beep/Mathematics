# A398769: independent audit of the two-five family

Audited 24 November 2026, starting from main at
`214cd49e660f31aaee0aaecd48d36a8ec3624653`, the merge commit of
[PR #6](https://github.com/lukeroyle-beep/Mathematics/pull/6).

## Separate verdicts

1. **Valid: the second five cannot be at position `i=3`, at any length.**
   [Fixed-position proof](FIXED_POSITION.md) checks Bugeaud–Laurent's
   hypotheses and constants, proves the cutoff inequality on both branches
   of the maximum, and combines the exact exponent classes `39 mod 42` and
   `2853939 mod 4941258` to cover every smaller length. Position `i=15` is
   the smallest still permitted by the earlier modulo-49 restrictions;
   that is not evidence that it satisfies the growing-power condition.
2. **Valid: only finitely many candidate pairs remain when `i` varies.**
   [Finite-pairs proof](FINITE_PAIRS.md) verifies every hypothesis of
   Evertse's Corollary 1, with `c=1`, `d=1/2`, four coordinates, and
   `S0={2,3,5,7}`. It supplies **no numerical maximum length**, list of
   survivors, or proof of emptiness.

Both deductions use only `7^(L-2) | F`. Neither deduction has an unsupported
step under the stated hypotheses. The unjustified further step would be
to infer emptiness, or a finite executable search cutoff, from abstract
finiteness alone. Separate mathematical reviewers checked the two source
corollaries and the elementary setup; see [review record](REVIEW.md).

## Self-contained reduction and exact problem

For a positive number `n` whose decimal digits are all 5 or 7, let `P` be
their product, `S` their sum, `L` their number, and `c` the number of fives.
Assume `P*S | n`.

- `n` is odd, so `S` and hence `L` are odd.
- Three fives would force `125 | n`. None of the eight three-place
  suffixes on `{5,7}` is divisible by 125: their residues, in the order
  `555,557,575,577,755,757,775,777`, are `55,57,75,77,5,7,25,27`.
  Therefore `c <= 2`.
- With zero fives, `n=7R_L`, `R_L=(10^L-1)/9`; `P*S` forces `49 | n`.
  Then `7 | R_L`, so `6 | L`, since 10 has order 6 modulo 7. This
  contradicts odd `L`, including `L=1`.
- With one five, divisibility by 5 forces that five to the units place.
  If a seven occurs then `7 | n`, whereas `n=7R_L-2`. If no seven occurs,
  `n=5` and `P*S=25` does not divide it.

Exactly two fives remain. One is at position zero; write `i` for the
other position. Because `L` is odd and at least 3, a seven occurs.
Replacing the two sevens in `7R_L` gives

```text
n = 7R_L - 2(1+10^i) = F/9,
F = 7*10^L - 18*10^i - 25,
P = 25*7^(L-2),      S = 7L-4.
```

The condition `7 | n` gives `10^i = -1 mod 7`, so `i=3 mod 6`.
Thus `3 <= i < L` and odd `L >= 5`. Conversely such positions specify
precisely the proposed decimal string, even if `i=L-1`.
Since `F=9n`, multiplication by 9 gives the exact equivalence

```text
P*S | n  if and only if  225*7^(L-2)*(7L-4) | F.
```

This equivalence uses no assumed coprimality. The analytic proofs apply
to the larger family satisfying only the necessary `7^(L-2) | F`.

## Preserved work and Lean boundary

The previously unpublished local `five-seven-follow-up` directory was
found and left untouched. Its five files are copied byte-for-byte into
[prior-notes](prior-notes/README.md) as historical evidence. Statements
there about an unresolved `i=3` case are superseded by this audit; the
fixed-modulus limitation in those notes remains correct.

[A398769/FiveSeven.lean](../../../A398769/FiveSeven.lean) is also an exact
copy of the local proof, now imported by the library. Lean checks these
three statements about the actual `Nat.digits 10 n`:

- `A398769.FiveSeven.atMostTwoFives`: for `n>0` with all digits in `{5,7}`
  and `P*S | n`, there are at most two fives.
- `A398769.FiveSeven.notExactlyOneFiveWithSeven`: exactly one five is
  impossible when a seven occurs.
- `A398769.FiveSeven.notExactlyOneFive`: exactly one five is impossible,
  including the single-digit case.

Each reports only `[propext, Classical.choice, Quot.sound]`. The new module
contains no `sorry`, custom axiom, or `native_decide`.
The odd-length argument, zero-five exclusion, positional and divisibility
reductions, analytic theorems and applications, cutoff calculus, modular
order proof, and finiteness conclusion are **ordinary mathematical proofs,
not Lean-checked statements**. Python checks the recorded finite modular
certificates and rational logarithm enclosures; it does not formalize the
papers. Existing Stage 2, 4 and 5 Lean results retain their prior scope.

## Reproduction and limits

From the repository root, using the pinned Lean 4.24.0 toolchain:

```sh
python3 research/a398769/five-seven/certificates.py
python3 research/a398769/five-seven/log_bounds.py
lake clean mathematics
lake build
lake env lean A398769/FiveSeven.lean
git diff --check
```

The dependency artifacts can be reused; the receipt identifies that
boundary. [verification.json](verification.json) records fresh commands,
outputs, preservation and source hashes. No earlier exhaustive search
was rerun or extended in this audit.

It remains open whether **any** pair in the remaining finite family
satisfies the full divisibility. In particular, the all-length exclusion
of the `{5,7}` subclass is not proved. The unrestricted A398769 conjecture
also remains open. No theorem here excludes all numbers involving other
digit patterns, nor converts prior bounded searches into an all-length
result. This branch is prepared for review; the merge decision belongs
to the repository owner.
