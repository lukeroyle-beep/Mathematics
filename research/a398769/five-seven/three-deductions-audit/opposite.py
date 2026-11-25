#!/usr/bin/env python3
"""Unseeded exhaustive audit of 12*i-5*L=+1; standard library only."""
from hashlib import sha256
from math import isqrt
from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def original_f(u, modulus):
    return (7 * pow(10, 12*u + 7, modulus)
            - 18 * pow(10, 5*u + 3, modulus) - 25) % modulus


def polynomial(x, modulus):
    return (2800000 * pow(x, 12, modulus)
            - 720 * pow(x, 5, modulus) - 1) % modulus


def derivative(x, modulus):
    return (33600000 * pow(x, 11, modulus)
            - 3600 * pow(x, 4, modulus)) % modulus


def exponent_route(depth):
    # Discover the initial order; test all six exponent classes, no seed.
    order = next(j for j in range(1, 7) if pow(10, j, 7) == 1)
    modulus = 7
    classes = list(range(order))
    rows = []
    for k in range(1, depth + 1):
        if k > 1:
            modulus *= 7
            new_order = next(order*j for j in range(1, 8)
                             if pow(10, order*j, modulus) == 1)
            classes = [u + j*order for u in classes
                       for j in range(new_order // order)]
            order = new_order
        candidates = [[u, original_f(u, modulus)] for u in classes]
        classes = [u for u, residue in candidates if residue == 0]
        require(len(classes) == 1, "exponent branch is not unique")
        require(order == 6*7**(k-1), "unexpected exact order")
        rows.append({"k": k, "modulus": modulus, "order": order,
                     "candidates": candidates, "classes": classes})
    return rows


def root_route(depth):
    # Evaluate all seven field residues, independently of exponent_route.
    modulus = 7
    roots = list(range(7))
    rows = []
    for k in range(1, depth + 1):
        if k > 1:
            old_modulus = modulus
            modulus *= 7
            roots = [r + j*old_modulus for r in roots for j in range(7)]
        candidates = [[r, polynomial(r, modulus)] for r in roots]
        roots = [r for r, residue in candidates if residue == 0]
        require(len(roots) == 1, "polynomial root is not unique")
        require(derivative(roots[0], 7) != 0, "root is not simple")
        rows.append({"k": k, "modulus": modulus, "candidates": candidates,
                     "roots": roots, "derivative_mod7": derivative(roots[0], 7)})
    # Independent exhaustive baby-step/giant-step discrete logarithm.
    order = 6*7**(depth-1)
    require(pow(10, order, modulus) == 1, "claimed order is not a period")
    divisors = [2, 3] + ([7] if depth > 1 else [])
    for prime in divisors:
        require(pow(10, order//prime, modulus) != 1,
                "claimed order is not minimal")
    width = isqrt(order) + 1
    babies = {}
    power = 1
    for b in range(width):
        require(power not in babies, "noninjective baby powers")
        babies[power] = b
        power = power*10 % modulus
    factor = pow(pow(10, width, modulus), -1, modulus)
    target = roots[0]
    matches = []
    blocks = (order + width - 1)//width
    for a in range(blocks):
        if target in babies:
            u = a*width + babies[target]
            if u < order:
                require(pow(10, u, modulus) == roots[0], "false log match")
                matches.append(u)
        target = target*factor % modulus
    require(len(matches) == 1, "discrete logarithm is not unique")
    return rows, {"order": order, "root": roots[0], "width": width,
                  "blocks": blocks, "classes": matches}


def main():
    exponent_rows = exponent_route(11)
    root_rows, log = root_route(11)
    require(exponent_rows[-1]["classes"] == log["classes"], "routes disagree")
    # Submitted claims are compared only after both discoveries finish.
    u = log["classes"][0]
    period = log["order"]
    require(u == 313281594, "submitted exponent fails")
    require(period == 1694851494, "submitted period fails")
    L, i = 12*u+7, 5*u+3
    require(L == 3759379135, "submitted least length fails")
    require(0 <= u < period and u-period < 0, "not least nonnegative class")
    require(L > 10**9, "modular and strip ranges do not overlap")
    for row in exponent_rows:
        k = row["k"]
        r = root_rows[k-1]["roots"][0]
        require(pow(10, row["classes"][0], row["modulus"]) == r,
                "intermediate root and exponent disagree")
    identities = 0
    for small_u in range(31):
        small_L, small_i = 12*small_u+7, 5*small_u+3
        F = 7*10**small_L - 18*10**small_i - 25
        P = 2800000*(10**small_u)**12 - 720*(10**small_u)**5 - 1
        require(F == 25*P, "polynomial identity fails")
        require(12*small_i-5*small_L == 1, "line identity fails")
        require(small_L >= 5 and small_L % 2 == 1 and 3 <= small_i < small_L,
                "parametrization domain fails")
        identities += 1
    small_F = 7*10**7 - 18*10**3 - 25
    require(small_F == 69981975 and small_F % 49 == 28, "small case fails")
    require(small_F % 7 == 0, "small positive-depth control fails")
    require(small_F % (9*45) == 0, "small-case digit-sum check fails")
    modulus = 7**11
    controls = {"u0_F": small_F, "u0_F_mod49": small_F % 49,
                "u0_exact_valuation": 1,
                "u0_S": 45, "u0_F_mod9S": small_F % (9*45),
                "representative_F_mod_7pow12": original_f(u, 7**12),
                "period_shift_residue": original_f(u+period, modulus),
                "adjacent_residue": original_f(u+1, modulus),
                "root_adjacent_residue": polynomial(log["root"]+1, modulus)}
    require(controls["representative_F_mod_7pow12"] % modulus == 0,
            "final positive-depth control fails")
    require(controls["representative_F_mod_7pow12"] != 0,
            "representative has greater depth than eleven")
    require(controls["period_shift_residue"] == 0, "periodicity fails")
    require(controls["adjacent_residue"] != 0, "adjacent rejection fails")
    require(controls["root_adjacent_residue"] != 0, "root rejection fails")
    negative_controls = 0
    for condition in [u == 313281595, period == 1694851495,
                      controls["adjacent_residue"] == 0]:
        try:
            require(condition, "intentional negative control")
        except RuntimeError:
            negative_controls += 1
    require(negative_controls == 3, "failure guard disabled")
    report = {"schema": 1, "claim": "opposite line 12i-5L=+1",
              "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "verdict": "PASS", "exponent_route": exponent_rows,
              "root_route": root_rows, "discrete_log": log,
              "observed": {"k": 11, "modulus": modulus, "u": u,
                           "period": period, "L": L, "i": i,
                           "least_permitted_L": L, "exact_valuation": 11},
              "controls": controls, "direct_integer_identity_cases": identities,
              "negative_controls_rejected": negative_controls,
              "scope": "one position per eligible length; no whole-length extension"}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
