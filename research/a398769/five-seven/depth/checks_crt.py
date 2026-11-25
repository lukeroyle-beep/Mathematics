#!/usr/bin/env python3
"""Exact bounded-position criterion checked against decimal words; Python 3.8+."""
import json
from math import gcd


def require(value, message):
    if not value:
        raise RuntimeError(message)


def crt(a, m, b, n):
    g = gcd(m, n)
    if (b-a) % g:
        return None
    factor = n // g
    step = 0 if factor == 1 else ((b-a)//g * pow(m//g, -1, factor)) % factor
    period = m * factor
    return (a + m * step) % period, period


def interval_positions(residue, period, low, high):
    first = low + (residue-low) % period
    count = max(0, 1 + (high-first)//period)
    return first, count


def seven_class(length, depth):
    residue, period, modulus = 3, 6, 7
    require((7*pow(10, length, modulus)-18*pow(10, residue, modulus)-25) % modulus == 0,
            'initial seven class')
    for _ in range(1, depth):
        modulus *= 7
        choices = [residue + step*period for step in range(7)
                   if (7*pow(10, length, modulus)-18*pow(10, residue+step*period, modulus)-25) % modulus == 0]
        require(len(choices) == 1, 'unique exponent lift')
        residue = choices[0]
        period *= 7
    return residue, period


def main():
    require(crt(1, 6, 3, 9) is None, 'incompatible overlap')
    require(crt(1, 6, 4, 9) == (13, 18), 'compatible overlap')
    require(crt(5, 101, 5, 103) == (5, 10403), 'large period small residue')
    require(interval_positions(13, 18, 1, 10) == (13, 0), 'least residue above length')
    require(interval_positions(5, 10403, 1, 10) == (5, 1), 'large period is not exclusion')
    require(interval_positions(41, 1, 42, 41)[1] == 0, 'empty strict interval at L=100')
    checked = comparisons = nonempty = 0
    for length in range(5, 302, 2):
        s = 7*length-4
        if s % 5 == 0:
            continue
        powers = {}
        value, exponent = 1, 0
        while value not in powers:
            powers[value] = exponent
            value = value*10 % s
            exponent += 1
        require(value == 1, 'order cycle starts at identity')
        order = exponent
        target = ((7*((10**length-1)//9)-2) * pow(2, -1, s)) % s
        sum_class = powers.get(target)
        direct = {}
        for position in range(3, length):
            word = '7'*(length-position-1) + '5' + '7'*(position-1) + '5'
            number = int(word)
            direct[position] = number
            require((number % s == 0) == (sum_class is not None and position % order == sum_class),
                    'full digit sum exponent equivalence')
            checked += 1
        for depth in range(1, 5):
            residue, period = seven_class(length, depth)
            merged = None if sum_class is None else crt(sum_class, order, residue, period)
            for low, high in [(3, length-1), (41*length//100+1, (42*length-1)//100)]:
                actual = [i for i, number in direct.items() if low<=i<=high and number % s == 0 and number % 7**depth == 0]
                if merged is None:
                    predicted = []
                else:
                    first, count = interval_positions(*merged, low, high)
                    predicted = [first+j*merged[1] for j in range(count)]
                require(actual == predicted, 'bounded CRT versus decimal enumeration')
                comparisons += 1
                nonempty += bool(actual)
    # Genuine positive sum control and factor-nine failure, not synthetic F.
    for length, position, passes in [(1225,417,True), (313,51,False)]:
        f=7*10**length-18*10**position-25
        require((f % (9*(7*length-4)) == 0) == passes, 'full factor-nine control')
    require(nonempty > 0, 'positive simultaneous controls exercised')
    print(json.dumps({'status':'PASS','decimal_positions':checked,
                      'length_depth_interval_comparisons':comparisons,
                      'nonempty_comparisons':nonempty,'lengths':'odd 5..301 excluding L=2 mod5',
                      'depths':[1,2,3,4], 'new_complete_length_interval':None}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
