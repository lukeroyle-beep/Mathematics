# Exhaustive finite coverage

The two fresh enumerations cover the 300 `(K,b)` partitions in README.md and
the separate original `K=17,b=289` interval. They use no inherited sampled
centres as coverage. Every `1<=a<b` with `gcd(a,b)=1` and every integer
`-K²<=h<=K²`, including zero and both endpoints, is counted before pruning.
The inequality `|bi-aL|<=K²` is equivalent to membership of one of these
labelled lines. A pair may belong to several lines or denominators: all pair
counts and hashes below retain those labels, and are not unique-pair totals.

## Necessary congruences and line counts

The residual decimal word is odd-length, with fives at zero and i. At depth
one, `F=-18*10^i-25 mod7` vanishes precisely when `10^i=-1 mod7`, so
`i=3 mod6`. A full witness has `L-2>22` on every finite interval here, and
therefore must satisfy this congruence.

Writing `L=2ell+1`, `i=6j+3` gives

```
2a*ell-6b*j = 3b-a-h.
```

Because `gcd(a,b)=1`, the gcd of the two left coefficients is
`2g`, where `g=gcd(a,3)`. Thus the necessary and sufficient compatibility
condition for an integral odd-length line is

```
h = 3b-a mod 2g.
```

The primary enumerator solves
`ell = ((3b-a-h)/(2g))*(a/g)^(-1) mod (3b/g)`.
This determines `L=2ell+1 mod (6b/g)`. Splitting this progression into its
g phases gives disjoint progressions with length step `6b` and position
step `6a`. It starts each at its first allowed length and enforces
`3<=i<L`; both inequalities persist because `a>0` and `b-a>0`.

The independent enumerator instead solves `L0=-h*a^(-1) mod b`, puts
`i0=(aL0+h)/b`, and explicitly tests all six parameter residues `t0=0..5`
in `(L0+bt0,i0+at0)` for odd length and `i=3 mod6`. It shifts each surviving
phase using exact ceiling divisions for all three lower bounds: length,
position at least three, and length minus position at least one.
Both parameterizations give every eligible pair exactly once on each
labelled line; they do not assume that the original small representative
lies in the actual length interval.

`verify.py` independently counts h in each congruence class by floor
differences. `independent_runner.py` instead loops over h and checks the
congruence directly. These agree with both C++ enumeration counters:

| K | Partitions | Labelled lines | Compatible lines |
|---:|---:|---:|---:|
|15|124|5,540,084|2,314,738|
|16|114|7,072,218|2,945,860|
|17|62|5,624,406|2,343,851|
|Total|300|18,236,708|7,604,449|

## Periodic coverage and all children

In each phase write `(L,i)=(L*,i*)+(6b,6a)u`, with `0<=u<=U` the
exact finite interval. Since `ord_(7^d)(10)=6*7^(d-1)`, the expression
F is periodic in u modulo `7^(d-1)`. This is a sufficient period even
when it is not the least period. At depth one, u=0 modulo one is the
single root class. Every class at depth k has exactly the seven possible
children

```
r+j*7^(k-1) mod 7^k,   j=0,...,6.
```

The binomial/LTE identity `10^(6*7^(k-1))=1+7^k mod7^(k+1)` gives

```
F(r+j*7^(k-1))/7^k = F(r)/7^k - 3a*j mod7.
```

Here `18*10^i=3 mod7` because every phase has `i=3 mod6`; the length
term's additional factor seven makes its first change vanish modulo
`7^(k+1)`. If `7∤a`, exactly one digit solves this equation. If `7|a`,
either all seven children survive this level or none do. Both programs
enumerate all surviving children and explicitly check the modular-root
invariant. They do not use a simple-root assumption in the singular case.
Higher singular cancellation is handled by the same exhaustive recursion.

For a root representative r, every represented u is `r+t*7^(k-1)` for
`t>=0`. Thus `r>U` proves that the whole class, and every descendant, is
outside the interval. This is the only bound pruning during lifting.
At an output depth, every `r+t*7^(k-1)<=U` is expanded to its actual
`(L,i)`, with explicit endpoint and position checks.

