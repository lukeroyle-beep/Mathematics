#!/usr/bin/env python3
"""Unseeded exhaustive original-F exponent lifts through depth 100."""
import hashlib
import json
import math
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def residue(u, modulus):
    return (7 * pow(10, 12 * u + 5, modulus)
            - 18 * pow(10, 5 * u + 2, modulus) - 25) % modulus


def depth(length):
    k, period = 1, 6
    while period <= length:
        k, period = k + 1, period * 7
    return k


def candidate(u, k):
    length, position = 12 * u + 5, 5 * u + 2
    total = 7 * length - 4
    rem = residue(u, 9 * total)
    next_rem = residue(u, 7 ** (k + 1))
    require(next_rem % (7 ** k) == 0, "candidate misses depth")
    require(next_rem != 0, "exact depth needs a further computation")
    return {"k": k, "u": u, "L": length, "i": position, "S": total,
            "K": depth(length), "F_mod_9S": rem,
            "gcd_F_S": math.gcd(rem, total), "S_mod_5": total % 5,
            "F_mod_7_to_k_plus_1": next_rem,
            "next_residue_coefficient": next_rem // (7 ** k),
            "v7_F": k}


def run():
    histories, exceptions = [], []
    previous_classes, previous_order = None, None
    modulus = 1
    for k in range(1, 101):
        modulus *= 7
        if k == 1:
            orders = [a for a in range(1, 7) if pow(10, a, modulus) == 1]
            order = min(orders)
            tested = list(range(order))
        else:
            # Reduction and the binomial theorem guarantee this list covers
            # every possible order and every class above a previous survivor.
            orders = [a * previous_order for a in range(1, 8)
                      if pow(10, a * previous_order, modulus) == 1]
            order = min(orders)
            tested = [u + a * previous_order for u in previous_classes
                      for a in range(order // previous_order)]
        values = [residue(u, modulus) for u in tested]
        classes = [u for u, value in zip(tested, values) if value == 0]
        require(order == 6 * 7 ** (k - 1), "unexpected order")
        require(len(classes) == 1, "unexpected class count")
        u = classes[0]
        lower = 0 if k == 1 else previous_order
        length = 12 * u + 5
        in_band = u >= 1 and lower <= length < order
        require(12 * (u + order) + 5 >= order,
                "a later representative could enter the band")
        require(u - order < 1, "a smaller admissible representative exists")
        histories.append({"k": k, "modulus": modulus, "T": order,
                          "u": u, "representative_L": length,
                          "band_lower_inclusive": lower,
                          "band_upper_exclusive": order,
                          "in_own_band": in_band,
                          "tested_exponents": tested, "F_residues": values})
        if in_band:
            exceptions.append(candidate(u, k))
        previous_classes, previous_order = classes, order

    # Supplied claims are checked only after complete unseeded discovery.
    require([row["k"] for row in exceptions] == [44, 56, 85, 92],
            "claimed exception depths fail")
    require(exceptions[0]["u"] == 329630660491118914435920553818196013,
            "claimed first exponent fails")
    require(exceptions[0]["K"] == 44 and
            exceptions[0]["next_residue_coefficient"] == 3,
            "claimed first exact depth fails")
    require(all(row["gcd_F_S"] == 1 for row in exceptions),
            "claimed coprimality fails")
    require(all(row["F_mod_9S"] != 0 for row in exceptions),
            "a depth exception passes the digit-sum test")

    # Nonzero positive control and neighboring negative/period controls.
    require(residue(5, 7) == 0 and residue(5, 49) == 7,
            "positive depth-one control failed")
    require(residue(4, 7) != 0, "negative control failed")
    require(residue(exceptions[0]["u"] + 6 * 7 ** 43, 7 ** 44) == 0,
            "period control failed")
    require(residue(exceptions[0]["u"] + 1, 7 ** 44) != 0,
            "neighbor control failed")
    require(depth(5) == 1, "depth-one endpoint failed")
    for k in range(2, 101):
        lo, hi = 6 * 7 ** (k - 2), 6 * 7 ** (k - 1)
        require(depth(lo) == k and depth(hi - 1) == k and
                depth(hi) == k + 1, "band endpoint failed")
    rejected = 0
    for false_claim in (False, residue(5, 49) == 0,
                        depth(6) == 1, exceptions[0]["F_mod_9S"] == 0):
        try:
            require(false_claim, "intentional negative guard")
        except ArithmeticError:
            rejected += 1
    require(rejected == 4, "guard disabled")
    return {"method": "all exponent classes using original F",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "max_depth": 100, "coverage_L_exclusive": 6 * 7 ** 99,
            "history": histories, "exceptions": exceptions,
            "positive_control": {"u": 5, "F_mod_49": 7, "v7_F": 1},
            "negative_guards_rejected": rejected}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
