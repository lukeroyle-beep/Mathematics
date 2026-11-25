#!/usr/bin/env python3
"""Independent lift/repunit audit of early rejection; standard library only.

No other checker is imported.  All arithmetic is arbitrary-precision Python
integer arithmetic.  The CLI bound is a memory/resource bound, not a theorem.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys


MAX_LENGTH = 9_999_999
BLOCK_SIZE = 50_000


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def uniqueness_depth(length):
    require(length >= 1, "positive length required")
    depth, period = 1, 6
    while period <= length:
        depth += 1
        period *= 7
    return depth, period


def repunit(length, modulus):
    """Return R_length modulo modulus by left-to-right concatenation.

    A block (p,r) represents 10^j and R_j.  Doubling has
    (p,r)->(p*p,r*(p+1)); appending one has (10*p,10*r+1).
    No division, modular or integer, occurs here.
    """
    require(length >= 0 and modulus >= 1, "invalid repunit arguments")
    power, result = 1 % modulus, 0
    for bit in bin(length)[2:]:
        result = result * (power + 1) % modulus
        power = power * power % modulus
        if bit == "1":
            result = (10 * result + 1) % modulus
            power = 10 * power % modulus
    return result


def sum_residue(length, position):
    total = 7 * length - 4
    n_mod_s = (7 * repunit(length, total) - 2
               - 2 * pow(10, position, total)) % total
    return 9 * n_mod_s


def linear_lift(length, position, depth):
    """Lift r_depth to r_(depth+1), using the linearized coefficient."""
    old_modulus = 7 ** depth
    modulus = 7 * old_modulus
    period = 6 * 7 ** (depth - 1)
    target = 7 * pow(10, length, modulus) - 25
    value = 18 * pow(10, position, modulus)
    delta = target - value
    require(delta % old_modulus == 0, "incoming lift is not exact")
    coefficient_numerator = pow(10, period, modulus) - 1
    require(coefficient_numerator % old_modulus == 0,
            "linear coefficient division is not exact")
    coefficient = coefficient_numerator // old_modulus
    digit = (delta // old_modulus) * pow(value * coefficient, -1, 7) % 7
    lifted = position + digit * period
    require(0 <= lifted < 7 * period, "lift outside canonical period")
    require((7 * pow(10, length, modulus)
             - 18 * pow(10, lifted, modulus) - 25) % modulus == 0,
            "outgoing lift congruence failed")
    return lifted


def representative(length, depth):
    position = 3
    for level in range(1, depth):
        position = linear_lift(length, position, level)
    return position


class LiftTables:
    """Cache lifts by odd L modulo T_(k-1), the RHS length period.

    At depth k>=2, 7*10^L modulo 7^k depends only on L modulo
    ord_(7^(k-1))(10)=T_(k-1).  Entry j corresponds to L=2*j+1.
    Every entry is obtained by exactly one linearized lift from depth k-1;
    these are NOT discrete-log/power-cycle tables.
    """

    def __init__(self):
        self.depth = 1
        self.table = [3]
        self.length_period = 2
        self.entries_built = 0

    def extend(self):
        old_depth = self.depth
        old_modulus = 7 ** old_depth
        modulus = 7 * old_modulus
        period = 6 * 7 ** (old_depth - 1)
        coefficient_numerator = pow(10, period, modulus) - 1
        require(coefficient_numerator % old_modulus == 0,
                "table coefficient division is not exact")
        coefficient = coefficient_numerator // old_modulus
        require(coefficient % 7 != 0, "singular lift coefficient")
        previous = self.table
        prior_period = self.length_period
        table = []
        power_l = 10 % modulus
        for length in range(1, period, 2):
            old_r = previous[(length % prior_period) // 2]
            value = 18 * pow(10, old_r, modulus)
            delta = 7 * power_l - 25 - value
            require(delta % old_modulus == 0, "table incoming congruence failed")
            digit = (delta // old_modulus) * pow(value * coefficient, -1, 7) % 7
            new_r = old_r + digit * period
            require(0 <= new_r < 7 * period, "table exponent outside period")
            require((7 * power_l - 18 * pow(10, new_r, modulus) - 25)
                    % modulus == 0, "table outgoing congruence failed")
            table.append(new_r)
            power_l = power_l * 100 % modulus
        require(power_l == 10 % modulus or
                (7 * power_l - 70) % modulus == 0,
                "length-side target did not close its period")
        self.depth += 1
        self.table = table
        self.length_period = period
        self.entries_built += len(table)

    def get(self, length, depth):
        require(depth >= self.depth, "stream must have nondecreasing depths")
        while self.depth < depth:
            self.extend()
        return self.table[(length % self.length_period) // 2]


def exact_depth(value):
    require(value != 0, "zero has no finite valuation")
    result = 0
    while value % 7 == 0:
        value //= 7
        result += 1
    return result


def controls():
    pair_count = 0
    parity_counts = [0, 0]
    sum_passes = 0
    for length in range(5, 202, 2):
        depth, period = uniqueness_depth(length)
        position = representative(length, depth)
        modulus = 7 ** depth
        require((7 * pow(10, length, modulus)
                 - 18 * pow(10, position, modulus) - 25) % modulus == 0,
                "control representative congruence failed")
        for i in range(3, length):
            digits = [7] * length
            digits[0] = digits[i] = 5
            n = int("".join(map(str, reversed(digits))))
            total = sum(digits)
            product = 1
            for digit in digits:
                product *= digit
            f = 7 * 10 ** length - 18 * 10 ** i - 25
            require(f == 9 * n, "literal decimal identity failed")
            require(total == 7 * length - 4 and product == 25 * 7 ** (length - 2),
                    "literal digit statistics failed")
            require(sum_residue(length, i) == f % (9 * total),
                    "repunit full-sum residue disagrees with literal word")
            require((n % (product * total) == 0)
                    == (f % (225 * total * 7 ** (length - 2)) == 0),
                    "full divisor equivalence failed")
            if total % 5:
                require((n % (product * total) == 0)
                        == (sum_residue(length, i) == 0
                            and f % (7 ** (length - 2)) == 0),
                        "separated full divisor equivalence failed")
            require((f % modulus == 0) == (i == position),
                    "unique actual representative equivalence failed")
            pair_count += 1
            parity_counts[i % 2] += 1
            sum_passes += n % total == 0
    boundaries = []
    for level in range(1, 10):
        period = 6 * 7 ** (level - 1)
        observed = [uniqueness_depth(period + offset)[0] for offset in (-1, 0, 1)]
        require(observed == [level, level + 1, level + 1],
                "strict period boundary failed, including even equality")
        boundaries.append({"k": level, "period": period, "depths": observed})
    positive = sum_residue(13, 12)
    positive_depth = exact_depth(7 * 10 ** 13 - 18 * 10 ** 12 - 25)
    positive_k = uniqueness_depth(13)[0]
    require(positive == 0 and (7 * 13 - 4) % 3 == 0,
            "shallow full-sum positive control failed")
    require(positive_depth == 0 and positive_k == 2,
            "shallow full-sum control was mislabeled")
    f_negative = 7 * 10 ** 151 - 18 * 10 ** 8 - 25
    negative = sum_residue(151, 8)
    require(f_negative % 1053 == 0 and negative == 8424,
            "loss-of-nine negative control failed")
    regression_value = 7 * 10 ** 23 - 18 * 10 ** 15 - 25
    regression_depth = exact_depth(regression_value)
    require(regression_depth == 2, "(23,15) exact valuation regression failed")
    require(regression_value % 49 == 0 and regression_value % 343 == 245,
            "(23,15) valuation residues failed")
    return {
        "literal_pairs": pair_count,
        "literal_positions_even_odd": parity_counts,
        "literal_full_sum_passes": sum_passes,
        "strict_boundaries": boundaries,
        "shallow_full_sum_positive": {"L": 13, "i": 12, "S": 87,
                                     "F_mod_9S": positive, "depth": positive_depth,
                                     "K": positive_k},
        "loss_of_nine_negative": {"L": 151, "i": 8, "S": 1053,
                                  "F_mod_S": 0, "F_mod_9S": negative},
        "valuation_regression": {"L": 23, "i": 15, "depth": regression_depth,
                                 "F_mod_49": regression_value % 49,
                                 "F_mod_343": regression_value % 343},
    }


def audit(min_length, max_length, records=None):
    require(5 <= min_length <= max_length <= MAX_LENGTH,
            f"supported CLI interval is inside 5..{MAX_LENGTH}")
    require(min_length % 2 == 1 and max_length % 2 == 1,
            "both CLI endpoints must be odd")
    table = LiftTables()
    full_hash = hashlib.sha256()
    block_hash = hashlib.sha256()
    prefix_hash = hashlib.sha256()
    counts = [0, 0, 0, 0]
    prefix_counts = [0, 0, 0, 0]
    blocks = []
    survivors = []
    number = 0
    block_first = min_length
    by_k = {}
    for length in range(min_length, max_length + 1, 2):
        depth, period = uniqueness_depth(length)
        position = table.get(length, depth)
        modulus = 7 ** depth
        require(0 <= position < period, "representative not canonical")
        require((7 * pow(10, length, modulus)
                 - 18 * pow(10, position, modulus) - 25) % modulus == 0,
                f"representative fails defining congruence at L={length}")
        require(position % 6 == 3, "modulo-seven exponent class failed")
        if not 3 <= position < length:
            category, residue = 1, "-"
        else:
            residue = sum_residue(length, position)
            if (7 * length - 4) % 5 == 0:
                category = 2
            else:
                category = 4 if residue == 0 else 3
        line = f"{length}:{depth}:{position}:{category}:{residue}\n".encode("ascii")
        full_hash.update(line)
        block_hash.update(line)
        if records is not None:
            records.write(line)
        counts[category - 1] += 1
        number += 1
        by_k[str(depth)] = by_k.get(str(depth), 0) + 1
        if length <= 100001:
            prefix_hash.update(line)
            prefix_counts[category - 1] += 1
        if category == 4:
            survivors.append({"L": length, "K": depth, "r": position,
                              "S": 7 * length - 4, "F_mod_9S": residue})
        if number % BLOCK_SIZE == 0 or length == max_length:
            blocks.append({"first": block_first, "last": length,
                           "count": (length - block_first) // 2 + 1,
                           "sha256": block_hash.hexdigest()})
            block_hash = hashlib.sha256()
            block_first = length + 2
    require(sum(counts) == (max_length - min_length) // 2 + 1,
            "coverage/partition count failed")
    return {
        "min_length": min_length, "max_length": max_length, "lengths": number,
        "counts": counts, "actual": sum(counts[1:]),
        "actual_five_free": sum(counts[2:]), "full_sum_passes": counts[3],
        "sha256": full_hash.hexdigest(), "blocks": blocks,
        "prefix_through_100001": {
            "lengths": sum(prefix_counts), "counts": prefix_counts,
            "actual": sum(prefix_counts[1:]),
            "actual_five_free": sum(prefix_counts[2:]),
            "sha256": prefix_hash.hexdigest()},
        "lengths_by_K": by_k, "survivors": survivors,
        "lift_table_entries": table.entries_built,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-length", type=int, default=5)
    parser.add_argument("--max-length", type=int, default=MAX_LENGTH)
    parser.add_argument("--records", type=Path)
    parser.add_argument("--controls-only", action="store_true")
    args = parser.parse_args()
    result = {"implementation": "B: linearized lifts and repunit concatenation",
              "schema": 1,
              "record_format": "L:K:r:category:F_mod_9S_or_dash\\n",
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "controls": controls()}
    if not args.controls_only:
        if args.records is None:
            result["audit"] = audit(args.min_length, args.max_length)
        else:
            with args.records.open("wb") as stream:
                result["audit"] = audit(args.min_length, args.max_length, stream)
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    print()


if __name__ == "__main__":
    main()
