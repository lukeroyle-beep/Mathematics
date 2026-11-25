#!/usr/bin/env python3
"""Independent whole-length enumeration by concatenating decimal blocks.

Standard library only. This program does not import another project checker,
read its receipt, evaluate 7*10**L-18*10**i-25, or divide a repunit by nine.
The two positions are read verbatim from the merged submission. Every tested
condition uses an explicit exception and remains active under python3 -O.
"""

from collections import Counter
from hashlib import sha256
import json
from math import gcd, isqrt, lcm
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def append_block(left, right, modulus):
    """Compose decimal blocks (value, 10**length) modulo modulus."""
    return ((left[0] * right[1] + right[0]) % modulus,
            left[1] * right[1] % modulus)


def repeat_digit(digit, count, modulus):
    require(0 <= digit <= 9 and count >= 0 and modulus > 0,
            "invalid repeated-digit block")
    result = (0, 1 % modulus)
    block = (digit % modulus, 10 % modulus)
    while count:
        if count & 1:
            result = append_block(result, block, modulus)
        block = append_block(block, block, modulus)
        count >>= 1
    return result


def decimal_word(length, position, modulus):
    """Read [7]*(L-i-1), 5, [7]*(i-1), 5 from left to right."""
    require(1 <= position < length, "position outside decimal word")
    value = (0, 1 % modulus)
    for digit, count in ((7, length - position - 1), (5, 1),
                         (7, position - 1), (5, 1)):
        value = append_block(value, repeat_digit(digit, count, modulus), modulus)
    return value[0]


def prime_factors(number):
    result = {}
    trial = 2
    while trial * trial <= number:
        while number % trial == 0:
            result[trial] = result.get(trial, 0) + 1
            number //= trial
        trial += 1
    if number > 1:
        result[number] = result.get(number, 0) + 1
    return result


