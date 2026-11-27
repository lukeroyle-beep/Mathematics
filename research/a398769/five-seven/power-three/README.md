# Power-of-three members and the three-length obstruction

**Among every three successive admissible exponents above B, at least one
length has no actual full-sum-compatible position surviving `7^9`.** Two
independent exact methods confirm the proposed counts **35, 14, 14, 7, 0**
at depths five through nine. The infinite individual-family assertion
`v7(F(L_a,s_a))<=L_a-3` remains **open**: no counterexample or effective
exponent cutoff was obtained.

The individual computation now excludes all **256 specified lengths**
`L_a=(3^a+4)/7`, `a=31+6u`, `0<=u<256`, ending at **a=1561**. This adds
128 lengths starting at the previously unchecked **a=799**. These are
isolated lengths, not an interval between their endpoints. The next
unchecked exponent in this sequence is **1567**.

## Exact predicate and results

For the decimal word with fives at positions 0 and i and sevens elsewhere,

```
S=7L-4, P=25*7^(L-2), F=7*10^L-18*10^i-25=9n,
PS|n iff 225*S*7^(L-2)|F.
```

The digit-sum condition is always **9S|F** at the same actual position
`3<=i<L`. In this family S is five-free, and `v5(F)=2`; an actual
sum-compatible position with valuation exactly `L-2` is already a full
witness. Every recorded exclusion fails modulo a seven power at depth
at most `L-2`.

The [single-member analysis](INDIVIDUAL.md) verifies the unique root
`theta in 1+9 Z_3`, `theta^7=10^4`, and proves **exactly**
`v3(10^L_a-theta)=a+2`. For `C=(7theta-25)/18`, the logarithms are defined,
`v3(C-1)=3`, and `kappa=log(C)/log(10)` satisfies `kappa=6 mod9`.
The joint position is the unique odd lift of `kappa mod3^(a-2)` to
`[0,2*3^(a-2))`. This is a complete description of the integer candidate,
but supplies no seven-adic escape deadline.

One explicit joint inequality for every actual sum candidate, with
`t=v7(F)`, is

```
(a+2) ln3 + t ln7 + ln25 < L_a ln10 + ln7.
```

Its coefficient `ln10/ln7` on L is greater than one. The additional
algebraic-norm and explicit three-adic logarithm estimates in the analysis
do not make it less than one or bound a. The first missing individual
inference is a uniform bound forcing a nonzero seven-adic residue by
depth `L_a-2` for every actual candidate; the one-variable three-adic
description and the theorem about three lengths do not imply it.

The [three-length proof](THREE_LENGTH.md) verifies the necessary transitions
`U_u G_u^k=U_(u+1)` and `U_(u+1) G_(u+1)^j=U_(u+2)` modulo `7^m`,
allowing **all** increments `0<=k,j<=728`. It proves the valid period
`R_m=7^(m-2)` for the pair `(U_u,G_u)`, including wraparound.

| m | Period | Starts allowing both transitions |
|---|---:|---:|
| 5 | 343 | 35 |
| 6 | 2,401 | 14 |
| 7 | 16,807 | 14 |
| 8 | 117,649 | 7 |
| 9 | 823,543 | **0** |

The nonzero control `m=8,u=14984,k=189,j=42` passes both congruences.
At depth eight all starts are `14984+16807r`, `0<=r<=6`; every one of
their 49 lifts fails at depth nine. Direct enumeration of every start in
the full periods agrees with residue-class lifting on every retained
start and increment. This proves the three-length statement for **all
u>=0**, without assuming that projected increments are actually realized.
It permits an isolated witness, and even two adjacent witnesses: a witness
does not force its neighbours to survive.

## Individual computations and original words

The primary computation uses a single high-precision Newton root and
modular logarithm to obtain kappa, then truncates it for each exponent.
It checks precision stability and the exact three-adic error at every row.
The independent adapter reuses the separately derived original-word
decimal-block implementation from PR #27, hash-bound to the current
baseline, and solves **each of the 256 classes from scratch** by ternary
lifting. It imports no primary arithmetic. This reuse is explicit; it is
not represented as a newly authored third independent engine.

| Range of u | Exponents | Class misses | Actual positions | Exact valuation histogram |
|---|---|---:|---:|---|
| 0–127 | 31–793, step 6 | 42 | 86 | `{1:76,2:8,3:2}` |
| 128–255 | 799–1561, step 6 | 42 | 86 | `{1:74,2:10,3:1,4:1}` |
| 0–255 | 31–1561, step 6 | **84** | **172** | `{1:150,2:18,3:3,4:1}` |

