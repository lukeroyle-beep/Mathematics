# Why the remaining region is not certified

This note records checked limitations of the methods investigated, not a
claim that no stronger theorem or argument exists. Sources were opened on
24 November 2026. None of the additional results below is used as an
unverified numerical cutoff.

## Effective estimates for few nonzero digits

Bugeaud, *On the digital representation of integers with bounded prime
factors*, [arXiv:1609.07926](https://arxiv.org/pdf/1609.07926), Theorem 1.2
(printed p. 3), supplies effectively computable positive constants `c4,c5`
depending on the fixed integer base `b>=2` and fixed nonempty finite prime
set `T`. For the increasing sequence `u_j` of positive integers not divisible
by `b` with at most three nonzero base-`b` digits, it gives

```text
[u_j]_T <= u_j^(1-c4), for j >= c5.
```

Here `[u]_T` means the part supported on primes in `T`, not the digit sum.
The source describes the obtainable saving as very small. Its digit
definition on printed p. 2 uses ordinary nonnegative base digits. Our
three-term expression `7*10^L-18*10^i-25` does not satisfy that digit
hypothesis; decimal borrowing creates long blocks. The theorem as stated
cannot simply be applied to `F`.

Even if an analogous effective bound were proved for `F` and `T={7}`, a
bare positive saving would not suffice. Since

```text
7^(L-2) <= [F]_{7},       F < 7*10^L,
```

an upper bound `F^(1-c)` yields an eventual contradiction by exponential
growth only if `7 > 10^(1-c)`, that is,

```text
c > 1-log(7)/log(10)  (approximately 0.154902).
```

No effective estimate with verified hypotheses and that margin was derived
here. Merely replacing an ineffective theorem by an effective one does not
establish that its quantitative strength is adequate.

## Greatest-prime-factor bounds and the unrestricted cofactor

Bugeaud–Kaneko, *On the digital representation of smooth numbers*,
[arXiv:1704.00432](https://arxiv.org/pdf/1704.00432), Theorems 1.1–1.2
(printed p. 2), give effective lower bounds involving the greatest prime
factor and the count of nonzero digits. Remark 4.4 describes analogous
results for the number of constant-digit blocks. Remark 4.3 distinguishes
strong ineffective prime-part estimates from weaker effective estimates.
These are relevant directions for our decimal words, which have at most
four constant-digit blocks, but full divisibility does not bound all their
prime factors in a fixed set.

In fact, if a witness has exact positive integer quotient `q=n/(P*S)`,
the elementary size bound gives only

```text
q < 343/(225*(7L-4)) * (10/7)^L.
```

This still permits an exponentially growing cofactor with unrestricted
prime factors, while the sum `S=7L-4` also varies. A lower bound for a large
prime factor therefore supplies no contradiction by itself.

## The remaining mathematical requirement

The variable-height two-logarithm bounds are fully explicit in
[EDGE_BOUNDS.md](EDGE_BOUNDS.md), and treat fixed position and fixed gap.
They do not uniformly control the central region. An estimate for a
multiplicative product minus one is not automatically an estimate for
this three-term additive expression; incorporating a sum into one base
reintroduces its growing height.

The full digit-sum congruence may still provide a successful route even
if a pair passes the weaker seven-power test. The filters proved in
[FULL_DIVISOR.md](FULL_DIVISOR.md) exclude infinite length classes, but
leave infinitely many admissible lengths. What is missing is a verified
full-divisor contradiction throughout the remaining domain, or a genuinely
global effective bound followed by complete arithmetic certification, or
an exact witness. The merged Evertse corollary and the chosen finite
search boundary supply none of those on their own.
