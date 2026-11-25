# High-depth position investigation

25 November 2026. **Verdict 4: No closing advance.** The all-length
`{5,7}` subclass remains open. No full witness, effective global valuation
bound, numerical cutoff, or new excluded length interval was obtained.

The investigation verifies the proposed single-position/zero-lift
formulation and proves a sharper stabilization lemma for the digit-sum
order. That lemma explains a limitation of using exponent CRT compatibility;
it removes no remaining witness and does not bound the zero run.

## Baseline and preservation

The starting commit on current `main` was
`b6db8703afd3d32211fd75de9ce1e34440dddfe8`, also the actual merge commit of
[PR #14](https://github.com/lukeroyle-beep/Mathematics/pull/14).
GitHub reported PR #14 merged, with audited head
`22ef46d55fa903b54e0b288a1b38ba0a6fa0659a`; both commits were verified as
ancestors of this checkout. The research uses a separate clone and branch
`research/a398769-high-depth-position`. Existing checkouts were not edited.
No applicable `AGENTS.md` was found in the repository or its directory
ancestors. Existing Markdown proof notes, standard-library exact Python
checkers, JSON receipts, and the ordinary-proof/Lean distinction are retained.

The inherited large certificates are reused from their committed audited
records, with source and receipt hashes checked against the starting commit.
They were **not** rerun in this investigation. PR #14 records their fresh
reproduction. This avoids repeatedly performing unchanged large computations.

## Self-contained problem and exact residual domain

All candidates reduce to a decimal word of odd length L with exactly two
fives, at positions 0 and i, and sevens elsewhere; position 0 is the units
place. Set

```
F=7*10^L-18*10^i-25, n=F/9, S=7L-4, P=25*7^(L-2).
```

The full condition is exactly `225*S*7^(L-2) | F`. For `i>=3`, the
suffix 775 gives `v_5(n)=2`; therefore `5 | S` is excluded, not assumed
away. On the remaining domain, `gcd(25,S)=1`, `7` does not divide S,
and `25 | n`. Hence the target is exactly

```
9S | F  ==>  v_7(F) <= L-3.
```

The nine is essential, including when `3 | S`. The following are inherited
**proved necessary restrictions**, not empirical observations:

```
L > 10,000,000, L odd,
417 <= i < L, i = 3 mod6, L-i >= 396,
(L mod6, i mod42) in {(1,39),(3,3),(5,15)},
gcd(S,5*11*13*37*101*127*239*1933*2689*4649*
       459691*909091*10838689)=1,
if 43 divides S, then L = 191 mod1806,
L-3 <= 63*(i+1)*max(log L+2,20)^2,
L-2 <= 63*(L-i+1)*max(log L+2,20)^2,
abs(L-2i) > 179.
```

Here and throughout, `log` is natural. In addition, `x=i/L` must lie in
one of the six **open** intervals

```
(1/25000,           299999/900000)
(300001/900000,     3999999/10000000)
(4000001/10000000,  59999/120000)
(60001/120000,      5999999/10000000)
(6000001/10000000,  599999/900000)
(600001/900000,     24999/25000).
```

Their endpoints are excluded. The fixed midpoint condition above also
applies; it is stronger than the proportional midpoint strip for
`L<10,740,000`. The exact full-sum congruence `9S | F` remains required.
The prior isolated and constructed whole-length exclusions below must
also be removed. This describes the residual domain relative to the
named inherited results; it does not assert that any pair survives all
these tests.

The complementary domains are covered by the existing elementary
digit-pattern/parity/position reduction, the finite certificate, the
edge inequalities, prime-divisor filters, proportional exclusions, and
whole-length proofs. The present lemmas apply to a larger domain and
silently discard none of that complement. Sources:
[initial reduction](../README.md), [settlement](../settlement/README.md),
[full divisor](../settlement/FULL_DIVISOR.md),
[proportional coverage](../proportional/COVERAGE.md),
[prime filters](../depth/PRIME_FILTERS.md), and
[whole-length proof](../whole-length/PROOF.md).

## What is proved here, and what is still missing

[PROOF.md](PROOF.md) checks the order `T_k=6*7^(k-1)`, existence and
uniqueness of `r_k`, `K(L)<=L-2`, the strict actual-position endpoints,
and the exact lift formula. A witness must use `i=r_K`, pass `9S | F`,
and have `a_K=...=a_(L-3)=0`. This formulation is an exact criterion,
not an exclusion.

For `d=ord_S(10)`, the new elementary lemma proves

```
v_7(d) <= K(L)-1.
```

For `e>=1`, a factor `7^e` of d forces a prime `q | S` with
`q>=2*7^e+1`; the special relation `S=3 mod7` forces `S/q>=3`.
Thus `6*7^(e-1)<=L-1`; the case `e=0` is immediate.
Consequently `gcd(d,T_k)` already stabilizes
for every `k>=K(L)`. If the full-sum and seven-power exponent classes
are compatible there, they remain compatible at every higher depth
when the upper position bound is dropped. This sharpens the older
stabilization threshold but supplies no valuation upper bound.

The unresolved obligation is to force some `a_k!=0` with
`K(L)<=k<=L-3` for every remaining actual, sum-compatible `r_K`, or
otherwise reject that representative. A uniform effective p-adic
approximation bound strong enough for this varying pair would supply
the missing ingredient. No such theorem is established here.
[ROUTES.md](ROUTES.md) records the attempted routes and their exact gaps.
No new external-theorem application or effective constants are claimed.

## Exact computational scope

[checks.py](checks.py) uses linearized lifts and direct modular powers.
[independent_blocks.py](independent_blocks.py) imports no primary code;
it enumerates complete unit cycles to recover discrete logarithms and
checks actual words by decimal-block concatenation. Their ordered
per-length digest agrees:

```
a54ad76ea69a6db88927613cfab5da3db41189fbeb5b7b81ebbef6d62247eab7
```

The fixed diagnostic window is every odd L from 5 through 100001
inclusive: 49,999 lengths, 28,371 actual `r_K`, and 22,713 of those
with `5` not dividing S. None of the latter passes the full digit sum.
No assertion about unexamined lengths follows. Zero-run controls show
that bounded representatives need not escape immediately. Full-sum
positive controls, loss-of-nine negative controls, literal decimal
checks, strict period boundaries, and sharp order-stabilization controls
test the separate mechanisms; see [COMPUTATION.md](COMPUTATION.md).

All essential checks use exceptions or explicit conditionals, not
removable `assert` statements. Ordinary and optimized Python outputs
agree. [REVIEW.md](REVIEW.md) records independent mathematical and
computational review. [verification.json](verification.json) records
the source hashes, unchanged inherited dependencies, and run results.

From the repository root:

```sh
python3 research/a398769/five-seven/high-depth/verify.py
python3 -O research/a398769/five-seven/high-depth/verify.py
git diff --check
```

The verifier runs both implementations under ordinary and optimized
Python and compares their committed receipts and common fields. It
does not rerun the ten-million certificates.

## Unchanged result and coverage boundary

| Result | Exact scope |
|---|---|
| Consecutive exclusion | Every length 1 through 10,000,000 inclusive. |
| Earlier isolated exclusion | `(898129*3^193+4)/7`, maximum depth six. |
| First appendix exclusion | `(3^164*17^41+4)/7`, maximum depth four. |
| Second appendix exclusion | `(3^103*898129^21+4)/7`, maximum depth seven. |
| Infinite whole-length family | For each fixed positive k and each prescribed open ratio interval in `(0,1)`, infinitely many lengths have maximum depth exactly k attained in that interval. |
| Qualitative bound | Uniform `v_7(F)=o(L)`, with no effective starting length. |
| This investigation | Diagnostic lemma and exact bounded audits; no added interval or full witness. |

The three specified giant lengths are distinct and do not extend the
consecutive interval. Fixed k followed by infinitely many lengths does
not meet the growing threshold `k=L-2`; it also rules out a constant
bound for all maximum depths. Fixed-modulus quotient survivors do not
give an exact quotient or witness. The rational-centre coverage
obstruction concerns the recorded uniform estimate, not every possible
refinement.

There is no numerical B and hence no claimed finite gap `(10,000,000,B)`
awaiting certification. The unresolved obligation remains unbounded in
length, except for inherited exclusions. The all-length subclass and the
full A398769 digit-1 conjecture both remain unresolved.

All new proofs are ordinary mathematics and all computations are exact
finite arithmetic outside Lean. No Lean source was changed, no new
formalization was added, and no new Lean build is claimed. Prepared as
a draft PR for owner review; merging remains with the owner.
