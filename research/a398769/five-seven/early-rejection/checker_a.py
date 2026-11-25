#!/usr/bin/env python3
"""Independent A: complete 7-power cycles, direct F modulo 9S.

No implementation code is imported from another checker.  Python integers
perform every arithmetic operation.  The array stores only least exponents;
its width is checked, and the supported length cap bounds each stored value.
The finite audit uses every odd length, with no full-witness prefilters.
"""

import argparse
from array import array
import hashlib
import json
from pathlib import Path


MAX_LENGTH = 34_588_805  # Last length with K <= 9; at most 7**9 entries.
BLOCK_SIZE = 50_000
EMPTY = 2**32 - 1


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def uniqueness_depth(length):
    require(length >= 1, "length must be positive")
    depth, period = 1, 6
    while period <= length:
        depth += 1
        period *= 7
    return depth, period


def full_cycle(depth):
    """Inverse table for the complete unit cycle of 10 modulo 7**depth."""
    modulus = 7**depth
    period = 6 * 7**(depth - 1)
    require(depth <= 9 and period < EMPTY, "unsupported cycle size")
    table = array("I", [EMPTY])
    require(table.itemsize == 4, "requires a four-byte unsigned array entry")
    table *= modulus
    value = 1
    for exponent in range(period):
        require(table[value] == EMPTY, "power cycle repeated too early")
        table[value] = exponent
        value = value * 10 % modulus
    require(value == 1, "power cycle did not close")
    require(period == modulus - modulus // 7, "unit group cardinality")
    return table


def recover(length, depth, table):
    modulus = 7**depth
    target = (7 * pow(10, length, modulus) - 25) * pow(18, -1, modulus)
    representative = table[target % modulus]
    require(representative != EMPTY, "target missing from complete unit cycle")
    return representative


def residue(length, position):
    modulus = 9 * (7 * length - 4)
    return (7 * pow(10, length, modulus) - 18 * pow(10, position, modulus) - 25) % modulus


def valuation(value):
    require(value != 0, "valuation of zero")
    depth = 0
    while value % 7 == 0:
        value //= 7
        depth += 1
    return depth


def controls():
    """Literal words test both position parities before any depth condition."""
    boundaries = []
    for depth in range(1, 13):
        period = 6 * 7**(depth - 1)
        expected = [depth, depth + 1, depth + 1]
        actual = [uniqueness_depth(length)[0] for length in (period - 1, period, period + 1)]
        require(actual == expected, "strict period boundary failure")
        require(pow(10, period, 7**depth) == 1, "order does not divide period")
        for prime in (2, 3, 7):
            if period % prime == 0:
                require(pow(10, period // prime, 7**depth) != 1, "period is not exact order")
        boundaries.append({"depth": depth, "period": period, "K_at_minus_equal_plus": actual})

    tables = {depth: full_cycle(depth) for depth in range(1, 4)}
    pairs = even_positions = odd_positions = sum_passes = depth_tests = 0
    for length in range(5, 202, 2):
        depth, period = uniqueness_depth(length)
        representative = recover(length, depth, tables[depth])
        modulus = 7**depth
        require(0 <= representative < period, "small representative bounds")
        require((7 * pow(10, length, modulus) - 18 * pow(10, representative, modulus) - 25) % modulus == 0,
                "small representative defining congruence")
        for position in range(3, length):
            digits = [7] * length
            digits[0] = digits[position] = 5
            number = int("".join(str(digit) for digit in reversed(digits)))
            digit_sum = sum(digits)
            digit_product = 1
            for digit in digits:
                digit_product *= digit
            polynomial = 7 * 10**length - 18 * 10**position - 25
            require(digit_sum == 7 * length - 4, "literal digit sum")
            require(digit_product == 25 * 7**(length - 2), "literal digit product")
            require(polynomial == 9 * number, "literal polynomial identity")
            require(number % 1000 == 775 and number % 25 == 0 and number % 125 != 0,
                    "suffix and exact five valuation")
            require(residue(length, position) == polynomial % (9 * digit_sum), "direct residue versus literal")
            require(polynomial % (9 * digit_sum) == 9 * (number % digit_sum), "normalization identity")
            require((number % (digit_product * digit_sum) == 0) ==
                    (polynomial % (225 * digit_sum * 7**(length - 2)) == 0), "exact full divisor")
            if digit_sum % 5:
                require((number % (digit_product * digit_sum) == 0) ==
                        (number % digit_sum == 0 and polynomial % 7**(length - 2) == 0),
                        "separated full condition")
            require((polynomial % modulus == 0) == (position == representative), "sole actual representative")
            if polynomial % 7 == 0:
                require(position % 6 == 3, "modulo-seven position class")
            for small_depth in range(1, 5):
                require((polynomial % 7**small_depth == 0) == (number % 7**small_depth == 0),
                        "literal valuation congruence")
                depth_tests += 1
            pairs += 1
            even_positions += position % 2 == 0
            odd_positions += position % 2 == 1
            sum_passes += number % digit_sum == 0

    positive = {"L": 13, "i": 12, "S": 87, "F_mod_9S": residue(13, 12),
                "exact_depth": valuation(7 * 10**13 - 18 * 10**12 - 25), "K": uniqueness_depth(13)[0]}
    require(positive["F_mod_9S"] == 0 and positive["S"] % 3 == 0 and positive["exact_depth"] < positive["K"],
            "shallow full-sum positive control")
    polynomial = 7 * 10**151 - 18 * 10**8 - 25
    negative = {"L": 151, "i": 8, "S": 1053, "F_mod_S": polynomial % 1053,
                "F_mod_9S": residue(151, 8)}
    require(negative["F_mod_S"] == 0 and negative["F_mod_9S"] == 8424, "loss-of-nine negative control")
    polynomial = 7 * 10**23 - 18 * 10**15 - 25
    regression = {"L": 23, "i": 15, "F_mod_49": polynomial % 49,
                  "F_mod_343": polynomial % 343, "exact_depth": valuation(polynomial)}
    require(regression["F_mod_49"] == 0 and regression["F_mod_343"] == 245 and regression["exact_depth"] == 2,
            "inherited valuation regression")
    return {"literal_domain": {"odd_lengths": [5, 201], "positions": "all 3 <= i < L", "pairs": pairs,
                               "even_positions": even_positions, "odd_positions": odd_positions,
                               "full_sum_passes": sum_passes, "depth_comparisons": depth_tests},
            "strict_period_boundaries_and_orders": boundaries,
            "shallow_full_sum_positive": positive, "loss_of_nine_negative": negative,
            "inherited_valuation_regression": regression}


def summarize(first, last, counts, digest):
    return {"first_length": first, "last_length": last, "lengths": sum(counts),
            "categories": {str(index + 1): count for index, count in enumerate(counts)},
            "actual_representatives": sum(counts[1:]), "actual_five_free": sum(counts[2:]),
            "full_sum_passes": counts[3], "sha256": digest.hexdigest()}


def audit(first, last, output_records):
    require(first >= 5 and first % 2 == 1 and last % 2 == 1 and first <= last <= MAX_LENGTH,
            "supported input: odd endpoints 5 <= min <= max <= 34588805")
    digest = hashlib.sha256()
    block_digest = hashlib.sha256()
    counts = [0] * 4
    block_counts = [0] * 4
    block_first = first
    blocks = []
    prefix = None
    passes = []
    current_depth = 0
    table = None
    for length in range(first, last + 1, 2):
        depth, period = uniqueness_depth(length)
        if depth != current_depth:
            del table
            table = full_cycle(depth)
            current_depth = depth
            modulus = 7**depth
            inverse_eighteen = pow(18, -1, modulus)
            length_power = pow(10, length, modulus)
        target = ((7 * length_power - 25) * inverse_eighteen) % modulus
        representative = table[target]
        require(representative != EMPTY and 0 <= representative < period, "representative outside power cycle")
        # These powers are recalculated from L and r, independently of the
        # recovery table and its incremental length-power state.
        require((7 * pow(10, length, modulus) - 18 * pow(10, representative, modulus) - 25) % modulus == 0,
                f"representative congruence failed at L={length}")
        length_power = length_power * 100 % modulus
        if not 3 <= representative < length:
            category, remainder = 1, "-"
        else:
            remainder = residue(length, representative)
            if (7 * length - 4) % 5 == 0:
                category = 2
            elif remainder:
                category = 3
            else:
                category = 4
                passes.append({"L": length, "K": depth, "r": representative, "S": 7 * length - 4})
        record = f"{length}:{depth}:{representative}:{category}:{remainder}\n".encode("ascii")
        if output_records is not None:
            output_records.write(record)
        digest.update(record)
        block_digest.update(record)
        counts[category - 1] += 1
        block_counts[category - 1] += 1
        if first == 5 and length == 100001:
            prefix = summarize(first, length, counts, digest)
        if sum(block_counts) == BLOCK_SIZE or length == last:
            blocks.append(summarize(block_first, length, block_counts, block_digest))
            block_first = length + 2
            block_counts = [0] * 4
            block_digest = hashlib.sha256()
    require(sum(counts) == (last - first) // 2 + 1, "coverage count mismatch")
    return {"summary": summarize(first, last, counts, digest), "prefix_through_100001": prefix,
            "block_size_lengths": BLOCK_SIZE, "blocks": blocks, "passing_pairs": passes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-length", type=int, default=5)
    parser.add_argument("--max-length", type=int, default=9_999_999)
    parser.add_argument("--records", type=Path, help="optional ordered ASCII record file")
    args = parser.parse_args()
    require(args.min_length >= 5 and args.min_length % 2 == 1 and args.max_length % 2 == 1 and
            args.min_length <= args.max_length <= MAX_LENGTH, "unsupported length interval")
    checks = controls()
    if args.records is None:
        result = audit(args.min_length, args.max_length, None)
    else:
        with args.records.open("wb") as stream:
            result = audit(args.min_length, args.max_length, stream)
    result.update({"schema": "a398769-early-rejection-v1", "implementation": "A-complete-power-cycles-direct-F",
                   "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   "record_format": "L:K:r:category:residue\\n (ASCII; residue is F mod 9S, or - in category 1)",
                   "controls": checks})
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
