#!/usr/bin/env python3
"""Exact arithmetic controls for proportional exclusions; not an all-length sieve."""
from fractions import Fraction as Q
from math import gcd, isqrt
import json


def require(ok, detail):
    if not ok:
        raise ArithmeticError(detail)


def log_bounds(x):
    """Rational atanh series with range reduction and a positive tail bound."""
    require(x > 0, "positive logarithm argument")
    if x < 1:
        lo, hi = log_bounds(1 / x)
        return -hi, -lo
    twos = 0
    while x >= 2:
        x /= 2
        twos += 1

    def series(y):
        z = (y - 1) / (y + 1)
        n = 48
        lo = 2 * sum((z ** (2*j+1) / (2*j+1) for j in range(n)), Q(0))
        return lo, lo + 2*z**(2*n+1)/((2*n+1)*(1-z*z))

    lo, hi = series(x)
    lo2, hi2 = series(Q(2))
    return lo + twos*lo2, hi + twos*hi2


def poly_value(coeffs, x):
    return sum(c*x**j for j, c in coeffs.items())


def polynomial(a, b, L, i):
    k, r = divmod(L, b)
    s = i-a*k
    shift = max(0, -s)
    return k, r, s, {b: 7*10**(r+shift), a: -18*10**(s+shift), 0: -25*10**shift}


