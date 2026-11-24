## Deduction 2: finitely many candidates with both exponents variable

**Verdict: valid as a finiteness argument.** It proves finiteness even for the
weaker necessary condition `7^(L-2) | F`. It does not prove that this finite
set is empty and supplies no numerical upper bound on `L`.

### Exact theorem used

J.-H. Evertse, *On sums of S-units and linear recurrences*, Compositio
Mathematica **53** (1984), 225–244, Corollary 1, printed p. 227,
equations (9)–(12), with the passage from projective points to primitive
integer tuples explained on printed p. 228. These are PDF pages 4–5,
including the Numdam cover. The height conventions are on printed p. 226.
[Original paper](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf).

In the rational-integer specialization, fix a finite set of prime numbers
`S0`, constants `c > 0` and `0 <= d < 1`, and the number of coordinates.
There are finitely many primitive integer tuples having zero coordinate
sum, no vanishing nonempty proper subsum, and

    product_j (|x_j| * product_{p in S0} |x_j|_p)
        <= c * (max_j |x_j|)^d.

Here `|a|_p = p^(-v_p(a))`. Thus the product on the left is precisely the
positive part of the coordinate product supported on primes outside `S0`.
The corollary requires a common greatest common divisor of 1, not pairwise
coprimality. The stronger pairwise condition discussed on p. 228 is not a
hypothesis of Corollary 1.

### All hypotheses for this family

Let `L >= 5`, `3 <= i < L`, and

    F = 7*10^L - 18*10^i - 25,
    A = 7*10^L/25, B = 18*10^i/25, C = F/25,
    x = (A, -B, -1, -C), S0 = {2,3,5,7}.

Both powers of ten are divisible by 25, so `A`, `B`, and `C` are integers.
Also `A > 0`, `B > 0`, and

    F >= (70-18)*10^i - 25 = 52*10^i - 25 > 0.

Thus `C > 0`, and the defining identity gives `A = B + 1 + C`.
Consequently:

- the sum of all four coordinates is zero;
- the common greatest common divisor is 1, because one coordinate is `-1`;
- every nonempty subsum without `A` is negative;
- every proper subsum containing `A` is positive, since it is the negative
  of the sum of the omitted, strictly negative coordinates.

In particular there is no zero coordinate and no vanishing nonempty proper
subsum. Since `A = B+1+C`, the height appearing in the corollary is exactly

    H = max(A, B, 1, C) = A = 7*10^L/25.

These integer coordinates are already primitive. This also equals the
associated rational projective height.

### Uniform outside-prime estimate

For a nonzero integer `a`, write

    [a]_(S0 outside) = |a| / product_{p in S0} p^(v_p(a)).

The coordinates `A`, `-B`, and `-1` have outside part 1: their factorizations
use only the primes 2, 3, 5, and 7. Explicitly,

    A = 7 * 2^L * 5^(L-2),
    B = 2^(i+1) * 3^2 * 5^(i-2).

Only `C` contributes to the corollary's product. Suppose the sole arithmetic
candidate condition `7^(L-2) | F` holds. Since 25 is a 7-adic unit,
`7^(L-2) | C`, and therefore

    product_j [x_j]_(S0 outside)
        = [C]_(S0 outside)
        <= C/7^(L-2)
        < H/7^(L-2).

In fact `c=1` works uniformly for all `L >= 5`. Indeed,

    H/7^(2L-4)
      = (7^5/25)*(10/49)^L
      <= (7^5/25)*(10/49)^5
      = 100000/420175
      < 1.

All quantities are positive, so `sqrt(H) < 7^(L-2)` and

    product_j [x_j]_(S0 outside) < H^(1/2).

This verifies equation (12) with the fixed constants `c=1`, `d=1/2`, and
with `n=3` in Evertse's notation (four coordinates). No constant depends on
`i` or `L`. Neither the oddness of `L` nor `i = 3 (mod 6)` was needed for
this estimate or for the other hypotheses.

### What follows, and what does not

Distinct pairs `(L,i)` give distinct tuples: `A` determines `10^L` and hence
`L`, and `B` determines `10^i` and hence `i`. Corollary 1 therefore proves
that the set

    {(L,i): L >= 5, 3 <= i < L,
             7^(L-2) | 7*10^L - 18*10^i - 25}

is finite. The original odd-length, `i=3 (mod 6)` family is a subset, as are
the pairs satisfying the full digit product-times-sum condition. Together
with the earlier elementary reduction to two fives, this proves finiteness
of the entire `{5,7}` subclass of potential A398769 counterexamples.

Finiteness means that some maximum length exists if this set is nonempty.
Corollary 1 does not give that maximum numerically; this application gives
neither a search cutoff nor a list of the surviving pairs. In particular,
it does not establish that there are no `{5,7}` counterexamples and it does
not settle the unrestricted conjecture. The application above is an
ordinary mathematical proof relying on the published corollary, not a Lean
formalization of Evertse's theorem or its application.
