#!/usr/bin/env python3
"""Exact fixed-position index lifting and independent ternary controls.

No research arithmetic is imported. All checks remain active under -O.
"""
from hashlib import sha256
import json
from math import gcd
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ArithmeticError(message)


def valuation(n, prime):
    need(n != 0, 'finite valuation requires a nonzero integer')
    result = 0
    while n % prime == 0:
        n //= prime
        result += 1
    return result


def f_mod(u, s, m):
    """F(L_u,s) mod 7^m without constructing the exponential length.

    The factor seven lowers the precision needed for 10^L. The residue
    of 3^a is obtained modulo SEVEN TIMES the exponent modulus, before
    the exact division by seven. m>=2 throughout the index construction.
    """
    need(u >= 0 and s >= 0 and m >= 2, 'index domain')
    order = 6 * 7**(m-2)
    numerator = pow(3, 31+6*u, 7*order) + 4
    need(numerator % 7 == 0, 'length residue division')
    length_residue = numerator//7
    modulus = 7**m
    return (7*pow(10, length_residue, modulus)
            - 18*pow(10, s, modulus) - 25) % modulus


def f_direct(u, s, m):
    """Independent direct exponentiation at manageable integer indices."""
    length = (3**(31+6*u)+4)//7
    modulus = 7**m
    return (7*pow(10, length, modulus)
            - 18*pow(10, s, modulus) - 25) % modulus


