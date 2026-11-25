# The opposite line `12i-5L=+1`

**Verdict: PASS.** The proposed congruence is exhaustive, its least
permitted length is correct, and every admissible position on this line
satisfies `v_7(F)<L-2`. Combining it with the inherited minus-line theorem
proves `|12i-5L|>=3` for every full witness. This is a position exclusion,
not an exclusion of all positions at the corresponding lengths.

## Exact parametrization and domain

Retain odd `L>=5`, `3<=i<L`, `S=7L-4`, and
`F=7*10^L-18*10^i-25`. The full-witness condition is exactly
`225*S*7^(L-2)|F`. In particular a full witness needs `v_7(F)>=L-2`.
The separate digit-sum condition is `9S|F`; statement (E), on `5` not
dividing `S`, asks for the sharper implication
`9S|F => v_7(F)<K(L)`. None of these three tests is identified with another.

Reducing `12i-5L=1` modulo twelve gives `L=7 (mod12)`, since five is its
own inverse modulo twelve. Substitution gives precisely

```
L=12u+7,  i=5u+3,  S=84u+45,  u>=0.
```

Indeed `L>=5` requires the integer `u>=0`; conversely such `u` gives
odd `L>=7`, `i>=3`, and `L-i=7u+4>0`. There is no parity filter on `i`
in this parametrization. Direct substitution gives

```
F/25 = R(10^u),
R(X)=2800000*X^12-720*X^5-1.
```

The factor twenty-five is a seven-adic unit.

## Two unseeded exact routes and their exhaustiveness

[opposite.py](opposite.py) contains two independent mathematical routes.
Neither receives the submitted representative, the other route's root,
or any retained lift as input. Submitted constants are checked only after
both routes have finished their discovery.

The first route tests the original expression for `F` at every exponent
class modulo six, starting with `0,1,2,3,4,5`. It discovers the order of ten
modulo seven by trying exponents one through six. At every new modulus it
discovers the new order among one through seven multiples of the old
order. This list is complete: reduction forces the new order to be a
multiple of the old order, and the binomial theorem makes seven times
the old order a period at the next depth. All observed growth factors
are seven. If `T_k=6*7^(k-1)`, the original expression is periodic in `u`
modulo `T_k`; every possible lift of a retained class is
`u+j*T_k`, `0<=j<7`. A solution at the next depth must reduce to a
retained class. Testing all these lifts, retaining all zero residues,
is therefore exhaustive by induction. Each depth has exactly one class.

The second route evaluates `R` at all seven residues modulo seven.
Here `R(X)=X^5-1 (mod7)`: zero fails, and the fifth-power map is an
automorphism on the group of order six. Thus its sole root is one.
Its derivative is

```
R'(X)=33600000*X^11-3600*X^4,  R'(1)=5 (mod7).
```

It is simple; testing all seven lifts of every retained root therefore
gives the complete root set at every successive power of seven. Every
higher root reduces to an earlier root, and Hensel's simple-root lemma
also proves that this unique branch continues. The program checks every
lift and rechecks the nonzero derivative.

The powers of ten modulo seven are `[1,3,2,6,4,5]`, and
`v_7(10^6-1)=1`. Odd-prime lifting of the exponent gives
`v_7(10^(6a)-1)=1+v_7(a)` for positive `a`. Any exponent giving one
modulo seven is divisible by six, so the exact order is
`ord_(7^k)(10)=6*7^(k-1)`. It equals the number of units, so ten
generates every unit. The root route additionally verifies that the
final claimed order is a period and that division by any of its distinct
prime factors `2,3,7` fails to give a period. These tests certify the
exact order, rather than merely an upper bound.

The final root's exponent is then recovered by exhaustive baby-step/
giant-step, independently of exponent lifting. With width `41169`,
every integer `0<=u<1694851494` is uniquely `u=a*41169+b`,
`0<=b<41169`; all `41169` necessary blocks are visited. The routine
retains all matches lying below the period. It finds exactly one.

