#!/usr/bin/env python3
"""Independent exact bounded verifier using a fixed-modulus lookup table.

No imports from the adaptive sieve; Python standard library only.  The
mathematical order argument is in the adjacent investigation note.  This
program verifies finite arithmetic, not an all-length theorem or Lean proof.
The default run covers every odd length 5 <= L <= 10,000,000 and every
position 3 <= i < L with i == 3 (mod 6), including i=3 and i=45.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path


def require(condition, message):
    """Checks remain active under python -O."""
    if not condition:
        raise RuntimeError(message)


def decimal_number(length, position):
    """Independent reconstruction: concatenate actual decimal digits."""
    require(1 <= position < length, "invalid second-five position")
    digits = [7] * length
    digits[0] = digits[position] = 5
    number = int("".join(str(d) for d in reversed(digits)))
    return number, math.prod(digits), sum(digits)


def direct_checks(max_length):
    """All two-five positions, not just positions admitted by modulo seven."""
    count = 0
    weak = []
    full = []
    for length in range(3, max_length + 1, 2):
        for position in range(1, length):
            number, product, digit_sum = decimal_number(length, position)
            numerator = 7 * 10**length - 18 * 10**position - 25
            power = 7 ** (length - 2)
            require(9 * number == numerator, "decimal/formula mismatch")
            require(product == 25 * power, "digit product mismatch")
            require(digit_sum == 7 * length - 4, "digit sum mismatch")
            passes_weak = number % power == 0
            passes_full = number % (product * digit_sum) == 0
            require(passes_weak == (numerator % power == 0), "weak mismatch")
            require(passes_full == (numerator % (9 * product * digit_sum) == 0),
                    "full-divisor mismatch")
            if passes_weak:
                weak.append([length, position])
                require(position % 6 == 3, "unexpected modulo-seven position")
            if passes_full:
                full.append([length, position])
            if position >= 3 and position % 6 == 3:
                require(number % 125 == 25, "suffix 775 mismatch")
                require(number % 11 == 7, "modulo-eleven mismatch")
                require(number % 13 != 0, "modulo-thirteen mismatch")
            count += 1
    regression = 7 * 10**23 - 18 * 10**15 - 25
    require(regression % 49 == 0 and regression % 343 == 245,
            "(23,15) regression mismatch")
    return dict(max_length=max_length, pair_count=count, weak_survivors=weak,
                full_survivors=full, regression_23_15={"mod49": 0, "mod343": 245})


def verify(limit, exponent, direct_limit):
    require(5 <= limit <= 10_000_000, "limit must be between 5 and 10,000,000")
    require(1 <= exponent <= 24, "exponent must be between 1 and 24")
    require(3 <= direct_limit <= 999, "direct-limit must be between 3 and 999")
    modulus = 7**exponent
    period = 6 * 7 ** (exponent - 1)
    require(period > limit - 1, "period must exceed the entire position range")
    require(pow(10, period, modulus) == 1, "order upper bound failed")
    order_witnesses = {}
    for prime in (2, 3, 7):
        if period % prime == 0:
            value = pow(10, period // prime, modulus)
            require(value != 1, "order minimality failed")
            order_witnesses[str(prime)] = value

    # When L >= exponent+2, divisibility by 7^(L-2) implies the chosen test.
    first_length = max(5, exponent + 2)
    if first_length % 2 == 0:
        first_length += 1
    lower_weak = []
    lower_pairs = 0
    for length in range(5, min(limit + 1, first_length), 2):
        for position in range(3, length, 6):
            number, _, _ = decimal_number(length, position)
            if number % 7 ** (length - 2) == 0:
                lower_weak.append([length, position])
            lower_pairs += 1

    # Map positions to 18*10^i+25.  Multiplication by 18 is invertible
    # modulo 7^k; the certified period exceeds every difference of positions.
    positions = {}
    residue = pow(10, 3, modulus)
    step = pow(10, 6, modulus)
    for position in range(3, limit, 6):
        key = (18 * residue + 25) % modulus
        require(key not in positions, "unexpected position collision")
        positions[key] = position
        residue = residue * step % modulus
    require(len(positions) == len(range(3, limit, 6)), "position endpoint mismatch")

    residue = pow(10, first_length, modulus)
    survivors = []
    scanned = 0
    for length in range(first_length, limit + 1, 2):
        position = positions.get(7 * residue % modulus)
        if position is not None and position < length:
            require((7 * pow(10, length, modulus)
                     - 18 * pow(10, position, modulus) - 25) % modulus == 0,
                    "lookup/direct modular mismatch")
            survivors.append([length, position])
        residue = residue * 100 % modulus
        scanned += 1
    require(scanned == len(range(first_length, limit + 1, 2)),
            "length endpoint mismatch")
    direct = direct_checks(min(direct_limit, limit))
    covered_max = limit if limit % 2 else limit - 1
    return dict(
        schema=1, method="independent fixed-modulus position lookup",
        limit_inclusive=limit, largest_odd_length=covered_max,
        position_domain="3 <= i < L; i = 3 (mod 6), including i=3 and i=45",
        exponent=exponent, modulus=modulus, period=period,
        order_witnesses=order_witnesses,
        lower_direct=dict(first_length=5, last_length=min(covered_max, first_length - 2),
                          pair_count=lower_pairs, weak_survivors=lower_weak),
        fixed_modulus=dict(first_length=first_length, length_count=scanned,
                           position_count=len(positions), survivors=survivors),
        direct_decimal_crosscheck=direct,
        excluded_entire_bounded_weak_domain=not lower_weak and not survivors,
        all_length_exclusion=False,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=10_000_000)
    parser.add_argument("--exponent", type=int, default=20)
    parser.add_argument("--direct-limit", type=int, default=199)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.limit, args.exponent, args.direct_limit)
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
