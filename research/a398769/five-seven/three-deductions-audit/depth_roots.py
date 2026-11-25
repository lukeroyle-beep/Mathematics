#!/usr/bin/env python3
"""Polynomial roots and independent exact 7-adic-log discrete logarithms."""
import hashlib
import json
from pathlib import Path


def check(condition, message):
    if not condition:
        raise ValueError(message)


def polynomial(x, modulus):
    return (28000 * pow(x, 12, modulus) - 72 * pow(x, 5, modulus) - 1) % modulus


def derivative(x):
    return (336000 * pow(x, 11, 7) - 360 * pow(x, 4, 7)) % 7


def padic_log(unit, k):
    """log(unit) mod 7^k, unit=1 mod7, by a finite rational series.

    For n>=2k, n-v7(n)>=n/2>=k. Removed denominators require
    extra modular precision before exact division by their seven-part.
    """
    modulus = 7 ** k
    z = (unit - 1) % modulus
    check(z % 7 == 0, "log outside the principal units")
    answer = 0
    for n in range(1, 2 * k):
        stripped, seven_part = n, 1
        while stripped % 7 == 0:
            stripped //= 7
            seven_part *= 7
        numerator = pow(z, n, modulus * seven_part)
        check(numerator % seven_part == 0, "nonintegral log term")
        term = (numerator // seven_part) * pow(stripped, -1, modulus)
        answer += term if n % 2 else -term
    return answer % modulus


def recover_exponent(root, k):
    """Recover from the root alone; no original-F or exponent-lift route."""
    modulus, order = 7 ** k, 6 * 7 ** (k - 1)
    bases = [e for e in range(6) if pow(10, e, 7) == root % 7]
    check(len(bases) == 1, "ambiguous exponent modulo six")
    e = bases[0]
    if k == 1:
        return e, 0, 0
    y = root * pow(pow(10, e, modulus), -1, modulus) % modulus
    numerator = padic_log(y, k)
    denominator = padic_log(10 ** 6, k)
    check(numerator % 7 == 0 and denominator % 7 == 0,
          "principal logarithm not divisible by seven")
    check(denominator % 49 != 0, "log generator is not depth one")
    reduced_modulus = 7 ** (k - 1)
    a = ((numerator // 7) * pow(denominator // 7, -1, reduced_modulus)
         % reduced_modulus)
    u = e + 6 * a
    check(0 <= u < order and pow(10, u, modulus) == root,
          "independent logarithm does not reproduce root")
    return u, numerator // 7, denominator // 7


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def record(u, k):
    length = 12 * u + 5
    position = 5 * u + 2
    total = 84 * u + 31
    modulus = 9 * total
    rem = 25 * polynomial(pow(10, u, modulus), modulus) % modulus
    modnext = 7 ** (k + 1)
    next_rem = 25 * polynomial(pow(10, u, modnext), modnext) % modnext
    check(next_rem % (7 ** k) == 0 and next_rem != 0, "exact depth failed")
    actual_k = 1
    while 6 * 7 ** (actual_k - 1) <= length:
        actual_k += 1
    return {"k": k, "u": u, "L": length, "i": position, "S": total,
            "K": actual_k, "F_mod_9S": rem,
            "gcd_F_S": gcd(rem, total), "S_mod_5": total % 5,
            "F_mod_7_to_k_plus_1": next_rem,
            "next_residue_coefficient": next_rem // (7 ** k), "v7_F": k}


def run():
    roots, old_modulus = [], 1
    rows, exceptions = [], []
    for k in range(1, 101):
        modulus = 7 ** k
        tested = list(range(7)) if k == 1 else [x + d * old_modulus
                                               for x in roots for d in range(7)]
        values = [polynomial(x, modulus) for x in tested]
        roots = [x for x, value in zip(tested, values) if value == 0]
        check(len(roots) == 1, "unexpected polynomial root count")
        root = roots[0]
        check(derivative(root) != 0, "root is not simple")
        order = 6 * 7 ** (k - 1)
        check(pow(10, order, modulus) == 1, "claimed order is not a period")
        for prime in ([2, 3] if k == 1 else [2, 3, 7]):
            check(pow(10, order // prime, modulus) != 1,
                  "claimed order is not minimal")
        u, log_numerator, log_denominator = recover_exponent(root, k)
        lower = 0 if k == 1 else order // 7
        length = 12 * u + 5
        band = u >= 1 and lower <= length < order
        rows.append({"k": k, "modulus": modulus, "T": order, "root": root,
                     "u": u, "representative_L": length,
                     "band_lower_inclusive": lower,
                     "band_upper_exclusive": order, "in_own_band": band,
                     "tested_roots": tested, "polynomial_residues": values,
                     "log_numerator_div_7": log_numerator,
                     "log_denominator_div_7": log_denominator})
        if band:
            exceptions.append(record(u, k))
        old_modulus = modulus

    # Audit the submitted values after the independent search is complete.
    check([item["k"] for item in exceptions] == [44, 56, 85, 92],
          "submitted exception depths fail")
    check(exceptions[0]["u"] == 329630660491118914435920553818196013,
          "submitted first exponent fails")
    check(exceptions[0]["next_residue_coefficient"] == 3,
          "submitted first next residue fails")
    check(all(item["gcd_F_S"] == 1 for item in exceptions),
          "submitted coprimality fails")
    # Independently exercise logarithm addition and powers, including
    # cancellation in log(1)=0 and negative powers in the principal units.
    log_controls = 0
    for k in range(2, 16):
        modulus = 7 ** k
        a, b = 10 ** 6, 1 + 7 * 23
        check(padic_log(a * b % modulus, k) ==
              (padic_log(a, k) + padic_log(b, k)) % modulus,
              "log addition control failed")
        for exponent in (-14, -1, 0, 1, 7, 49):
            check(padic_log(pow(a, exponent, modulus), k) ==
                  exponent * padic_log(a, k) % modulus,
                  "log power control failed")
            log_controls += 1
    check(25 * polynomial(pow(10, 5, 49), 49) % 49 == 7,
          "positive depth-one control failed")
    check(polynomial(0, 7) != 0 and polynomial(roots[0] + 1, 7 ** 100) != 0,
          "root perturbation control failed")
    rejected = 0
    for operation in (lambda: check(False, "intentional guard"),
                      lambda: padic_log(3, 5),
                      lambda: check(exceptions[0]["F_mod_9S"] == 0,
                                    "intentional digit-sum guard")):
        try:
            operation()
        except ValueError:
            rejected += 1
    check(rejected == 3, "guard disabled")
    return {"method": "polynomial roots and truncated 7-adic logarithms",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "max_depth": 100, "coverage_L_exclusive": 6 * 7 ** 99,
            "history": rows, "exceptions": exceptions,
            "log_power_controls": log_controls,
            "negative_guards_rejected": rejected}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