def main():
    N = 10_000_000
    lo7, hi7 = log_bounds(Q(7))
    lo10, hi10 = log_bounds(Q(10))
    require(168*hi10**2/lo7**4 < 63, "BL coefficient")
    require(10*hi7 < Q('19.5'), "degree-one maximum")
    _, loglog7_hi = log_bounds(hi7)
    for name, numerator, cap in [
        ('edges', Q(25001), Q(11)),
        ('midpoint', Q('30001.5'), Q('10.6')),
        ('thirds', Q(100002), Q(12)),
        ('fifths', Q(2_000_000, 7)+1, Q(13)),
    ]:
        _, hi = log_bounds(numerator/lo10)
        require(hi+loglog7_hi+Q(2, 5) < cap, name+' logarithm maximum')
    margins = {}
    for name, coefficient, divisor, additive, extra in [
        ('edges', 63*Q('19.5')**2, 25000, 1, 1),
        ('midpoint', 504*Q('10.6')**2, 60000, 2, 0),
        ('thirds', Q(63*27*144), 300000, 2, 0),
    ]:
        require(coefficient/divisor < 1, name+' affine slope')
        margin = N-2-extra-coefficient*(Q(N, divisor)+additive)
        require(margin > 0, name+' strict endpoint')
        margins[name] = str(margin)
    fifths_slope = Q(63*125*169*7, N)
    require(fifths_slope == Q(74529, 80000), 'fifths slope')
    require((1-fifths_slope)*N > 2, 'fifths endpoint')
    require(Q(165) < Q(N, 60000) < 167, 'midpoint strip parity endpoint')
    # Irreducibility in AUDIT.md permits D=2 throughout the enlarged strip.
    _, hi_fixed = log_bounds(Q(N+360, 362)/lo10)
    require(hi_fixed+loglog7_hi+Q(2, 5) < Q('10.46'), 'fixed strip179 log maximum')
    fixed_coefficient = Q(504*181)
    fixed_margin = N-2-fixed_coefficient*Q('10.46')**2
    require(fixed_margin == Q(11896376, 625) > 0, 'fixed strip179 endpoint')
    require(2*fixed_coefficient*Q('10.46')/N < 1, 'fixed strip179 derivative')

    excluded = [
        (Q(0), Q(1, 25000)),
        (Q(299999, 900000), Q(300001, 900000)),
        (Q(3999999, N), Q(4000001, N)),
        (Q(59999, 120000), Q(60001, 120000)),
        (Q(5999999, N), Q(6000001, N)),
        (Q(599999, 900000), Q(600001, 900000)),
        (Q(24999, 25000), Q(1)),
    ]
    gaps = [(left[1], right[0]) for left, right in zip(excluded, excluded[1:])]
    require(all(lo < hi for lo, hi in gaps), 'disjoint closed exclusions')
    require(any(lo < Q(41, 100) < Q(42, 100) < hi for lo, hi in gaps), 'explicit open gap')

    # Direct polynomial evaluation is separate from modular root lifting.
    identities = positives = comparisons = 0
    signs = {'negative': 0, 'zero': 0, 'positive': 0}
    for a, b in [(1, 3), (2, 3), (2, 5), (3, 5)]:
        for L in range(5, 102, 2):
            if L < b:
                continue
            for i in range(3, L):
                k, r, s, coeffs = polynomial(a, b, L, i)
                F = 7*10**L-18*10**i-25
                x = 10**k
                require(poly_value(coeffs, x) == 10**max(0, -s)*F, 'cleared identity')
                span = max(0, r, s)-min(0, r, s)
                require(Q(abs(b*i-a*L), b) <= span, 'span lower bound')
                require(span <= Q(abs(b*i-a*L), b)+b-1, 'span upper bound')
                require(sum(abs(c) for c in coeffs.values()) <= 50*10**span, 'height coefficient sum')
                identities += 1
                signs['negative' if s < 0 else 'positive' if s > 0 else 'zero'] += 1
                if F % 7:
                    continue
                positives += 1
                derivative = sum(j*c*x**(j-1) for j, c in coeffs.items() if j)
                require(derivative % 7 != 0, 'simple root')
                root, modulus = x % 7, 7
                for level in range(2, 7):
                    next_modulus = 7*modulus
                    lifts = [root+j*modulus for j in range(7)
                             if poly_value(coeffs, root+j*modulus) % next_modulus == 0]
                    require(len(lifts) == 1, 'unique Hensel lift')
                    root, modulus = lifts[0], next_modulus
                    require((F % modulus == 0) == ((x-root) % modulus == 0), 'root-distance equivalence')
                    comparisons += 1

    # No derivative-unit argument is available here when 7 divides a.
    k, r, s, coeffs = polynomial(7, 8, 27, 21)
    require(poly_value(coeffs, 10**k) % 7 == 0, 'multiple-root positive control')
    require(sum(j*c*(10**k)**(j-1) for j, c in coeffs.items() if j) % 7 == 0,
            '7-divisible numerator must be excluded from simple-root theorem')

    M = 6*5*11*13*37*101
    family = []
    for j in [1, 2, 3, 10, 100, 10000]:
        L = 1+M*j
        i = 39+42*((isqrt(2*L*L)-L-18)//42)
        require(L > N and L % 6 == 1 and i % 42 == 39 and 3 <= i < L, 'family congruences')
        require(all(L % p != bad for p, bad in [(5, 2), (11, 10), (13, 8), (37, 27), (101, 15)]),
                'family length filters')
        require((7*pow(10, L, 49)-18*pow(10, i, 49)-25) % 49 == 0, 'family modulo49')
        require(Q(41, 100) < Q(i, L) < Q(42, 100), 'family in displayed gap')
        # |i - (sqrt(2)-1)L| <= 21, certified by squaring positive endpoints.
        require((i+L-21)**2 < 2*L*L < (i+L+21)**2, 'exact irrational rounding')
        for b in range(2, 101):
            if 12600*b**3 >= L:
                continue  # Even H=2 already exceeds the target.
            require(168*b*b < L, 'rounding error below 1/(8b^2)')
            for a in range(1, b):
                if gcd(a, b) == 1:
                    require(abs(Q(i, L)-Q(a, b)) > Q(1, 6300*b**3), 'uniform majorant gap control')
        family.append({'L': L, 'i': i})

    L, i = 23, 15
    F = 7*10**L-18*10**i-25
    word = ''.join('5' if pos in (0, i) else '7' for pos in range(L-1, -1, -1))
    n = int(word)
    product = 1
    for digit in word:
        product *= int(digit)
    digit_sum = sum(map(int, word))
    require(F == 9*n and product == 25*7**(L-2) and digit_sum == 7*L-4, 'full digit identity')
    require(F % 49 == 0 and F % 343 == 245, 'regression powers')
    require(n % (product*digit_sum) != 0, 'regression is no full witness')

    print(json.dumps({
        'status': 'PASS', 'N': N, 'affine_margins_at_N': margins,
        'fifths_slope': str(fifths_slope),
        'midpoint_fixed_strip': 179, 'midpoint_fixed_margin': str(fixed_margin),
        'open_ratio_intervals': [[str(lo), str(hi)] for lo, hi in gaps],
        'polynomial_identities': identities, 'signed_s_counts': signs,
        'positive_mod7_controls': positives, 'hensel_comparisons': comparisons,
        'gap_family_controls': family,
        'complete_length_coverage_changed': False, 'new_lean_formalization': False,
        'scope': 'Finite arithmetic controls and rigorous constants; no new exhaustive length interval or witness.'
    }, indent=2))


if __name__ == '__main__':
    main()
