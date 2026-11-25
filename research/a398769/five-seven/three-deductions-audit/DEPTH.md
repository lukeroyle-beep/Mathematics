# The first depth-K exception on 12i-5L=-1

**Verdict: verified.** The claimed first exponent is the first admissible
line position with `v_7(F)>=K(L)`, in increasing L. Exactly four positions
pass their own depth test below `T_100=6*7^99`. Their respective depths are
44, 56, 85 and 92, and each has `gcd(F,S)=1`. Consequently (E) holds on
this line for every admissible position with `L<T_100` on its specified
domain `5` not dividing `S`. This is a bounded position theorem, not a
whole-length theorem or an all-length theorem for (E).

## Domain and three separate tests

Use the inherited exact definitions, read in
[early-rejection/README.md](../early-rejection/README.md) and the inherited
[strip proof](../strip-audit/PROOF.md):

```
L odd, L>=5, 3<=i<L,
S=7L-4, F=7*10^L-18*10^i-25,
T_k=6*7^(k-1), K(L)=min{k>=1:T_k>L}.
```

The digit-sum condition is `9S|F`. The depth test is `7^K(L)|F`.
The full-witness condition is exactly `225*S*7^(L-2)|F`. On `5` not
dividing S, statement (E) is the implication
`9S|F => v_7(F)<K(L)`. Neither a depth survivor nor its rejection by
the sum test is a whole-length conclusion.

Solving `12i-5L=-1` gives `L=12u+5`, `i=5u+2`, `S=84u+31`.
The requirement `L>=5` gives `u>=0`; `u=0` is invalid because `i=2`.
Conversely every integer `u>=1` has odd `L>=17`, `i>=7`, and
`L-i=7u+3>0`. We keep both parities of i initially. Substitution proves

```
F=25*P(10^u), P(X)=28000X^12-72X^5-1.
```

The factor 25 is a seven-adic unit. Thus `7^k|F` is equivalent to
`P(10^u)=0 (mod 7^k)`.

## Exhaustive order and polynomial root

Direct evaluation of all six exponent classes modulo six gives the
powers `[1,3,2,6,4,5]` modulo seven. Therefore `ord_7(10)=6`.
Also `10^6-1=7*142857` and `142857=1 (mod 7)`, so odd-prime LTE gives
`v_7(10^(6a)-1)=1+v_7(a)` for every positive integer a. Any exponent
giving one modulo a higher power must first be a multiple of six.
It follows that the exact order modulo `7^k` is `T_k` for every k.
It equals the entire unit-group size, so every unit has precisely one
exponent class modulo `T_k`.

The polynomial route starts by evaluating P at **all seven** residues.
Modulo seven it is `-2X^5-1`. Zero is not a root, and a nonzero X
satisfies `X^5=X^-1`, so its unique root is 5. At that root
`P'(5)=1 (mod 7)`. Simple-root Hensel lifting gives precisely one root
at each higher depth. Any higher root reduces to a lower root; no branch
can appear from an excluded residue. Combined with the full order of ten,
this proves a unique exponent class at every depth, not merely through
the computed depth 100.

## Two independent implementations

[depth_exponents.py](depth_exponents.py) uses only the original F
expression. It starts with all six exponents modulo six. At depth k+1
it tests every `u+d*T_k`, `0<=d<7`, above every surviving exponent.
It independently finds each new order as the least multiple of the old
order, among its first seven multiples, that gives one. Reduction makes
the new order a multiple of the old order; the binomial theorem shows
seven times the old order suffices. The induction therefore enumerates
**every** exponent class, with no submitted representative as a seed.
All tested exponents and original-F residues are retained in the receipt.

[depth_roots.py](depth_roots.py) evaluates all seven initial polynomial
residues and, at each depth, all seven lifts of every retained root.
It then recovers the exponent afresh **from that root alone** by a
truncated seven-adic logarithm. It never imports the first checker,
uses its classes, lifts exponents, or evaluates original F for discovery.
Here is the exact discrete-log argument used by this second route.

Let `a_k` be the polynomial root modulo `M=7^k`. Exhaust all `0<=e<6`
to find `10^e=a_k (mod 7)`, and put `y=a_k*10^-e (mod M)`.
Then y is in the principal units. The full order just proved implies
`y=(10^6)^a (mod M)` for a unique `a (mod 7^(k-1))`. For any principal
unit z, compute

