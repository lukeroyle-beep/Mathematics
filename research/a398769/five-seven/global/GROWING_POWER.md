# Growing powers of seven: a spacing lemma and the remaining gap

This investigation starts from merged PR #8. It does not produce a global
cutoff or a new fully excluded interval of lengths. All proofs below are
ordinary mathematics, not Lean statements.

Put `F(L,i)=7*10^L-18*10^i-25`. A weak solution means an admissible pair
with `7^(L-2) | F(L,i)`. The merged order computation gives
`ord_(7^k)(10)=6*7^(k-1)`.

## Exact pairwise restrictions

More generally, suppose two pairs `(L,i)` and `(L',i')` satisfy
`F(L,i)=F(L',i')=0 mod 7^k`, where `k>=2`, `i=i'=3 mod6`,
and `L=L' mod6`. If both differences `dL=L-L'` and `di=i-i'`
are nonzero, set

```text
a = 2+v_7(dL),       b = 1+v_7(di).
```

Then either `a=b<k` or both `a,b>=k`. In particular, whenever either
valuation is below `k`,

```text
v_7(di) = v_7(dL)+1.                         (1)
```

**Proof.** The elementary lifting identity is
`v_7(10^d-1)=1+v_7(d)` for a nonzero multiple `d` of 6; for negative
`d` use the numerator after dividing by the 7-adic unit `10^(-d)`.
Indeed `v_7(10^6-1)=1`; expansion of `(1+7u)^7` increases this valuation
by one, and raising to an exponent coprime to 7 preserves it. Iteration
proves the identity. Subtracting the two congruences gives

```text
7*(10^L-10^L') - 18*(10^i-10^i') = 0 mod 7^k.
```

The valuations of these two terms are exactly `a,b`. If they differ,
the valuation of their difference is their minimum, which cannot be
below `k`. This proves the assertion. No estimate of either large power
in the ordinary absolute value is used.

There are also exact restrictions for coincident coordinates:

* If `i=i'` and `L!=L'`, then
  `6*7^(k-2) | L-L'` under the stated `L=L' mod6` hypothesis.
* If `L=L'` and `i!=i'`, then `6*7^(k-1) | i-i'`.
* If `L-i=L'-i'` and the pairs are distinct, then
  `6*7^(k-1) | L-L'`. To see this, put `g=L-i` and subtract the
  identities `F=(7*10^g-18)*10^i-25`. The prefactor is a 7-adic unit.

For two weak solutions one may take `k=min(L,L')-2`. Thus equal positions
or equal gaps force exponentially large separation in length. Also there
is at most one weak-solution position at any given length `L>=5`:
`6*7^(L-3)>L-1`, whereas two allowed positions differ by less than `L`.

These are restrictions **between two solutions**. They place no upper
bound on the first hypothetical solution beyond the certified range.
They therefore cannot turn the finite exclusion into an all-length proof.
The checker [check_spacing.py](check_spacing.py) uses positive solutions
of lower-power congruences, rather than treating the absence of known weak
solutions as a test of (1).

From the repository root, reproduce its [receipt](spacing.json) with:

```sh
python3 -O research/a398769/five-seven/global/check_spacing.py > /tmp/a398769-spacing.json
cmp /tmp/a398769-spacing.json research/a398769/five-seven/global/spacing.json
```

It checks all fixed-power candidates through length 1001 for powers
`7^3,7^4,7^5`, including coincident coordinates, both high valuations,
and controls rejecting a wrong relation. These finite checks validate
the lemma's arithmetic on those inputs; they do not exclude new lengths.

## What the effective logarithm estimates still permit

The two bounds proved in [the merged edge argument](../settlement/EDGE_BOUNDS.md)
are

```text
L-3 <= 63*(i+1)*max(log L+2,20)^2,
L-2 <= 63*(L-i+1)*max(log L+2,20)^2.
```

For example, if `L/3 <= i <= 2L/3`, each right side is at least
`21*L*400`, so neither inequality contradicts the required valuation.
Taking the smaller of the two estimates does not change this conclusion.
Using `(18*10^i+25)/7` as a logarithm base incurs height proportional to
`i`; using `25/(7*10^(L-i)-18)` incurs height proportional to `L-i`.
Neither is a fixed-height application as the central pair varies.

Applying a logarithm estimate to a multiplicative expression cannot
silently replace this additive three-term expression. Incorporating its
unrestricted exact cofactor also incurs growing height. No estimate with
an explicit coefficient smaller than one in front of `L` was established.

## Why a quantitative finiteness theorem does not fill the gap

The source check here went beyond the merged qualitative finiteness
argument. Evertse--Ferretti, *A further improvement of the quantitative
Subspace Theorem*, Theorem 1.1 (printed p. 4) bounds the number of relevant
subspaces. Theorem 1.2 (printed p. 5) gives an effective exceptional
subspace and finitely many intervals `[Q_j,Q_j^omega)`, but explicitly
states that the endpoints `Q_j` are not effectively determined by its
proof. Consequently the effective interval count and effective subspace
are not an effective upper bound for the heights of all exceptional
points. This is a limitation of this proposed route, not a claim that no
other theorem could settle the present special family.
[Primary source, opened 24 November 2026](https://math.leidenuniv.nl/reports/files/2010-17.pdf).

No application of that theorem with new constants is asserted here; its
statement was checked to reject the inference from a quantitative count
to a numerical length cutoff. The already checked Evertse application
in [FINITE_PAIRS.md](../FINITE_PAIRS.md) remains the finiteness result used.

## A precise sufficient missing statement

One sufficient new theorem would provide explicit constants
`0<=c<1`, `C>=0`, and `L0`, independent of `i`, for which every remaining
admissible pair satisfying the full digit-sum condition has

```text
v_7(F(L,i)) <= c*L+C*log L,       L>=L0.
```

For clarity, such constants really would yield an executable cutoff.
Write `delta=1-c`. Choose any integer

```text
B >= max(L0, 4, 4/delta, (2*C/delta)^2).
```

For `x>=4`, `log x<=sqrt(x)` (check at 4 and differentiate
`sqrt(x)-log x`). Hence for every `L>B`,
`C*log L<=delta*L/2` and `delta*L/2>2`. It follows that
`c*L+C*log L<L-2`, contradicting weak divisibility. An upper rational
enclosure for the constants can be used to choose an integer `B`.
This conditional calculation is not a bound for the problem: its
required uniform valuation inequality remains unproved.

The actual remaining task is to prove such a uniform estimate (or another
global contradiction/cutoff), or to prove that both exact quotient
candidates fail for every remaining length, or to exhibit and verify a
witness. The spacing restrictions and the reviewed finiteness statements
do not establish any of these.