Every actual position fails the growing seven-power divisor. The largest
observed valuation is four at a=1231; the depth-three exponents are
97, 757 and 1393. At **a=799** the unique actual position has `t=1`,
and its original word has `n mod49=35`. Full L and s integers are retained
in both receipts. The first length is `88,239,056,611,993`; the final one
is exactly `(3^1561+4)/7`. No length outside this stated sequence is newly
certified by this individual enumeration.

The inherited positive control is independently recovered:
`a=25, L=121041229921, i=40582608819`, with full digit sum passing,
`n mod49=0`, and `n mod343=294` (exact valuation two). The negative control
`(L,i)=(313,51)` has `S=2187`, `F modS=0`, but `F mod9S=17496`
and `n modS=1944`; it detects dropping the factor nine. The independent
checker also reruns all **25,440** literal-word controls from PR #27,
calculating digits, product, sum and the exact original `PS|n` predicate.
For giant actual words, binary decimal-block concatenation checks sum and
nonzero residues without expanding the word or cancelling nine.
No putative witness was found, so no full-witness certificate is claimed.

## Baseline, inherited evidence, and reproduction

Starting main is **0a47180b889b392c2323bc1614a473af51f38d78**, exactly
the requested PR #27 merge. Its ancestry was checked after `git fetch
origin main`; no later main commits were present. Work is isolated on
`research/a398769-power-three-audit`. [baseline.json](baseline.json)
binds all **1,028** inherited tracked files. The new root README entry is
the only modification of an inherited file; all research inputs remain
byte-identical. Publication-time main and exact review bindings are recorded
in [REVIEW.md](REVIEW.md).

PR #27's aggregate verifier was rerun normally and under `python3 -O`:
all 128 inherited rows, recurrence links, six corrupted-receipt controls,
and 706 earlier input bindings pass. The recovered trillion archive in
merged PR #22 and the adjacent interval from PR #21 are inherited evidence;
their large enumerations were **not** rerun. The earlier memory-era archive
gap was repaired in PR #22 and is not a current repository gap.

All programs use standard-library Python and explicit exceptions, so
optimized execution does not disable checks. From the repository root:

```sh
pt=research/a398769/five-seven/power-three
python3 "$pt/verify.py" --run
python3 -O "$pt/verify.py" --run
python3 "$pt/review_checks.py" --check "$pt/review-checks.json"
python3 -O "$pt/review_checks.py" --check "$pt/review-checks.json"
git diff --check
```

The verifier reruns each of the four arithmetic programs in the invoking
interpreter's optimization mode, compares deterministic outputs byte for
byte, checks both complete result sets, rejects deliberately corrupted
receipts, and verifies source/proof/baseline bindings. Without `--run` it
checks retained receipts and their bindings only. [verification.json](verification.json)
records the exact reproducible scope. Direct individual commands are
`python3 "$pt/individuals.py"`, `python3 "$pt/individuals_independent.py"`,
`python3 "$pt/transitions.py"`, and `python3 "$pt/transitions_independent.py"`;
adding `-O` must reproduce their corresponding JSON files exactly.

## Separate verdicts and first missing inferences

| Target | Verdict | First missing inference |
|---|---|---|
| Every individual `S=3^a` member | **Open**; 256 named lengths excluded | Force `v7(F)<=L_a-3` at each remaining actual s, beginning with unchecked a=1567; no effective global exponent cutoff |
| Three successive admissible family members | **Proved**: at least one fails depth nine | None for this stated theorem; it does not exclude an isolated survivor |
| Consecutive whole-length coverage | **1–1,000,002,000,000 inclusive**, unchanged | Exclude every possible position at the next unproved odd length `1,000,002,000,001` and continue without gaps |
| Unrestricted `{5,7}` subclass | **Open** | Reject the full divisor at every residual actual position outside inherited exclusions, or exhibit a verified witness |
| Wider A398769 digit-1 conjecture | **Open** | Close every remaining no-digit-1 case, including the unresolved `{5,7}` subclass; a subfamily obstruction does not suffice |

The fixed-depth theorem concerns a larger two-prime digit-sum family with
each depth fixed before choosing lengths; it does not assert arbitrary
depth in this pure `3^a` sequence. The inherited qualitative `v7(F)=o(L)`
proves finiteness of full witnesses but provides no effective starting
length or emptiness certificate. See [INDIVIDUAL.md](INDIVIDUAL.md) for
the precise comparison. **No new Lean formalization or Lean build was
performed.** This work comprises ordinary proofs and independently checked
finite arithmetic. The PR is a draft; Luke retains merge control.
