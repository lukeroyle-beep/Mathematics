#!/usr/bin/env python3
"""Targeted exact validation of Route B refinements; no search extension."""
import hashlib
import json
from math import gcd
from pathlib import Path


def require(value, message):
    if not value:
        raise RuntimeError(message)


def digits(length, position):
    word = [7] * length
    word[0] = word[position] = 5
    n, product = 0, 1
    for digit in reversed(word):
        n = 10 * n + digit
        product *= digit
    return n, product, sum(word)


def sum_class(length):
    s = 7 * length - 4
    require(gcd(s, 10) == 1, "sum modulus must be coprime to ten")
    residues, x = {}, 1
    while x not in residues:
        residues[x] = len(residues)
        x = x * 10 % s
    require(x == 1 and len(residues) <= s - 1, "order cycle")
    repunit = (10**length - 1) // 9
    target = (7 * repunit - 2) * pow(2, -1, s) % s
    return len(residues), residues.get(target)


def seven_class(length, exponent):
    modulus = 7**exponent
    period = 6 * 7**(exponent - 1)
    target = (7 * pow(10, length, modulus) - 25) % modulus
    matches = [i for i in range(period)
               if 18 * pow(10, i, modulus) % modulus == target]
    require(len(matches) == 1, "unique seven-adic exponent class")
    return period, matches[0]