```
log(z) = sum_{n=1}^{2k-1} (-1)^(n+1)*(z-1)^n/n (mod 7^k).
```

Every omitted term is zero modulo `7^k`: its valuation is at least
`n-v_7(n)>=n/2>=k` when `n>=2k`. For n not divisible by seven the
denominator is inverted modulo M. In general write `n=7^b*c`, compute
the numerator modulo `M*7^b`, divide that representative exactly by
`7^b`, and invert c modulo M. Thus no rational denominators are
incorrectly inverted and no precision is lost before division.
Changing a unit representative by a multiple of M does not change its
logarithm modulo M. The usual formal-power-series identity
`log((1+Z)^a)=a*log(1+Z)` proves the corresponding identity for positive
integer a; convergence at `v_7(Z)>=1` makes reduction modulo M valid.
This identity also follows by differentiation and equality of constant
terms, so no transcendental numerical approximation is used here.

Since `v_7(log(10^6))=1` (its first term has valuation one and all
subsequent terms have valuation at least two), division by seven gives
a unit denominator modulo `7^(k-1)`. Hence

```
a = (log(y)/7) * (log(10^6)/7)^-1 (mod 7^(k-1)),
u = e+6a, 0<=u<T_k.
```

The case k=1 needs only e. Each recovered exponent is checked by
`10^u=a_k (mod M)`. At each depth this checker also verifies the exact
order by the period test and rejection of its quotients by 2, 3 and,
for k>=2, 7. The recorded tables agree on all 100 recovered exponent
classes. The second checker calculates `F mod9S` using `25P(10^u)`;
the first uses the original F. Their complete exceptional rows agree.

## Actual-position bands and minimality

For k=1 the condition is `L<T_1=6`; the only odd admissible length
would be L=5, but its line parameter is the invalid u=0. Thus no
admissible position on this line lies in the k=1 band.

For every k>=2, the definition with a **strict** upper cutoff gives

```
K(L)=k iff T_(k-1)<=L<T_k.
```

The lower endpoint belongs to band k, and the upper endpoint belongs
to band k+1. The T values are even, so neither endpoint is an actual
odd length, but the inequalities must still be handled with those
directions. Both exact implementations use them, and the first checks
`K(T_(k-1))=k`, `K(T_k-1)=k`, and `K(T_k)=k+1` through depth 100.

Let `u_k` be the unique least nonnegative exponent representative
modulo `T_k`. Every integer solution at depth k is `u_k+a*T_k`.
For an actual line position within its k band,
`12u+5<T_k`, hence `u<T_k` and `u>=1`. Thus only `a=0` is possible:
`a<0` makes u negative, and `a>=1` makes L greater than the band's
upper endpoint. If `u_k=0`, it is inadmissible and adding a period
cannot restore eligibility within that band. The complete test is
therefore exactly

```
u_k>=1 and T_(k-1)<=12u_k+5<T_k.
```

It is not enough to check just the upper endpoint. The table applies
both endpoints and discovers exactly the four depths listed below.
In particular there are none at depths 1 through 43. At depth 44 the
only eligible representative is the displayed u, and every earlier
admissible L has either a smaller K or a smaller representative in the
same band. Both cases fail the exhaustive depth test. This proves
minimality over **all** earlier admissible positions on this line,
not just over a list of chosen sample exponents.

## Exact exceptional values

The following integers are independently recovered. `R` denotes the
least nonnegative residue `F mod9S`; gcd denotes greatest common divisor.
The JSON receipts contain all these values and the full 100-depth traces.

