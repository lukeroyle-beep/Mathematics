# Three successive admissible lengths cannot all survive depth nine

For every integer `u>=0`, among the three lengths with exponents
`a=31+6u`, `a+6`, and `a+12`, at least one has **no actual full-sum-compatible
position** satisfying `7^9 | F`. Consequently at least one of those three
lengths has no full witness. The proposed fallback is confirmed.

This is an ordinary proof plus two independent exact finite computations.
It is not a Lean theorem. The theorem neither excludes an isolated witness
nor proves that an individual remaining member fails the full divisor.

## Exact domain and necessary transitions

Write

```
L_a=(3^a+4)/7, d_a=3^(a-2), D_a=2d_a,
F(L,i)=7*10^L-18*10^i-25=9n,
S=3^a, P=25*7^(L-2).
```

All exponents in this note are `a=31+6u`, `u>=0`. The exact original test is
`PS|n`, equivalently `225*S*7^(L-2)|F`. In particular the full sum test is
`9S|F`, not merely `S|F`. Already `7|F` forces
`10^i=-1 mod7`, hence `i=3 mod6`; thus every depth-nine position
is in the joint class used below.

The inherited sum-class argument is used in its precise form: there is one
joint representative `s_a` in `[0,D_a)`, congruent to `3 mod6`, passing
`9S|F`; because `D_a>L_a`, it is the sole actual position if `s_a<L_a`.
If `s_a>=L_a`, the length is already excluded. The least joint
representative is at least three. The exact successive relation is

```
s_(a+6)=s_a+D_a*k_a, 0<=k_a<=728, D_(a+6)=729D_a.
```

Indeed the length difference is `104*3^a`, so the powers of ten agree
modulo `3^(a+2)`, which preserves the complete sum test after exact division
by nine. The logarithm classes agree modulo `d_a`; both chosen representatives
are odd, so they agree modulo `D_a`. The bounds on both representatives give
the displayed bounds on `k_a`.

Set `U_u=7*10^L_a-25` and `G_u=10^D_a`. If both adjacent actual positions
survive depth `m`, then

```
U_u = 18*10^s_a (mod 7^m),
U_(u+1) = 18*10^(s_a+D_a*k_a) = U_u*G_u^k_a (mod 7^m).
```

Thus three actual survivors require **both** equations

```
U_u*G_u^k = U_(u+1) (mod 7^m),
U_(u+1)*G_(u+1)^j = U_(u+2) (mod 7^m)
```

for some independently allowed `k,j` in the entire inclusive interval
`[0,728]`. The finite tests below impose no condition that these increments
are realized by the three-adic position sequence. They test a necessary
superset. A successful projected test does not establish an actual position.

## Period proof

Put `q=729=3^6`. One has `q-1=728=7*104`, hence `v7(q-1)=1`.
The binomial lifting identity gives, for every positive integer `R`,

```
v7(q^R-1)=1+v7(R).
```

For `R=R_m=7^(m-2)` and `m>=2`,

```
L_(u+R)-L_u = 3^(31+6u)*(q^R-1)/7,
D_(u+R)-D_u = 2*3^(29+6u)*(q^R-1).
```

Their seven-adic valuations are respectively `m-2` and `m-1`.
Both differences are divisible by six: they have a factor three, and
`q^R-1` is even, with division by the odd integer seven preserving evenness.
Since `ord_(7^h)(10)=6*7^(h-1)` for `h>=1`, the first difference gives

```
10^L_(u+R)=10^L_u (mod 7^(m-1)),
U_(u+R)=U_u (mod 7^m),
```

where the leading factor seven is essential. The second difference gives
`G_(u+R)=G_u (mod 7^m)`. Therefore **the pair `(U_u,G_u)` has the valid
period `R_m`** modulo `7^m`. Minimality is neither asserted nor needed.
This holds for every `u>=0`, so reducing every start and its two successors
modulo `R_m`, including wraparound, is valid.

The order of ten used here follows from `ord_7(10)=6` and
`v7(10^6-1)=1`, followed by the same binomial lifting identity.
As `6|D_a` and `7` does not divide `D_a`, the order of `G_u` modulo
`7^m` is `7^(m-1)`. For `m>=5` this exceeds 728, so each projected edge
has at most one increment in the requested range.

## Independent exhaustive computations

The implementations share no arithmetic code and do not seed the pilot
counts. They agree on every surviving start and both increment lists.

