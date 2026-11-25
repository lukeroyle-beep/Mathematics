#!/usr/bin/env python3
"""Fresh review: Newton doubling, coefficient discrete logs, and exact controls.

Imports no submitted checker. Discovery never reads submitted representatives.
The finite controls support, but do not replace, the reviewed all-length proof.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def ensure(condition, message):
    if not condition:
        raise ArithmeticError(message)


def f(length, position, modulus):
    return (7*pow(10, length, modulus)-18*pow(10, position, modulus)-25) % modulus


def valuation(n):
    ensure(n != 0, 'valuation of zero')
    n = abs(n)
    k = 0
    while n % 7 == 0:
        k, n = k+1, n//7
    return k


def newton_root(a, b, depth):
    def poly(x, modulus):
        return (a*pow(x, 12, modulus)-b*pow(x, 5, modulus)-1) % modulus

    roots = [x for x in range(7) if poly(x, 7) == 0]
    ensure(len(roots) == 1, 'initial polynomial roots')
    root, k = roots[0], 1
    trace = [{'depth': k, 'root': root}]
    while k < depth:
        new_k = min(2*k, depth)
        modulus = 7**new_k
        derivative = (12*a*pow(root, 11, modulus)-5*b*pow(root, 4, modulus)) % modulus
        ensure(derivative % 7 != 0, 'Newton derivative')
        lifted = (root-poly(root, modulus)*pow(derivative, -1, modulus)) % modulus
        ensure(lifted % 7**k == root and poly(lifted, modulus) == 0,
               'Newton doubling failed')
        root, k = lifted, new_k
        trace.append({'depth': k, 'root': root})
    return root, trace


def discrete_log(root, depth):
    """Read base-seven digits of the principal exponent by linear coefficients."""
    residue_classes = [e for e in range(6) if pow(10, e, 7) == root % 7]
    ensure(len(residue_classes) == 1, 'initial logarithm residue')
    e = residue_classes[0]
    a = 0
    for j in range(depth-1):
        step, scale, modulus = 7**j, 7**(j+1), 7**(j+2)
        y = root*pow(pow(10, e, modulus), -1, modulus) % modulus
        remaining = y*pow(pow(10**6, a, modulus), -1, modulus) % modulus
        generator = pow(10**6, step, modulus)
        ensure((remaining-1) % scale == 0 and (generator-1) % scale == 0,
               'principal coefficient precision')
        coefficient = (generator-1)//scale
        digit = ((remaining-1)//scale)*pow(coefficient, -1, 7) % 7
        a += digit*step
        ensure(pow(10, e+6*a, modulus) == root % modulus, 'coefficient log digit')
    u, period = e+6*a, 6*7**(depth-1)
    ensure(0 <= u < period and pow(10, u, 7**depth) == root, 'complete logarithm')
    return u


def line_check(offset, depth):
    a, b = (28000, 72) if offset == 5 else (2800000, 720)
    root, trace = newton_root(a, b, depth)
    u_final = discrete_log(root, depth)
    records, exceptions = [], []
    for k in range(1, depth+1):
        period, modulus = 6*7**(k-1), 7**k
        u = u_final % period
        length, position = 12*u+offset, 5*u+(offset-1)//2
        ensure(f(length, position, modulus) == 0, 'original predicate')
        ensure(pow(10, period, modulus) == 1, 'period')
        for prime in ([2, 3] if k == 1 else [2, 3, 7]):
            ensure(pow(10, period//prime, modulus) != 1, 'exact order')
        own_band = u >= 1 and (0 if k == 1 else period//7) <= length < period
        records.append({'k': k, 'u': u, 'root': root % modulus, 'in_own_band': own_band})
        if offset == 5 and own_band:
            total = 7*length-4
            next_residue = f(length, position, modulus*7)
            ensure(next_residue != 0, 'exact candidate valuation')
            digit_sum_residue = f(length, position, 9*total)
            exceptions.append({'k': k, 'u': u, 'L': length, 'i': position,
                               'S': total, 'F_mod_9S': digit_sum_residue,
                               'gcd_F_S': gcd(digit_sum_residue, total),
                               'next_residue_coefficient': next_residue//modulus})
    # Exhaust the original predicate over the complete small period.
    brute = [u for u in range(6*7**4)
             if f(12*u+offset, 5*u+(offset-1)//2, 7**5) == 0]
    ensure(brute == [u_final % (6*7**4)], 'direct exhaustive depth-five check')
    return records, exceptions, trace


def log_bounds(x):
    """Alternating log(1+z), with scaling by 3/2; z stays in [0,1/2]."""
    x = Q(x)
    ensure(x >= 1, 'log domain')
    shifts = 0
    while x > Q(3, 2):
        shifts += 1
        x *= Q(2, 3)

    def small(z):
        lower = sum(((-1)**(j+1)*z**j/j for j in range(1, 33)), Q(0))
        return lower, lower+z**33/33

    lo, hi = small(x-1)
    base_lo, base_hi = small(Q(1, 2))
    return lo+shifts*base_lo, hi+shifts*base_hi


def strip_controls():
    n = 10**9
    lo7, hi7 = log_bounds(7)
    lo10, hi10 = log_bounds(10)
    ensure(168*hi10**2/lo7**4 < 63, 'BL prefactor')
    first = log_bounds((Q(n, 168)+1)/lo10)[1]+log_bounds(hi7)[1]+Q(2, 5)
    ensure(first < 16 and 10*hi7 < 20 and Q(10) < 20, 'all maximum entries')
    slope = Q(63*12**3*14*20**2, n)
    ensure(slope == Q(47628, 78125) and (1-slope)*n-3 == 390361597,
           'strong Hensel additive loss and margin')
    controls = []
    for length, position in [(17, 15), (81, 3), (233, 183)]:
        q, r = divmod(length, 12)
        s = position-7*q
        m = min(s, 0)
        x = 10**q
        coefficients = (7*10**(r-m), -18*10**(s-m), -25*10**(-m))
        t = valuation(7*10**length-18*10**position-25)
        modulus = 7**(t+2)
        aa, bb, cc = coefficients
        # Exhaust Q itself in x+49 Z modulo this modulus. There are seven
        # modular roots; uniqueness is for the p-adic root, not these residues.
        roots = [z for z in range(x % 49, modulus, 49)
                 if (aa*pow(z, 12, modulus)+bb*pow(z, 7, modulus)+cc) % modulus == 0]
        ensure(len(roots) == 7, 'singular modular root multiplicity')
        ensure(all(valuation((x-z) % modulus) == t-1 for z in roots),
               'exact strong Hensel distance')
        ensure(all(valuation((12*aa*pow(z, 11, 49)+7*bb*pow(z, 6, 49)) % 49) == 1
                   for z in roots), 'derivative at lifted roots')
        controls.append({'L': length, 'i': position, 't': t, 'modulus': modulus,
                         'roots_in_local_class': len(roots), 'exact_distance': t-1})
    return {'independent_slope': str(slope), 'strict_margin_at_N': 390361597,
            'log_method': '32-term alternating series scaled by 3/2',
            'direct_singular_root_controls': controls}


def main():
    minus, exceptions, minus_newton = line_check(5, 100)
    plus, unused, plus_newton = line_check(7, 11)
    ensure([r['k'] for r in exceptions] == [44, 56, 85, 92], 'exception depths')
    ensure(all(r['gcd_F_S'] == 1 and r['S'] % 5 for r in exceptions), 'exception sum test')
    # Submitted receipts enter only here, after independent discovery.
    for name in ('depth_exponents', 'depth_roots'):
        receipt = json.loads((HERE / (name+'.json')).read_text())
        ensure(len(receipt['history']) == 100, 'complete submitted history')
        for actual, submitted in zip(minus, receipt['history']):
            for key in ('k', 'u', 'in_own_band'):
                ensure(actual[key] == submitted[key], 'submitted minus history')
            if 'root' in submitted:
                ensure(actual['root'] == submitted['root'], 'submitted root')
        ensure(exceptions == [{key: r[key] for key in exceptions[0]} for r in receipt['exceptions']],
               'submitted exception arithmetic')
    opposite = json.loads((HERE / 'opposite.json').read_text())
    ensure(plus[-1]['u'] == opposite['observed']['u'] == 313281594, 'opposite class')
    ensure(12*plus[-1]['u']+7 == 3759379135, 'opposite least length')
    ensure(f(3759379135, 1566407973, 7**12) == 6*7**11, 'opposite exact depth')
    for actual, submitted in zip(plus, opposite['exponent_route']):
        ensure(actual['u'] == submitted['classes'][0], 'opposite intermediate class')
    negative_controls = 0
    for condition in (False, f(12*5+5, 5*5+2, 49) == 0,
                      exceptions[0]['F_mod_9S'] == 0, plus[-1]['u'] == 313281595):
        try:
            ensure(condition, 'deliberate false control')
        except ArithmeticError:
            negative_controls += 1
    ensure(negative_controls == 4, 'guards remain active')
    print(json.dumps({'verdict': 'PASS',
        'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'discovery': 'Newton doubling and principal-unit coefficient discrete log',
        'minus_depths_checked': 100, 'minus_exceptions': exceptions,
        'minus_newton_trace': minus_newton, 'plus_newton_trace': plus_newton,
        'opposite_u': plus[-1]['u'], 'opposite_period': 6*7**10,
        'opposite_least_L': 3759379135,
        'direct_exhaustive_depth5_classes_per_line': 6*7**4,
        'strip': strip_controls(), 'negative_controls_rejected': negative_controls,
        'scope': 'independent finite arithmetic and controls; no new whole-length search'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
