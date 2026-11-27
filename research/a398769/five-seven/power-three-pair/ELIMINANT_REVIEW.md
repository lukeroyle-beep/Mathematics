# Independent eliminant and modular audit

Reviewer context: `/root/eliminant_review`. Base commit:
`42e6a151c5279905a3e02b859c6fae737178fd7d`.
The inherited four `power-three` entry notes were read. This review derives
the elimination and complete shallow tests separately and imports no project
arithmetic. It does not establish the logarithm bound by itself.

## Exact predicate, positions and increment endpoints

Let `a=31+6u`, `u>=0`, `d=3^(a-2)`, `L=(9d+4)/7`, and let primes denote
the member at `a+6`. The original word is

```
n=7(1+10+...+10^(L-1))-2-2*10^s,
F(L,s)=9n=7*10^L-18*10^s-25,
S=3^a, P=25*7^(L-2).
```

Therefore `PS|n` is **equivalent** to `225*S*7^(L-2)|F`. In particular
`9S|F` must be retained at the same actual position `3<=s<L`. On that
domain `v5(F)=2`, so passing the sum condition and `v7(F)>=L-2` suffices;
equality at the threshold is not an exclusion.

The inherited sum-class theorem gives the unique joint representative in
`[0,2d)`, congruent to `3 mod6`. One can check the needed transition without
using an inherited numerical representative. Exact subtraction gives

```
L'-L=(729-1)*9d/7=936d,
v3(L'-L)=a.
```

Since `ord_(3^(a+2))(10)=3^a`, the length terms agree modulo `3^(a+2)`.
Subtracting the two full sum conditions and dividing by 18 implies
`10^s'=10^s mod3^a`. Thus `s'=s mod d`; both positions are odd from
`7|F`, so `s'-s=2dk` for an integer k. As `0<s<L<2d` and `s'>0`,
negative k is impossible. Also

```
L'=(6561d+4)/7 < 938d
```

because `5d>4`. From `2dk=s'-s<L'` we get `k<469`, hence **every actual
pair has `0<=k<=468`**, including both endpoints in the necessary superset.
No restriction to projected transitions realized by a candidate is used.

## Complete depth-three calculation

Put `U_u=7*10^L-25`, `G_u=10^(2d)`. A pair surviving depth three requires
`U_u*G_u^k=U_(u+1) mod343`. There are exactly seven u classes to test.
Indeed, `q=729` satisfies `v7(q^7-1)=2`; for a shift of seven in u,
`L_(u+7)-L_u` is divisible by `6*7`, and `2d_(u+7)-2d_u` is divisible
by `6*49`. Since `ord_49(10)=42` and `ord_343(10)=294`, the leading
factor seven in U makes both U and G periodic with period seven modulo
343. These order statements follow from `ord_7(10)=6` and
`v7(10^6-1)=1`. This period argument covers every nonnegative u,
including the last-to-first transition; minimality is not required.

The independent checker computes actual integer d and L at each of the
seven representatives and tests **every** k in `[0,468]`, 3,283 tests:

| u mod7 | U mod343 | U' mod343 | G mod343 |
|---|---:|---:|---:|
| 0 | 192 | 290 | 323 |
| 1 | 290 | 45 | 127 |
| 2 | 45 | 143 | 274 |
| 3 | 143 | 241 | 78 |
| 4 | 241 | 339 | 225 |
| 5 | 339 | 94 | 29 |
| 6 | 94 | 192 | 176 |

For **every** row the surviving k values are exactly

```
42, 91, 140, 189, 238, 287, 336, 385, 434.
```

Thus `k=42 mod49` is necessary, and intersecting with the proved actual
bounds leaves exactly these nine possibilities. This is a complete finite
test, not a sample of u or of possible increments. The checker also checks
the next complete period as an arithmetic consistency check; the algebraic
period proof supplies the universal scope.

## Elimination, sign and divisibility scope

Since `d=3^(29+6u)=5 mod7`, write `d=7w+5`. Also `d=3 mod6`; reducing
`7w+5=d` modulo six proves **`w=4 mod6`**. Here w is a positive integer.
Substitution gives

```
L=9w+7,
L'=6561w+4687,
2dk=(14w+10)k.
```

With `x=10^w`, direct cancellation of the two `18*10^s'` terms proves

```
F(L',s')-10^(2dk)*F(L,s)=H_k(x),
H_k(X)=7*10^4687*X^6561-25
       -10^(10k)*X^(14k)*(7*10^7*X^9-25).
```

This is an identity for any integer s with `s'=s+2dk`. There is no
assumption that the identity-test positions used by the checker pass the
sum test. The positivity can be proved for the entire larger interval
`0<=k<=468`, without a numerical evaluation:

```
H_k(10^w)
 =7*10^(L+2dk)*(10^(2d(468-k))-1)+25*(10^(2dk)-1)>0.
```

