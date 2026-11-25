# Broad early rejection: mathematical audit

These are ordinary mathematical arguments. No theorem here is formalized in
Lean. The truth of the all-length statement (E) is not presumed.

## 1. Exact domain and its relation to a full witness

For every odd integer `L>=5` and every integer `3<=i<L`, set

```
F=7*10^L-18*10^i-25, n=F/9, S=7L-4, P=25*7^(L-2).
```

The decimal word for n has two fives, at positions zero and i, and
sevens elsewhere. Thus it has sum S and product P. Multiplying integer
divisibility by nine gives the exact, unrestricted identity

```
PS | n  <=>  225*S*7^(L-2) | F.
```

The suffix is 775, hence `v_5(n)=2`. A full witness cannot have `5|S`.
Since `S=3 mod7`, on the remaining domain `5` does not divide S the
original condition separates exactly into

```
9S | F  and  v_7(F)>=L-2.
```

Indeed `25|n`, and 25, S, and `7^(L-2)` are pairwise coprime.
The factor nine stays in the full-sum test, even when `3|S`.
No conclusion about E is obtained from the exclusion of other inherited
full-witness domains: E is a stronger statement on its own broader domain.

## 2. Unique representatives and the exact equivalence

For `k>=1`, put `T_k=6*7^(k-1)`. Direct residues give order six
for 10 modulo seven, and `10^6=1+7 mod49`. The binomial theorem,
or elementary prime-power lifting applied successively, gives

```
v_7(10^(6m)-1)=1+v_7(m),   ord_(7^k)(10)=T_k.
```

The order equals the number of units modulo `7^k`. The target
`(7*10^L-25)*18^(-1)` is a unit, so exactly one exponent
`r_k in [0,T_k)` produces it. In particular, modulo seven this is
`10^i=-1`, so every depth-at-least-one position satisfies `i=3 mod6`.
The broad original position domain includes both parities; this restriction
is derived only after imposing positive seven-adic depth.

Define K to be the least k with `T_k>L`, using a strict inequality.
If an actual position satisfies `v_7(F)>=K`, it is congruent to `r_K`
modulo `T_K`. Both positions lie in `[0,T_K)`, so it equals `r_K`.
Conversely, if `3<=r_K<L`, its defining congruence certifies depth at
least K. Consequently the following two statements are equivalent:

* For every odd `L>=5` with `5` not dividing S, every actual position
  satisfying `9S|F` has depth less than K.
* For every such L, if `3<=r_K<L`, then `9S` does not divide
  `F(L,r_K)`.

This proves the stated equivalence independently of any experiment.
Examining only `r_K` exhausts all possible violations at each length.
No minimum-position, edge, midpoint, ratio, or prime-divisor witness
restriction is needed for this argument or the broad finite audit.

For all `L>=5`, `T_(L-2)>L`: it holds at L=5 because `294>5`,
and increasing L by one multiplies the left side by seven while adding
one on the right. Hence `K<=L-2`. If E were proved, its bound
`v_7(F)<K<=L-2` would reject every residual full witness. Together
with the inherited elementary complementary cases, it would settle the
all-5/7 subclass. It would say nothing by itself about other digit sets
in the wider digit-1 conjecture. The finite audit does not supply this
conditional premise.

## 3. Why later unrestricted CRT incompatibility cannot prove E

Write `d=ord_S(10)` and `e=v_7(d)`. The inherited stabilization
lemma can be independently reconstructed as follows. If e is positive,
some odd prime q dividing S has `7^e | q-1`; this follows by taking
the largest seven-part in the prime-power orders and using
`ord_(q^b)(10) | q^(b-1)*(q-1)`. Since `7` does not divide S,
the seven-part comes from q-1. Therefore `q>=2*7^e+1`. Also
`S/q=3 mod7` is a positive odd integer, so it is at least three.
It follows that `7L-4>=6*7^e+3` and `T_e<=L-1`. Thus

```
v_7(ord_S(10)) <= K-1.
```

Full-sum positions, if nonempty, form exactly one exponent class
`s mod d`. To retain the nine, obtain the target from
`n=7R_L-2-2*10^i` modulo S and invert only 2. The simultaneous
classes `i=s mod d` and `i=r_k mod T_k` are compatible precisely
when `s=r_k mod gcd(d,T_k)`. Because

```
gcd(d,T_k)=gcd(d,6)*7^min(e,k-1),
```

this gcd is already constant for every `k>=K`. Each lift changes
r by a multiple of `T_k`, so compatibility at K persists at every
higher level. This does not assert that a bounded representative exists
or remains compatible. It proves that a proposed later incompatibility
in this unrestricted exponent CRT system needs an additional condition.
This is inherited structural information, not a new proof of E.

## 4. A controlled small-period search reduction

If `ord_S(10)` divides a positive integer d, and a full-sum position
exists, put `a=L mod d`, `b=i mod d`. Necessarily

```
S | gcd(10^d-1, 7*10^a-18*10^b-25),
S=7L-4,  L mod d=a.
```

These are necessary conditions, not sufficient ones when S has a factor
of three. The independent direct `9S` check remains mandatory. This
observation motivates the finite cycle-gcd search in search_scope.json: a
large S with a small d gives many full-sum positions if compatibility is
present. The search enumerates specified gcds with their three-parts
varied; it does not enumerate every divisor of those gcds and does not
prove a theorem on the unresolved complement.

## 5. Remaining proof obligation

No argument here proves E or a new all-length restricted valuation bound.
The finite audit certifies only its specified interval, and the searches
only their declared families. The first missing step for E is a uniform
reason why the bounded `r_K(L)` cannot pass the full `9S` condition.
If that stronger assertion fails, the subclass can still be settled by
proving `v_7(F(L,r_K))<=L-3` on the narrower surviving witness domain.
Uniqueness does not prove absence; fixed-depth families do not reach a
threshold growing with L; `v_7(F)=o(L)` supplies neither a logarithmic
bound nor an effective start. No effective global cutoff is obtained.
