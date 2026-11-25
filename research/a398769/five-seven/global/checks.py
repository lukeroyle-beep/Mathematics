#!/usr/bin/env python3
"""Exact checks for the global follow-up; no global cutoff is asserted.

Python 3.8+ standard library. Default validation is deliberately small;
PR8's independent scripts retain the ten-million finite certificate.
--length L checks exactly that one odd length using the two-quotient theorem.
"""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def valuation(n, p):
    require(n > 0 and p > 1, "positive valuation arguments required")
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def decimal_pair(length, position):
    require(0 < position < length, "invalid digit position")
    digits = [7] * length
    digits[0] = digits[position] = 5
    n, product = 0, 1
    for digit in reversed(digits):
        n = n * 10 + digit
        product *= digit
    return n, product, sum(digits)


def digit_blocks_mod(length, position, modulus):
    """Concatenate the actual four digit blocks by binary composition."""
    require(0 < position < length and modulus > 0, "invalid block arguments")
    result = 0
    for digit, count in [(7, length - position - 1), (5, 1),
                         (7, position - 1), (5, 1)]:
        power, value = 1, 0
        block_power, block_value = 10 % modulus, digit % modulus
        while count:
            if count & 1:
                value = (value * block_power + block_value) % modulus
                power = power * block_power % modulus
            block_value = (block_value * block_power + block_value) % modulus
            block_power = block_power * block_power % modulus
            count //= 2
        result = (result * power + value) % modulus
    return result


