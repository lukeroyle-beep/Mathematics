# Effectivity investigation: new partial results, family still open

25 November 2026. Starting main was exactly
`4dc97536a57d1b216f79e4856c333ea2c8e6d1ae`, the verified merge of
[PR #9](https://github.com/lukeroyle-beep/Mathematics/pull/9).
Work uses the separate branch `research/a398769-five-seven-effective`
in an isolated clone. Earlier checkouts were left untouched. No applicable
`AGENTS.md` was present in the clone or its workspace ancestors; the root
README and the inherited research and review notes supplied repository
conventions. The pinned Lean toolchain and dependency remain unchanged.

**Outcome 4: new partial results. The complete `{5,7}` subclass remains
unresolved.** There is no global effective cutoff or full witness.
The certified complete interval remains every length through 10,000,000
inclusive; no new interval above that is claimed.

## Results and scope

- [Uniform qualitative valuation bound](QUALITATIVE.md): for every
  `epsilon>0`, finitely many integer pairs `L>=5, 3<=i<L` have
  `v_7(F)>=epsilon*L`. Thus `v_7(F)=o(L)` uniformly over positions.
  This checks the requested `epsilon=1/2` application with `c=1,d=3/4`
  and derives the general statement from the same Evertse corollary.
  It uses no digit-sum assumption and has no effective starting length.
- [Explicit valuation bound and central-strip exclusion](ROUTE_A.md):
  for every odd `L>=5`, `3<=i<L`, the new effective estimate is
  `v_7(F)<=504*(|L-2i|+2)*max(log L+2,20)^2`.
  It needs no digit-sum assumption and displays the dependence on the
  changing offset. On `|L-2i|<=47` it contradicts the necessary valuation
  above 10,000,000; the reproduced inherited certificate covers every
  lower length. Thus no full witness lies in this strip at any length,
  and no finite verification remains for that restricted result. Both
  position and gap can grow without bound there. It is not a global
  length cutoff.
- [Exact quotient and digit-sum refinements](ROUTE_B.md): the first
  quotient's exact range can be enlarged to a split of size
  `(log 7/log 10)*L+(log L/log 10)+O(1)`, defined by integer comparisons.
  An exponent CRT retains the full digit sum, including when `3|S`.
  Neither refinement uniformly rejects the candidates.
- [Conditional cutoff calculation](CUTOFF.md) checks endpoints and rounding
  if a uniform effective estimate is eventually proved. It supplies no
  values for the missing constants.

See [independent review](REVIEW.md) for the accepted scope and exact
reviewed hashes. All new proofs here are ordinary mathematics and the
computational checks are exact finite arithmetic. No new Lean theorem or
fresh Lean build is claimed.

## Exact problem and inherited restrictions

Position zero is the units position. The two fives are at `0,i` and the
other digits are seven. With natural logarithms in estimates,

```text
n = (7*10^L-18*10^i-25)/9,   F = 9n,
P = 25*7^(L-2),              S = 7L-4,
S | n   iff   9S | F,
PS | n  iff   225*7^(L-2)*S | F.
```

Every full witness has `v_7(F)=v_7(n)>=L-2`. The inherited reduction and
certificates in [settlement](../settlement/README.md) and
[global](../global/README.md) impose

```text
L > 10000000 odd,    417 <= i < L,    L-i >= 396,
i = 3 mod 6,
(L mod 6,i mod 42) in {(1,39),(3,3),(5,15)},
L != 2 mod 5, 10 mod 11, 8 mod 13, 27 mod 37, 15 mod 101,
L-3 <= 63*(i+1)*max(log L+2,20)^2,
L-2 <= 63*(L-i+1)*max(log L+2,20)^2.
```

These restrictions are necessary, not sufficient. The qualitative result
has the broader domain stated above. The quotient reduction and Route B
use odd `L>=5`, `i=3 mod6`, `3<=i<L` and `5` not dividing `S`, before
imposing the stronger inherited restrictions. No argument replaces
`9S|F` by `S|F`.

The new theorem adds both necessary restrictions

```text
|L-2i| >= 49,
L-2 <= 504*(|L-2i|+2)*max(log L+2,20)^2.
```

The offset is odd because `L` is odd. The second inequality additionally
excludes a growing band around the midpoint as the length increases.

In quotient notation, `A=9*7^(L-2)*S`, `H=25A`, `X=7*10^L/H`,
`m=ceil(L/2)`, `K=10^m/25`; `H` is a divisor, distinct from Evertse's
height `h=U`. The corrected merged bounds, with `L=2r+1`, remain

```text
X/K = 49/(9S)*(10/49)^r < 1,
0 < X-q <= 301/(225S)*(10/49)^r < 1   when i<m.
```

The two candidates are `floor(X)` and the least nonnegative residue
`-A^(-1) mod K`. Position recovery and all modular checks must still be
followed by `Hq=F(L,i)`. Neither a large modulus nor a small candidate
count is an exclusion proof.

## What is still missing

For the whole remaining family, no proved uniform effective estimate
`v_7(F)<=cL+C log L`, with explicit `c<1,C,L0`, was obtained, even after
requiring `9S|F`. The quadratic method's success on a fixed relation
between `L` and `i` does not make its heights uniform when that relation
varies. The quotient and digit-sum descriptions still require exclusion
of their exact small representatives over unbounded lengths.

A sufficient next lemma is such a uniform effective valuation estimate
on every residual pair outside the newly excluded subfamily. An
alternative is uniform rejection of both exact quotient candidates,
including their full equality and varying digit sum, or another effective
global reduction. Any finite interval left by a cutoff must be certified
before all-length exclusion can be asserted. An exact independently
verified witness would also resolve the subclass question in the other
direction; emptiness is not assumed.

The explicit prime set and constants in Evertse's application do not bound
its exceptional heights. Finite counts of subspaces, intervals or pairs
do not determine the largest exceptional length. The investigation does
not assert that no stronger method exists.

## Reproduction and evidence

From the repository root with Python 3.8+ and, for the inherited lifting
certificate, a C++17 compiler supporting unsigned 128-bit arithmetic:

```sh
python3 research/a398769/five-seven/certificates.py
python3 research/a398769/five-seven/log_bounds.py
python3 research/a398769/five-seven/settlement/verify.py --output /tmp/a398769-effective-lifting.json
python3 research/a398769/five-seven/settlement/verify_fixed.py --output /tmp/a398769-effective-fixed.json
python3 research/a398769/five-seven/effective/route_b_checks.py > /tmp/a398769-route-b.json
cmp /tmp/a398769-route-b.json research/a398769/five-seven/effective/route_b_checks.json
python3 -O research/a398769/five-seven/effective/independent_checks.py > /tmp/a398769-effective-independent.json
cmp /tmp/a398769-effective-independent.json research/a398769/five-seven/effective/independent.json
git diff --check
```

The new [independent checks](independent_checks.py) test the quadratic
identities and 7-adic root distances on actual digit constructions, all
48 strip discriminants by modular nonsquare certificates, and the exact
logarithm inequalities. They do not establish the asymptotic theorem by
enumeration. The new [quotient checks](route_b_checks.py) compare the
split and digit-sum CRT with exact digit arithmetic, including an actual
case where `S|F` holds but `S|n` fails, the `(23,15)` regression, and
explicitly labelled synthetic quotient successes.

[verification.json](verification.json) records the starting commit,
inherited source hashes, and the parent investigator's executed checks.
The two unchanged ten-million programs were rerun to validate the finite
coverage completing the strip exclusion: the fixed-modulus receipt is
identical to its merged record, and the lifting receipt differs only in
elapsed time. This is a reproduction of existing coverage.
[independent.json](independent.json),
[route_b_checks.json](route_b_checks.json), and
[review.json](review.json) preserve the new check counts and reviewed
content hashes. The proof notes identify primary-source URLs, printed
pages, parameter choices and downloaded PDF hashes.

No original search or quotient implementation was changed. Tests of
truncated powers, synthetic divisors and digit-sum survivors retain their
explicit limited scope. This branch is prepared for a draft pull request;
merging is outside this investigation.