The primary carries both modular powers modulo `7^22`, records all actual
depth-13 pairs, and continues the bounded tree through depth 22. The
independent implementation carries powers modulo `7^13`, expands every
actual depth-13 pair, and tests `F mod7^22` by separate modular
exponentiation at that actual pair. Thus its depth-22 result does not
depend on continuing the primary's tree. Multipliers for successive
depths are obtained by seventh powering, avoiding overflow from explicitly
forming `6b*7^(k-1)` at high depth.

For canonical comparison, each depth-13 stream consists of
`a,h,L,i\n` in increasing numerical `(a,h,L,i)` order, with decimal
integers, commas, LF, no spaces or header. Each denominator has its own
SHA-256. The two streams agree in count and digest for every partition,
including the entire original b=289 interval. Disjoint phase construction
and explicit duplicate checks prevent double counting within a labelled
line; overlap between different labelled lines is intentional.

## Full digit sum and original decimal controls

For each actual depth-13 pair, both programs also test `5∤S` and the
exact full sum condition; these tests are not used to prune the depth-22
coverage. The primary calculates F modulo **9S** with modular powers.
The independent program calculates the original decimal value modulo S:

```
n=7R_L-2-2*10^i,
R_L modS = (10^L mod(9S)-1)/9.
```

The division is exact because `10^L mod9S=1 mod9`. This preserves every
factor of three in S. Modular arithmetic never cancels nine modulo S.
The five-free condition is necessary because `v5(F)=2` for `i>=3`.
The exact original witness predicate is `225*S*7^(L-2)|F`.

There are no depth-22 survivors in either implementation. Hence each
actual finite-band pair fails a proved necessary condition no later than
depth 22, strictly below its witness deadline `L-2`. There is no unresolved
joint survivor and no need to build enormous strings or to test the full
astronomical divisor. Zero digit-sum passes at depth 13 is an additional
finite result; it is not asserted as a global fixed-depth theorem.

`controls.py` and `independent_controls.py` independently compare complete
small searches with literal original decimal words. They include nonzero
sum passes, singular lifts, inclusive singleton length endpoints, offset
endpoints and zero, and an actual nonzero depth-13 pair. The primary
control set additionally includes `v7(a)>=2` cases. The compiled arithmetic
of both programs is checked against an independent decimal concatenation
algorithm on a nonzero depth-22 pair, composite digit sums, and the
lost-factor-nine trap `(L,i)=(313,51)`. `135` is a positive control for
the original digit-product-times-digit-sum predicate, not a witness in
this two-five family. All Python checks use explicit exceptions and pass
under `python3 -O`.

## Receipts and restart semantics

Each runner finishes one denominator, hashes its canonical actual-pair
streams, and atomically renames a compact JSON receipt into place. The
receipt fixes source SHA-256, baseline commit, exact bounds, all counts,
pair hashes and the complete list of depth-22 survivors (empty here).
Temporary pair streams need not be committed. The primary additionally
binds its runner source; the aggregate binds both runners and all other
implementation artifacts. The independent runner verifies an explicitly
supplied binary against a freshly compiled copy before using it.

An interruption leaves complete receipts usable; an unfinished partition
is recomputed. Existing receipts with the wrong source or bounds cause an
error. Changed code requires a new output directory. Aggregation requires
exactly the expected filename set and identities, rejecting missing,
duplicate, extra or mislabeled partitions. The documented resume commands
use these checks and do not silently treat a partial search as complete.

The integer domain is bounded explicitly. Production lengths are below
`2*10^14`; `7^22=3909821048582988049` fits uint64, modular products use
unsigned 128-bit arithmetic, and signed primary line arithmetic uses
signed 128-bit arithmetic. All powers, positions, indices and modulus
products used in these searches fit their declared types. Controls do
not extend the supported C++ modulus beyond `7^22`.
