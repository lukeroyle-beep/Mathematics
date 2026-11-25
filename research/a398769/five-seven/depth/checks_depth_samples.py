#!/usr/bin/env python3
"""Exhaust all full-digit-sum positions at the supplied a=193 length.

This standalone exact check imports no project checker.  It constructs the
complete exponent class, bounds its actual representatives, and independently
checks every resulting word by concatenating its four constant-digit blocks.
No decimal word of length L, and no integer F of that size, is allocated.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from math import gcd
from pathlib import Path

C = 898129
D = 56133
A = 193
CONTROL_L = 15582704697570091495948156638491914590405161120787807516829906317314612303918977615165179656913553
CONTROL_I = 6477065490626893175017379503058848761317334778884442403179846853582090755525695000140054741394429


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def f_remainder(length, position, modulus):
    return (7 * pow(10, length, modulus)
            - 18 * pow(10, position, modulus) - 25) % modulus


def block_word_remainder(length, position, modulus):
    """Concatenate [7]*(L-i-1), [5], [7]*(i-1), [5] modulo modulus.

    The integer division in the repunit formula is done modulo 9*modulus,
    so this also works when 3 divides modulus.  This does not evaluate F/9.
    """
    value = 0
    for digit, count in ((7, length-position-1), (5, 1),
                         (7, position-1), (5, 1)):
        require(count >= 0, 'negative block length')
        power = pow(10, count, 9*modulus)
        require((power-1) % 9 == 0, 'repunit division is exact')
        value = (value*power + digit*((power-1)//9)) % modulus
    return value


def three_log(target, exponent):
    """Recover the exponent of 10 by ternary digits, in O(exponent) products.

    For g=10**(3**j), LTE gives (g-1)/3**(j+2)=1 (mod 3).
    This determines the next digit without recomputing a large modular power.
    """
    modulus = 3**exponent
    require(exponent >= 2 and target % 9 == 1, 'three-log domain')
    residue, value, generator, place, precision = 0, 1, 10, 1, 9
    for _ in range(exponent-2):
        require((target-value) % precision == 0, 'lift input precision')
        require((generator-1) % precision == 0, 'generator precision')
        require(((generator-1)//precision) % 3 == 1, 'generator leading unit')
        digit = ((target-value)//precision) % 3
        residue += digit*place
        value = value*pow(generator, digit, modulus) % modulus
        require((target-value) % (3*precision) == 0, 'lift output precision')
        generator = pow(generator, 3, modulus)
        place *= 3
        precision *= 3
    require(place == 3**(exponent-2), 'exponent class period')
    require(pow(10, residue, modulus) == target, 'three-log direct readback')
    return residue, place


def merge_classes(r, m, s, n):
    common = gcd(m, n)
    require((s-r) % common == 0, 'compatible sum exponent classes')
    modulus = m*(n//common)
    multiplier = ((s-r)//common * pow(m//common, -1, n//common)) % (n//common)
    residue = (r+m*multiplier) % modulus
    require(residue % m == r % m and residue % n == s % n,
            'CRT direct readback')
    return residue, modulus


def valuation_from_nonzero_residue(residue, prime):
    require(residue != 0, 'valuation precision exhausted')
    depth = 0
    while residue % prime == 0:
        residue //= prime
        depth += 1
    return depth


def direct_controls():
    comparisons = 0
    for length in range(5, 31):
        for position in range(3, length):
            decimal = ('7'*(length-position-1)+'5'+'7'*(position-1)+'5')
            integer = int(decimal)
            require(9*integer == 7*10**length-18*10**position-25,
                    'small direct decimal identity')
            for modulus in (7, 49, 343, 16807, 9, 81, 7*length-4):
                require(block_word_remainder(length, position, modulus)
                        == integer % modulus, 'small direct word remainder')
                comparisons += 1
    for exponent in range(2, 9):
        period = 3**(exponent-2)
        for residue in range(min(period, 100)):
            require(three_log(pow(10, residue, 3**exponent), exponent)
                    == (residue, period), 'small logarithm inversion')
    require(f_remainder(23, 15, 49) == 0, '(23,15) inherited seven control')
    require(f_remainder(23, 15, 9*(7*23-4)) != 0,
            '(23,15) is not a full digit-sum witness')
    return comparisons


def run():
    comparisons = direct_controls()
    length = (C*3**A+4)//7
    digit_sum = 7*length-4
    require(length == CONTROL_L and digit_sum == C*3**A, 'exact sample length')
    require(gcd(C, 3) == 1 and gcd(10, C) == 1, 'coprime sum components')
    require(D == 3**6*7*11, 'complete factorization of exponent period')
    require(pow(10, D, C) == 1, 'period modulo c')
    proper_powers = {str(p): pow(10, D//p, C) for p in (3, 7, 11)}
    require(all(value != 1 for value in proper_powers.values()),
            'order modulo c is exactly d')
    require(f_remainder(length, 11337, C) == 0, 'unique exponent class modulo c')

    power = 3**A
    numerator = 7*pow(10, length, 9*power)-25
    require(numerator % 9 == 0, 'division before inversion')
    target = numerator//9 * pow(2, -1, power) % power
    residue3, period3 = three_log(target, A)
    residue, spacing = merge_classes(residue3, period3, 11337, D)
    require(spacing == 77*3**(A-2), 'complete sum-class spacing')
    first = residue + ((3-residue+spacing-1)//spacing)*spacing
    last = residue + ((length-1-residue)//spacing)*spacing
    count = (last-first)//spacing+1
    require(3 <= first <= last < length, 'actual position endpoints')
    require(first-spacing < 3 and last+spacing >= length, 'complete position endpoints')

    precision = 10
    modulus7 = 7**precision
    histogram = Counter()
    odd_histogram = Counter()
    regional_histogram = Counter()
    positions = []
    digest = sha256()
    # Direct F modular powers establish all exact valuations.  A nonzero residue
    # modulo 7**10 is required for every position; otherwise this check stops.
    for position in range(first, last+1, spacing):
        require(f_remainder(length, position, 9*digit_sum) == 0,
                'full digit-sum congruence')
        depth = valuation_from_nonzero_residue(
            f_remainder(length, position, modulus7), 7)
        histogram[depth] += 1
        if position % 6 == 3:
            odd_histogram[depth] += 1
        if 41*length < 100*position < 42*length:
            regional_histogram[depth] += 1
        positions.append((position, depth))
        digest.update(f'{position}:{depth}\n'.encode())
    maximum = max(histogram)
    require(sum(histogram.values()) == count, 'all sum positions enumerated')
    require(maximum < length-2, 'full witness growing power is absent')

    # Independent decimal construction for every position, at the full sum
    # modulus and at a modulus exceeding the observed maximum valuation.
    check_modulus = 7**(maximum+1)
    for position, depth in positions:
        require(block_word_remainder(length, position, digit_sum) == 0,
                'independent decimal sum check')
        require(valuation_from_nonzero_residue(
            block_word_remainder(length, position, check_modulus), 7) == depth,
            'independent decimal exact valuation')
    control_depth = dict(positions)[CONTROL_I]
    require(control_depth == 4, 'supplied control valuation')
    require(f_remainder(length, CONTROL_I, 16807) == 9604,
            'supplied control remainder')
    return {
        'status': 'passed',
        'scope': 'all residual positions 3<=i<L at the single displayed length',
        'a': A, 'c': C, 'length': str(length),
        'complete_length_coverage_unchanged': [1, 10000000],
        'additional_isolated_length_excluded': str(length),
        'full_digit_sum_exponent_class': {
            'least_residue': str(residue), 'spacing': str(spacing),
            'first_position': str(first), 'last_position': str(last),
            'count': count, 'exact_order_mod_c': D,
            'proper_divisor_power_controls': proper_powers},
        'valuation_histogram': dict(sorted(histogram.items())),
        'admissible_i_3_mod_6_histogram': dict(sorted(odd_histogram.items())),
        'open_ratio_41_100_to_42_100_histogram': dict(sorted(regional_histogram.items())),
        'maximum_valuation': maximum,
        'maximal_positions': [str(i) for i, v in positions if v == maximum],
        'control_valuation': control_depth,
        'valuation_modulus_exponent': precision,
        'independent_word_modulus_exponent': maximum+1,
        'independent_word_positions_checked': count,
        'small_direct_word_comparisons': comparisons,
        'ordered_position_depth_sha256': digest.hexdigest(),
        'limits': ['No all-t bound is claimed.',
                   'No complete interval above ten million is certified.',
                   'No Lean theorem or build is claimed.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(encoded, encoding='utf-8')
    print(encoded, end='')