def roots(s, maximum):
    need(s >= 0 and s % 42 == 39 and maximum >= 2, 'fixed-s root domain')
    residue, period = 0, 1
    result = [dict(depth=2, residue=0, modulus=1)]
    for m in range(2, maximum):
        need(f_mod(residue, s, m) == 0, 'parent survives')
        carry = f_mod(residue, s, m+1)//7**m
        digit = (-4*carry) % 7  # inverse of the constant slope 2 modulo 7
        children = [c for c in range(7)
                    if f_mod(residue+c*period, s, m+1) == 0]
        need(children == [digit], 'digit formula versus all seven children')
        for c in range(7):
            change = (f_mod(residue+c*period, s, m+1)
                      - f_mod(residue, s, m+1)) % 7**(m+1)
            need(change//7**m == 2*c % 7, 'constant digit slope')
        residue += digit*period
        period *= 7
        result.append(dict(depth=m+1, residue=residue, modulus=period,
                           digit=digit, carry=carry))
    return result


def ternary_position(a):
    """Recover kappa using a direct seventh-root exponent and digit lifting.

    This does not import the inherited Newton/log engine or either new
    individual engine. The target retains both precision losses by nine.
    """
    need(a >= 7 and a % 6 == 1, 'integral odd-length family')
    modulus, d = 3**a, 3**(a-2)
    theta_modulus = 9*modulus
    exponent = 4*pow(7, -1, modulus) % modulus
    theta = pow(10, exponent, theta_modulus)
    need(pow(theta, 7, theta_modulus) == 10000 % theta_modulus,
         'seventh-root readback')
    numerator = (7*theta-25) % theta_modulus
    need(numerator % 9 == 0, 'C division precision')
    target = numerator//9 * pow(2, -1, modulus) % modulus
    r, value, increment, order = 0, 1, 10, 1
    digit_modulus = 27
    for _ in range(a-2):
        options = [c for c in range(3)
                   if value*pow(increment, c, digit_modulus) % digit_modulus
                   == target % digit_modulus]
        need(len(options) == 1, 'unique ternary digit')
        c = options[0]
        r += c*order
        value = value*pow(increment, c, modulus) % modulus
        increment = pow(increment, 3, modulus)
        order *= 3
        digit_modulus *= 3
    need(order == d and value == target and pow(10, r, modulus) == target,
         'ternary class readback')
    s = r if r % 2 else r+d
    length = (modulus+4)//7
    need(3 <= s < 2*d and s % 6 == 3 and
         (7*pow(10, length, 9*modulus)-18*pow(10, s, 9*modulus)-25)
         % (9*modulus) == 0, 'same-position full 9S condition')
    common = gcd(length, s)
    p, q = s//common, length//common
    need((7*q*r-4*p) % d == 0, 'rational ternary relation')
    return dict(a=a, u=(a-31)//6, L=length, s=s, actual=s < length,
                g=common, p=p, q=q, q_fourth_exceeds_L=q**4 > length,
                s_mod_42=s % 42, s_mod_126=s % 126,
                s_mod_294=s % 294, ternary_relation_mod_d=0)


def main():
    direct_comparisons = 0
    depth_two_cases = 0
    for u in range(49):
        for s in range(294):
            need((f_direct(u, s, 2) == 0) == (s % 42 == 39),
                 'depth-two iff')
            need((f_direct(u, s, 3) == 0) ==
                 (s % 294 == (123+126*u) % 294), 'depth-three iff')
            depth_two_cases += 1
    for u in range(60):
        for s in (0, 3, 39, 81, 123, 165, 207, 249, 291, 333):
            for m in range(2, 9):
                need(f_mod(u, s, m) == f_direct(u, s, m),
                     'reduced exponent versus direct exponentiation')
                direct_comparisons += 1
    differences = 0
    for u in range(100):
        for v in range(u):
            t = 2+valuation(u-v, 7)
            delta = (f_direct(u, 39, t+1)-f_direct(v, 39, t+1)) % 7**(t+1)
            need(delta != 0 and valuation(delta, 7) == t,
                 'difference exact valuation')
            differences += 1
    permutation_checks = []
    for s in (39, 81, 123, 165, 207, 249, 291):
        for j in range(1, 4):
            period = 7**j
            images = [f_direct(u, s, j+2)//49 for u in range(period)]
            need(sorted(images) == list(range(period)), 'complete permutation')
            root = roots(s, j+2)[-1]['residue']
            need([u for u, value in enumerate(images) if value == 0] == [root],
                 'digit lift agrees with full direct enumeration')
            permutation_checks.append(dict(s=s, j=j, classes=period, root=root))
    lift_controls = [dict(s=s, roots=roots(s, 10)) for s in (39, 123, 291)]
    actual_controls = []
    for a in (97, 1231, 1573, 1579):
        row = ternary_position(a)
        u, s = row['u'], row['s']
        row['F_mod_7_powers'] = [f_direct(u, s, m) for m in range(2, 7)]
        if s % 42 == 39:
            row['index_roots'] = roots(s, 8)
            row['index_mismatches'] = [entry['depth'] for entry in row['index_roots']
                                       if u % entry['modulus'] != entry['residue']]
            for entry in row['index_roots']:
                need((u % entry['modulus'] == entry['residue']) ==
                     (f_direct(u, s, entry['depth']) == 0),
                     'actual ternary position versus fixed-s index class')
        actual_controls.append(row)
    by_a = {row['a']: row for row in actual_controls}
    need(by_a[1231]['actual'] and by_a[1231]['F_mod_7_powers'][:3] == [0, 0, 0]
         and by_a[1231]['F_mod_7_powers'][3] != 0,
         'actual depth-four positive control')
    need(not by_a[1573]['actual'] and by_a[1573]['s_mod_126'] == 123,
         '1573 class miss despite shallow residue')
    need(by_a[1579]['actual'] and by_a[1579]['F_mod_7_powers'][0]
         * pow(9, -1, 49) % 49 == 14, '1579 actual first failure')
    result = dict(schema=1, status='PASS',
                  source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  depth_two_and_three_cases=depth_two_cases,
                  direct_exponentiation_comparisons=direct_comparisons,
                  exact_difference_pairs=differences,
                  complete_permutations=permutation_checks,
                  digit_lift_controls=lift_controls,
                  ternary_controls=actual_controls,
                  scope='Finite controls only; no moving-position escape theorem.')
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
