# Uniform qualitative valuation bound

This is a corollary of the same published method used in
[FINITE_PAIRS.md](../FINITE_PAIRS.md), not a claim of novelty or an
effective cutoff. It is an ordinary mathematical proof, not a Lean
formalization. All logarithms below are natural.

## Statement and domain

For integers `L>=5` and `3<=i<L`, put

```text
F(L,i) = 7*10^L - 18*10^i - 25,   t(L,i) = v_7(F(L,i)).
```

For every fixed real `epsilon>0`, there are only finitely many pairs in
this domain with `t(L,i)>=epsilon*L`. Equivalently,

```text
lim_{L -> infinity} max_{3<=i<L} t(L,i)/L = 0.
```

In particular only finitely many pairs have `t(L,i)>=L/2`.
Neither oddness, the position residue restrictions, nor `9*(7L-4)|F`
is needed. The statement includes both growing positions and growing
gaps, and is stronger in scope than finiteness of full witnesses.
It does not give an algorithm for the starting length associated with
any `epsilon`.

## Published input

J.-H. Evertse, *On sums of S-units and linear recurrences*, Compositio
Mathematica **53** (1984), 225–244,
[original PDF](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf),
Corollary 1, printed p. 227, equations (9)–(12); height conventions on
printed p. 226 and primitive projective representatives on p. 228.
These are zero-based PDF indices 2, 3 and 4, with the Numdam cover included.

In its rational-integer form the corollary fixes `c>0`, `0<=d<1`,
a finite prime set `Sigma`, and the number of coordinates. It gives
finitely many integer tuples with zero sum, common gcd 1, no nonempty
proper zero subsum, and

```text
product_j out_Sigma(x_j) <= c*h^d,
h = max_j |x_j|,
out_Sigma(a) = |a| / product_{p in Sigma} p^v_p(a).
```

The common gcd requirement is not pairwise coprimality. No theorem for
a product minus one is being applied to an additive expression here.

The downloaded source was checked on 25 November 2026; its SHA-256 is
`5b02e0e31c546f7f8c6c34071b2caa4d7137be24f16d11d483cdcc65377b2f6d`.

## Hypotheses, checked for every pair

Set

```text
U = 7*10^L/25 = 7*2^L*5^(L-2),
V = 18*10^i/25 = 2^(i+1)*3^2*5^(i-2),
W = F/25 = U-V-1,
x = (U,-V,-1,-W),   Sigma = {2,3,5,7}.
```

The stated exponent ranges make `U,V,W` integers. Since `L>=i+1`,

```text
F >= (70-18)*10^i-25 = 52*10^i-25 > 0.
```

Thus all four coordinates are nonzero and `W>0`. Their sum is zero.
The coordinate `-1` makes their common gcd 1. A nonempty subsum omitting
`U` is strictly negative. A proper subsum containing `U` is the negative
of its nonempty omitted subsum, so is strictly positive. This checks all
nonempty proper subsums, including those with three terms.

Because `U=V+1+W`, the exact height is `h=U`. This also equals the rational
projective height of this primitive integer tuple. It is unrelated to
the divisor denoted `H` in [TWO_QUOTIENTS.md](../global/TWO_QUOTIENTS.md).
The displayed factorizations show that only `W` contributes primes
outside `Sigma`. Since `v_7(25)=0`, `v_7(W)=t(L,i)`. Consequently

```text
product_j out_Sigma(x_j) = out_Sigma(W)
    <= W/7^t < U/7^t.                         (1)
```

This does not assert that `W`, or a witness's unrestricted cofactor,
has all its prime factors in `Sigma`.

## The requested half-length threshold

For every positive `L`, `U=(7/25)*10^L<49^L`. Thus
`U^(1/4)<7^(L/2)`. If `t>=L/2`, (1) gives

```text
out_Sigma(W) < U/7^(L/2) < U^(3/4).
```

Apply Corollary 1 with `c=1`, `d=3/4`, this fixed `Sigma`, and `n=3`
in the source notation (four coordinates). These constants are independent
of both exponents. The map from pairs to tuples is injective: `U`
determines `L`, and `V` determines `i`. Therefore the finitely many
tuples give finitely many such pairs. A maximum exceptional length
exists if the exceptional set is nonempty, but is not supplied by the
corollary.

## The uniform little-o conclusion

Fix `epsilon>0`, set `e=min(epsilon,1/2)`, and choose

```text
d = 1 - e*log(7)/log(10),    c = 1.
```

Here `0<d<1`, since `0<e<=1/2` and `0<log(7)/log(10)<1`.
The constants depend only on the chosen `epsilon` and the fixed bases.
If `t>=epsilon*L`, then `t>=e*L`. From `U<10^L` we obtain

```text
U^(1-d) < 7^(e*L),
out_Sigma(W) < U/7^(e*L) < U^d.
```

The same fixed-dimension corollary and injection give finitely many
pairs for each `epsilon`. For each fixed length there are only `L-3`
positions in the domain. The finite exceptional set therefore has a
maximum length, establishing the uniform limit in the statement.
Nonnegativity of `t` completes the equivalence with that limit.

## Effectivity boundary

The explicitly chosen `c,d` are parameters in a qualitative theorem;
they are not a bound for its exceptional heights. Evertse states the
p-adic Subspace Theorem as Theorem 4 on printed p. 231 and uses it to
prove Theorem 2 in section 2. After (22) on p. 232, constants depend on
the coefficient tuples of the unspecified exceptional subspaces; the
height argument in section 3, pp. 234–235, inherits this dependence.
The resulting finiteness of admissible primitive tuples does not
enumerate those tuples or bound their largest height effectively.
This application adds no information removing that limitation.

For a full witness `v_7(F)=v_7(n)>=L-2`. Since `L-2>=L/2` for `L>=4`,
the half-length result again proves qualitative finiteness of the
residual family. It does not prove emptiness. In particular, it does
not certify a single new length above 10,000,000 or provide numerical
constants `c<1,C,L0` in an effective uniform valuation inequality.

Lengths below 5 and positions below 3 are outside this corollary;
their exclusions for full witnesses belong to the inherited elementary
reduction and finite certificates. No small endpoint is newly excluded
by an unspecified asymptotic statement.