def candidates(length, a):
    """Algebraic helper; callers supply the true A except synthetic controls."""
    require(length >= 5 and length % 2 == 1 and a > 0, "invalid candidate domain")
    k = 10 ** ((length + 1) // 2) // 25
    require(math.gcd(a, k) == 1, "A must be a unit modulo K")
    numerator, denominator = 7 * 10**length, 25 * a
    require(numerator < denominator * k, "X < K required")
    return numerator // denominator, (-pow(a, -1, k)) % k


def recover_position(length, a, q):
    """Check the full defining equality, not merely the necessary valuations."""
    if q <= 0:
        return None
    t = a * q + 1
    i = valuation(t, 5) + 2
    if not (3 <= i <= length - 2 and i % 6 == 3):
        return None
    if valuation(t, 2) != i + 1:
        return None
    if 25 * a * q != 7 * 10**length - 18 * 10**i - 25:
        return None
    return i


def check_length(length):
    require(length >= 5 and length % 2 == 1, "supply an odd length >=5")
    s = 7 * length - 4
    if s % 5 == 0:
        return {"length": length, "excluded_by": "exact 5-adic digit-sum filter",
                "witnesses": []}
    a = 9 * 7 ** (length - 2) * s
    qs = candidates(length, a)
    witnesses = []
    for q in sorted(set(qs)):
        i = recover_position(length, a, q)
        if i is not None:
            n, product, digit_sum = decimal_pair(length, i)
            require(n > 0 and product * digit_sum * q == n,
                    "independent direct-digit witness check failed")
            quotient_bytes = q.to_bytes((q.bit_length() + 7) // 8, "big")
            witnesses.append({"position": i, "quotient_bit_length": q.bit_length(),
                              "quotient_sha256_big_endian": hashlib.sha256(quotient_bytes).hexdigest(),
                              "digit_rule": "all 7 except positions 0 and i are 5",
                              "direct_digit_remainder": n % (product * digit_sum)})
    return {"length": length, "candidate_count": len(set(qs)),
            "witnesses": witnesses, "excluded": not witnesses}


def prime_divisors(n):
    result, p = [], 2
    while p * p <= n:
        if n % p == 0:
            result.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        result.append(n)
    return result


def fixed_modulus_example(modulus, offset=0):
    require(modulus >= 1 and offset >= 0, "invalid fixed modulus control")
    d = math.prod(p for p in prime_divisors(modulus) if p != 2)
    exponent = max(1, valuation(modulus, 7))
    period, power = 6 * 7 ** (exponent - 1), 7**exponent
    require(pow(10, period, power) == 1, "order upper bound")
    require(all(pow(10, period // p, power) != 1 for p in prime_divisors(period)),
            "order minimality")
    multiple = (3 * period + d - 1) // d
    if multiple % 2 == 0:
        multiple += 1
    length = (multiple + 2 * offset) * d
    lo, hi = (length + 2) // 3, 2 * length // 3
    require(hi - lo + 1 >= period, "interval endpoints")
    target = (7 * pow(10, length, power) - 25) % power
    classes = [r for r in range(period) if 18 * pow(10, r, power) % power == target]
    require(len(classes) == 1, "unique logarithm class")
    r = classes[0]
    i = lo + (r - lo) % period
    s = 7 * length - 4
    require(lo <= i <= hi and i % 6 == 3 and i >= 3 and length - i >= 2,
            "central position")
    require(math.gcd(s, modulus) == 1, "sum coprimality")
    # F mod 9M divided by 9 is n mod M, including when 3 divides M.
    f9m = (7 * pow(10, length, 9 * modulus)
           - 18 * pow(10, i, 9 * modulus) - 25) % (9 * modulus)
    require(f9m % 9 == 0, "division by nine must be exact")
    nmod = f9m // 9
    psmod = 25 * pow(7, length - 2, modulus) * s % modulus
    g = math.gcd(psmod, modulus)
    require(nmod % g == 0, "linear congruence solvability")
    reduced = modulus // g
    q = 0 if reduced == 1 else (nmod // g) * pow(psmod // g, -1, reduced) % reduced
    require((psmod * q - nmod) % modulus == 0, "modular quotient")
    return {"M": modulus, "L": length, "i": i, "q_mod_M_over_gcd": q,
            "gcd_PS_M": g, "T": period}


def self_check():
    pair_count, length_count, sum_only_count = 0, 0, 0
    for length in range(5, 302, 2):
        result = check_length(length)
        direct_witnesses = []
        s, h = 7 * length - 4, (length - 1) // 2
        a = 9 * 7 ** (length - 2) * s
        k = 10 ** (h + 1) // 25
        x = Fraction(7 * 10**length, 25 * a)
        require(x / k == Fraction(49, 9 * s) * Fraction(10, 49)**h < 1,
                "corrected exact X/K bound")
        if s % 5:
            q1, q2 = candidates(length, a)
            require(0 <= q1 < k and 0 <= q2 < k and (a * q2 + 1) % k == 0,
                    "quotient representatives")
        for i in range(3, length, 6):
            n, product, digit_sum = decimal_pair(length, i)
            f = 7 * 10**length - 18 * 10**i - 25
            require(9 * n == f and product == 25 * 7**(length - 2)
                    and digit_sum == s, "direct digit identity")
            for modulus in (7, 27, 343, s):
                require(digit_blocks_mod(length, i, modulus) == n % modulus,
                        "binary digit-block concatenation")
            require((n % (product * s) == 0) == (f % (25 * a) == 0), "full test")
            require((n % s == 0) == (f % (9 * s) == 0), "retain factor 9")
            t = f // 25 + 1
            require(valuation(t, 5) + 2 == i and valuation(t, 2) == i + 1,
                    "valuation recovery on actual digits")
            if i < h + 1:
                require(Fraction(18 * 10**i + 25, 25 * a)
                        <= Fraction(301, 225 * s) * Fraction(10, 49)**h < 1,
                        "corrected small-position error bound")
            if n % s == 0:
                sum_only_count += 1
            if n % (product * s) == 0:
                direct_witnesses.append(i)
            pair_count += 1
        require([w["position"] for w in result["witnesses"]] == direct_witnesses,
                "two-quotient/direct enumeration mismatch")
        length_count += 1
    controls = []
    for length, i, a, q, expected in [(7, 3, 311031, 9, (9, 329)),
                                      (11, 9, 433015873, 63, (64, 63))]:
        qs = candidates(length, a)
        require(qs == expected and q in qs, "synthetic quotient positive control")
        require(recover_position(length, a, q) == i, "synthetic position recovery")
        require(recover_position(length, a, q + 1) is None, "wrong quotient rejected")
        n, p, s = decimal_pair(length, i)
        require(n % (p * s) != 0, "synthetic control is not an original witness")
        controls.append({"L": length, "i": i, "synthetic_A": a, "q": q,
                         "q1": qs[0], "q2": qs[1], "original_problem_witness": False})
    examples = [fixed_modulus_example(m, offset)
                for m in range(1, 129) for offset in range(3)]
    special = [2**8 * 3**3 * 5**4 * 7**4 * 11 * 13,
               49 * 5 * 11 * 13 * 37 * 101]
    examples.extend(fixed_modulus_example(m) for m in special)
    regression = 7 * 10**23 - 18 * 10**15 - 25
    require(regression % 49 == 0 and regression % 343 == 245, "23,15 regression")
    # Explicitly demonstrate the literal attachment bounds are too small.
    length, i, s = 9, 3, 59
    a = 9 * 7**(length - 2) * s
    x = Fraction(7 * 10**length, 25 * a)
    k = 10**((length + 1) // 2) // 25
    require(x / k > Fraction(343, (9 * s)**length), "literal first bound countercheck")
    require(Fraction(18 * 10**i + 25, 25 * a) > Fraction(43 * 49, (225 * s)**length),
            "literal second bound countercheck")
    # An actual S-only survivor; no product-divisibility claim.
    n, product, s = decimal_pair(1225, 417)
    require(s == 8571 and n % s == 0 and n % (product * s) != 0,
            "varying digit-sum positive control")
    require(valuation(9 * n, 7) == 3, "digit-sum control has only three sevens")
    require(all(1225 % p != residue for p, residue in
                [(5, 2), (11, 10), (13, 8), (37, 27), (101, 15)]),
            "digit-sum positive control retains inherited length filters")
    require((1225 % 6, 417 % 42) in {(1, 39), (3, 3), (5, 15)},
            "digit-sum positive control retains modulo49 table")
    big_l, big_i = 121041229921, 40582608819
    big_s = 7 * big_l - 4
    require(big_s == 3**25 and (big_l + 2) // 3 <= big_i <= 2 * big_l // 3,
            "large digit-sum control is central")
    require(all(big_l % p != residue for p, residue in
                [(5, 2), (11, 10), (13, 8), (37, 27), (101, 15)])
            and (big_l % 6, big_i % 42) == (1, 39), "large control filters")
    big_residues = {}
    for modulus in (9 * big_s, 49, 343):
        fmod = (7 * pow(10, big_l, modulus)
                - 18 * pow(10, big_i, modulus) - 25) % modulus
        require(fmod == 9 * digit_blocks_mod(big_l, big_i, modulus) % modulus,
                "independent large digit-block/formula comparison")
        big_residues[str(modulus)] = fmod
    require(big_residues[str(9 * big_s)] == 0 and big_residues["49"] == 0
            and big_residues["343"] == 245, "large sum-only control")
    require(digit_blocks_mod(big_l, big_i, big_s) == 0
            and digit_blocks_mod(big_l, big_i, 343) == 294,
            "direct large digit-block residues")
    return {"schema": 1, "direct_residual_pairs": pair_count,
            "direct_odd_lengths_5_through_301": length_count,
            "two_quotient_matches_direct": True, "full_witnesses": [],
            "sum_only_pairs_through_301": sum_only_count,
            "synthetic_positive_controls": controls,
            "fixed_modulus_controls": len(examples),
            "fixed_modulus_controls_sha256": hashlib.sha256(
                json.dumps(examples, sort_keys=True).encode()).hexdigest(),
            "large_fixed_modulus_examples": examples[-2:],
            "sum_only_control": {"L": 1225, "i": 417, "S": s, "S_remainder": n % s,
                                 "v7_F": valuation(9 * n, 7),
                                 "full_remainder_zero": False},
            "large_sum_only_control": {"L": big_l, "i": big_i, "S": big_s,
                                       "F_residues": big_residues,
                                       "n_mod_S_from_digit_blocks": 0,
                                       "n_mod_343_from_digit_blocks": 294,
                                       "v7_F": 2, "original_problem_witness": False,
                                       "certifies_entire_length_exclusion": False},
            "regression_F_23_15": {"mod49": 0, "mod343": 245},
            "new_certified_interval_above_10000000": None,
            "global_cutoff": None, "all_length_exclusion": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--length", type=int, help="check exactly one odd length; large inputs cost memory")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = self_check() if args.length is None else check_length(args.length)
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
