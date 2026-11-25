#!/usr/bin/env python3
"""Exact controls for the submitted infinite family, not a full-witness search."""
from fractions import Fraction
from math import gcd, lcm
import json

C = 898129
D = 56133
CONTROL_L = 15582704697570091495948156638491914590405161120787807516829906317314612303918977615165179656913553
CONTROL_I = 6477065490626893175017379503058848761317334778884442403179846853582090755525695000140054741394429


def require(condition, detail):
    if not condition:
        raise ArithmeticError(detail)


def f_mod(length, position, modulus):
    return (7*pow(10, length, modulus)-18*pow(10, position, modulus)-25) % modulus


def word_mod(length, position, modulus):
    """Concatenate the four decimal blocks 7...7, 5, 7...7, 5.

    The repunit residue uses division in integers modulo 9*modulus;
    it never cancels 9 modulo a possibly non-coprime modulus.
    """
    value = 0
    for digit, count in ((7, length-position-1), (5, 1), (7, position-1), (5, 1)):
        require(count >= 0, 'nonnegative block length')
        power = pow(10, count, 9*modulus)
        require(power % 9 == 1, 'exact repunit division')
        repunit = (power-1)//9
        value = (value*(power % modulus)+digit*repunit) % modulus
    return value


def combine(left, right):
    """Generalized CRT, returning the least representative and spacing."""
    r, m = left
    s, n = right
    g = gcd(m, n)
    require((s-r) % g == 0, 'compatible CRT classes')
    step = ((s-r)//g * pow(m//g, -1, n//g)) % (n//g) if n//g != 1 else 0
    period = lcm(m, n)
    return (r+m*step) % period, period


def three_exponent(length, exponent):
    """Lift the unique exponent modulo 3**(exponent-2), checking each digit."""
    require(exponent >= 2, 'three exponent domain')
    modulus = 3**exponent
    numerator = 7*pow(10, length, 9*modulus)-25
    require(numerator % 9 == 0, 'integer division before modular inversion')
    target = (numerator//9 * pow(2, -1, modulus)) % modulus
    require(target % 9 == 1, 'target subgroup membership')
    residue, step, level = 0, 1, 9
    for _ in range(exponent-2):
        level *= 3
        candidates = [residue+j*step for j in range(3)
                      if pow(10, residue+j*step, level) == target % level]
        require(len(candidates) == 1, 'unique ternary lift')
        residue = candidates[0]
        step *= 3
    require(pow(10, residue, modulus) == target, 'final ternary lift')
    return residue, step


def seven_exponent(length, depth):
    require(depth >= 1, 'positive seven depth')
    modulus, period = 7, 6
    candidates = [r for r in range(period) if f_mod(length, r, modulus) == 0]
    require(len(candidates) == 1, 'primitive root at seven')
    residue = candidates[0]
    for _ in range(1, depth):
        modulus *= 7
        candidates = [residue+j*period for j in range(7)
                      if f_mod(length, residue+j*period, modulus) == 0]
        require(len(candidates) == 1, 'unique seven lift')
        residue = candidates[0]
        period *= 7
    return residue, period


def family_class(exponent, depth):
    require(exponent >= 193 and (exponent-193) % 1470 == 0, 'submitted exponent progression')
    total = C*3**exponent
    require((total+4) % 7 == 0, 'integral length')
    length = (total+4)//7
    three = three_exponent(length, exponent)
    seven = seven_exponent(length, depth)
    residue, spacing = combine(combine((11337, D), three), seven)
    # Strict lower endpoint: floor((41L-100r)/(100W))+1 steps.
    steps = (41*length-100*residue)//(100*spacing)+1
    position = residue+steps*spacing
    return length, position, residue, spacing, 100*position < 42*length


def inherited(length, position):
    require(length > 10_000_000 and length % 2 == 1, 'length domain')
    require(3 <= position < length and position % 6 == 3, 'position domain')
    require((length % 6, position % 42) == (1, 39), 'modulo-49 table')
    require(position >= 417 and length-position >= 396, 'inherited endpoint bounds')
    for prime, excluded in ((5, 2), (11, 10), (13, 8), (37, 27), (101, 15)):
        require(length % prime != excluded, 'inherited length filter '+str(prime))
    require(100*position > 41*length and 100*position < 42*length, 'open ratio interval')
    require(25000*position > length and 25000*(length-position) > length, 'edge strips')
    require(300000*abs(length-3*position) > length, 'one-third strip')
    require(60000*abs(length-2*position) > length and abs(length-2*position) >= 181,
            'midpoint strips')
    require(300000*abs(2*length-3*position) > length, 'two-thirds strip')
    require(2000000*abs(5*position-2*length) > length, 'two-fifths strip')
    require(2000000*abs(5*position-3*length) > length, 'three-fifths strip')


def main():
    a = 193
    total = C*3**a
    length = (total+4)//7
    require(D == 3**6*7*11, 'd factorization')
    require(length == CONTROL_L, 'submitted length')
    require((total+4) % 7 == 0, 'initial divisibility by seven')
    require((length % D, length % 294) == (11248, 97), 'initial length residues')
    require(7*lcm(D, 294) == 3**6*7546, 'length period modulus')
    require(pow(3, 1470, 7546) == 1, 'exponent progression period')
    require((pow(10, D, C), pow(10, 11248, C), pow(10, 11337, C)) == (1, 508973, 597101),
            'c power residues')
    require(tuple(pow(10, D//p, C) for p in (3, 7, 11)) == (66723, 631165, 615263),
            'exact order modulo c')
    require((7*508973-18*597101-25) % C == 0, 'c congruence')
    require((pow(10, 97, 2401), pow(10, 1635, 2401)) == (2159, 1105), 'seven residues')
    require(pow(10, 2058, 2401) == 1 and pow(10, 294, 343) == 1, 'seven exponent periods')
    require(7*2159-18*1105-25 == -4802, 'seven residue identity')
    require(length % 6561 == 4687, 'three-adic length overlap')
    require((pow(10, 4687, 59049), pow(10, 402, 59049)) == (42427, 49303),
            'three power residues')
    require((7*42427-18*49303-25) % 59049 == 0, 'three overlap identity')
    require(gcd(D, 2058) == 21 and 11337 % 21 == 1635 % 21, 'first CRT overlap')
    require(11337 % 729 == 402 and 1635 % 3 == 402 % 3, 'ternary CRT overlaps')
    pairwise = (C, 3**(a+2), 7**4, 25)
    require(all(gcd(x,y) == 1 for j,x in enumerate(pairwise) for y in pairwise[j+1:]),
            'pairwise coprime factors')
    require(700*7546 < 9*C, 'strict interval spacing constant')
    require(all(C % p for p in (5,11,13,37,101)), 'all inherited S factors avoided')
    generated_length, position, residue, spacing, exists = family_class(a, 4)
    require(exists and generated_length == length, 'constructed interval representative')
    require(spacing == 7546*3**(a-2) and 100*spacing < length, 'exact CRT spacing')
    require(CONTROL_I % spacing == residue, 'submitted representative belongs to class')
    require(CONTROL_I == position, 'submitted representative is first above lower endpoint')
    inherited(length, CONTROL_I)
    full_truncated = 225*7**4*total
    require(f_mod(length, CONTROL_I, 9*total) == 0, 'full digit-sum F control')
    require(f_mod(length, CONTROL_I, 7**5) == 9604, 'exact seven valuation four')
    require(f_mod(length, CONTROL_I, full_truncated) == 0, 'combined F divisor')
    require(word_mod(length, CONTROL_I, 25*7**4*total) == 0, 'decimal blocks combined divisor')
    require(9*word_mod(length, CONTROL_I, 7**5) % 7**5 == 9604,
            'decimal blocks exact seven valuation')
    for small_length in range(5, 24, 2):
        for small_position in range(3, small_length):
            word = '7'*(small_length-small_position-1)+'5'+'7'*(small_position-1)+'5'
            require(len(word) == small_length, 'small word length')
            for modulus in (9, 25, 49, 343, 9*(7*small_length-4)):
                require(word_mod(small_length, small_position, modulus) == int(word) % modulus,
                        'literal word comparison')
    # Old rounded-family negative control and preserved (23,15) regression.
    require(f_mod(16031731, 6640575, 343) == 147, 'rounded-family seven control')
    require(f_mod(16031731, 6640575, 9*(7*16031731-4)) == 123356871,
            'rounded-family full sum control')
    regression_n = int('7'*(23-15-1)+'5'+'7'*(15-1)+'5')
    require(9*regression_n % 49 == 0 and 9*regression_n % 343 == 245,
            '(23,15) exact inherited regression')
    require(regression_n % (25*7**21*(7*23-4)) != 0, '(23,15) remains no full witness')
    print(json.dumps({
        'status': 'PASS', 'a': a, 'length': str(length), 'position': str(CONTROL_I),
        'spacing': str(spacing), 'least_crt_representative': str(residue),
        'spacing_over_length_upper_bound': str(Fraction(7*7546,9*C)),
        'full_digit_sum_remainder': 0, 'F_mod_16807': 9604,
        'exact_7_adic_valuation': 4, 'full_witness': False,
        'complete_length_coverage': [1, 10_000_000],
        'scope': 'exact controls for an ordinary infinite-family proof; no new exhaustive interval'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
