# Structural investigation and independent retained controls

Starting point inspected: main `0c8a8f2dd1c8340cc6fb7c2485ad206cba72bdd7`,
the merge of PR #20. This note supplies no proof of absence above a
trillion digits and no full witness. Its new elementary family-count
observation makes a finite family search cheaper; it does not turn
spacing into an exclusion.

## Evidence boundary

Targeted filename searches, including hidden files, under the Mathematics
workspace and `~/Downloads` found neither
`A398769-Trillion-Length-Investigation.md` nor
`A398769-Trillion-Length-Evidence.zip`. No attachment was supplied as a
readable resource in this task. Consequently no controls from that archive
were inspected, and its large finite computations were not reproduced.
This is a statement about those locations and available resources, not
proof that the files do not exist elsewhere.

The user's reported complete exclusion through `L=10^12` inclusive and
reported broad-(E) coverage through odd `L=1,694,851,493` are retained as
**reported, not freshly certified here**. They are different claims.
The inspected main and merged PR #20 themselves retain only the older
consecutive exclusion through 10,000,000 and broad (E) through odd
9,999,999; PR #20 adds no whole-length coverage. No later main update
was present at the initial fetch. Neither older large search was rerun
by this note. New search ranges are stated elsewhere in this directory.

## Exact target and why the available structural routes stop

The merged [two-five reduction](../README.md) starts from the original
digit condition and excludes every other count of fives. With the units
position numbered zero, the remaining number is the decimal word

```
7^(L-i-1 copies) 5 7^(i-1 copies) 5,
```

where superscripts in this display are run lengths, not powers. Its
digit sum is `S=7L-4`, product `P=25*7^(L-2)`, and nine times its
value is `F=7*10^L-18*10^i-25`. The suffix 775 has valuation exactly
two at five. Since `S=3 mod7`, excluding `5|S` leaves the exact joint
requirements `9S|F` and `v7(F)>=L-2`. In particular the nine is not
cancelled from a congruence modulo S.

The exact order `T_j=6*7^(j-1)` makes the least exponent representative
`r_j` unique. At `K=min{j:T_j>L}`, every full witness must use the
single actual position `i=r_K` in `[3,L)`. It must also satisfy the
full-sum test at that same position. If it does, write

```
r_(j+1)=r_j+a_j*T_j,   0<=a_j<=6.
```

Every nonzero digit for `j>=K` moves the representative permanently
above L. The outstanding obligation is to force one nonzero digit in
the exact interval **K through L-3 inclusive**. A first nonzero digit
at index t means exact valuation t; index `L-2` is too late to reject
a witness. The defining formula can compute individual digits but
does not furnish a uniform upper bound on the first nonzero index.

Three apparent closing arguments were checked against the merged
[lift analysis](../uniform-bound/LIFTS.md) and
[analytic analysis](../uniform-bound/ANALYTIC.md):

1. If full-sum exponents exist, they form one class modulo
   `d=ord_S(10)`. With `e=v7(d)`, the proved inequality `e<=K-1`
   makes `gcd(d,T_j)` constant for every `j>=K`. Thus unbounded
   exponent CRT compatibility, once present at K, persists at every
   higher depth. It cannot later contradict itself. The missing fact
   is a bound on the actual representative, not another CRT check.
2. Extracting the sum yields the integer `C=F/(225S)` when the sum
   test passes. Its valuation at seven is still `v7(F)`, since
   `7` does not divide `225S`. PR #20's exact size comparison proves
   `F>225S*7^(L-2)` for every L>=12 and actual i, so positive size
   permits the full witness threshold. No extra cancellation or
   forced nonzero base-seven digit follows merely from this division.
3. PR #20 bounds derivatives in its polynomial-root parameterization
   uniformly and excludes multiplicatively dependent selected roots.
   Its remaining independent-root bound depends on the actual root
   degree and height. Taking the rational centre `i/L` eliminates
   the offset but can give denominator L; that is not a uniform
   height/degree solution. No theorem controlling those parameters
   for every sum-compatible `r_K` was found here. The repository's
   qualitative finiteness result supplies no executable last length.

