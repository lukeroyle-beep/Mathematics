# Uniform valuation bound: sufficiency and quantified method obstructions

25 November 2026. **Overall outcome: no closing advance.** The proposed
`v7(F)<=100000*K(L)^2` remains unproved and unrefuted. This investigation
does prove uniform auxiliary estimates, a general Hensel reduction, and
precise limitations of the available estimates. It supplies neither a
global bound for `v7(F)` strong enough to close the subclass nor a new
effective global cutoff.

| Objective | Verdict | Verified result |
| --- | --- | --- |
| 1. Sufficient uniform valuation bound | Sufficiency proved; bound unresolved | The exact quadratic comparison holds at every remaining length. The lift criterion and its endpoints are checked. A sharper digit-sum order bound and an exact size-method obstruction are proved. |
| 2. Uniform analytic method | Auxiliary uniform reduction proved; closing estimate unavailable | Every hypothetical full witness admits strong Hensel lifting at every reduced centre `0<a<b<=L`. Its selected root must be multiplicatively independent of ten. The remaining bound explicitly retains degree, height, offset, derivative loss, and every logarithmic maximum branch. |
| 3. Exact obstruction | Demonstrated for specified methods | Stable unbounded exponent compatibility cannot later become incompatible; the size bound permits the witness threshold at all `L>=12`; all ten Bugeaud--Laurent degree/span envelopes miss an explicit rational-position family. None is a general impossibility theorem. |

## Results and reading order

Start with [baseline and inherited scopes](BASELINE.md), then
[sufficiency, lifts, and digit-sum analysis](LIFTS.md),
[uniform analytic estimates and their limitations](ANALYTIC.md), and
[primary-source theorem audit](SOURCES.md).
[Computational evidence and reproduction](COMPUTATION.md) distinguish
proof from finite checks. [Independent review](REVIEW.md) records the
review procedure and findings; the draft PR identifies its exact final
reviewed commit.

For odd `L>10,000,000` and `3<=i<L`, the main auxiliary analytic result uses

```
K=K(L), B_K=1+252*(K+1)^3, L>10000000,
L=bq+r, i=aq+s, m=min(0,s), x=10^q,
Q(X)=7*10^(r-m)*X^b-18*10^(s-m)*X^a-25*10^(-m).
```

For **every** reduced `0<a<b<=L`, put `d=v7(Q'(x))`. Then
`d<=B_K` and `2B_K<L-2`. Thus a hypothetical full witness, whose
valuation `t=v7(F)` is at least `L-2`, has a unit root `alpha` in `Q_7`
with `v7(x-alpha)=t-d`. Every multiplicatively dependent selected root
would instead give `t<=B_K+K+1<L-2`. These are genuine uniform
auxiliary bounds; `B_K` bounds the **derivative**, not `v7(F)`.

For an independent root of actual global degree D, the justified bound
still contains `D^3*H`, where `H=w+2` and
`w=max(0,r,s)-min(0,s)`. The precise maximum and derivative loss are in
[ANALYTIC.md](ANALYTIC.md). Replacing D by b and using this span height
fails to give uniform coverage even after optimizing all ten explicit
parameter choices in the source theorem. Proper-factor degree, sharper
root-specific height, or extra full-divisor information could improve
that method; they have not been uniformly controlled here.

The digit-sum order sharpening is also unconditional on its stated
five-free domain. If `e=v7(ord_S(10))>=1`, then
`L>=2*T_e+1`. It is sharp at `L=13` and `85`, and makes the inherited
compatibility stabilization earlier in part of each K band. It forces
no lift digit to be nonzero.

## Exact coverage and status

**No whole-length coverage has been added.** The new position theorems
are the dependent-root branch exclusion and the general parameterwise
thresholds (13a)--(13c) in [ANALYTIC.md](ANALYTIC.md). They exclude their
specified positions above their own effective starts; the finite gaps
before those starts are not discharged. No finite union covering all
remaining admissible positions is proved. All previously named strips
and individual exclusions retain their scopes:

- Consecutive whole-length exclusion: **1 through 10,000,000 inclusive**.
- Broad (E): every odd length **5 through 9,999,999 inclusive**.
- Restricted minus-line (E): **`L<6*7^99`**; the qualifying depths through
  100 are 44, 56, 85, and 92, each with `gcd(F,S)=1`.
- Existing closed rational strips, both `12i-5L=+/-1` line exclusions,
  and isolated/infinite whole-length exclusions retain their precise
  original statements; a position result is not a whole-length result.

The depth-44 example refutes only the unconditional inequality
`v7(F)<K`. It fails the digit-sum premise. No counterexample to broad
(E), to the proposed quadratic bound, or full witness is found here.
Broad all-length (E), the all-length `{5,7}` subclass, and the wider
digit-1 conjecture remain **open**. Ineffective finiteness and `o(L)`
do not furnish an executable final search.

This work consists of ordinary mathematical proofs and exact computation.
No new Lean theorem, Lean formalization of an external theorem, or Lean
build is claimed. The inherited large searches were **not rerun**;
their retained certificates, independent receipts and integrity were checked.

From the repository root:

```sh
python3 research/a398769/five-seven/uniform-bound/verify.py > /tmp/uniform-verification.json
python3 -O research/a398769/five-seven/uniform-bound/verify.py > /tmp/uniform-verification-O.json
cmp /tmp/uniform-verification.json /tmp/uniform-verification-O.json
cmp /tmp/uniform-verification.json research/a398769/five-seven/uniform-bound/verification.json
git diff --check
```

The branch and draft PR are for owner review. Merging remains with the owner.
