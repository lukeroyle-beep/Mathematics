# Trillion-length archive: independent audit

The recovered archive supports exclusion of **every length 1 through
1,000,000,000,000 inclusive** for the original `{5,7}` digit family. Both
complete enumerations were freshly compiled and run in this audit; their
complete candidate lists agree with each other and the archived list. A new
verifier reconstructed the original decimal runs independently and rejected
every candidate at its exact valuation. This is finite coverage, not an
all-length proof.

## Identity and provenance

The [handoff](https://chatgpt.com/space/page_78343827a5248191bf9cf30f544b7df1)
and [text recovery page](https://chatgpt.com/space/page_41ea1c38c3d481918d76e6b5a5941c0e)
were read on 26 November 2026. The two complete source-text references were
decoded, with strict base64 validation, to
[`evidence/trillion-evidence.zip`](evidence/trillion-evidence.zip).

* ZIP: 920,596 bytes; 28 members; SHA-256
  `b657f158d6362c77c570b87c3c193fe54c6f3c385889379edf5bf79b71f05c0a`.
* Both text parts: 621,775 and 621,840 bytes; hashes respectively
  `46aef5b2d325fc8e5a3a0df9cddd7937cdb8e2765a2f293543a3d7cab2b77b68`
  and `268b6f09069027d845ff2bdf10f1a53dbeaecc1d9b5276f2c05975a63ef19d1e`.
* Every ZIP member passed CRC verification. All 27 hashes in the internal
  `SHA256SUMS.txt` were checked, with no omitted or extra member.
* The exact [Space report](evidence/space-report.md) is 6,111 bytes with hash
  `5f54f5ba84369c4516f33ae9d556f58da927e5aaabb5f1ea5b72bc8ceb81fbc9`.
* The canonical 74,601-row candidate CSV has hash
  `919c091c978ee1e6011f9239fadbba675985714f286d8dcffa1a29ed043cf8e4`.

The archive was obtained directly from the handoff's recovery references;
no pre-PR-21 pack was used as current repository authority.

## Why the enumeration is complete

The archived `valuation/lattice/PROOF.md`, `lattice.cpp`,
`valuation/floor-sum/PROOF.md`, and `scan.cpp` were audited together.
The common mathematical input is

\[
\operatorname{ord}_{7^k}(10)=6\,7^{k-1}=:T_k,
\]

from order six modulo seven and `v7(10^6-1)=1`.
At depth `d`, all solutions have a unique representation

\[
L=h+jT_{d-1},\qquad i=r+vT_d,
\]

where `h` is odd in `[1,T_(d-1))`, `0<=r<T_d`, and `j,v>=0`.
For each `h` there is exactly one `r`, because powers of ten enumerate
the units modulo `7^d` and `(7*10^h-25)/18` is a unit. Every such `r`
is `3 mod 6`, so restricting the lattice base enumeration to that class
loses no depth-`d` candidate.

For `P=7^(d-1), U=T_(d-1), V=T_d`, divide the exact first-order expansion
by `7^d` modulo `P`:

\[
F(h+jU,r+vV)/7^d
\equiv c+10^h a j-18\,10^r b v\pmod P,
\]

where `a=(10^U-1)/P` and `b=(10^V-1)/7^d` are units modulo `P`.
The omitted terms have valuation at least `2d-1` before division, including
the extra leading factor seven in the first exponential. Thus this is an
equivalence for depth `2d-1`, not a heuristic linearization.

The lattice implementation, with `d=10`, inverts the coefficient of `j`
and visits exactly the points of an affine lattice in a closed rectangle.
Euclidean changes of lattice basis preserve determinant `P`; the signed
ceiling/floor bounds enumerate every integer line and every point on it.
The rectangle has `j<=floor((B-h)/U)` and
`v<=floor((B-1-r)/V)`; the final predicate is `L>=5, i<L`. Hence equality
at `L=B` is allowed and equality at `i=L` is rejected.
An independent higher-modulus check on each enumerated point retains
exactly those reaching depth 22.

The second implementation starts from **all** depth-two bases and lifts
each length residue through seven children. The linear congruence uniquely
determines the position child. At `d=11` this gives `T_10/2=121060821`
leaves. It inverts the coefficient of `v` and counts residues in a
rectangle using exact floor-sum recursion, then recursively enumerates
the nonempty intervals and applies `5<=L, 3<=i<L`. The rectangle may
include `i=B`, but the final strict inequality removes it. Its depth-21
survivors are independently tested modulo `7^22`.

The signed lattice products remain below `1.7e15` at the supported bound;
the larger modular products use unsigned 128-bit arithmetic. In the
floor method, `7^21=558545864083284007`, so `18*(7^21-1)+25<2^64`.
Its rectangle has at most 4,131 length indices and 591 position indices;
floor-sum terms and affine products fit unsigned 64 bits. The final
modulus is `7^22` and that check uses 128 bits. The diagnostic signature
alone intentionally wraps modulo `2^64`; no conclusion depends on that
signature without candidate-list comparison.

## Fresh runs and independent decimal verification

Compilation used Apple clang 21.0.0, arm64, `-O3 -std=c++17` (the system
`g++` frontend), with `-DDEPTH=11` for the floor method. Full runs were
sequential, not overlapping CPU searches. The observed summaries were:

```text
limit 1000000000000 base_depth 10 groups 17294403 depth_19 25586997 depth_20 3654595 depth_21 522020 depth_22 74601
B 1000000000000 seeds 121060821 rectangular 1044321 domainDepth 21 domainCount 522020 pass22 74601 sig 18130229677626043502
```

Both complete output lists were compared entry-for-entry with the
canonical archived CSV, including uniqueness, ordering after sorting,
and domain checks. Their raw output hashes and source hashes are in
[`evidence/archive-audit.json`](evidence/archive-audit.json).
The exact individual compile/run commands, successful exit codes,
compiler identity, executable hashes and raw stdout hashes are retained
separately in [`evidence/enumeration-runs.json`](evidence/enumeration-runs.json).
Its mode is `provided_outputs_verified`: the new checker consumed the
outputs of the two preceding fresh subprocess runs, rather than claiming
to have launched those runs itself.

The new [`archive_audit.py`](archive_audit.py) imports none of the archive's
programs and does not use the formula for `F` to evaluate the number.
It concatenates `7^(L-i-1),5,7^(i-1),5`, where superscripts here denote
decimal repetitions. Binary powering of the concatenation monoid
`(value,10^length)` computes this word modulo `7^28` without division.
All 74,601 candidates have nonzero residues there and exact valuations:

| `v7(n)=v7(F)` | 22 | 23 | 24 | 25 | 26 | 27 |
|---|---:|---:|---:|---:|---:|---:|
| Pairs | 63,974 | 9,161 | 1,272 | 162 | 29 | 3 |

The three depth-27 pairs and their `F/7^27 mod7` residues are
`(206013221471,70699701213):5`,
`(636442113223,552133548915):4`, and
`(778826473305,776307582249):1`.
They all also fail the full digit-sum test, as recorded in the receipt.
Any omitted pair has valuation below 22 by completeness; therefore the
global maximum **within the finite domain** is exactly 27. For `L>=30`
this is below `L-2`. All 182 original decimal words for odd `5<=L<=29`
and `3<=i<L` were literally constructed and checked against `7^(L-2)`.
The elementary reduction in the archive/root research handles the other
patterns and lengths, so the resulting whole-length interval begins at 1.

Additional fresh controls were:

* Lattice versus independent direct modular tables at `(d,B)=(3,25000)`
  and `(4,70000)`: lower-depth counts 10,843 and 1,688, and nonempty final
  candidate sets of 29 and 5, with full set equality.
* The floor helper's 20,000 deterministic random integer comparisons.
* Floor scan at `(d,B)=(3,1800)` versus a separately generated exhaustive
  modular table: 113 rectangle hits, 64 domain hits, signature
  `7261989003630623330`.
* The original archived decimal checker, independently of the new one.
* Positive sum-only control `(L,i)=(61,57)`: `n mod423=0` while
  `F mod49=35`. It is not a full witness.
* The new checker normally and under `python3 -O`: identical JSON receipts.

The separate 842-million-length early-rejection search was **not rerun**
and its source proof was not independently audited here. Its historical
claim is not promoted to a new `(E)` certificate by this valuation audit.
The narrower candidate-depth theorem is sufficient for the whole-length
trillion bound.

## Reproduction

From the repository root:

```sh
python3 research/a398769/five-seven/prime-sum/archive_audit.py
python3 -O research/a398769/five-seven/prime-sum/archive_audit.py
python3 research/a398769/five-seven/prime-sum/archive_audit.py --rerun-enumerations --output /tmp/archive-rerun.json
```

The first two verify archive integrity and every retained pair; they do
not reproduce enumeration completeness by themselves. The third extracts
the authenticated source into a temporary directory, compiles and freshly
runs both exhaustive enumerations, compares their complete lists, and
records `freshly_executed`. That computation is finite and uses no
digit-sum pruning or unproved global estimate.

## Audit of the Space density-one statement

The archive's `proofs/digit-sum-density.md` is a valid ordinary proof
that lengths permitting `S|F(L,i)` for any integer `i>=0` have natural
density zero, also within each fixed arithmetic progression. It is a
different density denominator from prime digit sums.

Here are the critical quantifiers and independence checks. Fix a modulus
`M` first. For primes `p=1 mod40` with `p` not dividing `M` and
`ord_p(10)>=20M*sqrt(p)`, the event `p|7L-4` has frequency `1/p` in
every class modulo `M`. Conditional on it, `10^L` runs uniformly through
a multiplicative coset of size at least `20sqrt(p)`. A character expansion
of its indicator and the Jacobi-sum bound show at least one third of
this coset has `7*10^L-25` a quadratic nonresidue. Since `18*10^i` is a
nonzero square at these primes, this excludes every exponent `i`.

The order theorem applies to the positive function
`epsilon(x)=log(20M)/log(x)` for sufficiently large `x`, which tends to
zero; it leaves `o(x/log x)` bad primes. Thus good primes in `1 mod40`
have divergent reciprocal sum for each fixed `M`. This use is
unconditional; it is part (i), not the GRH-dependent part (ii), of the
statement in [Akbary–Yazdani, Lemma 2.3](https://www.cs.uleth.ca/~akbary/Akbary-Yazdani.pdf).
The exact character bounds were checked against
[Conrad, Corollary 2.5 and Theorem 2.6](https://kconrad.math.uconn.edu/blurbs/gradnumthy/Gauss-Jacobi-sums.pdf).

Independence of the character events is **not** assumed. For distinct
good primes their intersection is bounded above by the divisibility
event `pq|7L-4`, whose relative frequency is `1/(pq)` by CRT. A finite
set with reciprocal sum `s>=1` therefore has first moment at least
`s/3` and second moment at most `s+s^2`; Cauchy–Schwarz excludes at
least `1/18` of every progression. Replace `M` by the least common
multiple of the finitely many new periods and repeat. After any fixed
number `j` of stages the surviving periodic superset has density at
most `(17/18)^j`. Taking upper densities and then `j` to infinity is
legitimate; no assertion about an infinite product of independent
events is needed.

This density-one exclusion still allows exceptional lengths, including
all prime-sum lengths as a set of zero density among integers. Neither
this proof nor the prime Chebotarev fractions imply an effective last
exception or emptiness of the exceptional set.
