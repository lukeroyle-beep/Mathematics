# Actual digit-sum positions and the seven-adic escape deadline

**No all-length escape proof, effective cutoff, or witness was obtained.**
The exact bounded-class reduction below isolates the missing implication.
The reproducible fallback excludes every one of the **128 specified lengths**
`L_a=(3^a+4)/7`, `a=31+6u`, `0<=u<128` (last exponent 793).

Two independently implemented checkers agree: **42** joint sum-position
classes miss `[3,L_a)`; the other **86** have a unique actual position,
with exact seven-adic valuations `{1:76, 2:8, 3:2}`. The two depth-three
cases have `a=97,757`. Every actual candidate already fails before K, so
none is an actual `r_K` survivor. These results neither prove nor refute
the universal deadline at actual sum-compatible `r_K` positions.

The first tested length is **88,239,056,611,993** and the last is exactly
`(3^793+4)/7`; the full decimal values and every intermediate length are
in [primary.json](primary.json) and [independent.json](independent.json).
These are 128 isolated lengths, not an interval between the endpoints.

## Exact statement and first missing implication

For odd `L>B=1,000,002,000,000`, the word has fives at positions 0 and i
from the units end and sevens elsewhere. Throughout, all conditions refer
to that same actual `3<=i<L`:

```
S=7L-4, P=25*7^(L-2), F=7*10^L-18*10^i-25=9n,
PS|n  iff  225*S*7^(L-2)|F.
```

Retain `5∤S` and the complete sum condition **`9S|F`**, even when three
divides S. At a possible witness, PR #26 forces the seven-free part
`q0` of `n/(PS)` above `L^35`; PR #25 forces
`|bi-aL|>K^2` for every reduced `0<a<b<=K^2`. Neither supplies an upper
bound contradicting the witness condition in this complement.

The [independent mathematical derivation](MATH_REVIEW.md) proves the
following complete reduction, including shallow depths. Put
`d=ord_S(10)`, `D=lcm(d,6)`. If a joint full-sum and `i=3 mod6` class
exists, let s be its least member at least three. If `s>=L`, there is no
candidate. Otherwise write `i=s+Dh`, `0<=h<=M=floor((L-1-s)/D)`.
Set `c=1+v7(D)`, `G=10^D`, and
`Y=(7*10^L-25)/(18*10^s)`, using the inverse denominator modulo seven
powers. Then:

| Depth | Exact period in h | Compatibility | Bounded candidate test |
|---|---|---|---|
| `m<=c` | 1 | `Y=1 mod7^m` | Every h in `[0,M]` if compatible |
| `m>c` | `Q_m=7^(m-c)` | `Y=1 mod7^c` | Least solution `h_m<=M` |

At compatible depths, all solutions are `h=h_m mod Q_m`. One has
`c<=K` and `D*Q_K=lcm(D,T_K)>L`. Consequently an actual sum-compatible
`r_K` supplies compatibility at every later unrestricted depth and is
the sole bounded candidate there until it escapes. Increasing the period
does not force the representative to increase.

**The first missing implication is `h_(L-2)>M` at every remaining actual
sum-compatible `r_K`.** Equivalently, a nonzero lift digit must occur at
some index in the inclusive interval **`[K,L-3]`**. A first change at
`L-2` gives exact `t=L-2`, which already meets the full witness threshold
on this eligible sum-compatible domain. No arithmetic bound forcing that
change has been proved here. No new cutoff is asserted; the unrestricted
outstanding range is every admissible odd `L>=1,000,002,000,001`, after
applying the inherited position and quotient exclusions and the isolated
length exclusions recorded here.

## Power-of-three family

For `S=3^a`, integrality is `a=1 mod6`. Above B the exponents start at 31.
For admissible `a>=7`, elementary lifting gives

```
d=3^(a-2), D=2*3^(a-2), D-L=(5*3^(a-2)-4)/7>0.
```

Recover the exponent from the original sum equation
`10^i=(7R_L-2)/2 mod3^a`, where `R_L=(10^L-1)/9`.
To use F, first work modulo `3^(a+2)` and divide the integer residue by
nine; cancellation modulo `3^a` is invalid. The target is `1 mod27`, so
its log class modulo d is divisible by three. Exactly one of its two
lifts modulo D is odd, yielding s with `s=3 mod6`. Thus s either misses
`[3,L)` or is the unique actual candidate. In the latter case `M=0`,
`c=1`, and the desired infinite-family theorem is exactly
`h_(L-2)!=0`. Uniqueness alone contributes no valuation deadline.