def certify_order(modulus, order, factors):
    """A^d=1 and A^(d/q)!=1 for every prime q|d certify exact order."""
    product = 1
    for prime, exponent in factors.items():
        require(prime_factors(prime) == {prime: 1}, "order factor is not prime")
        product *= prime ** exponent
    require(product == order, "order factorization is incomplete")
    value = pow(10, order, modulus)
    require(value == 1, "claimed order is not a period")
    controls = {str(p): str(pow(10, order // p, modulus)) for p in factors}
    require(all(int(x) != 1 for x in controls.values()), "order not minimal")
    return {"modulus": str(modulus), "order": str(order),
            "factorization": {str(p): e for p, e in factors.items()},
            "power_at_order": value, "power_at_order_divided_by_prime": controls}


def valuation(residue):
    require(residue != 0, "valuation precision exhausted; increase precision")
    exponent = 0
    while residue % 7 == 0:
        residue //= 7
        exponent += 1
    return exponent


def small_controls():
    comparisons = 0
    for length in range(2, 41):
        for position in range(1, length):
            literal = int("7" * (length-position-1) + "5"
                          + "7" * (position-1) + "5")
            for modulus in (1, 7, 49, 81, 225, 343, 7*length-4, 16807):
                require(decimal_word(length, position, modulus) == literal % modulus,
                        "literal decimal word disagrees with block construction")
                comparisons += 1

    # Exhaust literal decimal words at small lengths independently of the
    # large-number spacing enumeration, including all even positions.
    tested_lengths = 0
    compatible_positions = 0
    lengths_with_three_factor_and_positions = 0
    for length in range(5, 502, 2):
        digit_sum = 7 * length - 4
        if gcd(digit_sum, 10) != 1:
            continue
        order, value = 1, 10 % digit_sum
        while value != 1:
            value = value * 10 % digit_sum
            order += 1
        actual = []
        for position in range(3, length):
            literal = int("7" * (length-position-1) + "5"
                          + "7" * (position-1) + "5")
            require(sum(map(int, str(literal))) == digit_sum,
                    "literal digit sum mismatch")
            if literal % digit_sum == 0:
                actual.append(position)
        tested_lengths += 1
        compatible_positions += len(actual)
        if actual:
            anchor = actual[0]
            predicted = list(range(anchor, length, order))
            require(actual == predicted, "literal all-position spacing mismatch")
            if digit_sum % 3 == 0:
                lengths_with_three_factor_and_positions += 1
    return {"literal_block_comparisons": comparisons,
            "literal_spacing_lengths": tested_lengths,
            "literal_spacing_lengths_upper_bound": 501,
            "literal_sum_compatible_positions": compatible_positions,
            "literal_three_factor_lengths_with_positions":
                lengths_with_three_factor_and_positions}


def example(a, prime, b, exact_depth, anchor):
    digit_sum = 3**a * prime**b
    length, remainder = divmod(digit_sum+4, 7)
    require(remainder == 0 and length % 2 == 1, "invalid appendix length")
    require(3 <= anchor < length and 41*length < 100*anchor < 42*length,
            "supplied position not in its strict interval")
    base_order = 16 if prime == 17 else 56133
    base_factors = {2: 4} if prime == 17 else {3: 6, 7: 1, 11: 1}
    require(all(prime % t for t in range(2, isqrt(prime)+1)),
            "prime claim failed exhaustive trial division")
    base_certificate = certify_order(prime, base_order, base_factors)
    square_residue = pow(10, base_order, prime*prime)
    coefficient, remainder = divmod(square_residue-1, prime)
    require(remainder == 0 and coefficient % prime != 0,
            "prime-power order does not lift by a factor of p")
    component_order = base_order * prime**(b-1)
    component_factors = dict(base_factors)
    component_factors[prime] = b-1
    lifted_certificate = certify_order(prime**b, component_order, component_factors)
    three_order = 3**(a-2)
    three_certificate = certify_order(3**a, three_order, {3: a-2})
    spacing = lcm(three_order, component_order)
    factors = ({2: 4, 3: a-2, 17: b-1} if prime == 17 else
               {3: a-2, 7: 1, 11: 1, prime: b-1})
    full_certificate = certify_order(digit_sum, spacing, factors)
    lower = -((anchor-3)//spacing)
    upper = (length-1-anchor)//spacing
    first = anchor + lower*spacing
    last = anchor + upper*spacing
    require(3 <= first <= last < length and first-spacing < 3
            and last+spacing >= length, "incomplete signed endpoints")
    require(lower <= 0 <= upper, "anchor was lost from enumeration")

    # The modulus has enough 7-adic precision only if every resulting residue
    # is nonzero modulo 7**precision; valuation() enforces that for all words.
    precision = 10
    seven_modulus = 7**precision
    combined_modulus = 25*digit_sum*seven_modulus
    hist = Counter()
    parity = {"even": Counter(), "odd": Counter()}
    residue_classes = Counter()
    digest = sha256()
    maximum_positions = []
    maximum_depth = -1
    for h in range(lower, upper+1):
        position = anchor + h*spacing
        word = decimal_word(length, position, combined_modulus)
        require(word % (25*digit_sum) == 0, "word fails full digit sum or factor 25")
        depth = valuation(word % seven_modulus)
        hist[depth] += 1
        parity["odd" if position % 2 else "even"][depth] += 1
        residue_classes[position % 6] += 1
        digest.update(f"{position}:{depth}\n".encode())
        if depth > maximum_depth:
            maximum_depth, maximum_positions = depth, [str(position)]
        elif depth == maximum_depth:
            maximum_positions.append(str(position))
    count = upper-lower+1
    require(sum(hist.values()) == count, "enumeration count mismatch")
    require(maximum_depth < length-2, "length not excluded by its maximum depth")
    anchor_modulus = 25*digit_sum*7**exact_depth
    anchor_residue = decimal_word(length, anchor, anchor_modulus)
    next_modulus = 7**(exact_depth+1)
    next_residue = decimal_word(length, anchor, next_modulus)
    require(anchor_residue == 0 and valuation(next_residue) == exact_depth,
            "supplied position fails claimed exact depth")
    return {
        "a": a, "prime": prime, "b": b, "supplied_depth": exact_depth,
        "S": str(digit_sum), "L": str(length), "i": str(anchor),
        "order_certificates": {"base_prime": base_certificate,
            "prime_squared_residue": str(square_residue),
            "prime_squared_nonzero_coefficient": coefficient,
            "prime_power": lifted_certificate, "three_power": three_certificate,
            "full_S": full_certificate},
        "d": str(spacing), "h_min": lower, "h_max": upper,
        "first_position": str(first), "last_position": str(last),
        "position_before_first": str(first-spacing),
        "position_after_last": str(last+spacing),
        "count": count, "word_modulus": str(combined_modulus),
        "valuation_precision": precision,
        "valuation_histogram": dict(sorted(hist.items())),
        "parity_histograms": {key: dict(sorted(value.items()))
                              for key, value in parity.items()},
        "position_mod_six_counts": dict(sorted(residue_classes.items())),
        "maximum_depth": maximum_depth, "maximum_positions": maximum_positions,
        "ordered_position_depth_sha256": digest.hexdigest(),
        "anchor_n_mod_25S7k": anchor_residue,
        "anchor_n_mod_7k_plus_1": next_residue,
        "anchor_F_mod_7k_plus_1_from_n": 9*next_residue % next_modulus,
        "anchor_F_mod_225S7k_from_n": 9*anchor_residue,
        "whole_length_excluded": True,
    }


def main():
    source = Path(__file__).resolve().parent.parent / "fixed-depth" / "SUBMISSION.txt"
    content = source.read_bytes()
    positions = re.findall(r"(?m)^\d{50,}$", content.decode("utf-8"))
    require(len(positions) == 2, "expected the two exact merged appendix positions")
    report = {"status": "passed",
        "method": "independent binary decimal-block concatenation for every position",
        "imports_or_executes_other_checker": False,
        "evaluates_F_formula": False,
        "source_submission_sha256": sha256(content).hexdigest(),
        "small_controls": small_controls(),
        "appendix_examples": [example(164, 17, 41, 4, int(positions[0])),
                              example(103, 898129, 21, 7, int(positions[1]))],
        "scope": "all digit-sum-compatible positions at the two appendix lengths"}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
