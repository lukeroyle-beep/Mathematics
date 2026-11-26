# The remaining quotient and lift obstruction

The new five-adic theorem excludes small seven-free quotients uniformly in
the position. It does not close the unrestricted `{5,7}` subclass. This
note isolates what remains after that theorem and PR #25. All statements
about a witness retain the full divisor at one and the same actual `(L,i)`.

Write `B=1,000,002,000,000`, `epsilon=1/10^9`, and, for a hypothetical
full witness with `L>B`,

```
S=7L-4, F=7*10^L-18*10^i-25,
t=v7(F), A=9S*q0, F=25*A*7^t.
```

The new theorem gives `ln A>epsilon*L`. Since `t>=L-2` and
`F<7*10^L`, the exact elementary upper bound is

```
A < (343/25)*(10/7)^L.
```

Consequently the still-allowed logarithmic interval has width

```
ln(343/25) + (ln(10/7)-epsilon)*L.
```

The coefficient lies strictly between `356674942/10^9` and
`356674943/10^9`. At the first remaining length `L=B+1`, this width
is greater than `356675656291`. These comparisons use rational series
enclosures in [obstruction_checks.py](obstruction_checks.py), not rounded
floating-point constants. The upper exponential slope is more than
356 million times the lower slope. An interval of this size does not
establish that any quotient in it comes from the required decimal word;
it only records that the two proven size bounds do not contradict.

The same calculation bounds the actual valuation by

```
t < c*L + ln(7/25)/ln7,
c=(ln10-epsilon)/ln7,
1183294661/10^9 < c < 1183294662/10^9.
```

In particular `c>1`: a permitted run of zero lift digits can still
extend about `0.18329466*L` past the required witness threshold. The
new height estimate therefore does not force a lift change by `L-3`.

## What the position and digit sum currently supply

PR #25 forces the strict complement

```
|bi-aL| > K(L)^2
for every reduced 0<a<b<=K(L)^2,
K(L)=min{k>=1:6*7^(k-1)>L}.
```

This condition constrains the exponent i. The exact magnitude remains
`F=7*10^L-18*10^i-25`. Even the inherited stronger leading-end condition
`L-i>L/25000` makes the relative subtraction satisfy

```
0 < (18*10^i+25)/(7*10^L)
  < (18/7)*10^(-L/25000)+(25/7)*10^(-L).
```

Thus replacing `F<7*10^L` by its actual position-dependent value changes
the upper bound's small multiplicative correction; these magnitude
estimates do not reduce its exponential slope to `epsilon`. No argument
has been obtained here that turns the rational-centre complement into
the missing upper bound on A or q0.

The exact digit sum gives `A=9S*q0`, with `5` and `7` not dividing A,
including all factors of three in `9S`. Multiplicity and congruence
restrictions of this kind alone do not bound q0 above. In particular,
dividing by `9S` removes a factor whose logarithm is less than `ln(63L)`;
it does not remove the positive linear-in-L height interval above.
This is a limitation of the inequalities established here, not a claim
that the full digit-sum equation could never imply a stronger theorem.

There are concrete actual pairs satisfying the complete digit-sum test
and the centre complement. The two examples already recorded in
[fixed-depth/checks.json](../fixed-depth/checks.json) were freshly
verified from their decimal runs:

| Inherited S | K | Exact t | Nearest centre | Full non-seven divisor | Centre complement |
|---|---:|---:|---|---|---|
| `3^164*17^41` | 152 | 4 | `4927/11738` | `25S|n`, equivalently `225S|F` | Every `b<=23104` checked |
| `3^103*898129^21` | 206 | 7 | `5899/14279` | `25S|n`, equivalently `225S|F` | Every `b<=42436` checked |

The exact L, i, distances and modular residues are in
[obstruction-checks.json](obstruction-checks.json). Both S are divisible
by three. An independent modular concatenation of seven and five runs
checks n directly and agrees with F at nine times the modulus. No
enormous decimal integer is materialized. All denominators are checked;
nearest-integer enumeration suffices because, for fixed b, the nearest
numerator minimizes `|bi-aL|`. A global positive minimum is reduced,
since reducing a pair would otherwise decrease its distance. At zero
distance the least-denominator tie is reduced.

