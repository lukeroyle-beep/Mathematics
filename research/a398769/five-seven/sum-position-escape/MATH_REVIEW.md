# Independent mathematical review

Reviewer: a separate mathematical agent, independently deriving the arithmetic
from the decimal word and the five requested repository notes. Base main:
`9d958f86fc81188de68af97909614e23a186df9f` (PR #26 merge).
This review establishes the reductions below. It does not claim an all-length
escape theorem, an effective cutoff, or a witness. The code review at the end
records a repaired control-coverage issue separately from the mathematics.

## Exact bounded class, including shallow seven-adic depths

For the literal word with fives at units positions 0 and i,

```
n = 7(10^L-1)/9 - 2 - 2*10^i,
S = 7L-4,
P = 25*7^(L-2),
F = 9n = 7*10^L-18*10^i-25.
```

Thus `PS|n` is equivalent to `225*S*7^(L-2)|F`, without a coprimality
assumption. Since `v5(F)=2` for `i>=3`, `5|S` excludes a witness.
For odd L with `5∤S`, the integer S is coprime to ten. Suppose one
position passes the full sum condition. Subtracting **n**, not an
improperly reduced F congruence, shows that another position differs from
it by a multiple of `d=ord_S(10)`: `S|2*10^min(i,j)*(10^|i-j|-1)`.
More explicitly, with `R_L=(10^L-1)/9`, the original sum equation is
`10^i=C_L=(7R_L-2)/2 mod S`, where only two is inverted. A full-sum
class exists exactly when C_L belongs to the cyclic subgroup generated
by ten. If its discrete log is rho modulo d, joint compatibility with
`i=3 mod6` is exactly `rho=3 mod gcd(d,6)`, by the elementary CRT.
On compatibility the joint class is unique modulo `D=lcm(d,6)`.
Let s be its least member at least three.
If `s>=L` the whole length is excluded. Otherwise all actual candidates
are `i=s+Dh`, `0<=h<=M=floor((L-1-s)/D)`.

Put `e=v7(D)`, `c=e+1`, `G=10^D`, and regard

```
Y = (7*10^L-25)/(18*10^s)
```

as a seven-adic unit. Every use of division in a modulus `7^m` is by
the inverse of the denominator, which is a unit. The numerator is
`-25 mod7`, also a unit. Since `6|D` and `v7(10^6-1)=1`, elementary
binomial lifting gives `v7(G-1)=c`. The exact order of G modulo `7^m`
is therefore

```
Q_m = 7^max(0,m-c).
```

The image and compatibility conditions are as follows.

* If `m<=c`, G is one modulo `7^m`. Compatibility is exactly
  `Y=1 mod7^m`, and every integer h works. The exponent period is one.
* If `m>c`, the powers of G form precisely the subgroup of units
  congruent to one modulo `7^c`. Inclusion follows from `G=1 mod7^c`;
  equality follows because this subgroup and the cyclic group generated
  by G both have order `7^(m-c)`. Compatibility is exactly
  `Y=1 mod7^c`. On compatibility there is one exponent class modulo
  `Q_m`.

In every compatible case write its least nonnegative representative as
`h_m`, with `0<=h_m<Q_m`. An actual candidate at depth m exists exactly
when `h_m<=M`; its full set of h values is
`h_m+Q_m*z` in `[0,M]`. This last comparison is indispensable.

For `m>=c`, the compatible lifts have the explicit form

```
h_(m+1) = h_m + beta_m*Q_m,  0<=beta_m<=6,
u = (G-1)/7^c mod7 != 0,
beta_m = u^(-1) * ((Y*G^(-h_m)-1)/7^m) mod7.
```

Here the displayed seven-adic quotient is an integer at compatible
h_m; only its residue modulo seven is needed. Also
`u=D/(6*7^e) mod7`, since `(10^6-1)/7=1 mod7`.
The formula follows by expanding `G^Q_m=1+u*7^m mod7^(m+1)`.
It gives nondecreasing representatives, but permits arbitrarily many
zero beta digits unless further arithmetic of this particular Y is used.
This is a limitation of the deduction, not an assertion that such zero
runs are realized by actual decimal words.

## Why compatibility cannot settle the deadline after K

The inherited bound `e<=K-1` applies equally to d and D because adjoining
the factor six does not change the seven-adic valuation. For completeness,
if `e>=1` then some prime p dividing S has `7^e|(p-1)`, since `7∤S`.
The smallest possibility `p=1+2*7^e` is divisible by three and larger
than three. Thus `p>=1+4*7^e`; the odd cofactor `S/p` is `3 mod7`
and hence at least three. This gives
`L>=1+12*7^(e-1)=1+2*T_e`, so `e<K`.

It follows that `c<=K`. At depth K a compatible class has

```
D*Q_K = lcm(D,T_K) >= T_K > L.
```

Thus it has at most one actual position. An actual sum-compatible r_K
supplies that position, so it already supplies compatibility modulo
`7^c`. All subsequent unrestricted h congruences remain compatible.
Their increasing periods establish uniqueness, not absence.

The exact still-missing bound is

```
h_(L-2) > M
```

for every remaining L with an actual compatible r_K, equivalently a
nonzero lift digit of r at an index `K<=j<=L-3`. If the first change is
at `j=L-2`, then `t=L-2` and the original full predicate already holds,
provided `5∤S` and `9S|F` at that same position. The upper endpoint
cannot be increased by one. Neither extracting `9S` nor the lower bound
`q0>L^35` supplies the required lower bound on h's least representative.
The rational-centre exclusion must also be retained as a necessary
restriction on any proposed witness; it does not cover its complement.

## The family S=3^a

The condition that `L_a=(3^a+4)/7` is an integer is `a=1 mod6`.
For such `a>=7`, L is odd and S is five-free. The last exponent below
B is a=25 and the first above B is a=31, as direct integer comparison
shows. Elementary lifting at three gives

```
ord_(3^a)(10) = 3^(a-2),
d_a = 3^(a-2),
D_a = 2*3^(a-2) > L_a.
```

The last inequality is exactly `5*3^(a-2)>4`, so it holds for every
admissible `a>=7`. The powers of ten modulo `3^a` are exactly the
units congruent to one modulo nine.

Recover the sum class using the original word:

```
R = (10^L-1)/9 mod3^a,
C = (7R-2)/2 mod3^a,
10^i = C mod3^a.
```

Compute R by first computing `10^L mod3^(a+2)` and then dividing the
integer residue minus one by nine. Two is inverted modulo `3^a`.
This retains the full factor nine in `F=9n` and is valid even though
three divides S. It must not be replaced by solving `F=0 mod3^a`.

Because `L=16 mod27`, the expansion
`R=L+9*L*(L-1)/2 mod27` gives `R=16 mod27`, hence `C=1 mod27`.
There is therefore one exponent class modulo d_a, and it is divisible
by three. Since d_a is odd, exactly one of its two lifts modulo D_a
is odd. Let s_a be that odd lift in `[0,D_a)`. It is `3 mod6`, hence
at least three. It is the sole possible actual position when `s_a<L_a`;
if `s_a>=L_a` the entire length is excluded. The strict upper endpoint
is essential. A unique position still needs the seven-power test.

Here `v7(D_a)=0`, so `c=1` and `Q_m=7^(m-1)`. Every depth remains
compatible for unrestricted h, because `s_a=3 mod6` ensures `Y=1 mod7`.
When s_a is actual, `M=0`. Thus the desired conclusion reduces to
`h_(L_a-2)!=0`, exactly the claim that the one actual position has
`t<=L_a-3`. The fact that D_a exceeds L_a does not prove this claim.

## Successive powers of three and the individual-exception problem

The exact difference is

```
L_(a+6)-L_a = 104*3^a.
```

The order of ten modulo `3^(a+2)` is `3^a`, which divides this
difference. Consequently the two powers of ten agree modulo
`3^(a+2)`, the R values agree modulo `3^a`, and the C values agree
modulo `3^a`. The exponent classes agree modulo d_a. Both chosen lifts
are odd, so they also agree modulo D_a. Precisely,

```
s_(a+6)=s_a+k_a*D_a,  0<=k_a<=728,
D_(a+6)=729*D_a.
```

This gives a compatible three-adic sequence of position classes. It
provides no bound for the seven-adic valuation of the sole actual
position at any one length. It does not guarantee that the next class
has an actual representative either.

The inherited pairwise seven-adic spacing lemma can constrain two
surviving positions. Here `v7(L_(a+6)-L_a)=0` and both lengths are
`1 mod6`. If both actual positions survive modulo `7^m`, with `m>=3`,
subtracting their F congruences forces
`v7(s_(a+6)-s_a)=1`, hence `v7(k_a)=1`. In particular the zero k case
cannot occur for two such survivors. This only restricts pairs; it
neither supplies a surviving neighbour nor excludes an isolated survivor.
No claim that at most one member of the infinite family survives has
been proved here. Even such a claim would require a separate bound or
certificate to control that individual exception.

## Independent spot checks and scope

A fresh direct modular computation, derived without importing a repository
checker, recovered the inherited positive control

```
a=25, L=121041229921, s=40582608819, t=2.
```

The full digit sum passes and the third power of seven fails. Fresh
checks also give `(a,s,t)=(31,45794167518741,1)` and
`(37,20223125112794343,1)`. For a=43, the least joint sum-position
representative is `61358897416486435125`, exceeding
`L=46893852484933868233`, so that class misses the actual interval.
These checks do not stand in for the independently implemented complete
128-case receipt; that receipt is reviewed separately.

The derivations above are ordinary mathematics. No Lean theorem or Lean
build was performed by this reviewer. They leave the unrestricted family,
the infinite S=3^a subfamily, and the wider A398769 question open.

## Arithmetic implementation review

The reviewer inspected both `primary.py` and `independent.py`. They import no
shared arithmetic implementation. The primary uses F modulo nine times
the requested modulus and searches the three possibilities for each newly
needed ternary digit. It recovers a=25 from scratch and each following class
by six further ternary digits, checking reduction of the new target first.
The independent checker reconstructs n by decimal-block concatenation and
recovers every exponent from scratch using tracked powers and a nonzero
ternary coefficient. Both use explicit exceptions, not removable assertions.

One review finding was repaired: the primary's initial literal-word range
ended at L=101 and contained no factor-nine negative control, so its own
nonvacuity check would fail. The range was extended through L=321, with
`i=3 mod6` required for the negative. This recovers L=313, i=51, S=2187:
`F modS=0`, `F mod9S=17496`, and `n modS=1944`. It detects the exact
loss-of-nine error on a position satisfying the seven-adic depth-one filter.
The revised code was reread; no unresolved arithmetic findings remained.

The reviewer also independently executed the primary's general class and
deadline controls: two actual small sum classes, ten bounded comparisons,
78,408 subgroup membership checks, and six synthetic lift examples on both
sides of the deadline passed. The synthetic examples are explicitly not
claimed to be original decimal-word witnesses. They test the first-change
index, including the fact that changing at L-2 is too late for exclusion.
The independent receipt's 86 actual positions have valuation histogram
`{1:76, 2:8, 3:2}`; the other 42 classes miss the interval. All actual
positions have t<K. Accordingly these computations do not produce an
actual sum-compatible r_K survivor, nor directly refute or prove the
universal deadline assertion. Final source and receipt bindings are in
the task's verification receipt.
