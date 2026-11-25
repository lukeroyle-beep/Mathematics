# Attempted routes and unresolved steps

The investigation treats E as a conjectural statement. Its zero counts are
finite evidence. The routes below do not supply an all-length valuation
bound or an effective cutoff.

## 1. Exponent CRT compatibility

The full-sum condition, when solvable, specifies one exponent class modulo
`d=ord_S(10)`. Seven-adic depth k specifies one class modulo
`T_k=6*7^(k-1)`. The inherited proof gives `v_7(d)<=K-1`, so their
compatibility gcd stabilizes at K. Once compatible at K, the unrestricted
classes stay compatible at every higher depth. The first unproved step is
an additional restriction forcing the *bounded* representative to fail the
sum or to escape. A later gcd incompatibility by itself cannot do so.

## 2. Uniqueness and varying representatives

`T_K>L` proves that at most one actual position survives, and that its
identity is `r_K`. It does not prove that this position is outside the
interval or fails `9S|F`. Across lengths, even at one fixed K, the
representative is not monotone: at L=13 and L=15, K=2 while the
representatives are respectively 39 and 3. Both lengths have `5` not
dividing S. The latter passes the actual-position condition but fails the
full sum. Thus ordering the representatives by length supplies no
monotonic rejection mechanism. The missing uniform assertion is precisely
the sum failure at every actual r_K, which is E itself.

## 3. Tractable sums and complete power cycles

The declared smooth-family search selects `S=3^a*p^b` with
`p in {17,898129}`. These primes come from the inherited exact full-sum
constructions; the search does not assume their fixed-depth examples
reach K. All selected lengths are tested directly at their own K, with
no full-witness position or length filters.

The complementary cycle-gcd search seeks large sums with small
multiplicative period. If `ord_S(10)|d`, then full-sum exponents occur
in classes modulo d, possibly giving many actual positions. For each
specified d,a,b it computes

```
G=gcd(10^d-1,7*10^a-18*10^b-25)
```

and examines the declared quotients obtained by removing seven-powers and
varying the three-part. The required relation `S=7L-4` is imposed before
checking the unique representative. The exact factor-nine test is still
performed; `S|F` alone is never used as success. This finite search does
not enumerate all divisors of G or all d, and absence there is not an
exclusion of the unresolved complement.

The exact scope was saved in search_scope.json before computation. The
result is search.json; the program completed that scope without extending
it after zero observations:

| Declared family | Raw parameters | Distinct lengths | Actual r_K failing full sum | Outside actual interval | Pass |
|---|---:|---:|---:|---:|---:|
| `3^a*p^b`, `p in {17,898129}`, `0<=a<=200`, `0<=b<=40` | 16,482 | 2,731 | 1,193 | 1,538 | 0 |
| Cycle gcd, `1<=d<=240`, `0<=a,b<d`, declared three-part quotients | 4,636,840 | 37 | 14 | 23 | 0 |

The union has 2,768 distinct lengths, of which 2,721 exceed 9,999,999.
The smooth family ranges from L=313 to the exact 333-digit maximum in
search.json. The cycle-gcd candidates range from 9 through 14,731:
this selection produced no new large candidate, so it supplied no test of
E beyond the main audited interval. There was no full-sum-compatible actual
r_K in either family. All selected sums are five-free.

Every actual representative's direct F residue is independently compared
with `9*(n mod S)`, using a geometric-sum recurrence without division by
nine. Each family's SHA-256 hashes sorted ASCII records
`L:K:r_K:category:residue\n`; categories are `outside`, `excluded_five`,
`fail`, `pass`, and the residue is `-` outside the actual interval.
The source and fixed-scope hashes are in the receipt. Normal Python and
`python3 -O` reproduce byte-identical receipts. These are sparse finite
family searches, not a new consecutive length certificate. No difficult
factorization or unresolved large discrete logarithm is silently turned
into an exclusion.

## 4. Existing fixed-depth and whole-length constructions

For each fixed k, the inherited density construction produces infinitely
many lengths whose maximum full-sum depth is exactly k. Those lengths
are unbounded, hence eventually exceed `T_k`, at which point `K(L)>k`.
Consequently their tail satisfies E, but this is an immediate consequence
of the inherited maximum theorem, not a new structural advance.

The missing diagonal claim would require one of the constructed actual
positions to have `k>=K(L)` at its own length, or a proof that this never
happens. Fixed-depth density supplies neither. In particular, increasing
k first also changes the grid steps exponentially in k and gives no
upper bound for the first length where the selected arc is attained.

## 5. Qualitative and elementary valuation estimates

The inherited uniform `v_7(F)=o(L)` compares depth with a linear scale.
It does not imply comparison with the logarithmic threshold K, and its
exceptional starting length is ineffective. Even knowing a finite set of
possible full witnesses would not enumerate that set or bound its largest
length.

When `9S|F`, the known factor 25 additionally gives `225S|F`, and

```
225*S*7^v <= F < 7*10^L.
```

Taking real logarithms yields an upper bound with leading coefficient
`log(10)/log(7)>1` times L; the varying sum supplies only a logarithmic
subtraction. This is much weaker than E. The missing step is a new
arithmetic estimate connecting S to r_K that yields enough saving.

No external theorem is newly applied in this investigation. The inherited
analytic results retain their established hypotheses and limitations.
No term involving `10^L` or `10^i` is treated as a fixed-height parameter.
No numerical cutoff, finite remaining gap, or new Lean verification is
claimed.
