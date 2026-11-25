# Early rejection for the two-five family

25 November 2026. **Primary verdict: no structural advance; finite evidence
audited.** Both reported count rows reproduce independently, with agreement
on ordered per-length results. The declared structured search found no
counterexample to (E). No all-length or new restricted valuation theorem,
full witness, effective global cutoff, or Lean formalization was obtained.

**Certified finite statement:** (E) holds for every odd L from **5 through
9,999,999 inclusive**. The inherited consecutive exclusion remains every
length **1 through 10,000,000 inclusive**. The all-length `{5,7}` subclass
and the wider A398769 digit-1 conjecture remain open.

## Verified starting point and preservation

The actual starting commit is `de64c6da6d616455b69eb9bcf33646ce4e798279`,
the freshly verified current `main` and merge commit of
[PR #15](https://github.com/lukeroyle-beep/Mathematics/pull/15).
Its audited research head `cd4df1843e8a17655115275e5df956cf985a5819` is an
ancestor. There was no later work on main at startup. A separate clone and
branch `research/a398769-early-rejection` preserve all existing checkouts.
No applicable `AGENTS.md` was found in the repository or directory ancestors.

The investigation read the pinned high-depth
[report](../high-depth/README.md), [proof](../high-depth/PROOF.md),
[routes](../high-depth/ROUTES.md), and [computation](../high-depth/COMPUTATION.md),
then followed the elementary reduction, full divisor, whole-length family,
qualitative bound and complete remaining restrictions. Existing large
certificates are reused with source/receipt hashes and starting-commit bytes
checked, not rerun. Only the new early-rejection claim is freshly reproduced.

## Statement and exact domain

For odd `L>=5`, **every** position `3<=i<L` (initially both parities), set

```
F(L,i)=7*10^L-18*10^i-25,
n=F/9, S=7L-4, P=25*7^(L-2),
T_k=6*7^(k-1), K(L)=min{k>=1:T_k>L}.
```

The decimal word n has fives at positions 0 and i and sevens elsewhere.
Its actual digit sum is S and product is P. The original condition is
exactly `225*S*7^(L-2) | F`. Its suffix 775 gives `v_5(n)=2`, excluding
`5|S` from full witnesses. On the remaining five-free domain it separates
as `9S|F` and `v_7(F)>=L-2`. **The nine is indispensable.**

The proposed statement (E), whose truth is not assumed, is

```
For every odd L>=5 with 5 not dividing S, and every 3<=i<L,
9S | F(L,i)  ==>  v_7(F(L,i)) < K(L).
```

Because `ord_(7^k)(10)=T_k`, there is a unique `0<=r_k<T_k` satisfying
`18*10^r_k = 7*10^L-25 mod7^k`. The strict actual-position condition is
`3<=r_K<L`. [PROOF.md](PROOF.md) independently proves the equivalent form

```
3<=r_K(L)<L  ==>  9S does not divide F(L,r_K(L)).
```

Modulo seven, positive depth forces `i=3 mod6`; this derives the parity
restriction for the depth test rather than imposing it on the broad sum
domain. Integer arithmetic computes K, including even equality boundaries.
Since `K<=L-2`, a proof of E plus the inherited complementary elementary
cases would settle the `{5,7}` subclass. It would not settle other digit sets.

## The finite audit

| Odd lengths | Lengths | Actual r_K | Actual r_K, five-free S | Full-sum passes |
|---|---:|---:|---:|---:|
| 5..100001 | 49,999 | 28,371 | 22,713 | 0 |
| 5..9999999 | 4,999,998 | 1,958,137 | 1,566,063 | 0 |

These are independently recovered results, not targets forced into the
implementations. [COMPUTATION.md](COMPUTATION.md) defines all four partition
categories, controls, integer bounds, the record format and mismatch isolation.
[A](checker_a.py) uses complete power cycles and `F mod9S`.
[B](checker_b.py) uses successive linearized lifts and division-free modular
repunit concatenation for `n mod S`. Neither imports the other's code.

Both full ordered streams have SHA-256
`037a7a03e48eceea6893641af0459885380975e2234aa11b6820a0d2a6c5f08f`.
All 100 block hashes agree. Each implementation gives byte-identical full
receipts under normal and optimized Python. No full-sum-compatible actual
`r_K` with five-free S was found in either the main audit or structured search.

## Declared falsification search

[search_scope.json](search_scope.json) was written before execution.
[search.py](search.py) completes exactly that scope with no inherited
witness filters and no enlargement after zero observations:

1. `S=3^a*p^b`, `p in {17,898129}`, `0<=a<=200`, `0<=b<=40`;
   retain `S>=31`, `S=3 mod7`, odd `L=(S+4)/7`, five-free S. These primes
   come from inherited tractable full-sum constructions. Test each length
   at its own K; no fixed-depth-to-growing-depth inference is made.
2. For every `1<=d<=240` and `0<=a,b<d`, form
   `G=gcd(7*10^a-18*10^b-25,10^d-1)`, remove all factors of seven,
   and test every quotient obtained by removing zero or more factors of
   three. Retain the broad length domain and `L mod d=a`. This seeks
   large S with short full-sum exponent periods. It covers the specified
   gcd quotients, **not every divisor of G**.

The [receipt](search.json) records exact ranges, maxima and ordered hashes:

| Family | Raw parameter/exponent pairs | Distinct lengths | Outside actual interval | Actual, fails full sum | Passes |
|---|---:|---:|---:|---:|---:|
| Smooth sums | 16,482 | 2,731 | 1,538 | 1,193 | 0 |
| Cycle gcds | 4,636,840 | 37 | 23 | 14 | 0 |

The union contains 2,768 lengths, including 2,721 above 9,999,999.
The smooth-family maximum is `(3^199*898129^40+4)/7`, a 333-digit length;
the cycle-gcd maximum is only 14,731. The latter construction did not produce
large candidate sums in this scope. Both searches completed, with no
unresolved factorization or discrete logarithm. Every actual representative's
full-sum residue was separately checked by a geometric-sum recurrence.
No counterexample certificate is claimed because none was found.
These sparse checks do not fill any consecutive interval above 10,000,000.

## Structural outcome and the remaining obligation

[PROOF.md](PROOF.md) reconstructs the equivalence and the inherited bound
`v_7(ord_S(10))<=K-1`. Thus unrestricted full-sum/seven-power exponent CRT
compatibility stabilizes by K. Compatibility at K persists at every greater
depth; a later-incompatibility argument needs an additional bounded-position
condition. Uniqueness alone does not reject the representative.

[ROUTES.md](ROUTES.md) records the first unproved step in each route.
Fixed-depth whole-length families allow lengths to grow and do not control
the diagonal K(L). The inherited qualitative `v_7(F)=o(L)` supplies neither
the proposed logarithmic bound nor an effective starting length. No external
estimate is newly applied and no varying `10^L` or `10^i` is hidden in a
fixed-height parameter. The cycle-gcd reduction guides a finite search but
supplies no new uniform valuation bound. The verdict remains **no structural
advance**, rather than presenting audited reductions as a new theorem.

To prove broad E still requires a uniform rejection of the full `9S` test
at every actual `r_K(L)` in its five-free domain. To settle the subclass,
the weaker sufficient obligation is to prove `v_7(F(L,r_K))<=L-3` on the
narrower surviving full-witness domain, or obtain and discharge an effective
global cutoff. There is currently no explicit cutoff and no finite gap
claimed complete.

## The narrower full-witness domain is preserved separately

None of these restrictions was used to discard potential counterexamples
to broad E. Inherited full witnesses would have to satisfy all of:

```
L>10,000,000 odd, 417<=i<L, L-i>=396, i=3 mod6,
(L mod6,i mod42) in {(1,39),(3,3),(5,15)},
gcd(S,5*11*13*37*101*127*239*1933*2689*4649*
       459691*909091*10838689)=1,
if 43 divides S, L=191 mod1806,
L-3 <= 63*(i+1)*max(log L+2,20)^2,
L-2 <= 63*(L-i+1)*max(log L+2,20)^2,
abs(L-2i)>179,
9S | F,  v_7(F)>=L-2.
```

Here log is natural. Additionally `i/L` lies in one of the six open intervals

```
(1/25000,             299999/900000)
(300001/900000,       3999999/10000000)
(4000001/10000000,    59999/120000)
(60001/120000,       5999999/10000000)
(6000001/10000000,   599999/900000)
(600001/900000,      24999/25000).
```

Endpoints are excluded. The fixed midpoint condition remains separate and
is stronger than the proportional midpoint strip below 10,740,000.
Sources are the [initial reduction](../README.md),
[full divisor](../settlement/FULL_DIVISOR.md),
[edge bounds](../settlement/EDGE_BOUNDS.md),
[prime filters](../depth/PRIME_FILTERS.md),
[proportional coverage](../proportional/COVERAGE.md), and
[whole-length proof](../whole-length/PROOF.md).

The separate giant isolated exclusions at lengths
`(898129*3^193+4)/7`, `(3^164*17^41+4)/7`, and
`(3^103*898129^21+4)/7`, and the infinite fixed-maximum-depth whole-length
families, remain separate from consecutive coverage. Their unchanged scope
is inherited. The new sparse search is likewise not a consecutive certificate.

## Reproduction and review

From the repository root:

```sh
python3 research/a398769/five-seven/early-rejection/verify.py --recompute
python3 -O research/a398769/five-seven/early-rejection/verify.py
python3 research/a398769/five-seven/early-rejection/search.py > /tmp/early-search.json
cmp /tmp/early-search.json research/a398769/five-seven/early-rejection/search.json
```

[REVIEW.md](REVIEW.md) records separate implementation, arithmetic and
adversarial review contexts, must-fix resolutions and exact reviewed artifacts.
All new arguments are ordinary mathematics and all computations are exact
finite arithmetic outside Lean. Existing Lean sources are unchanged; no
new Lean theorem or new Lean build is claimed. Delivered in one draft PR;
merging remains with the owner.
