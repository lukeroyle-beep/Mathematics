# Complete position searches in an enlarged digit-sum family

The new family is

```
c = 898129, D = 56133 = 3^6*7*11,
a = 193+210t, t >= 0,
S = c*3^a, L = (S+4)/7.
```

This enlarges the inherited `a=193+1470t` family. Every length is odd,
exceeds `10^12`, and has `5` not dividing S. For every such length,
all positions with `3 <= i < L` passing the **full** `9S | F` condition
are one residue class modulo `W=77*3^(a-2)`. The search does not select
just the position in the inherited `(0.41L,0.42L)` interval: it covers
**every** position satisfying the full digit-sum condition at each of
its explicitly listed lengths.

## Why the 210 progression works

At `a=193`, direct integer checks give `L mod D=11248`. Since

```
7D = 3^6*539, 3^210 = 1 mod 539,
```

and `a>=193`, the increment in `c*3^a` after increasing a by 210 is
divisible by `7D`. Thus L remains an integer and its residue modulo D
is unchanged. Its numerator is odd, so L is odd. Also `c` is coprime
to 3, 5, and 7.

The order of ten modulo c is exactly D: `10^D=1 mod c`, while
`10^(D/p) != 1 mod c` for `p=3,7,11`. The fixed relation

```
7*10^11248 - 18*10^11337 - 25 = 0 mod c
```

then proves `c | F` if and only if `i=11337 mod D`. No assumption that
c is prime is needed: uniqueness of the exponent class follows from
its exact order and the existence of the displayed solution.

Write `A=(7*10^L-25)/9`, which is an integer. Because `F/9=A-2*10^i`,
the three-part of the full digit sum is

```
3^(a+2) | F  iff  10^i = A/2 mod 3^a.
```

The notation `A/2 mod 3^a` means multiplication by the inverse of 2;
division by 9 occurred in the integers first. By the elementary
identity `v3(10^m-1)=2+v3(m)`, ten generates exactly the subgroup
of units congruent to 1 modulo 9, and has order `3^(a-2)` modulo
`3^a`. Here `L=4687 mod 6561` and

```
7*10^4687 - 18*10^402 - 25 = 0 mod 3^10.
```

Consequently the target is in that subgroup and its unique exponent
class `r3 mod 3^(a-2)` satisfies `r3=402 mod729`. Since
`11337=402 mod729`, generalized CRT combines the two necessary and
sufficient classes into one class `r mod W`, with

```
W = lcm(D,3^(a-2)) = 77*3^(a-2).
```

The c part and three part are coprime. The combined congruence is
therefore exactly `9S | F`, including all powers of 3 in the extra
factor nine. This is an ordinary proof, not a Lean formalization.

The number of actual positions in `[3,L)` is either 14996 or 14997:

```
L/W = 9c/539 + 4/(7W),
14996 < 9c/539 < 14997.
```

The receipt gives the exact count, first position, least residue and
spacing separately at each searched length.

## Seven-adic lifts and exact completeness

At depth k, the primitive-root order `T_k=6*7^(k-1)` gives a unique
seven-adic exponent `r7 mod T_k`. At k=1 it is 3 modulo 6. The script
tests all seven possible next representatives, checks uniqueness, and
combines the resulting class with `r mod W` by generalized CRT.
For this family the common divisor of W and `T_k` is 3 at k=1 and
21 for k>=2; the classes agree. Indeed L is 1 modulo 6, so its
depth-two exponent is 39 modulo42 and `11337=39 mod21`.

Each row records the least combined residue, combined spacing, and
number of members of `[3,L)`. The survivor sets are nested. The count
at depth k minus the count at depth k+1 is therefore the exact number
of positions having valuation k. The search stops at the first empty
set. At that point all actual digit-sum-compatible positions are
rejected, without needing to visit each enormous position separately.
The receipt also includes **every** position at the greatest surviving
depth and its nonzero residue modulo the next power of seven.

The accelerated three-adic logarithm doubles precision using
`(1+3^m*c)^d = 1+3^m*c*d mod 3^(2m)`. Every doubled step is checked by
exact modular exponentiation. Small tests compare this method with
separate three-way digit lifting and known nonzero logarithms.

## Fresh result

The full normal run covered `t=0,...,31`, or `a=193,403,...,6703`.
All **479894** actual digit-sum-compatible positions were rejected.
The greatest valuation was eight, achieved at `t=13,24,26`. At those
lengths `K=1657,2961,3198` respectively, so these are shallow failures.
The 32 lengths have `116 <= K <= 3791`; zero pairs pass depth K.

| Exact `v7(F)` | Number of positions |
| ---: | ---: |
| 0 | 239950 |
| 1 | 0 |
| 2 | 205666 |
| 3 | 29382 |
| 4 | 4198 |
| 5 | 597 |
| 6 | 85 |
| 7 | 13 |
| 8 | 3 |

For the three depth-eight pairs the respective residues modulo `7^9`
are `11529602=2*7^8`, `23059204=4*7^8`, and `5764801=7^8`.
Their exact positions are retained in `results.json`, along with all
64 deepest positions across the 32 lengths. All 64 were freshly
checked against the full `9S` modulus and the next seven-power modulus.
The receipt contains one self-contained case record per t; individual
cases can be reproduced with equal `--first-t` and `--last-t` values.

The normal full run and optimized two-case prefix `t=0,1` were freshly
executed. The optimized prefix rows match the corresponding full-run
rows exactly. A full optimized 32-case rerun was **not** executed.
`validation.json` records those exact scopes and byte identities.

## Reproduction and scope

From the repository root:

```sh
python3 research/a398769/five-seven/trillion-witness/families/search_families.py --first-t 0 --last-t 31 > /tmp/families.json
cmp /tmp/families.json research/a398769/five-seven/trillion-witness/families/results.json
# Optional full optimized rerun (not part of the fresh checks recorded here):
python3 -O research/a398769/five-seven/trillion-witness/families/search_families.py --first-t 0 --last-t 31 > /tmp/families-O.json
cmp /tmp/families.json /tmp/families-O.json
# The optimized prefix actually run:
python3 -O research/a398769/five-seven/trillion-witness/families/search_families.py --first-t 0 --last-t 1 > /tmp/families-prefix-O.json
```

These are 32 selected lengths, with `a=193,403,...,6703`, and complete
position coverage at each length. They do **not** cover the lengths
between them. The source hash binds the receipt to the executed code;
that hash is provenance, not a certificate of omitted valuations.

The construction is an infinite theorem about digit-sum compatibility.
The rejection search is finite in t. No theorem here forces a failed
lift for all t, or for arbitrary remaining digit-sum-compatible lengths.
The common-divisor constraints stabilize at depth two; thereafter CRT
compatibility persists, while the actual representative may leave the
interval `[3,L)`. This stabilization does not force it to leave at a
uniform depth. A full witness would require an actual position to remain
fixed through all lift digits K through L-3. The new finite search
finds none even at K and does not discharge that infinite obligation.