These are limitations of those particular arguments, not a theorem
that no structural argument can exist. This investigation found no
new global reason that forces a failed lift on the entire remaining
full-sum-compatible domain. Neither broad (E) nor the weaker witness
exclusion is assumed for pruning.

## A useful exact count for the inherited sum-compatible family

The merged [family proof](../depth/FAMILY.md) gives

```
c=898129, d=56133=3^6*7*11,
a=193+1470t, t>=0,
S=c*3^a, L=(S+4)/7.
```

It constructs full-sum positions at depth four, including positions
in the open interval `(41L/100,42L/100)`. It does not assert that its
chosen position is the only position passing the sum.

For these parameters, the condition modulo `3^a` gives one exponent
class modulo `3^(a-2)`. The condition modulo c gives one class modulo
d. At seven-adic depth k there is one class modulo T_k. When these
three classes are compatible, all their common exponents form one
class modulo their least common multiple. For k>=2 this is exactly

```
W_k=lcm(3^(a-2),d,T_k)=22*7^(k-1)*3^(a-2).
L/W_k=(9c+4/3^(a-2))/(154*7^(k-1)).
```

If compatibility fails, there are zero positions. Otherwise a single
class has at most `ceil(L/W_k)` members in `[3,L)`. Since `a>=193`,
the ratio is strictly less than `(9c+1)/(154*7^(k-1))`. Exact integer
comparisons therefore give the following bounds for **every** t>=0:

| Required seven-adic depth | At most this many actual full-sum positions |
| ---: | ---: |
| 4 | 154 |
| 5 | 22 |
| 6 | 4 |
| 7 | 1 |

These counts concern every actual sum-compatible position, not just
the position chosen in the published middle interval. They justify
enumerating the full class at depth four and lifting all its actual
members, or obtaining the unique possible actual member by depth
seven. A failed tested member must not be substituted for the other
members at earlier depths.

The bound one at depth seven means **at most one**, not zero. Increasing
a makes both L and the exponent period scale by the same factor
`3^(a-2)`; it does not improve the limiting ratio at a fixed depth.
The least representative still depends on a. Thus this family count
does not prove rejection for all t, and does not turn any finite tested
parameter range into an infinite theorem of absence.

There is also a precise reason that increasing a introduces a new
arithmetic question rather than a free extra digit-sum parameter. The
three-adic exponent class is universal for lengths of the form
`L=(c*3^a+4)/7`, not specific to the chosen c. Here is a finite
congruence proof, avoiding assumptions about infinite digit statistics.
If two such lengths have exponents `a1<=a2`, both lengths are congruent
to `4/7 modulo 3^a1` (division means the inverse of seven). The identity
`v3(10^h-1)=2+v3(h)` shows that their powers of ten agree modulo
`3^(a1+2)`. Dividing their target numerators by nine and multiplying
by the inverse of two leaves targets agreeing modulo `3^a1`.
Consequently their exponent classes agree modulo `3^(a1-2)`.

Thus the unique exponents `r_a mod 3^(a-2)` form nested truncations of
one three-adic integer. Its new digits, and the least representative
after intersection with the seven-adic class, still need to be
controlled. Nesting alone gives no bound on where that representative
lies in `[0,W_k)` relative to L. In particular it proves neither
avoidance of the actual interval nor a uniform eventual failed lift.
The independent family checker verifies all 31 adjacent nesting
relations in the 32 recorded length samples; that finite check is
separate from the elementary general argument above.

## Fresh original-decimal checks

[`archive-audit.py`](archive-audit.py) imports no search or inherited
checker. Its only number inputs are pairs `(L,i)` and the original
four-block digit specification. It independently derives the length,
sum, factored product, and positions of the two fives. It evaluates
each original decimal number modulo affordable moduli using the
concatenation monoid

```
(x,10^a) * (y,10^b) = (x*10^b+y,10^(a+b)) mod M.
```

Binary powering builds runs of repeated sevens without a decimal
string, division by nine, the F formula, or stored discovery residues.
There are 14,700 comparisons with literal small decimal strings.
The following retained main controls were freshly checked; they are
not controls retrieved from the missing archive:

