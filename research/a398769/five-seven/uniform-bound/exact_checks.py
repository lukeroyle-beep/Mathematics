#!/usr/bin/env python3
"""Exact bounded controls for the uniform-bound investigation; no global search.

Standard library only. All essential checks are explicit and survive -O.
"""
from fractions import Fraction as R
from hashlib import sha256
from math import comb, gcd
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def valuation(n, p=7):
    require(n != 0, 'valuation of zero')
    n = abs(n)
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def K(L):
    require(L >= 5, 'length domain')
    k, period = 1, 6
    while period <= L:
        k, period = k+1, 7*period
    return k


def residue(L, i, modulus):
    return (7*pow(10, L, modulus)-18*pow(10, i, modulus)-25) % modulus


def log_interval(x):
    """60-term rational atanh series after reduction to [1,2]."""
    x = R(x)
    require(x > 0, 'log domain')
    scale = 0
    while x > 2:
        x /= 2
        scale += 1
    while x < 1:
        x *= 2
        scale -= 1

    def unit(y):
        z = (y-1)/(y+1)
        low = 2*sum((z**(2*j+1)/R(2*j+1) for j in range(60)), R(0))
        tail = 2*z**121/(121*(1-z*z))
        return low, low+tail

    lo, hi = unit(x)
    a, b = unit(R(2))
    return (lo+scale*a, hi+scale*b) if scale >= 0 else (lo+scale*b, hi+scale*a)


def cutoff_checks():
    require(6*7**8 == 34588806, 'T9')
    require(K(10000001) == K(34588805) == 9, 'first remaining band')
    require(100000*9**2 == 8100000 < 9999999, 'K9 cutoff')
    require(100000*10**2 == 10000000 < 34588805, 'K10 cutoff')
    rows = []
    for k in range(9, 201):
        Lmin = 10000001 if k == 9 else 6*7**(k-2)+1
        d = 1+252*(k+1)**3
        target = 100000*k*k
        require(target < Lmin-2, 'quadratic comparison')
        require(2*d < Lmin-2, 'uniform strong Hensel comparison')
        require(d+k+1 < Lmin-2, 'dependent root comparison')
        require(7*k*k-(k+1)**2 > 0, 'quadratic induction increment')
        require(7*(k+1)**3-(k+2)**3 > 0, 'cubic induction increment')
        if k <= 10:
            rows.append({'K': k, 'minimum_remaining_odd_L': Lmin,
                         'quadratic_bound': target, 'D_K': d,
                         'quadratic_margin': Lmin-2-target,
                         'strong_Hensel_margin': Lmin-2-2*d,
                         'dependent_margin': Lmin-2-(d+k+1)})
    for L in range(5, 301):
        require(K(L) <= L-2, 'whole-length reduction K<=L-2')
    A, B = 52*10**11-25, 225*(7*12-4)*7**10
    require(A-B == 115445517975 > 0, 'size obstruction base')
    require(21*12 > 61, 'size growth comparison base')
    l7, u7 = log_interval(7)
    l10, u10 = log_interval(10)
    coefficient_upper = 168*u10*u10/l7**4
    require(coefficient_upper < 63 and u7 < 2 and l10 > 2,
            'certified logarithmic constants')
    parameterwise = []
    for b, Delta, expected_k in [(3, 0, 10), (12, 1, 12), (101, 0, 17), (12, 10**9, 21)]:
        H0 = R(Delta, b)+b+1
        k = 10
        while True:
            start = 6*7**(k-2)
            upper = 1+252*(k+1)**2*((k+1)+b**3*H0)
            if start >= b and upper+1 < start:
                break
            k += 1
        require(k == expected_k, 'parameterwise effective threshold')
        parameterwise.append({'b': b, 'Delta': Delta, 'H0': str(H0), 'first_k0': k,
                              'L_start_inclusive': start, 'R_at_k0': str(upper),
                              'earlier_finite_gap_discharged': False})
    return {'base_rows': rows, 'finite_induction_controls_K': [9, 200],
            'fixed_offset_threshold_examples': parameterwise,
            'all_K_argument': 'algebraic induction in LIFTS.md and ANALYTIC.md',
            'size_base_L': 12, 'size_base_difference': A-B,
            'coefficient_upper_less_than': 63,
            'log_7_upper_less_than': 2, 'log_10_lower_greater_than': 2,
            'log_series_terms': 60}


