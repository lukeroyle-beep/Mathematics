#!/usr/bin/env python3
"""Independent finite audit: complete power tables and decimal concatenation.

Imports no primary checker. No conclusion above the requested finite window.
All essential checks use explicit exceptions, including under python -O.
"""
import argparse
from collections import Counter
import hashlib
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def join(a, b, modulus):
    """Pairs are (decimal value, power of ten for block length), modulo m."""
    return ((a[0] * b[1] + b[0]) % modulus, a[1] * b[1] % modulus)


def repeat(digit, count, modulus):
    require(count >= 0 and modulus > 0, "invalid block")
    result, block = (0, 1 % modulus), (digit % modulus, 10 % modulus)
    while count:
        if count & 1:
            result = join(result, block, modulus)
        block = join(block, block, modulus)
        count //= 2
    return result


def word(L, i, modulus):
    require(0 < i < L, "invalid word")
    value = repeat(7, L - i - 1, modulus)
    for digit, size in ((5, 1), (7, i - 1), (5, 1)):
        value = join(value, repeat(digit, size, modulus), modulus)
    return value[0]


def table(k):
    modulus, period = 7 ** k, 6 * 7 ** (k - 1)
    result, value = {}, 1
    for exponent in range(period):
        require(value not in result, "premature repeated power")
        result[value] = exponent
        value = 10 * value % modulus
    require(value == 1 and len(result) == period, "incomplete unit cycle")
    require(all(x % 7 for x in result), "nonunit in table")
    return result


def actual_depth(L, i, start):
    k = start
    require(word(L, i, 7 ** k) == 0, "base depth failed")
    while word(L, i, 7 ** (k + 1)) == 0:
        k += 1
        require(k < 2 * L, "positive word size bound violated")
    return k


def run(limit):
    require(5 <= limit <= 100001, "this bounded audit supports 5..100001 only")
    tables = {}
    counts, actuals, runs = Counter(), Counter(), Counter()
    digest = hashlib.sha256()
    fullsum, actual_total, allowed_total = [], 0, 0
    for L in range(5, limit + 1, 2):
        # Strict threshold, computed without logs or the primary lifting code.
        k, period = 1, 6
        while period <= L:
            k += 1
            period *= 7
        require(k <= L - 2, "threshold exceeds witness depth")
        require(k == 1 or period // 7 <= L, "threshold not minimal")
        if k not in tables:
            tables[k] = table(k)
        modulus = 7 ** k
        # This is the defining target; all actual-word checks below use blocks.
        target = (7 * pow(10, L, modulus) - 25) * pow(18, -1, modulus) % modulus
        r = tables[k][target]
        counts[k] += 1
        if 3 <= r < L:
            actual_total += 1
            actuals[k] += 1
            depth = actual_depth(L, r, k)
            S = 7 * L - 4
            remainder = 9 * word(L, r, S)
            require(0 <= remainder < 9 * S, "incorrect full-sum residue")
            runs[depth - k] += 1
            if S % 5:
                allowed_total += 1
                if remainder == 0:
                    fullsum.append([L, r, k, depth])
            row = f"{L}:{k}:{r}:{period}:{depth}:{remainder}\n"
        else:
            row = f"{L}:{k}:{r}:{period}:-:-\n"
        digest.update(row.encode("ascii"))
    literal_pairs = 0
    for L in range(5, 102, 2):
        for i in range(3, L):
            n = int("7" * (L - i - 1) + "5" + "7" * (i - 1) + "5")
            for m in (7, 49, 343, 2401, 7 * L - 4, 225 * (7 * L - 4)):
                require(word(L, i, m) == n % m, "literal/block mismatch")
            literal_pairs += 1
    controls = []
    for L, i in ((151, 8), (313, 51), (13, 12), (17, 15), (97127, 89265),
                 (69489, 40323)):
        S = 7 * L - 4
        n_mod = word(L, i, S)
        f_mod_9S = 9 * n_mod
        depth = 0
        while word(L, i, 7 ** (depth + 1)) == 0:
            depth += 1
        controls.append({"L": L, "i": i, "S": S, "n_mod_S": n_mod,
                         "F_mod_9S": f_mod_9S, "depth": depth})
    require(controls[0]["F_mod_9S"] == 8424, "lost-nine control")
    require(controls[1]["n_mod_S"] == 1944, "residual lost-nine control")
    require(controls[-2]["depth"] == 12, "long zero-run control")
    require(controls[-1]["depth"] == 11 and controls[-1]["S"] % 5 != 0,
            "five-free zero-run control")
    order_controls = []
    for L in (13, 85, 589):
        S, value, d = 7 * L - 4, 10 % (7 * L - 4), 1
        while value != 1:
            value = value * 10 % S
            d += 1
            require(d < S, "order enumeration failed")
        e, quotient = 0, d
        while quotient % 7 == 0:
            quotient //= 7
            e += 1
        K, period = 1, 6
        while period <= L:
            K += 1
            period *= 7
        require(e == K - 1, "expected sharp stabilization control")
        order_controls.append({"L": L, "S": S, "d": d, "e": e, "K": K})
    return {"method": "complete unit-cycle tables plus decimal blocks",
            "limit": limit, "odd_lengths": sum(counts.values()),
            "by_K": dict(sorted(counts.items())),
            "actual_by_K": dict(sorted(actuals.items())),
            "actual_representatives": actual_total,
            "actual_with_5_not_dividing_S": allowed_total,
            "zero_run_histogram": dict(sorted(runs.items())),
            "full_sum_survivors": fullsum, "ordered_sha256": digest.hexdigest(),
            "literal_pairs": literal_pairs, "controls": controls,
            "order_controls": order_controls,
            "scope": "bounded reduction audit only; no new excluded length interval"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=100001)
    args = parser.parse_args()
    print(json.dumps(run(args.limit), indent=2, sort_keys=True))
