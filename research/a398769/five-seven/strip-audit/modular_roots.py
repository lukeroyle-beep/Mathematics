#!/usr/bin/env python3
"""Discover all polynomial roots, then recover the exponent by BSGS.

Standard library only. No supplied representative initializes discovery.
All mathematical checks raise explicit exceptions, including under -O.
"""

from hashlib import sha256
from math import isqrt
from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def polynomial(x):
    return 28000 * x**12 - 72 * x**5 - 1


def derivative(x):
    return 336000 * x**11 - 360 * x**4


def valuation(n, prime):
    require(n != 0, "valuation of zero")
    count = 0
    while n % prime == 0:
        n //= prime
        count += 1
    return count


def discrete_log(base, target, modulus, order):
    """Exhaustive BSGS over [0, order), independent of exponent lifting."""
    width = isqrt(order) + 1
    babies = {}
    residue = 1
    for exponent in range(width):
        require(residue not in babies, "unexpected repeated baby step")
        babies[residue] = exponent
        residue = residue * base % modulus
    stride = pow(pow(base, width, modulus), -1, modulus)
    giant = target
    solutions = set()
    for block in range((order - 1) // width + 1):
        if giant in babies:
            exponent = block * width + babies[giant]
            if exponent < order:
                require(pow(base, exponent, modulus) == target,
                        "invalid BSGS match")
                solutions.add(exponent)
        giant = giant * stride % modulus
    return sorted(solutions), width


def main():
    # The complete residue field is searched, including the nonunit zero.
    roots = [x for x in range(7) if polynomial(x) % 7 == 0]
    derivatives = [derivative(x) % 7 for x in roots]
    require(len(roots) == 1, "not exactly one root modulo seven")
    require(all(d != 0 for d in derivatives), "root is not simple")
    root_rows = [{"depth": 1, "modulus": 7, "roots": roots[:]}]
    modulus = 7
    for depth in range(2, 11):
        candidates = [x + digit * modulus for x in roots for digit in range(7)]
        new_modulus = 7 * modulus
        lifted = [x for x in candidates if polynomial(x) % new_modulus == 0]
        require(len(lifted) == len(roots), "nonunique or absent simple lift")
        require(all(derivative(x) % 7 != 0 for x in lifted),
                "derivative became nonunit")
        roots = lifted
        modulus = new_modulus
        root_rows.append({"depth": depth, "modulus": modulus, "roots": roots[:]})

    cycle = [pow(10, exponent, 7) for exponent in range(6)]
    require(len(set(cycle)) == 6 and pow(10, 6, 7) == 1,
            "order of ten modulo seven is not six")
    initial_depth = valuation(10**6 - 1, 7)
    require(initial_depth == 1, "LTE order-growth hypothesis failed")
    order_rows = []
    for depth in range(1, 11):
        current_modulus = 7**depth
        order = 6 * 7**(depth - 1)
        factors = [2, 3] if depth == 1 else [2, 3, 7]
        proper = {str(p): pow(10, order // p, current_modulus) for p in factors}
        require(pow(10, order, current_modulus) == 1, "claimed order is not a period")
        require(all(value != 1 for value in proper.values()), "claimed order is not minimal")
        order_rows.append({"depth": depth, "order": order,
                           "proper_prime_quotient_residues": proper})

    order = order_rows[-1]["order"]
    exponents, width = discrete_log(10, roots[0], modulus, order)
    require(len(exponents) == 1, "root does not have exactly one exponent class")
    representative = exponents[0]
    least_positive = representative if representative > 0 else order
    least_length = 12 * least_positive + 5
    image = pow(10, representative, modulus)
    require(image == roots[0] and polynomial(image) % modulus == 0,
            "recovered exponent does not reach the root")

    # Only now compare discoveries with the claims submitted for audit.
    observed = {"modulus": modulus, "order": order, "representative": representative,
                "power_residue": image, "least_possible_length": least_length}
    claimed = {"modulus": 282475249, "order": 242121642, "representative": 185987897,
               "power_residue": 213654628, "least_possible_length": 2231854769}
    require(observed == claimed, "a submitted numerical claim failed")

    # Nonzero controls exercise the equation, the discovered root, and the guard.
    require(polynomial(0) == -1, "constant-term control failed")
    perturbed = polynomial((roots[0] + 1) % modulus) % modulus
    require(perturbed != 0, "perturbed root was accepted")
    exact_control = polynomial(10**5)
    control_depth = valuation(exact_control, 7)
    require(control_depth == 1, "nonzero positive-depth polynomial control failed")
    explicit_failure_exercised = False
    try:
        require(False, "intentional negative guard control")
    except ValueError:
        explicit_failure_exercised = True
    require(explicit_failure_exercised, "explicit failure guard was disabled")

    result = {"status": "PASS", "method": "complete polynomial roots; Hensel; exhaustive BSGS",
              "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "initial_derivatives_mod7": derivatives, "root_lifts": root_rows,
              "ten_mod7_cycle": cycle, "v7_ten_to_six_minus_one": initial_depth,
              "orders": order_rows, "bsgs_width": width, "exponent_classes": exponents,
              "observed": observed,
              "controls": {"polynomial_at_zero": -1, "perturbed_root_residue": perturbed,
                           "u5_exact_depth": control_depth,
                           "explicit_failure_exercised": explicit_failure_exercised}}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
