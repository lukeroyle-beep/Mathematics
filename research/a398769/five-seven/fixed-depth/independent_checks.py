#!/usr/bin/env python3
"""Independent review calculations: linearized lifts and recursive word sums.

Standard library only; does not import or execute checks.py. All calculations
precede comparison with checks.json. The submitted positions are read verbatim
from SUBMISSION.txt. Explicit checks remain active under python -O.
"""

import hashlib
import json
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def logarithm(length, prime, depth):
    """Solve each new exponent digit by its linear coefficient, not enumeration."""
    modulus = prime ** depth
    if prime == 3:
        numerator = 7 * pow(10, length, 9 * modulus) - 25
        require(numerator % 9 == 0, "nonintegral division by nine")
        target = numerator // 9 * pow(2, -1, modulus) % modulus
        start, exponent, period = 2, 0, 1
    else:
        require(prime == 17, "unsupported logarithm prime")
        target = (7 * pow(10, length, modulus) - 25) * pow(18, -1, modulus) % modulus
        base = [e for e in range(16) if pow(10, e, 17) == target % 17]
        require(len(base) == 1, "base logarithm is not unique")
        start, exponent, period = 1, base[0], 16
    require(pow(10, exponent, prime ** start) == target % (prime ** start),
            "initial logarithm does not match")
    for power in range(start, depth):
        old_modulus = prime ** power
        next_modulus = prime * old_modulus
        coefficient = (pow(10, period, next_modulus) - 1) // old_modulus % prime
        error = target * pow(pow(10, exponent, next_modulus), -1, next_modulus) % next_modulus
        require((error - 1) % old_modulus == 0, "current logarithm lost precision")
        digit = (error - 1) // old_modulus * pow(coefficient, -1, prime) % prime
        exponent += digit * period
        period *= prime
    require(pow(10, exponent, modulus) == target, "final logarithm does not match")
    return exponent, period


def grid_point(m, j):
    a, b = 12 + 84 * m, 1 + 42 * j
    digit_sum = 3 ** a * 17 ** b
    length, remainder = divmod(digit_sum + 4, 7)
    require(remainder == 0, "nonintegral grid length")
    r3, p3 = logarithm(length, 3, a)
    r17, p17 = logarithm(length, 17, b)
    # First combine coprime moduli by their CRT idempotents.
    period = p3 * p17
    residue = (r3 * p17 * pow(p17, -1, p3)
               + r17 * p3 * pow(p3, -1, p17)) % period
    # The remaining overlap with 42 is six. Divide only after checking it.
    require(period % 6 == 0 and (3 - residue) % 6 == 0, "CRT overlap mismatch")
    digit = (3 - residue) // 6 * pow(period // 6, -1, 7) % 7
    residue += digit * period
    period *= 7
    require(0 <= residue < period and residue % 42 == 3, "CRT residue mismatch")
    return {"m": m, "j": j, "a": a, "b": b, "S": str(digit_sum),
            "L": str(length), "r": str(residue), "W": str(period),
            "three_log": str(r3), "seventeen_log": str(r17)}


