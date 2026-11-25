#!/usr/bin/env python3
"""Independent arithmetic review; finite controls are not analytic proofs.

Run without arguments. All checks use explicit exceptions and run under -O.
The modular crosscheck fully scans two small residue spaces; the delivered
implementations independently establish the complete depth-ten class.
"""

from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys


HERE = Path(__file__).resolve().parent


def need(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def exponential_bounds(x, degree=80):
    term = Fraction(1)
    partial = term
    for k in range(1, degree + 1):
        term *= x / k
        partial += term
    next_term = term * x / (degree + 1)
    tail_ratio = x / (degree + 2)
    need(0 <= tail_ratio < 1, "invalid exponential tail ratio")
    return partial, partial + next_term / (1 - tail_ratio)


def f_mod(u, modulus):
    return (7 * pow(10, 12*u + 5, modulus)
            - 18 * pow(10, 5*u + 2, modulus) - 25) % modulus


def main():
    # Rational certificates for the elementary logarithmic comparisons.
    need(exponential_bounds(Fraction(2303, 1000))[0] > 10,
         "log(10) upper bound failed")
    need(exponential_bounds(Fraction(389, 200))[1] < 7,
         "log(7) lower bound failed")
    need(exponential_bounds(Fraction(2))[0] > 7,
         "log(7) < 2 failed")
    need(exponential_bounds(Fraction(2))[1] < 10,
         "log(10) > 2 failed")
    need(exponential_bounds(Fraction(1))[0] > 2,
         "log(2) < 1 failed")
    need(exponential_bounds(Fraction(15))[0] > 3000000,
         "log(3000000) < 15 failed")
    source_coefficient_upper = (168 * Fraction(2303, 1000)**2
                                / Fraction(389, 200)**4)
    need(source_coefficient_upper < 63, "BL coefficient bound failed")
    need((Fraction(10**9, 168) + 1) / 2 < 3000000,
         "b-prime upper bound failed")
    need(Fraction(15) + 1 + Fraction(2, 5) < 20,
         "first logarithmic maximum entry exceeds 20")
    multiplier = Fraction(63 * 12**3 * 14 * 20**2, 10**9)
    need(multiplier == Fraction(47628, 78125), "wrong strip multiplier")
    margin = (1 - multiplier) * 10**9 - 2
    need(margin == 390361598 and margin > 0, "strict margin failed")
    need(Fraction(1, 12) + 13 <= 14, "threshold height comparison failed")
    need(Fraction(14, 10**9) < 1, "dependent height is not less than L")

    # Negative-offset controls for the general coefficient-span inequality.
    span_controls = 0
    for r in range(12):
        for s in range(-100, 101):
            delta = 12*s - 5*r
            span = max(0, r, s) - min(0, r, s)
            need(span <= Fraction(abs(delta), 12) + 11,
                 "coefficient-span control failed")
            span_controls += 1

    # Full scans, not lifting, independently check every class at depth five.
    small_modulus = 7**5
    small_order = 6 * 7**4
    field_roots = [x for x in range(small_modulus)
                   if (28000*x**12 - 72*x**5 - 1) % small_modulus == 0]
    exponent_roots = [u for u in range(small_order)
                      if f_mod(u, small_modulus) == 0]
    need(len(field_roots) == len(exponent_roots) == 1,
         "small exhaustive residue spaces have unexpected roots")
    need(pow(10, exponent_roots[0], small_modulus) == field_roots[0],
         "small exhaustive polynomial and F roots disagree")

    runs = {}
    for name in ("modular_roots", "modular_exponents"):
        source = HERE / (name + ".py")
        normal = subprocess.check_output([sys.executable, str(source)])
        optimized = subprocess.check_output([sys.executable, "-O", str(source)])
        need(normal == optimized, name + " changes under -O")
        need(normal == (HERE / (name + ".json")).read_bytes(),
             name + " stored receipt differs from execution")
        receipt = json.loads(normal)
        need(receipt["source_sha256"] == sha256(source.read_bytes()).hexdigest(),
             name + " source hash mismatch")
        need(receipt["status"] == "PASS", name + " failed")
        runs[name] = receipt
    observed = runs["modular_roots"]["observed"]
    need(observed == runs["modular_exponents"]["observed"],
         "independent depth-ten implementations disagree")
    u = observed["representative"]
    modulus = observed["modulus"]
    need(u % small_order == exponent_roots[0], "depth-five projection failed")
    need(observed["power_residue"] % small_modulus == field_roots[0],
         "depth-five root projection failed")
    need(f_mod(u, modulus) == 0 and f_mod(u, 7*modulus) != 0,
         "nonzero exact-depth-ten control failed")
    need(f_mod(5, 7) == 0 and f_mod(5, 49) != 0,
         "nonzero exact-depth-one control failed")
    need(12*u + 5 == observed["least_possible_length"] > 10**9,
         "line cutoff arithmetic failed")
    need(u > 0 and u - observed["order"] < 0, "least exponent check failed")

    guard_checked = False
    try:
        need(False, "intentional review guard failure")
    except RuntimeError:
        guard_checked = True
    need(guard_checked, "review failure guard disabled")
    print(json.dumps({
        "status": "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "BL_coefficient_upper_rational": str(source_coefficient_upper),
        "strip_multiplier": str(multiplier),
        "threshold_strict_margin": int(margin),
        "span_finite_controls": span_controls,
        "full_scan_depth": 5,
        "full_scan_polynomial_residues": small_modulus,
        "full_scan_exponent_classes": small_order,
        "full_scan_polynomial_roots": field_roots,
        "full_scan_exponent_roots": exponent_roots,
        "depth_ten_observed": observed,
        "normal_and_optimized_receipts_agree": True,
        "explicit_failure_exercised": guard_checked,
        "scope": "Arithmetic review and finite controls; analytic proof reviewed separately."
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