| m | Complete period `0<=u<R_m` | Starts with one transition | Starts with both transitions |
|---|---:|---:|---:|
| 5 | 343 | 105 | 35 |
| 6 | 2,401 | 105 | 14 |
| 7 | 16,807 | 105 | 14 |
| 8 | 117,649 | 105 | 7 |
| 9 | 823,543 | 105 | **0** |

1. [`transitions.py`](transitions.py) visits **every** `u` in each displayed
   period, computing `L_(u+1)=729L_u-416` and `D_(u+1)=729D_u` modulo
   `6*7^(m-1)`. It first completely enumerates all 729 increments at each
   of the seven depth-three residues. Those computations leave exactly
   `k=42+49r`, `0<=r<=14`, at every depth-three residue. It checks **all**
   these necessary candidates directly modulo `7^m` at every visited start;
   it does not restrict starts using survivors from a previous reported
   depth. It compares the entire depth-five edge stream with an unfiltered
   729-increment computation. Consecutive passing edges, including the
   last-to-first pair, give the displayed starts. Every recorded survivor
   is independently rechecked by unfiltered enumeration in the same program.
2. [`transitions_independent.py`](transitions_independent.py) begins at
   depth two with its complete period and all increments `0..728`, then
   lifts every retained start to all seven residues in the next period.
   It evaluates each lifted start from independently reduced powers of
   three, divides the length numerator by seven exactly, and retests all
   729 increments at each candidate start. A survivor at a higher depth must
   reduce to one at the previous depth, so this lifting loses none.

The direct run visits `960,743` starts across the five reported periods.
Its ordered complete edge streams, including empty edges, have retained
SHA-256 digests. Both receipts retain every surviving start and both
increment lists; the primary receipt also binds the four inherited entry
notes and its own source. The independent receipt binds its source.
Both programs use explicit failures rather than removable assertions.

The depth-eight positive control is retained and verified without assuming
that it is an actual position:

```
u=14984, k=189, j=42, modulus=7^8=5764801,
(U_u,U_(u+1),U_(u+2))=(4532643,1079760,627098),
(G_u,G_(u+1))=(5422712,3001965).
```

Both congruence residuals are zero. In fact all seven depth-eight starts are
`14984+16807r`, `0<=r<=6`, with these same two increments. All 49 lifts
of those starts to the depth-nine period fail the two-transition test.
The direct full-period enumeration confirms that there are no omitted
starts elsewhere in that period. The empty result proves the theorem for
every `u>=0` by periodicity and necessity of the two transitions.

## Scope and reproduction

A full witness above the stated bound necessarily survives depth nine,
since `L_a-2>=9`. Therefore no three consecutive admissible family members
can all be full witnesses. The theorem still permits an isolated full
witness, two consecutive full witnesses, or any sequence without a run of
three. It does not force the neighbours of a hypothetical witness to
survive, and it does not bound the valuation of that one witness.
The 105 surviving individual projected edges at depth nine do not prove
any pair of actual survivors either.

The theorem excludes infinitely many lengths but does not identify the
failing member of every triple from its index alone. It does not extend
consecutive whole-length coverage or settle the unrestricted `{5,7}` or
wider digit-1 conjectures. No witness, individual effective cutoff, or
Lean verification is inferred from these computations.

From the repository root:

```sh
pt=research/a398769/five-seven/power-three
python3 "$pt/transitions.py" > /tmp/power-three-transitions.json
python3 -O "$pt/transitions.py" > /tmp/power-three-transitions-O.json
cmp /tmp/power-three-transitions.json /tmp/power-three-transitions-O.json
cmp /tmp/power-three-transitions.json "$pt/transitions.json"
python3 "$pt/transitions_independent.py" > /tmp/power-three-independent.json
python3 -O "$pt/transitions_independent.py" > /tmp/power-three-independent-O.json
cmp /tmp/power-three-independent.json /tmp/power-three-independent-O.json
cmp /tmp/power-three-independent.json "$pt/transitions-independent.json"
python3 - <<'PY'
import json
from pathlib import Path
p = Path('research/a398769/five-seven/power-three')
a = json.loads((p/'transitions.json').read_text())
b = json.loads((p/'transitions-independent.json').read_text())
for row in a['levels']:
    other = next(x for x in b['levels'] if x['m'] == row['m'])
    if row['period'] != other['period'] or row['starts'] != other['starts']:
        raise RuntimeError('Transition disagreement at depth ' + str(row['m']))
print('PASS: every depth-five through depth-nine start and increment agrees')
PY
```

The normal and optimized primary runs produced byte-identical retained
receipts; the independent implementation reports the same result and its
own normal/optimized equality. No inherited large enumeration or Lean
build is part of these transition runs.