def geometric_sum(count, modulus):
    """Return (10**count, 1+10+...+10**(count-1)) modulo modulus."""
    if count == 0:
        return 1 % modulus, 0
    power, total = geometric_sum(count // 2, modulus)
    power, total = power * power % modulus, total * (1 + power) % modulus
    if count % 2:
        power, total = 10 * power % modulus, (10 * total + 1) % modulus
    return power, total


def decimal_word(length, position, modulus):
    """Build both seven-blocks and both fives, without F or division by nine."""
    require(1 <= position < length and modulus > 0, "invalid decimal word")
    value = 7 * geometric_sum(length - position - 1, modulus)[1]
    value = (10 * value + 5) % modulus
    power, total = geometric_sum(position - 1, modulus)
    value = (value * power + 7 * total) % modulus
    return (10 * value + 5) % modulus


def appendix_example(a, c, b, k, position, claimed_next):
    digit_sum = 3 ** a * c ** b
    length, remainder = divmod(digit_sum + 4, 7)
    require(remainder == 0 and length % 2 == 1, "invalid appendix length")
    low_margin, high_margin = 100 * position - 41 * length, 42 * length - 100 * position
    require(low_margin > 0 and high_margin > 0 and 3 <= position < length,
            "position outside the strict interval or digit domain")
    next_modulus = 7 ** (k + 1)
    residues = {"n_mod_25S7_to_k": decimal_word(length, position, 25 * digit_sum * 7 ** k),
                "n_mod_7_to_k": decimal_word(length, position, 7 ** k),
                "n_mod_7_to_k_plus_1": decimal_word(length, position, next_modulus)}
    residues["nine_times_n_mod_7_to_k_plus_1"] = 9 * residues["n_mod_7_to_k_plus_1"] % next_modulus
    require(residues["n_mod_25S7_to_k"] == 0 and residues["n_mod_7_to_k"] == 0,
            "decimal-word divisibility failed")
    require(residues["n_mod_7_to_k_plus_1"] != 0
            and residues["nine_times_n_mod_7_to_k_plus_1"] == claimed_next,
            "decimal-word exact depth or claimed next residue failed")
    return {"a": a, "c": c, "b": b, "k": k, "i": str(position),
            "S": str(digit_sum), "L": str(length),
            "100i_minus_41L": str(low_margin), "42L_minus_100i": str(high_margin),
            "independent_decimal_blocks": residues}


def main():
    directory = Path(__file__).resolve().parent
    submission_bytes = (directory / "SUBMISSION.txt").read_bytes()
    positions = re.findall(r"(?m)^\d{50,}$", submission_bytes.decode("utf-8"))
    require(len(positions) == 2, "expected exactly two submitted position literals")
    points = [grid_point(m, j) for m in range(2) for j in range(2)]
    lookup = {(point["m"], point["j"]): point for point in points}
    reductions = []
    for lower, higher in (((0, 0), (1, 0)), ((0, 0), (0, 1)),
                           ((0, 1), (1, 1)), ((1, 0), (1, 1))):
        lo, hi = lookup[lower], lookup[higher]
        remainder = int(hi["r"]) % int(lo["W"])
        require(remainder == int(lo["r"]), "adjacent representative reduction failed")
        reductions.append({"lower": list(lower), "higher": list(higher),
                           "higher_r_mod_lower_W": str(remainder), "status": "passed"})
    examples = [appendix_example(164, 17, 41, 4, int(positions[0]), 2401),
                appendix_example(103, 898129, 21, 7, int(positions[1]), 1647086)]

    # Only now consult the primary receipt; none of its numbers drive calculation.
    receipt_bytes = (directory / "checks.json").read_bytes()
    primary = json.loads(receipt_bytes)
    for independent, reference in zip(points, primary["depth_one_grid"]["points"]):
        require(all(independent[key] == reference[key] for key in independent),
                "independent grid calculation differs from primary receipt")
    require(len(primary["depth_one_grid"]["points"]) == len(points), "grid count mismatch")
    require(len(primary["appendix_examples"]) == len(examples), "appendix count mismatch")
    for independent, reference in zip(examples, primary["appendix_examples"]):
        require(all(independent[key] == reference[key] for key in independent),
                "independent appendix calculation differs from primary receipt")
    report = {"method": "linearized prime-adic logarithms, CRT idempotents, recursive decimal geometric sums",
              "imports_or_executes_primary_checker": False,
              "source_sha256": {"SUBMISSION.txt": hashlib.sha256(submission_bytes).hexdigest(),
                                "checks.json": hashlib.sha256(receipt_bytes).hexdigest()},
              "depth_one_grid": points, "adjacent_reductions": reductions,
              "appendix_examples": examples,
              "primary_receipt_comparison": "all independently computed fields match",
              "status": "passed",
              "scope": "reproducible finite review calculations; not proof of the infinite theorem"}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