def lift_checks():
    comparisons, zero_digits, nonzero_digits = 0, 0, 0
    digest = sha256()
    for L in range(5, 302, 2):
        r, T = 3, 6
        for j in range(1, 9):
            modulus = 7**(j+1)
            quotient = residue(L, r, modulus)//7**j
            require(residue(L, r, 7**j) == 0, 'previous lift depth')
            require((pow(10, T, modulus)-1)//7**j == 1, 'lift coefficient c_j')
            a = 5*quotient % 7
            roots = [z for z in range(7) if residue(L, r+z*T, modulus) == 0]
            require(roots == [a], 'linearized digit vs exhaustive seven lifts')
            if a:
                nonzero_digits += 1
                require(residue(L, r, modulus) != 0, 'first nonzero digit valuation')
            else:
                zero_digits += 1
            digest.update(f'{L},{j},{r},{a}\n'.encode())
            r += a*T
            T *= 7
            comparisons += 1
        # Exhaustive original-position enumeration gives independent r_K test.
        k = K(L)
        actual = [i for i in range(3, L) if residue(L, i, 7**k) == 0]
        rr, tt = 3, 6
        for j in range(1, k):
            rr += (5*(residue(L, rr, 7**(j+1))//7**j) % 7)*tt
            tt *= 7
        require(actual == ([rr] if 3 <= rr < L else []), 'representative exhaustion')
    require(zero_digits > 0 and nonzero_digits > 0, 'nonvacuous lift controls')
    L = 3955567925893426973231046645818352161
    i = 1648153302455594572179602769090980067
    S = 7*L-4
    require(K(L) == 44 and residue(L, i, 7**45) == 3*7**44,
            'retained depth44 exact certificate')
    require(residue(L, i, 9*S) == 220492367892872959611320275821615897912,
            'depth44 full sum residue')
    require(gcd(residue(L, i, 9*S), S) == 1, 'depth44 gcd')
    a44 = 5*3 % 7
    require(a44 == 1, 'depth44 first escape digit')
    rr, tt, run_digits = 3, 6, []
    for j in range(1, 12):
        digit = 5*(residue(69489, rr, 7**(j+1))//7**j) % 7
        if j >= 6:
            require(rr == 40323, 'constant representative during zero run')
            run_digits.append(digit)
        rr += digit*tt
        tt *= 7
    require(K(69489) == 6 and run_digits == [0, 0, 0, 0, 0, 4], 'zero-run indexing')
    require(residue(69489, 40323, 7**12) == 9886633715 == 5*7**11,
            'zero-run exact valuation')
    require(residue(69489, 40323, 9*(7*69489-4)) == 2218743,
            'zero-run sum premise fails')
    F61 = 7*10**61-18*10**57-25
    C61, remainder = divmod(F61, 225*423)
    require(remainder == 0 and valuation(F61) == valuation(C61) >= 1,
            'nonzero full-sum cofactor control')
    require((5*(F61//7**valuation(F61))) % 7 == (C61//7**valuation(C61)) % 7,
            'cofactor lift digit identity')
    return {'odd_L_domain': [5, 301], 'digit_indices': [1, 8],
            'seven_lift_comparisons': comparisons, 'zero_digits': zero_digits,
            'nonzero_digits': nonzero_digits, 'ordered_sha256': digest.hexdigest(),
            'depth44': {'L': L, 'i': i, 'K': 44, 'v7_F': 44, 'a_44': a44,
                        'F_mod_9S': residue(L, i, 9*S), 'gcd_F_S': 1},
            'zero_run': {'L': 69489, 'i': 40323, 'K': 6, 'v7_F': 11,
                         'digits_a6_through_a11': run_digits, 'F_mod_9S': 2218743},
            'positive_full_sum_control': {'L': 61, 'i': 57, 'S': 423,
                                         'v7_F': valuation(F61), 'K': K(61)}}


def polynomial(L, i, a, b):
    require(0 < a < b and gcd(a, b) == 1, 'reduced centre domain')
    require(3 <= i < L and L >= 5, 'position domain')
    q, r = divmod(L, b)
    s = i-a*q
    m = min(0, s)
    terms = {b: 7*10**(r-m), a: -18*10**(s-m), 0: -25*10**(-m)}
    return q, r, s, m, terms


def evaluate(terms, x):
    return sum(c*x**j for j, c in terms.items())


def strong_root_check(terms, x, t, d):
    require(t > 2*d, 'strong Hensel strict hypothesis')
    step, divisor = 7**(d+1), 7**(2*d+1)
    degree = max(terms)
    transformed = {}
    for k in range(degree+1):
        numerator = sum(c*comb(j, k)*x**(j-k)*step**k
                        for j, c in terms.items() if j >= k)
        require(numerator % divisor == 0, 'integral transformed polynomial')
        transformed[k] = numerator//divisor
    require(transformed[1] % 7 != 0, 'transformed derivative unit')
    require(all(c % 7 == 0 for k, c in transformed.items() if k >= 2),
            'transformed higher coefficients')
    y, modulus = 0, 1
    # The output precision is strictly above the known exact distance.
    for unused in range(max(2, t-2*d+1)):
        roots = [y+z*modulus for z in range(7)
                 if evaluate(transformed, y+z*modulus) % (7*modulus) == 0]
        require(len(roots) == 1, 'unique transformed lift')
        y = roots[0]
        modulus *= 7
    alpha = x+step*y
    require(alpha != x and valuation(alpha-x) == t-d, 'exact Hensel distance')
    require(evaluate(terms, alpha) % (divisor*modulus) == 0, 'root residue')
    return {'t': t, 'd': d, 'distance': t-d, 'precision': (2*d+1)+valuation(modulus)}


def polynomial_checks():
    count, positive, singular, roots = 0, 0, 0, 0
    signs = {'negative': 0, 'zero': 0, 'positive': 0}
    digest = sha256()
    for L in range(5, 62, 2):
        for i in range(3, L):
            F = 7*10**L-18*10**i-25
            t = valuation(F)
            for b in range(2, min(L, 16)+1):
                for a in range(1, b):
                    if gcd(a, b) != 1:
                        continue
                    q, r, s, m, terms = polynomial(L, i, a, b)
                    require(q >= 1, 'positive exponent domain')
                    x = 10**q
                    Q = evaluate(terms, x)
                    derivative = sum(j*c*x**(j-1) for j, c in terms.items() if j)
                    identity = 10**(-m)*(a*F+7*(b-a)*10**L+25*a)
                    require(Q == 10**(-m)*F, 'Q identity')
                    content = gcd(*terms.values())
                    require(content == (2 if s < 0 else 5**min(2, r, s)), 'polynomial content')
                    require(x*derivative == identity, 'derivative identity')
                    d = valuation(derivative)
                    if a % 7:
                        expected = 0
                    elif a % 49 == 0:
                        expected = 1
                    else:
                        expected = 1+valuation(b*10**(L-i)-18*(a//7))
                    require(d == expected, 'three derivative branches')
                    w = max(0, r, s)-m
                    delta = b*i-a*L
                    require(R(abs(delta), b) <= w <= R(abs(delta), b)+b-1,
                            'span both bounds')
                    require(w <= L-1, 'uniform span upper bound')
                    signs['negative' if s < 0 else 'positive' if s > 0 else 'zero'] += 1
                    count += 1
                    positive += int(t > 0)
                    singular += int(t > 0 and d > 0)
                    digest.update(f'{L},{i},{a},{b},{q},{s},{w},{t},{d}\n'.encode())
                    # Bounded nontrivial root-distance controls, both simple and singular.
                    if t > 2*d and (L <= 25 or d > 0):
                        strong_root_check(terms, x, t, d)
                        roots += 1
    controls = []
    for L, i, a, b in [(11, 3, 7, 9), (11, 9, 7, 9), (15, 3, 14, 15),
                        (53, 45, 7, 12), (101, 15, 49, 50)]:
        q, r, s, m, terms = polynomial(L, i, a, b)
        x = 10**q
        t = valuation(evaluate(terms, x))
        d = valuation(sum(j*c*x**(j-1) for j, c in terms.items() if j))
        controls.append({'L': L, 'i': i, 'a': a, 'b': b, 'q': q, 't': t, 'd': d,
                         'strong_Hensel': t > 2*d})
    require(controls[0]['d'] == 2 and controls[1]['d'] == 3,
            'counterexamples to derivative always one')
    require(controls[2]['t'] == controls[2]['d'] == 2,
            'failed strong Hensel control')
    require(controls[4]['d'] == 1, '49-divisible numerator branch')
    q, unused_r, unused_s, unused_m, terms = polynomial(101, 15, 49, 50)
    extra_root = strong_root_check(terms, 10**q, 3, 1)
    q, unused_r, unused_s, unused_m, terms = polynomial(233, 183, 7, 9)
    d2_root = strong_root_check(terms, 10**q, 5, 2)
    require(roots > 0 and singular > 0 and all(signs.values()), 'nonvacuous polynomial controls')
    q0 = polynomial(11, 3, 1, 12)[0]
    require(q0 == 0, 'b>L omitted positive exponent control')
    return {'odd_L_domain': [5, 61], 'position_domain': 'all 3<=i<L',
            'centre_domain': 'all reduced 0<a<b<=min(L,16)',
            'identities': count, 'positive_depth': positive, 'singular_positive_depth': singular,
            's_signs': signs, 'strong_root_checks': roots, 'controls': controls,
            'q_zero_control': [11, 3, 1, 12], 'degree50_singular_root_control': extra_root,
            'derivative_two_root_control': {'L': 233, 'i': 183, 'a': 7, 'b': 9, **d2_root},
            'ordered_sha256': digest.hexdigest()}


def lte_controls():
    count = 0
    for degree_factor in (1, 2, 7, 14, 49):
        for h in (-7, -1, 1, 7):
            y = R(10)**(6*h)
            distance = valuation((y-1).numerator)-valuation((y-1).denominator)
            z = y**(6*degree_factor)-1
            raised = valuation(z.numerator)-valuation(z.denominator)
            require(raised == distance+valuation(degree_factor), 'LTE degree correction')
            require(distance == 1+valuation(6*h*degree_factor)-valuation(degree_factor),
                    'dependent distance identity')
            count += 1
    return {'algebraic_LTE_controls': count, 'degree_factors': [1, 2, 7, 14, 49],
            'signed_h': [-7, -1, 1, 7],
            'scope': 'LTE identity controls; not examples of degree-49 selected roots'}


def order_controls():
    rows = []
    checked = 0
    for L in range(5, 502, 2):
        S = 7*L-4
        if S % 5 == 0:
            continue
        x, d = 10 % S, 1
        while x != 1:
            x = 10*x % S
            d += 1
            require(d <= S, 'order termination')
        e = valuation(d)
        require(e <= K(L)-1, 'inherited stabilization')
        if e:
            require(L >= 12*7**(e-1)+1, 'sharpened stabilization')
        if L in (13, 85):
            rows.append({'L': L, 'S': S, 'order': d, 'e': e, 'K': K(L),
                         'equality_in_new_bound': L == 12*7**(e-1)+1})
        checked += 1
    require(rows == [{'L': 13, 'S': 87, 'order': 28, 'e': 1, 'K': 2,
                     'equality_in_new_bound': True},
                    {'L': 85, 'S': 591, 'order': 98, 'e': 2, 'K': 3,
                     'equality_in_new_bound': True}], 'sharp order controls')
    return {'odd_L_domain': [5, 501], 'five_free_lengths': checked, 'sharp_controls': rows}


def failure_controls():
    labels = []

    def reject(label, action):
        try:
            action()
        except ValueError:
            labels.append(label)
        else:
            raise ValueError('negative control accepted: '+label)

    reject('zero valuation', lambda: valuation(0))
    reject('unreduced centre', lambda: polynomial(11, 3, 2, 4))
    reject('strong Hensel equality t=2d', lambda: strong_root_check({1: 7, 0: 49}, 0, 2, 1))
    reject('removable-assert substitute', lambda: require(False, 'deliberate'))
    reject('factor-nine cancellation', lambda: require(residue(151, 8, 9*1053) == 0,
                                                       'S divides F but 9S does not'))
    require(residue(151, 8, 1053) == 0 and residue(151, 8, 9*1053) == 8424,
            'factor-nine failure fixture')
    reject('depth44 falsely labelled E counterexample',
           lambda: require(residue(3955567925893426973231046645818352161,
                                  1648153302455594572179602769090980067,
                                  9*27688975481253988812617326520728465123) == 0,
                           'full digit-sum premise fails'))
    return labels


def main():
    result = {'status': 'PASS', 'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'cutoff': cutoff_checks(), 'lifts': lift_checks(),
              'polynomials': polynomial_checks(), 'orders': order_controls(), 'LTE': lte_controls(),
              'negative_controls_rejected': failure_controls(),
              'new_whole_length_coverage': [],
              'new_position_theorems': 'ANALYTIC (12), (13a)-(13c); no global cover',
              'new_Lean_claim': False}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
