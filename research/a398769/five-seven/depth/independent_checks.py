#!/usr/bin/env python3
"""Independent exact audit of the period-42 prime sieve and digit controls.

Only Python's standard library is required. All checks survive ``python -O``.
No finite exhaustive length certificate is claimed by these targeted tests.
"""
import json
from math import gcd, isqrt, prod


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def prime_trial(n):
    """Deterministic division by every possible divisor <= sqrt(n)."""
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def blocks(length, position, modulus):
    """Evaluate the four decimal blocks modulo modulus by concatenation.

    Doubling a repunit uses R_(2m) = R_m*(10^m+1). This path never
    uses F, a geometric-series division, or modular inverses.
    """
    require(0 < position < length, "invalid decimal position")

    def repunit(count):
        value, power = 0, 1
        for bit in bin(count)[2:]:
            value = value * (power + 1) % modulus
            power = power * power % modulus
            if bit == '1':
                value = (10 * value + 1) % modulus
                power = 10 * power % modulus
        return value, power

    left, _ = repunit(length - position - 1)
    right, right_power = repunit(position - 1)
    return (((7 * left * 10 + 5) * right_power + 7 * right) * 10 + 5) % modulus


def fmod(length, position, modulus):
    return (7 * pow(10, length, modulus)
            - 18 * pow(10, position, modulus) - 25) % modulus


def main():
    q = 10 ** 42 - 1
    divisor = 27 * 49 * 43
    require(q % divisor == 0, "B division is not exact")
    b = q // divisor
    primes = [11, 13, 37, 127, 239, 1933, 2689, 4649,
              459691, 909091, 10838689]
    require(prod(primes) == b, "B factorization")
    require(all(prime_trial(p) for p in primes), "nonprime factor")
    require(prime_trial(898129), "family coefficient is prime")
    require(pow(10, 56133, 898129) == 1 and
            all(pow(10, 56133 // p, 898129) != 1 for p in (3, 7, 11)),
            "exact order of 10 modulo the family coefficient")
    table = {1: 39, 3: 3, 5: 15}
    for h in [1, 3, 5]:
        matches = [r for r in range(3, 42, 6) if fmod(h, r, 49) == 0]
        require(matches == [table[h]], "modulo-49 position table")
    rows = []
    for h in range(1, 42, 2):
        r = table[h % 6]
        g = gcd(q, 7 * 10 ** h - 18 * 10 ** r - 25)
        expected = 1323 if h % 6 == 1 else 18963 if h == 23 else 441
        require(g == expected, "gcd table at h=" + str(h))
        require(gcd(g, b) == 1, "gcd is not coprime to B")
        rows.append([h, r, g])
    residues = [[p, 4 * pow(7, -1, p) % p] for p in primes]
    require(residues[3:] == [[127, 55], [239, 103], [1933, 829],
                            [2689, 1153], [4649, 1993], [459691, 197011],
                            [909091, 389611], [10838689, 4645153]],
            "new forbidden length residues")
    require(4 * pow(7, -1, 43) % 43 == 19, "43 length residue")
    require(191 % 42 == 23 and 191 % 43 == 19, "43 combined class")
    require(gcd(112222110, 127) == 1, "rounded-family coefficient")
    require((-3 * pow(112222110, -1, 127)) % 127 == 68,
            "rounded-family index")

    rounded_l, rounded_i = 16031731, 6640575
    large_l = int('15582704697570091495948156638491914590405161120787807516829906317314612303918977615165179656913553')
    large_i = int('6477065490626893175017379503058848761317334778884442403179846853582090755525695000140054741394429')
    require(7 * large_l - 4 == 898129 * 3 ** 193, "large-control length")
    controls = []
    for name, length, position, expected in [
        ('rounded', rounded_l, rounded_i, {49: 0, 343: 147,
                                           9 * (7 * rounded_l - 4): 123356871}),
        ('sum_and_seven_four', large_l, large_i,
         {2401: 0, 16807: 9604, 9 * (7 * large_l - 4): 0,
          225 * 2401 * (7 * large_l - 4): 0}),
        ('regression_23_15', 23, 15, {49: 0, 343: 245, 9 * 157: 1269}),
    ]:
        require(0 < position < length, name + ' position bound')
        values = {}
        for modulus, wanted in expected.items():
            direct = fmod(length, position, modulus)
            decimal = 9 * blocks(length, position, modulus) % modulus
            require(direct == decimal == wanted,
                    name + ' modular control at modulus ' + str(modulus))
            values[str(modulus)] = direct
        controls.append({'name': name, 'L': length, 'i': position,
                         'F_remainders': values})
    for length in range(5, 80, 2):
        for position in range(3, length, 6):
            actual = int('7' * (length-position-1) + '5' +
                         '7' * (position-1) + '5')
            for modulus in [49, 343, 16807, 9 * (7 * length - 4)]:
                require(blocks(length, position, modulus) == actual % modulus,
                        'block implementation direct-decimal control')
    print(json.dumps({'status': 'PASS', 'B': b, 'factorization': primes,
                      'primality_method': 'all divisors through integer square root',
                      'gcd_table_h_r_G': rows,
                      'forbidden_length_residues_p_L': residues,
                      'rounded_family_forbidden_q_mod_127': 68,
                      'controls': controls}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