def combined_class(period, r, d, s):
    if s is None:
        return None
    common = gcd(period, d)
    if (s - r) % common:
        return None
    reduced = d // common
    shift = 0 if reduced == 1 else (
        (s - r) // common * pow(period // common, -1, reduced) % reduced)
    total = period * reduced
    result = (r + period * shift) % total
    require(result % period == r and result % d == s, "CRT readback")
    return total, result


def split(length, a):
    m = (length + 1) // 2
    h = 25 * a
    choices = [t for t in range(m, length)
               if 18 * 10**(t - 1) + 25 < h]
    require(choices, "at least the original split exists")
    t = max(choices)
    require(t == length - 1 or 18 * 10**t + 25 >= h,
            "largest split endpoint")
    k = 10**t // 25
    require(7 * 10**length < h * k, "strict X < K_t")
    return t, k


def main():
    pairs = comparisons = filtered_lengths = weak_sum_false_positives = 0
    positive_crt = stabilized = 0
    for length in range(5, 302, 2):
        s = 7 * length - 4
        if s % 5 == 0:
            continue
        filtered_lengths += 1
        a = 9 * 7**(length - 2) * s
        h = 25 * a
        t, k = split(length, a)
        old_k = 10**((length + 1) // 2) // 25
        qt, qm = (-pow(a, -1, k)) % k, (-pow(a, -1, old_k)) % old_k
        require(qt >= qm and (qt - qm) % old_k == 0, "inverse lifting")
        require((qt == qm) == ((a * qm + 1) % k == 0), "unchanged lift iff")
        if h * qt < 7 * 10**length:
            require(qt == qm, "small lift must remain unchanged")
        d, r_sum = sum_class(length)
        seven = [seven_class(length, power) for power in range(1, 5)]
        crt = [combined_class(period, r, d, r_sum) for period, r in seven]
        e, rest = 0, d
        while rest % 7 == 0:
            rest //= 7
            e += 1
        require(7**(length - 3) > s, "full power beyond stabilization")
        require(gcd(6 * 7**(length - 3), d) == gcd(6, d) * 7**e,
                "full-power compatibility stabilization")
        stabilized += 1
        for position in range(3, length, 6):
            n, product, actual_sum = digits(length, position)
            f = 7 * 10**length - 18 * 10**position - 25
            require(f == 9 * n and actual_sum == s, "digit identity")
            require(product == 25 * 7**(length - 2), "digit product")
            require((n % s == 0) == (f % (9 * s) == 0), "full factor nine")
            require((n % s == 0) == (r_sum is not None and position % d == r_sum),
                    "sum class versus actual digits")
            weak_sum_false_positives += (f % s == 0 and n % s != 0)
            if position < t:
                require(0 < 18 * 10**position + 25 < h, "low branch correction")
            else:
                require((f // 25 + 1) % k == 0, "high branch decimal factor")
            for power, item in enumerate(crt, 1):
                direct = n % s == 0 and f % 7**power == 0
                predicted = item is not None and position % item[0] == item[1]
                require(direct == predicted, "CRT versus actual digits")
                positive_crt += direct
                comparisons += 1
            pairs += 1
    require(positive_crt > 0, "nonempty CRT positive controls")

    # Actual digit construction showing why S | F cannot replace S | n.
    n9, _, s9 = digits(313, 51)
    require(s9 == 2187 and (9 * n9) % s9 == 0 and n9 % s9 == 1944,
            "actual factor-nine negative control")

    # Actual original-problem controls: sum-only/truncated, never full witnesses.
    n, p, s = digits(1225, 417)
    require(n % s == 0 and n % (p * s) != 0, "sum-only control")
    require((9 * n) % 7**3 == 0 and (9 * n) % 7**4 != 0,
            "sum-only control exact seven valuation")
    d, r_sum = sum_class(1225)
    require(d == 408 and r_sum == 9, "sum-only exponent class")
    for power in range(1, 5):
        period, r = seven_class(1225, power)
        item = combined_class(period, r, d, r_sum)
        predicted = item is not None and 417 % item[0] == item[1]
        require(predicted == (power <= 3), "sum-only CRT positive/negative control")
    regression = 7 * 10**23 - 18 * 10**15 - 25
    require(regression % 49 == 0 and regression % 343 == 245, "23,15 regression")

    synthetic = []
    for length, position, a, q in [(7, 3, 311031, 9), (11, 9, 433015873, 63)]:
        t, k = split(length, a)
        q1 = 7 * 10**length // (25 * a)
        q2 = (-pow(a, -1, k)) % k
        require(25 * a * q == 7 * 10**length - 18 * 10**position - 25,
                "synthetic full equality")
        require(q == (q1 if position < t else q2), "synthetic branch success")
        require(t > (length + 1) // 2, "synthetic enlarged split exercised")
        n, p, s = digits(length, position)
        require(n % (p * s) != 0, "synthetic is not original witness")
        if position >= t:
            require(q2 != q1, "distinct high branch synthetic control")
        synthetic.append({"length": length, "position": position, "synthetic_A": a,
                          "split": t, "q": q, "q1": q1, "q2": q2,
                          "original_problem_witness": False})

    here = Path(__file__).resolve()
    source_hashes = {}
    for path in [here, here.with_name("ROUTE_B.md"),
                 here.parent.parent / "global/TWO_QUOTIENTS.md",
                 here.parent.parent / "global/FIXED_MODULUS.md",
                 here.parent.parent / "settlement/FULL_DIVISOR.md"]:
        source_hashes[str(path.relative_to(here.parents[4]))] = hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps({"scope": "targeted reduction checks, no new search interval",
                      "filtered_odd_lengths_5_through_301": filtered_lengths,
                      "direct_digit_pairs": pairs, "CRT_comparisons_powers_1_through_4": comparisons,
                      "CRT_positive_controls": positive_crt,
                      "S_divides_F_but_not_n_controls": weak_sum_false_positives,
                      "full_power_stabilization_checks": stabilized,
                      "factor_nine_negative_control": {"L": 313, "i": 51, "S": 2187,
                                                       "F_mod_S": 0, "n_mod_S": 1944},
                      "actual_sum_only_control": {"L": 1225, "i": 417, "d": 408,
                                                   "r_S": 9, "v7_F": 3,
                                                   "original_problem_witness": False},
                      "synthetic_controls": synthetic, "source_sha256": source_hashes},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