| Control | Original-decimal result |
| --- | --- |
| `(69489,40323)` | exact valuation 11; `n mod S=246527`, hence fails sum |
| Published `a=193` family pair | `n mod S=0` and `25*S*7^4|n`, but exact valuation 4 |
| PR #19 exceptions at depths 44, 56, 85, 92 | exact valuation equals K in each case; every one fails sum |
| `(313,51)`, `S=2187` | `n mod S=1944`; `9n mod S=0` but `9n mod(9S)=17496` |

The last row is a concrete negative control for improperly dropping
the factor nine, and has `i=3 mod6`. All inspected original words
have `n mod125=25`, confirming their exact five valuation. The sum
positive control and all four high-depth negative controls have
lengths above a trillion. They are individual pairs, not whole-length
certificates.

Each exact seven valuation was established by checking original n
at every depth through its first nonzero residue, at most depth 93.
The maximum 92 is a greatest certified **exact depth for these
controls**, not a partial full-witness certificate; each pair is
already definitively rejected by its exhibited failed condition.
No enormous modulus `7^(L-2)` was allocated or required.

Normal Python and `python3 -O` produced byte-identical
[`archive-audit.json`](archive-audit.json). Three deliberate mutations
are rejected by explicit checks, including promotion of the depth-four
positive control to a full witness and omission of the factor nine.
No large exhaustive search or Lean build was run by this checker.

From the repository root:

```sh
python3 research/a398769/five-seven/trillion-witness/archive-audit.py > /tmp/archive-audit.json
python3 -O research/a398769/five-seven/trillion-witness/archive-audit.py > /tmp/archive-audit-O.json
cmp /tmp/archive-audit.json /tmp/archive-audit-O.json
cmp /tmp/archive-audit.json research/a398769/five-seven/trillion-witness/archive-audit.json
```

## Independent complete-class audit of the new family search

[`review-family.py`](review-family.py) independently checks the enlarged
family's 32 samples `a=193+210t`, `0<=t<=31`. Its proof audit confirms
that `3^210=1 mod539` preserves the required length class, that the
exact order modulo c requires no primality assumption, and that
retaining the full three-part gives a necessary and sufficient sum
class, not just a necessary filter.

For each length, this checker evaluates the original four-block
decimal word at the least sum-class representative modulo S. It
checks the exact order from coprime factors to establish that the
recorded class contains **every** full-sum-compatible position. It
then constructs each seven-adic intersection by enumerating the
extensions of the previous joint class, with the decimal word as
its modular predicate. This method uses neither the discovery
logarithm/CRT implementation nor its asserted residues. The class
counts are recomputed by separate floor differences. A further
4,350 small literal-word comparisons check this block evaluator.

The result is complete position exclusion at those **32 isolated
lengths**, with 479,894 full-sum-compatible actual positions rejected:

| Exact valuation at seven | Number of actual positions |
| ---: | ---: |
| 0 | 239,950 |
| 1 | 0 |
| 2 | 205,666 |
| 3 | 29,382 |
| 4 | 4,198 |
| 5 | 597 |
| 6 | 85 |
| 7 | 13 |
| 8 | 3 |

All counts, every least joint class representative, every class period,
and every terminal empty class agree independently. Every rejection
depth is below that length's K, which ranges from 116 to 3791; zero
positions survive to K. The exact sum and seven tests concern the
same positions throughout. The interval between these length samples
is not covered by this audit.

Normal and optimized executions produced byte-identical
[`review-family.json`](review-family.json), including all 31 adjacent
nested three-adic class checks. No discovery code is imported.

```sh
python3 research/a398769/five-seven/trillion-witness/review-family.py > /tmp/review-family.json
python3 -O research/a398769/five-seven/trillion-witness/review-family.py > /tmp/review-family-O.json
cmp /tmp/review-family.json /tmp/review-family-O.json
cmp /tmp/review-family.json research/a398769/five-seven/trillion-witness/review-family.json
```