```
k = K(L) = 44
u = 329630660491118914435920553818196013
L = 3955567925893426973231046645818352161
i = 1648153302455594572179602769090980067
S = 27688975481253988812617326520728465123
R = 220492367892872959611320275821615897912
gcd(F,S) = 1
F mod7^45 = 45860101895827728581295557307830479203 = 3*7^44

k = K(L) = 56
u = 9947547394254831864255026916481853522611100723
L = 119370568731057982371060322997782242271333208681
i = 49737736971274159321275134582409267613055503617
S = 835593981117405876597422260984475695899332460763
R = 6766599739258291813673376749798612223120139953867
gcd(F,S) = 1
F mod7^57 = 3*7^56

k = K(L) = 85
u = 19362934432456610386903430264947376562146511521656744678964245193278409
L = 232355213189479324642841163179368518745758138259880936147570942319340913
i = 96814672162283051934517151324736882810732557608283723394821225966392047
S = 1626486492326355272499888142255579631220306967819166553032996596235386387
R = 12881779930935013054243266666806881518960753192538652081634179239021153557
gcd(F,S) = 1
F mod7^86 = 7^85

k = K(L) = 92
u = 30973508212110618883323762497941117462584226427229689017607955339425136892649
L = 371682098545327426599885149975293409551010717126756268211295464073101642711793
i = 154867541060553094416618812489705587312921132136148445088039776697125684463247
S = 2601774689817291986199196049827053866857075019887293877479068248511711498982547
R = 13675329978772134956853163278653705038321395119698943504984110850274533615577786
gcd(F,S) = 1
F mod7^93 = 7^92
```

In the first case the band endpoints are

```
T_43 = 1871840893707254227807981930931856294
T_44 = 13102886255950779594655873516522994058.
```

They place L strictly inside the correct band. The displayed next-depth
residue proves exact valuation 44, not just a lower bound. The other
next-depth residues likewise show exact valuations 56, 85 and 92.
The four S residues modulo five are respectively 3, 3, 2 and 2,
so all four lie in the domain of (E).

## What follows, and what does not

Every admissible line position with `L<T_100` has `K(L)<=100`.
Except for these four positions, the exhaustive band test proves
`v_7(F)<K(L)` directly. At the four positions, `gcd(F,S)=1` and `S>1`
prove that even `S|F` fails, hence `9S|F` fails. Here the gcd is
computed exactly as `gcd(F mod9S,S)`, which equals `gcd(F,S)`.
Thus the implication (E) is true at **every** position of this line
in the stated range, including these four positions where its antecedent
is false. This proves no assertion for the other positions at the same
lengths, and no assertion at or above the cutoff `T_100`.

The first example refutes the unconditional universal inequality
`v_7(F)<K(L)` on this line (and therefore on all admissible positions).
It does **not** refute (E), which retains its digit-sum hypothesis.
It also does not refute the already merged, much weaker all-length
inequality `v_7(F)<L-2` on this line: here `44<L-2` by a huge margin.
No full witness is produced. The unconditional full-witness exclusion
of the entire line was already established by PR #18.

This advances bounded **line-position (E)** coverage from the inherited
modular consequence `L<2231854769` to `L<6*7^99`, while identifying
exactly where the formerly stronger unconditional depth inequality
first fails. Consecutive whole-length exclusion remains 1 through
10,000,000; broad all-position (E) remains certified at odd lengths
5 through 9,999,999. No extension of either whole-length range is
claimed. All-length (E), the all-length `{5,7}` subclass, and the wider
digit-1 conjecture remain open.

## Reproduction and controls

From the repository root:

```sh
python3 research/a398769/five-seven/three-deductions-audit/depth_exponents.py > /tmp/depth-exponents.json
python3 -O research/a398769/five-seven/three-deductions-audit/depth_exponents.py > /tmp/depth-exponents-O.json
cmp /tmp/depth-exponents.json /tmp/depth-exponents-O.json
cmp /tmp/depth-exponents.json research/a398769/five-seven/three-deductions-audit/depth_exponents.json
python3 research/a398769/five-seven/three-deductions-audit/depth_roots.py > /tmp/depth-roots.json
python3 -O research/a398769/five-seven/three-deductions-audit/depth_roots.py > /tmp/depth-roots-O.json
cmp /tmp/depth-roots.json /tmp/depth-roots-O.json
cmp /tmp/depth-roots.json research/a398769/five-seven/three-deductions-audit/depth_roots.json
```

Both scripts use only standard-library exact integers. Output is
deterministic and contains the source SHA-256. Essential checks raise
exceptions explicitly and remain active with `python3 -O`. The first
route has four intentional negative guard controls, original-F neighbor
and period checks, and a nonzero depth-one control `u=5, F mod49=7`.
The second has independent polynomial controls, 84 logarithm power
controls (including negative powers, zero and seven-divisible powers),
14 logarithm addition controls, and three intentional negative guards.
All these checks pass. They support the algorithms; exhaustiveness
comes from the proofs above, not from sampling.
