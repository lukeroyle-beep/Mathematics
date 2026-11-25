# Proportional position exclusions: verified strips, incomplete coverage

25 November 2026. Starting `main`:
`2aea8ff77232225a68f5ebe694b812bc3a9438b8`, the verified merge of PR #10.
Research branch: `research/a398769-proportional-position-bounds`.
The attached *A398769 proportional position bounds* investigation was
executed on a separate checkout, preserving the earlier research branches.

**All five proposed inequalities pass independent audit.** The requested
all-length midpoint extension to 165 is valid, and retaining the height
parameter more carefully improves the fixed strip to **179**. Two further
positive-width strips exclude neighbourhoods of **2/5 and 3/5**, with
offsets allowed to grow linearly with length. Coverage is still incomplete.
The general degree-and-height estimate demonstrably misses an explicit
family near `sqrt(2)-1`; it does not supply a global effective cutoff.

## Verified mathematical results

For a residual pair, let

```text
L odd, L>=5, 3<=i<L, i=3 (mod 6),
F=7*10^L-18*10^i-25, n=F/9,
P=25*7^(L-2), S=7L-4.
```

The full witness test remains `225*7^(L-2)*(7L-4) | F`, or equivalently
`n=q*P*S` for an integer `q`. In particular the digit-sum condition is
`9*S | F`; merely checking `S | F` is insufficient.

Every possible witness must satisfy all of the following:

| Position region | Verified strict necessary condition |
|---|---|
| Units end | `i > L/25000` |
| Leading end | `L-i > L/25000` |
| One-third | `abs(L-3i) > L/300000` |
| Midpoint | `abs(L-2i) > L/60000` and `abs(L-2i) >= 181` |
| Two-thirds | `abs(2L-3i) > L/300000` |
| Two-fifths, new | `abs(5i-2L) > L/2000000` |
| Three-fifths, new | `abs(5i-3L) > L/2000000` |

[AUDIT.md](AUDIT.md) checks the primary Bugeaud--Laurent corollary,
the denominator in `b'`, local and global degrees, heights, independence,
negative cubic offsets, dependent roots, and all strict numerical margins.
It proves the fixed midpoint strip through 179, including its comparison
for every real `L>=10000000`.

[COVERAGE.md](COVERAGE.md) proves the two new strips, gives exact open
intervals remaining after the five and seven proportional inequalities,
and explains the additional length-dependent midpoint refinement.
The seven proportional conditions leave, for example, the entire open
interval `(41/100,42/100)`. This interval is a gap in those inequalities,
not evidence that a witness exists there. The inherited congruence and
digit-sum filters still apply inside the remaining intervals.

## Why adding rational centres does not establish complete coverage

For a reduced centre `a/b`, the cleared polynomial has degree at most `b`
and coefficient exponent span

```text
w=max(0,r,s)-min(0,r,s),
L=bk+r, 0<=r<b, i=ak+s.
```

The standard height choice `H=w+2` is at least
`L*abs(i/L-a/b)` and at least 2. The uniform independent-root bound
using degree `b` has the lower floor `6300*b^3*H`. It can contradict
`v_7(F)>=L-2` only if both

```text
b^3 < L/12600,
abs(i/L-a/b) < 1/(6300*b^3).
```

These requirements cannot simultaneously cover the following family:

```text
M=16031730, L=1+M*j (j>=1), xi=sqrt(2)-1,
i=39+42*floor((xi*L-39)/42+1/2).
```

Every member passes parity, the modulo-49 position table, and the five
inherited digit-sum length filters. The family lies in the displayed gap.
The first member is `(L,i)=(16031731,6640575)`. The proof uses the uniform
lower bound `abs(xi-a/b)>1/(4b^2)` and explicitly checks the denominator
threshold against each actual length. Rational density does not overcome
these quantitative requirements.

This is a failure of the stated uniform degree/height bound. It is not an
impossibility theorem for lower-degree factors, sharper root heights,
dependent roots, or another argument. The growing-power divisibility and
full digit-sum test have not been established for this family. No witness
is claimed. The exact two-quotient procedure inherited from PR #9/#10
remains an available per-length test; uniform rejection over these gaps
is still unproved.

## Finite coverage, validation, and reproduction

Every new analytic exclusion starts at `N=10,000,000` inclusive. Both
inherited exact certificate programs were rerun at their full defaults.
They continue to exclude all residual odd lengths through 9,999,999;
the inherited elementary reduction also excludes the other original
words and even lengths. Thus complete coverage remains **all lengths
1 through 10,000,000 inclusive**. No new exhaustive length interval
above that endpoint is certified.

There is no residual finite interval between an analytic threshold and
the existing certificate for any strip claimed here. No global cutoff
`B` was obtained; the unresolved full problem includes lengths above
10,000,000 in the uncovered position regions. Qualitative finiteness
does not change that statement.

From the repository root, with Python 3.8+ and a C++17 compiler for the
inherited lifting program:

```sh
python3 research/a398769/five-seven/proportional/checks.py
python3 -O research/a398769/five-seven/proportional/checks.py
python3 research/a398769/five-seven/proportional/independent_checks.py
python3 -O research/a398769/five-seven/proportional/independent_checks.py
python3 research/a398769/five-seven/settlement/verify.py --output /tmp/a398769-proportional-lifting.json
python3 research/a398769/five-seven/settlement/verify_fixed.py --output /tmp/a398769-proportional-independent.json
git diff --check
```

The new checkers use exact integer and rational arithmetic, including
rigorous logarithm enclosures with remainder bounds. They verify the
strict comparison at `N`, ratio endpoints, both signs in the polynomial
parameterizations, positive modular/root-lifting controls, the midpoint
refinement, the gap-family arithmetic, the `(23,15)` regression, and the
full-divisor distinction. Neither imports the other. Checks remain active
under `python3 -O`.

The lifting rerun matches the inherited receipt except elapsed runtime;
the independently implemented fixed-modulus rerun matches every field.
[verification.json](verification.json) records commands, receipt hashes,
coverage and exact comparison results. [REVIEW.md](REVIEW.md) and
[review.json](review.json) record independent proof and arithmetic review.

No Lean source changed, no new Lean formalization was added, and no new
Lean build is claimed. These are ordinary proofs using the cited theorem,
with machine-checked finite arithmetic outside Lean. The branch is for a
draft pull request; merging remains with the owner.
