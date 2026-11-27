# Individual certificates and the finite pair cutoff

The first previously unchecked exponent **a=1567 is excluded**. Its unique
joint representative is actual, and the original decimal word has
`n mod7=0`, **`n mod49=7`**. Thus `v7(n)=v7(F)=1`, strictly below `L-2`.
No witness was found. The universal individual-family assertion remains open.

## A fresh computation of the same-position class

[`individual_check.py`](individual_check.py) imports no arithmetic from the
primary pair program or any inherited individual program. It builds the
all-seven word modulo `S=3^a` by binary decimal-block concatenation. If this
word is `N`, the complete sum condition for the actual two-five word is

```
n=N-2-2*10^s,
n=0 modS iff 10^s=(N-2)/2 modS.
```

The division is inversion of two modulo the odd integer S. In particular
the class is not recovered by dropping nine from an F congruence.
Starting at modulus nine, every next ternary digit tests **all three**
possible lifts, retaining the unique match. The exact order
`ord_(3^a)(10)=3^(a-2)=d` follows from LTE and is also checked numerically.
Hence this enumerates the complete sum class `s=r mod d`.

A full witness must also have `s=3 mod6`, since `7|F` gives
`10^s=-1 mod7`. The sum representative is divisible by three; exactly one
of `r,r+d` is odd. This gives the unique joint representative in `[0,2d)`.
The inequality `L<2d` makes it the only possible actual position. A
representative at least L is a class miss, and is never passed to the
original-word evaluator.

For every actual candidate, the program separately concatenates the four
decimal blocks

```
7 repeated L-s-1 times | 5 | 7 repeated s-1 times | 5
```

modulo `S`, `25S`, and successive powers of seven. It also reads back
`F mod9S=0` at the same s. Every excluded actual candidate has its first
nonzero residue at a depth at most `L-2`; the inclusive witness threshold
is retained. No resource limit is treated as an exclusion.

## The finite starts and the crossing pair

The starts `a=31+6u<100` are exactly the following twelve rows. All were
already excluded in both inherited 256-member receipts; the fresh program
recovers them and compares every numerical field to both receipts.

| a | Result | Exact v7(F) | First nonzero original n residue |
|---|---|---:|---|
| 31 | Actual candidate fails | 1 | 35 modulo 49 |
| 37 | Actual candidate fails | 1 | 35 modulo 49 |
| 43 | Class miss | — | — |
| 49 | Actual candidate fails | 1 | 21 modulo 49 |
| 55 | Actual candidate fails | 1 | 14 modulo 49 |
| 61 | Class miss | — | — |
| 67 | Class miss | — | — |
| 73 | Actual candidate fails | 1 | 42 modulo 49 |
| 79 | Actual candidate fails | 1 | 35 modulo 49 |
| 85 | Actual candidate fails | 1 | 21 modulo 49 |
| 91 | Actual candidate fails | 1 | 42 modulo 49 |
| 97 | Actual candidate fails | 3 | 2058 modulo 2401 |

In particular the pair **(97,103)** crossing the a=100 cutoff is excluded
by its starting member. For completeness its successor a=103 is also
freshly recovered: it has an actual position, exact valuation one, and
`n mod49=7`. Thus no admissible starting exponent is lost between the
finite certificates and the large-a pair proof.

## Exact a=1567 certificate

Here `L=(3^1567+4)/7`, and the exact unique joint representative is

```
62616169610141368487908430484479668524698062268901125286236795619703442551610297405265840221081953300684563032626900283675946570405754331089037160632466584216807391148001177032844287605209011265417392318250718632065367111967443076421023672250138864762606389471355080314327810937270889090940750938544790438340932982019607739579055819129136092540463828252460576936666282756371751591142422656576067563073394890863355981704091379346017260225712376888953623676398046363375639738348506632961036910665781846778232596478699485993278721527866686155357246332789892729429953032070205247542153917367841561636035825919994768971807957842031702233992220670042390596770923733771594789447017090624724836089459354564341075865105127627596979331770413532309939769233
```

The receipt retains this s and all of L, S, d and D as exact decimal
integers. It checks `3<=s<L`, `s=3 mod6`, `n modS=0`, `n mod25S=0`,
and `F mod9S=0`. The first two original-word residues at seven are `[0,7]`,
for moduli `[7,49]`; equivalently `F mod49=14`. Therefore
`PS` does **not** divide n. The failure happens long before the full
witness threshold, so a full-product divisibility expansion is unnecessary.

With the inherited certificates, **257 named lengths** `a=31+6u`,
`0<=u<=256`, through **a=1567**, are excluded. There are 84 class misses,
173 actual candidates and exact-valuation histogram
`{1:151,2:18,3:3,4:1}`. The next unchecked individual exponent is **1573**.
Only the twelve finite starts, their crossing successor, and a=1567 are
recomputed by this new program; the other historical members remain
inherited evidence.

## Controls, receipts and scope

The sum-positive control `a=25` is freshly recovered at
`L=121041229921`, `s=40582608819`, with `n modS=n mod25S=0` and
seven-power residues `[0,0,294]` modulo `[7,49,343]`. Its exact valuation
is two. This is a positive sum control, not a full witness.

The literal 313-digit word at `(L,s)=(313,51)` is built from its digits;
the program checks its product, sum, `F=9n`, and equivalence of the two
full-product predicates. It recovers `F modS=0`, `F mod9S=17496` and
`n modS=1944`, so losing the factor nine is detected. An additional
complete original-word enumeration at a=7 independently verifies
actual-class completeness.

The deterministic [`individual.json`](individual.json) binds the fresh
source and both inherited 256-row receipts by SHA-256. Normal and optimized
runs produced identical bytes:

```sh
pt=research/a398769/five-seven/power-three-pair
PYTHONDONTWRITEBYTECODE=1 python3 "$pt/individual_check.py" > /tmp/pair-individual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O "$pt/individual_check.py" > /tmp/pair-individual-O.json
cmp /tmp/pair-individual.json /tmp/pair-individual-O.json
cmp /tmp/pair-individual.json "$pt/individual.json"
```

The pair theorem says `not(W_u and W_(u+1))`. If both neighbours of a
member fail, both adjacent pair statements are already satisfied and impose
no condition on that member. Neither this theorem nor the computation
proves an implication from an isolated witness to a surviving neighbour.
The first missing universal individual step is a direct bound below `L-2`
for every remaining actual position, or another proved implication excluding
an isolated witness. The individual family, unrestricted `{5,7}` problem,
and wider digit-1 assertion therefore remain open. Consecutive whole-length
coverage stays **1–1,000,002,000,000 inclusive**. No Lean theorem or Lean
build was performed by this check.
