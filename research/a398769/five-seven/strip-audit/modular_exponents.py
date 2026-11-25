#!/usr/bin/env python3
"""Exhaust all exponent classes by lifting the original F, without P.

This implementation imports no other checker and never uses a supplied
representative to initialize the search. Checks remain active under -O.
"""

import hashlib
import json
from pathlib import Path


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def original_f(u, modulus):
    length = 12 * u + 5
    position = 5 * u + 2
    return (7 * pow(10, length, modulus)
            - 18 * pow(10, position, modulus) - 25) % modulus


def main():
    # Determine the starting period and then the successive exact orders.
    first_periods = [n for n in range(1, 7) if pow(10, n, 7) == 1]
    check(first_periods == [6], "initial order discovery failed")
    period = first_periods[0]
    classes = list(range(period))
    modulus = 1
    rows = []
    for depth in range(1, 11):
        modulus *= 7
        if depth > 1:
            previous_period = period
            multipliers = [m for m in range(1, 8)
                           if pow(10, previous_period * m, modulus) == 1]
            check(multipliers, "no next order found in the sevenfold bound")
            period = previous_period * min(multipliers)
            check(period == 7 * previous_period, "order did not grow sevenfold")
            # Every class above a surviving old class is tried once.
            classes = [u + digit * previous_period for u in classes for digit in range(7)]
        candidate_count = len(classes)
        check(len(set(classes)) == candidate_count, "repeated exponent candidate")
        check(all(0 <= u < period for u in classes), "class out of canonical range")
        evaluated = [{"u": u, "F_modulus": original_f(u, modulus)} for u in classes]
        classes = sorted(row["u"] for row in evaluated if row["F_modulus"] == 0)
        check(len(classes) == 1, "unexpected number of surviving classes")
        rows.append({"depth": depth, "modulus": modulus, "period": period,
                     "candidates_tested": candidate_count, "evaluated": evaluated,
                     "surviving_classes": classes[:]})

    discovered = classes[0]
    least_positive = discovered if discovered else period
    least_length = 12 * least_positive + 5
    residue = pow(10, discovered, modulus)
    result_values = {"modulus": modulus, "order": period, "representative": discovered,
                     "power_residue": residue, "least_possible_length": least_length}
    # Audit claims after the complete original-F enumeration is finished.
    check(result_values == {"modulus": 282475249, "order": 242121642,
                            "representative": 185987897, "power_residue": 213654628,
                            "least_possible_length": 2231854769},
          "submitted numerical claims disagree with complete F lifting")
    check(discovered > 0 and discovered - period < 0, "incorrect least positive exponent")
    check(least_length > 10**9, "certificate does not reach the requested cutoff")

    # Exact positive-depth and nonzero controls, always on the original F.
    check(original_f(5, 7) == 0 and original_f(5, 49) != 0,
          "u=5 is not an exact depth-one positive control")
    next_residue = original_f(discovered, 7 * modulus)
    check(next_residue != 0 and next_residue % modulus == 0,
          "reported representative is not an exact depth-ten positive control")
    check(original_f(discovered + 1, modulus) != 0, "perturbed exponent was accepted")
    check(original_f(discovered + period, modulus) == 0, "periodic positive control failed")
    guard = False
    try:
        check(False, "intentional negative guard control")
    except RuntimeError:
        guard = True
    check(guard, "explicit failure guard was disabled")

    print(json.dumps({"status": "PASS", "method": "all six initial classes; original-F exponent lifting",
                      "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      "lifts": rows, "observed": result_values,
                      "controls": {"u5_F_mod49": original_f(5, 49),
                                   "representative_F_mod7_to11": next_residue,
                                   "representative_exact_depth": 10,
                                   "perturbed_exponent_residue": original_f(discovered + 1, modulus),
                                   "next_period_residue": original_f(discovered + period, modulus),
                                   "explicit_failure_exercised": guard}},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