Both summands are nonnegative. For `k<468` the first is positive; for
`k=468` the second is positive. In particular the polynomial value never
vanishes on the actual domain. For the nine retained k its degree is
exactly 6561 because `14k+9<6561`.

If **both** lengths have full witnesses, each F term is divisible by
`7^(L-2)`: the second length has the still larger threshold `L'-2`.
Therefore `7^(L-2)|H_k(10^w)` is necessary for a full pair. An isolated
witness gives no such conclusion, because its neighbour's F need not
have this divisibility. This is the precise scope of the eliminant.

## Complete derivative test

The value of `10^w mod343` has period 294. Exactly 49 of these residue
classes have `w=4 mod6`: they are `4,10,...,292`. For each of the nine k,
the independent program evaluates the expanded polynomial at x and x+343
modulo `343^2`, then performs the exact division

```
((H_k(x+343)-H_k(x)) mod343^2)/343 mod343.
```

The binomial theorem identifies this residue with `H'_k(x) mod343`:
all second and higher difference terms contain `343^2`. This does not
reuse a derivative evaluator. All **441** results equal **49**, hence

```
v7(H'_k(10^w))=2
```

for every eligible w and all nine k. The program records every pair,
not merely a count or minimum. Periodicity and the proved residue
restriction make this complete. The test actually holds on a superset
of the w produced by powers of three.

## Reproduction and review scope

From the repository root:

```sh
pp=research/a398769/five-seven/power-three-pair
python3 "$pp/independent_modular.py" > /tmp/pair-modular.json
python3 -O "$pp/independent_modular.py" > /tmp/pair-modular-O.json
cmp /tmp/pair-modular.json /tmp/pair-modular-O.json
python3 "$pp/independent_modular.py" --check "$pp/independent-modular.json"
python3 -O "$pp/independent_modular.py" --check "$pp/independent-modular.json"
```

Both normal and optimized executions produced identical receipts. The
program uses explicit exceptions; optimization does not remove checks.
It additionally checks the identity independently at all nine k and
14 admissible exponents, over six moduli (756 comparisons). Those checks
support implementation correctness; the displayed cancellation proves
the exact identity. Source hashes bind the checker and all four inherited
entry notes. No Lean formalization or Lean build is performed here.

## Independent review of the analytic proof

After authoring the separate modular implementation, this reviewer read the
root agent's `PAIR.md` and the other specialist's `LOGARITHMS.md`, including
their complete changed-file context. Neither analytic proof was authored by
this reviewer. No unresolved mathematical finding was identified.

The reviewed mathematical files have these SHA-256 bindings:

```
PAIR.md        6eb9cc9e64a79820778cdc95654e1b83af3913f676292724adc585cd7939c0cb
LOGARITHMS.md  44a062d3b832f178f4bb043da42fa3137052cf1c06fd1961254e92bb7f3cda68
```

The reviewer separately reopened Bugeaud--Laurent's primary PDF, checking
the definitions on printed pages 2--4 and Corollary 2 on page 5. The stated
208 bound, actual degree parameter, height floors and b-prime denominators
match the source. Its application to the sixth powers has principal units,
positive exponents and multiplicative independence in the independent case.

The rescaling `H(x+343Y)/7^5` is an integral polynomial with unit linear
coefficient and all higher coefficients divisible by seven. Its simple
Hensel root has distance valuation at least three; Taylor expansion then
forces the exact loss two. The sixth-power cofactor is a unit, so no
valuation is lost there. The minimal-polynomial/Mahler-measure argument
bounds absolute logarithmic height without requiring H to be monic or
irreducible.

In the dependent case the unique-minimum argument at a place above two
proves the stated negative valuation interval. Dependence makes
`alpha^e/10^r` torsion in Q_7, giving the sixth-power identity; the positive
integer `ew-r` prevents vanishing. Lifting the exponent gives the exact
formula `q+v7(e)=1+v7(ew-r)`. Thus this case does not quietly invoke the
independent logarithm theorem.

Independent integer arithmetic reproduced
`C=1618798436980968297600000`, `C+2<10^30`, and the positive crossover
numerator gap
`515377520731910531036461129765621272702107521991` at a=100.
The induction polynomial is `2a^2+78a+759`, positive for a>=0.
Both proofs consistently compare with the smaller threshold, and the
finite exclusions include the crossing start a=97. They make no universal
individual inference when both exterior neighbours fail.

The reviewer also inspected `pair_checks.py` and `individual_check.py`:
the former's independent recurrence and dual-number derivative are correct;
the latter's ternary generator and all-three-lift checks preserve the full
sum class, and the original decimal-block readback retains the factor nine.
`logarithm_checks.py` was rerun against its bound receipt normally and under
`python3 -O`; outputs were byte-identical, including the nine nonzero
strong-Hensel controls. This is mathematical and computational review,
not Lean verification.
