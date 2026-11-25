# Three deductions: depth 44, the seven-twelfths strip, and the opposite line

25 November 2026. **Each proposed deduction passes**, with the scopes below.
The first exception refutes an unconditional depth bound; it does not
refute statement (E). These are ordinary proofs and exact computations,
not new Lean formalizations.

| Objective | Verdict | Precisely established |
| --- | --- | --- |
| First exception and depth-100 enumeration | PASS | The submitted depth-44 position is the first admissible minus-line position with `v7(F)>=K(L)`. Exactly depths 44, 56, 85, 92 have their representative in their own band through depth 100. All four have `gcd(F,S)=1`. Restricted (E) holds on that line for `L<6*7^99`. |
| Closed seven-twelfths strip | PASS | Every full witness satisfies `abs(12i-7L)>L/10^9` at every admissible length, with closed endpoints excluded. |
| Opposite line | PASS | The submitted depth-11 congruence and least length are correct. Every admissible position on `12i-5L=+1` has `v7(F)<L-2`. Together with the inherited minus line, full witnesses require `abs(12i-5L)>=3`. |

## Baseline and definitions actually used

This work starts on fresh branch `audit/a398769-three-deductions` from
current `main` **`8677446ad39f3a8d72f3a2123c6012c012f2d271`**.
GitHub identifies it as the merge of
[PR #18](https://github.com/lukeroyle-beep/Mathematics/pull/18).
Git ancestry and the merge's second parent independently confirm that it
contains audited head `54081b0a43beead5686aa205cce41a0b5135c03c`.
The starting main tree is identical to that audited head: no later
relevant file changes exist at startup. A fresh GitHub comparison before
publication still selected the same main commit, with zero intervening
commits or changed files. Existing checkouts are untouched.
No applicable `AGENTS.md` or GitHub Actions workflows were found.

Before using inherited conclusions, the audit read the pinned
[strip proof](../strip-audit/PROOF.md),
[modular computation](../strip-audit/COMPUTATION.md),
[definition and proof of (E)](../early-rejection/PROOF.md),
[early-rejection record](../early-rejection/README.md), and
[logarithmic estimate](../proportional/AUDIT.md) with its
[coverage limitations](../proportional/COVERAGE.md).
All inherited files other than root README navigation are preserved
byte for byte; the aggregate verifier checks this against starting main.

For odd `L>=5` and every `3<=i<L`, without an initial parity filter on `i`,

```
S=7L-4, F=7*10^L-18*10^i-25,
T_k=6*7^(k-1), K(L)=min{k>=1:T_k>L}.
```

The corresponding decimal word is `n=F/9`, with product
`25*7^(L-2)` and sum `S`. Full divisibility is exactly
`225*S*7^(L-2)|F`. The suffix gives `v5(n)=2`, so full witnesses have
`5` not dividing `S`; in that domain the condition splits into
**`9S|F` and `v7(F)>=L-2`**. Statement (E) is the stronger implication
**`9S|F => v7(F)<K(L)`**, only on `5` not dividing `S`.
The digit-sum condition, depth `K(L)`, and full threshold `L-2` remain
distinct in every proof and receipt.

## The first exception and the restricted implication

[DEPTH.md](DEPTH.md) gives the complete proof, the exact four records,
and the independent algorithms. Both start from all possibilities
modulo seven: original-F exponent lifts, and polynomial-root lifts
followed by exact 7-adic logarithms to recover the exponent afresh at
each depth. Their complete 100-row histories agree.

At the first exception,

```
u = 329630660491118914435920553818196013
L = 3955567925893426973231046645818352161
i = 1648153302455594572179602769090980067
S = 27688975481253988812617326520728465123
K(L) = v7(F) = 44
F mod7^45 = 3*7^44
F mod9S = 220492367892872959611320275821615897912
gcd(F,S) = 1.
```

For `k>=2`, `K(L)=k` means `T_(k-1)<=L<T_k`. On this line,
at most the least nonnegative exponent representative can have its
length in that band. The proof separately treats `k=1`, the invalid
`u=0`, representatives below or above the band, and both endpoints.
There is no admissible earlier exception. Through depth 100 the only
four exceptions all fail `9S|F`, proving restricted (E) on the entire
admissible minus line below `T_100=6*7^99`.

The first example refutes `v7(F)<K(L)` **without** the digit-sum premise,
even in the five-free domain. It satisfies (E) because that premise is
false. It is not a full witness, and it does not refute the inherited
all-length minus-line bound `v7(F)<L-2`.

## The new strip and opposite line

[SEVEN_TWELFTHS.md](SEVEN_TWELFTHS.md) checks the integral polynomial,
coefficient span for both signs of the offset, root height and degree,
and each hypothesis of strong Hensel lifting and the published
Bugeaud--Laurent estimate. At positive depth, odd `L` makes the
derivative valuation exactly one. For `t>=3`, the lifted root has
`v7(x-alpha)=t-1`; using the simple-root equality `t` here would be an
invalid inference. Both root branches account for this loss.

For an independent root the exact bound is
`t<=1+(47628/78125)*L = 1+0.6096384L`; its strict margin below `L-2`
at `L=10^9` is **390361597** and increases thereafter.
For a dependent root the formula is
`t=2+v7(Dq-j)-v7(D)`, retaining the subtraction at `D=7`.
The cases `t<=2` and the empty small-length strip are handled separately.

[OPPOSITE.md](OPPOSITE.md) proves the exact domain
`(L,i)=(12u+7,5u+3)`, `u>=0`, and exhaustively verifies

```
7^11 | F  iff  u=313281594 mod1694851494.
least permitted L = 3759379135.
```

The small case `u=0` has `F=69981975` and `v7(F)=1<5`.
All other positions below `10^9` fail the depth-eleven necessary test;
all positions from `10^9` onward fall within the merged 5/12 strip.
There is no gap between these arguments. Odd parity and the two line
exclusions give `abs(12i-5L)>=3` for every full witness.

## Coverage gain and unresolved complement

These are **position exclusions**, not whole-length exclusions.
The exact new closed ratio strip is

```
[6999999999/12000000000, 7000000001/12000000000].
```

It splits only the inherited open interval
`(60001/120000,5999999/10000000)` into

```
(60001/120000, 6999999999/12000000000)
(7000000001/12000000000, 5999999/10000000).
```

All other inherited strips, finite certificates and discrete restrictions
remain in force. The opposite line is now excluded at all its admissible
positions; the minus line was already excluded for full witnesses by
PR #18. The new stronger restricted (E) certificate extends that line's
previous bound `L<2231854769` to **`L<6*7^99`**. It says nothing about
other positions at those lengths, or about (E) beyond that line's new bound.

Consecutive whole-length exclusion remains **1 through 10,000,000
inclusive**. Broad (E) remains certified at all odd lengths **5 through
9,999,999 inclusive**. No additional whole length, consecutive interval,
effective global cutoff, or Lean theorem/build is claimed. The inherited
isolated and infinite whole-length exclusions retain their existing scope.

No submitted claim failed. The unresolved finding is the same global
gap: the remaining positions still lack a uniform rejection of the full
divisor (or of the digit-sum-compatible depth-K representative for broad
(E)). **Broad all-length (E), the all-length `{5,7}` subclass, and the
wider digit-1 conjecture all remain open.**

## Reproduction and review

From the repository root, using standard-library Python 3 (observed
CPython 3.14.4 on Darwin arm64):

```sh
python3 research/a398769/five-seven/three-deductions-audit/verify.py > /tmp/three-deductions.json
python3 -O research/a398769/five-seven/three-deductions-audit/verify.py > /tmp/three-deductions-O.json
cmp /tmp/three-deductions.json /tmp/three-deductions-O.json
cmp /tmp/three-deductions.json research/a398769/five-seven/three-deductions-audit/verification.json
git diff --check
```

The aggregate runs the four audit checkers and the independent review
checker in both modes, compares their
complete outputs to committed receipts, compares all 100 independently
recovered exponent classes and all four exception records, checks source
hashes and inherited-file preservation, and reruns the inherited receipt
verifier. Essential checks use explicit exceptions; `-O` cannot disable
them. Every checker has nonzero positive controls and deliberate failure
controls. Each proof file also gives its standalone reproduction commands.

The inherited verifier checks 100 stored blocks with `fresh_full_runs=[]`;
the old ten-million searches are **not** rerun. The precise validation
scope is recorded in [verification.json](verification.json).
The independent final-commit review is recorded in the draft PR, with
its reproducible findings in [REVIEW.md](REVIEW.md). Merging remains with
the repository owner.