The recurrence is valid at the precision required by the complete sum:

```
L_(a+6)-L_a=104*3^a,
10^L_(a+6)=10^L_a mod3^(a+2),
s_(a+6)=s_a+k_a*D_a, 0<=k_a<=728.
```

All 128 consecutive links from `a=25` through `a=793` are freshly
checked. If two consecutive actual positions both survive depth at least
three, the seven-adic spacing lemma requires `v7(k_a)=1`. This is a
restriction on two survivors, not a bound on one exception. No theorem
that even limits the infinite family to one exception is established;
if such a theorem were found, that exception would still need its own
bound or certificate.

The inherited positive digit-sum control is independently recovered:
`a=25`, `L=121041229921`, `i=40582608819`, `t=2`. Its original word has
`n mod S=0`, `n mod49=0`, and `n mod343=294`. The prior consecutive
coverage already excludes all admissible pure-power lengths through
`a=25`; the new work exhausts the next 128 admissible exponents through
793. The first unchecked exponent in this specified sequence is **799**.
The infinite family remains open.

## Arithmetic, controls, and reproduction

Both programs use only Python's standard library. They import no shared
arithmetic implementation. The primary evaluates F at full precision and
uses the proven class recurrence, checking each of six new ternary digits
by modular exponentiation. The independent program reconstructs n by
binary decimal-block concatenation and solves each length from scratch
by a tracked-power ternary lift. Thus it never needs to expand a giant
word or cancel nine. Each receipt binds its own source.

Each of the 128 case rows certifies either a class miss or the unique
actual position, its exact t, and the first nonzero original-word residue
modulo `7^(t+1)`. Preceding powers pass. Any unclosed depth search raises
an error; a resource guard cannot become an exclusion certificate.
Any future putative witness would require independent original-word,
digit-product, digit-sum and full `PS|n` certification at the same pair.
There is no putative witness in these receipts.

Each checker tests **25,440 literal words** through length 321, calculating
their actual digit sums and products and the original divisibility test.
There are positive digit-sum controls, including three-divisible sums.
The residual-position factor-nine negative `(L,i)=(313,51)` has
`S=2187`, `F mod S=0`, but `F mod9S=17496` and `n mod S=1944`.
This catches the false acceptance caused by losing the factor nine.
The primary also tests all subgroup-membership residues in its declared
small-depth controls, including compatible and incompatible shallow
cases. Both programs check both sides of the lift deadline; those
synthetic targets are explicitly labelled **abstract controls**, not
claimed decimal witnesses or actual sum-compatible `r_K` survivors.

From the repository root:

```sh
sp=research/a398769/five-seven/sum-position-escape
python3 "$sp/primary.py" > /tmp/sum-position-primary.json
python3 -O "$sp/primary.py" > /tmp/sum-position-primary-O.json
cmp /tmp/sum-position-primary.json /tmp/sum-position-primary-O.json
cmp /tmp/sum-position-primary.json "$sp/primary.json"
python3 "$sp/independent.py" > /tmp/sum-position-independent.json
python3 -O "$sp/independent.py" > /tmp/sum-position-independent-O.json
cmp /tmp/sum-position-independent.json /tmp/sum-position-independent-O.json
cmp /tmp/sum-position-independent.json "$sp/independent.json"
python3 "$sp/verify.py"
python3 -O "$sp/verify.py"
```

The verifier binds the inherited inputs and current proof/receipt sources,
compares all 128 rows and controls across implementations, and reruns both
programs in both modes. [REVIEW.md](REVIEW.md) records independent review
and its exact revision bindings. [INHERITED.md](INHERITED.md) distinguishes
fresh receipt checks from historical large enumerations.

## Baseline and scope

Starting main is **`9d958f86fc81188de68af97909614e23a186df9f`**, exactly
the requested PR #26 merge, with no later commits at the initial fetch.
[baseline-inputs.json](baseline-inputs.json) binds the inherited sources;
publication-time main is recorded in the review. Work is isolated on
`research/a398769-sum-position-escape`, for an unmerged draft PR.

Consecutive whole-length exclusion remains **1–1,000,002,000,000
inclusive**. The earlier missing trillion archive was recovered and
verified in merged PR #22; its evidence is now in this repository. The
new 128 isolated lengths do not increase that endpoint. Neither the
infinite `S=3^a` family nor the unrestricted `{5,7}` subclass is settled.
The wider A398769 digit-1 conjecture also remains open. These are ordinary
proofs and independently checked finite computations; **no new Lean
formalization or Lean build was performed**.
