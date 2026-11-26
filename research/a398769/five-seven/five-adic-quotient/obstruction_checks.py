#!/usr/bin/env python3
"""Exact controls on the remaining obstruction; standard library only.

The two input pairs are inherited examples, not newly searched witnesses.
This checker imports no earlier arithmetic or search implementation.
"""

from fractions import Fraction
from hashlib import sha256
import json
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "fixed-depth" / "checks.json"


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def repeat_digit(digit, length, modulus):
    """Return (the repeated word, 10**length) modulo modulus by doubling."""
    require(0 <= digit <= 9 and length >= 0 and modulus > 0, "run input")
    value, scale = 0, 1
    block, block_scale = digit % modulus, 10 % modulus
    while length:
        if length & 1:
            value = (value * block_scale + block) % modulus
            scale = scale * block_scale % modulus
        block = (block * block_scale + block) % modulus
        block_scale = block_scale * block_scale % modulus
        length //= 2
    return value, scale


def decimal_word(length, position, modulus):
    """Literal specification: 7...(L-i-1)...7,5,7...(i-1)...7,5."""
    require(1 <= position < length, "position input")
    value = 0
    for digit, count in ((7, length - position - 1), (5, 1),
                         (7, position - 1), (5, 1)):
        block, scale = repeat_digit(digit, count, modulus)
        value = (value * scale + block) % modulus
    return value


def nearest_centre(length, position, K):
    """Minimum |bi-aL| over reduced 0<a<b<=K**2.

    For each denominator only floor(b*i/L) and its successor can minimize
    distance. A non-reduced pair of positive distance is improved by its
    reduction; at distance zero the least denominator tie is reduced.
    Thus minimizing over all such pairs also minimizes over reduced pairs.
    """
    require(0 < position < length and K >= 1, "centre input")
    best = None
    for b in range(2, K * K + 1):
        a0 = b * position // length
        for a in (a0, a0 + 1):
            if 0 < a < b:
                candidate = (abs(b * position - a * length), b, a)
                if best is None or candidate < best:
                    best = candidate
    if best is not None:
        require(gcd(best[1], best[2]) == 1, "minimum must be reduced")
    return best