| Depth `k` | Exact order `T_k` | Sole exponent class | Sole polynomial root |
| ---: | ---: | ---: | ---: |
| 1 | 6 | 0 | 1 |
| 2 | 42 | 24 | 29 |
| 3 | 294 | 192 | 78 |
| 4 | 2058 | 486 | 1793 |
| 5 | 14406 | 8718 | 8996 |
| 6 | 100842 | 66342 | 25803 |
| 7 | 705894 | 570552 | 614048 |
| 8 | 4941258 | 1982340 | 3908220 |
| 9 | 34588806 | 1982340 | 26967424 |
| 10 | 242121642 | 71159952 | 269089066 |
| 11 | 1694851494 | 313281594 | 1963940560 |

Consequently, for every integer `u>=0`,

```
7^11 | F(12u+7,5u+3)
  iff u=313281594 (mod1694851494).
```

Here `7^11=1977326743`. The representative is in `[0,T_11)`, and
subtracting one period makes it negative. Since the allowed domain
starts at zero, the least permitted length is exactly

```
12*313281594+7 = 3759379135,
i=1566407973.
```

This is a necessary-modulus survivor. It has exact valuation eleven:
`F mod7^12=11863960458=6*7^11`, so it is far below its full-witness
threshold. No enormous decimal integer is constructed for this check.

## Small case and combination with the merged strip

The case `u=0`, namely `(L,i)=(7,3)`, must be separated before applying a
depth-eleven necessary condition: its full threshold is only `L-2=5`.
Direct calculation gives

```
F=69981975,  F mod49=28,  v_7(F)=1<5=L-2.
```

Here `S=45` and `F mod(9S)=0`; passing the digit-sum condition does
not make this a full witness. Since `5|S`, this case is outside the
stated domain of (E). The valuation alone excludes the position.
For `u>=1`, `L>=19` and `L-2>=17>11`.
For `L<10^9`, the computed least length is larger than `10^9`, so
`7^11` fails to divide `F`, giving `v_7(F)<11<L-2`.

For `L>=10^9`, this line satisfies
`|12i-5L|=1<=L/10^9`, so the merged
[five-twelfths strip proof](../strip-audit/PROOF.md) gives
`v_7(F)<L-2`. That inherited proof establishes this valuation bound
at every admissible position in the closed strip, without assuming
either a Fermat congruence or `9S|F`; its conclusion is stronger than
merely a full-witness rejection. The split has no gap and includes the
equality boundary. Although `10^9` is even and not an admissible length,
the same non-strict strip comparison is valid at the boundary.

Hence every admissible position on `12i-5L=+1` satisfies
`v_7(F)<L-2`. The inherited minus-line theorem proves the same statement
on `12i-5L=-1`. Since `12i-5L` is an odd integer for odd `L`, its absolute
value cannot be zero or two; excluding both values of absolute value one
therefore gives the unconditional necessary condition

```
full witness => |12i-5L|>=3.
```

This is a new all-length position exclusion on the plus line. It adds no
whole-length exclusion or consecutive interval and proves no all-length
instance of (E) on this line merely from `v_7(F)<L-2`. Inherited broad
(E) coverage remains the odd lengths `5..9999999`; consecutive
whole-length full-witness exclusion remains `1..10000000`. The
all-length `{5,7}` subclass and the wider digit-1 conjecture remain open.

## Reproduction and controls

From the repository root:

```sh
python3 research/a398769/five-seven/three-deductions-audit/opposite.py > /tmp/a398769-opposite.json
python3 -O research/a398769/five-seven/three-deductions-audit/opposite.py > /tmp/a398769-opposite-O.json
cmp /tmp/a398769-opposite.json /tmp/a398769-opposite-O.json
cmp /tmp/a398769-opposite.json research/a398769/five-seven/three-deductions-audit/opposite.json
```

Both modes pass with byte-identical output. The committed
[machine-readable receipt](opposite.json) includes the source SHA-256,
every lift candidate and residue in both routes, the independent
discrete logarithm, and exact controls. Essential checks use explicit
exceptions and survive `-O`. Three intentionally false controls are
rejected. Direct integer substitution checks the polynomial and line
identities at every `u=0..30`. Positive controls include exact depths one
and eleven; adding a full period passes, while adding one to the final
exponent fails with residue `852820607`. Perturbing the final root by one
fails with residue `334898112`. These controls do not replace the
exhaustiveness proof or the all-length analytic strip theorem.