**Both examples have `t<K`. They are not actual `r_K` survivors and
are not witnesses.** They demonstrate compatibility of the full sum
test with the centre complement. They do not test, prove, or refute a
universal deadline for sum-compatible positions already surviving K.
The inherited [fixed-depth theorem](../fixed-depth/PROOF.md) also allows
arbitrarily large fixed valuations in each fixed open ratio interval,
but fixes the depth before allowing L to grow. It cannot be specialized
by setting that depth to `L-2`.

## Exact lift deadline

For completeness, the inherited argument in
[explicit-length/ROUTE2.md](../explicit-length/ROUTE2.md) gives the
following precise closing target. Put `T_j=6*7^(j-1)`. Since
`ord_(7^j)(10)=T_j`, there is a unique representative `0<=r_j<T_j`
with

```
18*10^r_j = 7*10^L-25 mod 7^j.
```

For a full witness `i=r_K`, because `t>=L-2>=K` and `i<L<T_K`.
The lift has the form

```
r_(j+1)=r_j+a_j*T_j,  0<=a_j<=6,
a_j=5*(F(L,r_j)/7^j) mod7.
```

Indeed `10^T_j=1+7^j mod7^(j+1)` and `18*10^r_j=3 mod7`.
For `j>=K`, a nonzero a_j takes the representative beyond L, and
later representatives never decrease. As long as the representative
is constant at the actual i, a_j is zero exactly when
`7^(j+1)|F(L,i)`. Thus the first nonzero a_j is indexed by
`j=t=v7(F(L,i))`. Positivity of F ensures eventual change but gives
no adequate deadline by itself.

On the eligible domain `5∤S` and `9S|F`, `v5(F)=2` implies that
`H=F/(225S)` is an integer and `v7(H)=t`. During the constant portion,

```
a_j = H/7^j mod7,
```

since `225S=3 mod7` and `5*3=1 mod7`. Extracting the complete sum
factor preserves the trailing seven-adic zeros. It does not shorten
their run. Therefore the exact witness equivalence is

```
full witness  iff  a_K=a_(K+1)=...=a_(L-3)=0
```

at a sum-compatible actual `r_K`. The first nonzero digit at **L-2**
would already be too late to exclude a witness.

A later contradiction from the gcd in the exponent CRT is also
unavailable from the inherited order argument alone. Let
`o=ord_S(10)` and `e=v7(o)`. Any two sum-compatible actual positions
are congruent modulo o, by subtracting their original n values and
inverting two modulo odd S. If `e>=1`, some prime p dividing S has
`7^e|(p-1)`; since p is odd, and `1+2*7^e` is a multiple of three,
`p>=4*7^e+1`. Also `S/p` is a positive odd integer congruent to
three modulo seven, so is at least three. Hence

```
L>=12*7^(e-1)+1=2*T_e+1,
e<=K-1.
```

It follows that `gcd(o,T_j)=gcd(o,6)*7^e` is constant for `j>=K`.
The representatives r_j reduce to r_K modulo T_K, so sum compatibility
at K keeps the unbounded exponent congruences compatible at every
later depth. Their least common representative need not remain below
L. Bounding that representative, or forcing a nonzero lift digit before
the deadline, is precisely the unresolved step.

The first missing implication remains a proof, for **every** remaining
actual `r_K` outside the certified centres with `5∤S` and `9S|F`, that
some `a_j` is nonzero for `K<=j<=L-3`; alternatively one needs an
effective cutoff and complete checking of its finite remainder. The
new quotient theorem supplies neither for arbitrary q0. No witness,
new whole-length interval, or new Lean formalization is claimed.

## Reproduction and evidence boundary

From the repository root:

```sh
fq=research/a398769/five-seven/five-adic-quotient
python3 "$fq/obstruction_checks.py" > /tmp/five-adic-obstruction.json
python3 -O "$fq/obstruction_checks.py" > /tmp/five-adic-obstruction-O.json
cmp /tmp/five-adic-obstruction.json /tmp/five-adic-obstruction-O.json
cmp /tmp/five-adic-obstruction.json "$fq/obstruction-checks.json"
```

Both modes were freshly run and agree byte for byte. The checker uses
explicit exceptions, so optimization does not remove checks. It includes
12,096 literal decimal modular comparisons, 2,970 nearest-centre checks
against full reduced-numerator enumeration, an inclusive band boundary,
a strict outside case and a zero-distance reduction control. It imports
no prior arithmetic implementation. Input and checker hashes bind the
receipt. The two input pairs and the general order/lift results are
inherited; the decimal modular evaluations, complete centre-complement
checks and rational gap enclosures here are fresh.