def depth_start(length):
    K, period = 1, 6
    while period <= length:
        K, period = K + 1, period * 7
    require(period > length, "strict K definition")
    require(K == 1 or period // 7 <= length, "minimal K")
    return K, period


def log_interval(x, terms=96):
    """Rational enclosure from 2*atanh((x-1)/(x+1)), for 1<x<=2.

    Tail after terms summands is at most
    2*z**(2*terms+1)/((2*terms+1)*(1-z*z)).
    """
    require(Fraction(1) < x <= Fraction(2), "log interval input")
    z = (x - 1) / (x + 1)
    total = sum((2 * z ** (2*j+1) / (2*j+1) for j in range(terms)), Fraction())
    tail = 2 * z ** (2*terms+1) / ((2*terms+1) * (1-z*z))
    return total, total + tail


def controls():
    literal = 0
    for length in range(2, 65):
        for position in range(1, length):
            digits = ["7"] * length
            digits[-1] = "5"
            digits[length - position - 1] = "5"
            number = int("".join(digits))
            for modulus in (1, 7, 49, 81, 125, 225 * (7*length-4)):
                require(decimal_word(length, position, modulus) == number % modulus,
                        "literal decimal word")
                literal += 1

    comparisons = 0
    for length in range(3, 36):
        for position in range(1, length):
            for K in range(1, 6):
                brute = [(abs(b*position-a*length), b, a)
                         for b in range(2, K*K+1)
                         for a in range(1, b) if gcd(a, b) == 1]
                expected = min(brute) if brute else None
                require(nearest_centre(length, position, K) == expected,
                        "nearest centre against complete numerator enumeration")
                comparisons += 1
    boundary = nearest_centre(100, 48, 2)
    outside = nearest_centre(101, 46, 2)
    require(boundary[0] == 2**2, "inclusive rational-centre boundary")
    require(outside[0] > 2**2, "strict rational-centre complement")
    require(nearest_centre(100, 50, 2) == (0, 2, 1), "zero distance reduction")
    return {"literal_decimal_modular_comparisons": literal,
            "complete_centre_controls": comparisons,
            "boundary": {"L": 100, "i": 48, "K": 2, "distance": boundary[0]},
            "outside": {"L": 101, "i": 46, "K": 2, "distance": outside[0]}}


def examples():
    inputs = json.loads(SOURCE.read_text())["appendix_examples"]
    require(len(inputs) == 2, "expected inherited example count")
    results = []
    for data in inputs:
        L, i, S = (int(data[key]) for key in ("L", "i", "S"))
        k = int(data["k"])
        require(S == 3**int(data["a"]) * int(data["c"])**int(data["b"]),
                "input digit-sum factorization")
        require(S == 7*L-4 and L % 2 == 1 and 3 <= i < L, "actual pair")
        require(S % 3 == 0 and S % 5 != 0 and S % 7 != 0, "sum factors")
        K, period = depth_start(L)
        nearest = nearest_centre(L, i, K)
        require(nearest[0] > K*K, "outside every certified rational-centre band")

        # This is n from the decimal runs, not from the closed formula for F.
        modulus = 25*S*7**(k+1)
        residue = decimal_word(L, i, modulus)
        require(residue % (25*S) == 0, "full non-seven divisor on decimal word")
        require(residue % 7**k == 0 and residue % 7**(k+1) != 0, "exact valuation")
        F_residue = (7*pow(10, L, 9*modulus)-18*pow(10, i, 9*modulus)-25) % (9*modulus)
        require(F_residue == 9*residue, "independent F formula versus decimal runs")
        require(F_residue % (225*S) == 0, "retain complete factor nine")
        require(F_residue % 7**(k+1) == int(data["claimed_F_next_residue"]),
                "inherited claimed next residue")
        require(k < K and K <= L-2, "examples are not actual r_K survivors")
        results.append({
            "L": str(L), "i": str(i), "S": str(S), "K": K, "K_squared": K*K,
            "T_K": str(period), "exact_t": k,
            "nearest_centre": {"a": nearest[2], "b": nearest[1], "distance": str(nearest[0])},
            "outside_all_certified_centres": True,
            "n_mod_25S": 0, "F_mod_225S": 0,
            "F_mod_next_seven_power": F_residue % 7**(k+1),
            "S_divisible_by_3": True, "actual_r_K_survivor": False,
            "full_witness": False,
        })
    return results


def gap():
    lo, hi = log_interval(Fraction(10, 7))
    epsilon = Fraction(1, 10**9)
    lower, upper = Fraction(356674942, 10**9), Fraction(356674943, 10**9)
    require(lower < lo-epsilon <= hi-epsilon < upper, "strict log-gap enclosure")
    B = 1000002000000
    # ln7 = 3*ln2 - ln(8/7); ln10 = ln(10/7) + ln7.
    l2, u2 = log_interval(Fraction(2))
    l87, u87 = log_interval(Fraction(8, 7))
    l400343, u400343 = log_interval(Fraction(400, 343))
    require(4*l2-u400343 + (lo-epsilon)*(B+1) > 356675656291,
            "gap at first remaining length")
    l7, u7 = 3*l2-u87, 3*u2-l87
    coefficient_lower = 1 + (lo-epsilon)/u7
    coefficient_upper = 1 + (hi-epsilon)/l7
    require(Fraction(1183294661, 10**9) < coefficient_lower <= coefficient_upper
            < Fraction(1183294662, 10**9), "strict lift-coefficient enclosure")
    return {"log_upper_minus_lower_coefficient_strict_interval":
                ["356674942/1000000000", "356674943/1000000000"],
            "log_range_width_at_B_plus_1_strictly_greater_than": 356675656291,
            "lift_upper_bound_coefficient_strict_interval":
                ["1183294661/1000000000", "1183294662/1000000000"],
            "method": "96-term rational atanh series with positive geometric tail"}


def main():
    result = {
        "status": "PASS",
        "scope": "Two inherited pairs, freshly verified; no length search or new full witness",
        "source": "../fixed-depth/checks.json",
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "controls": controls(), "examples": examples(), "gap": gap(),
        "limitation": "Both exact depths are below K; neither pair reaches the actual-r_K obstruction",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
