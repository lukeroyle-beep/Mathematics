#!/usr/bin/env python3
"""Independent projected-transition audit by complete residue-class lifting.

No arithmetic is imported from the direct enumerator. Every allowed increment
is tested; no observed count or control value seeds the search.
"""

import argparse
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def values(u, m):
    """Compute U_u,G_u with full exponent-period precision, before multiplying 7."""
    require(u >= 0 and m >= 2, "invalid index or depth")
    a = 31 + 6 * u
    modulus = 7 ** m
    exponent_period = 6 * 7 ** (m - 1)
    numerator = pow(3, a, 7 * exponent_period) + 4
    require(numerator % 7 == 0, "length numerator lost divisibility")
    length = numerator // 7
    twice_d = 2 * pow(3, a - 2, exponent_period)
    return (7 * pow(10, length, modulus) - 25) % modulus, pow(10, twice_d, modulus)


def increments(u, m):
    """Return every k in [0,728] satisfying U_u G_u^k = U_(u+1)."""
    modulus = 7 ** m
    source, generator = values(u, m)
    target = values(u + 1, m)[0]
    found = []
    current = source
    for k in range(729):
        if current == target:
            found.append(k)
        current = current * generator % modulus
    return found


def projected_start(u, m):
    first = increments(u, m)
    if not first:
        return None
    second = increments(u + 1, m)
    if not second:
        return None
    return {"u": u, "first_increments": first, "second_increments": second}


def level(m, candidates):
    rows = []
    for u in sorted(candidates):
        row = projected_start(u, m)
        if row is not None:
            rows.append(row)
    period = 7 ** (m - 2)
    require(all(0 <= row["u"] < period for row in rows), "out-of-period start")
    return {"m": m, "period": period, "tested_starts": len(candidates),
            "start_count": len(rows), "starts": rows}


def audit():
    # m=2 has period one, so the initial search is complete. Reduction of a
    # surviving transition modulo 7^(m-1) preserves its same bounded increment.
    # Consequently every higher-depth start reduces to a previous survivor;
    # all seven lifts of each such start are therefore necessary and sufficient.
    levels = []
    candidates = [0]
    for m in range(2, 10):
        result = level(m, candidates)
        levels.append(result)
        old_period = result["period"]
        candidates = [row["u"] + j * old_period
                      for row in result["starts"] for j in range(7)]
        require(len(candidates) == len(set(candidates)), "duplicate lift")

    # Literal big-integer exponents for small u independently check reduction
    # before division by seven, not merely equivalence of two reduced formulas.
    literal_checks = 0
    for u in range(5):
        a = 31 + 6 * u
        length = (3 ** a + 4) // 7
        twice_d = 2 * 3 ** (a - 2)
        for m in range(2, 10):
            modulus = 7 ** m
            exact = ((7 * pow(10, length, modulus) - 25) % modulus,
                     pow(10, twice_d, modulus))
            require(values(u, m) == exact, "literal exponent control failed")
            literal_checks += 1

    # Endpoint checks explicitly exercise a transition across the period end
    # and the subsequent transition across that same end in a three-term window.
    period_checks = []
    for m in range(2, 10):
        period = 7 ** (m - 2)
        probes = sorted({0, 1, period - 1, period, 2 * period - 1})
        for u in probes:
            require(values(u + period, m) == values(u, m), "period check failed")
            require(increments(u + period, m) == increments(u, m), "wrap check failed")
        require(projected_start(period - 1, m) ==
                (None if projected_start(2 * period - 1, m) is None else
                 dict(projected_start(2 * period - 1, m), u=period - 1)),
                "triple wrap failed")
        period_checks.append({"m": m, "probes": probes})

    # A published positive control is checked after enumeration. Both transitions
    # pass at depth eight and each increment has both an excluded endpoint
    # neighbour and a wrong target control; no vacuous empty-loop pass is possible.
    control_u, control_m = 14984, 8
    positive = projected_start(control_u, control_m)
    require(positive is not None, "positive control start absent")
    require(189 in positive["first_increments"] and 42 in positive["second_increments"],
            "positive control increments absent")
    require(positive in levels[6]["starts"], "positive control omitted by lifting")
    control_residues = []
    for u, k in [(control_u, 189), (control_u + 1, 42)]:
        source, generator = values(u, control_m)
        target = values(u + 1, control_m)[0]
        modulus = 7 ** control_m
        require((source * pow(generator, k, modulus) - target) % modulus == 0,
                "direct positive-control power failed")
        wrong_k = (source * pow(generator, k + 1, modulus) - target) % modulus
        wrong_target = (source * pow(generator, k, modulus) - target - 1) % modulus
        require(wrong_k != 0 and wrong_target != 0, "negative control passed")
        control_residues.append({"u": u, "k": k, "wrong_k_residue": wrong_k,
                                 "wrong_target_residue": wrong_target})

    return {"schema": 1, "method": "all seven lifts of every surviving start class",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "increment_range_inclusive": [0, 728], "levels": levels,
            "literal_exponent_controls": literal_checks,
            "period_and_wrap_controls": period_checks,
            "positive_control": positive, "negative_controls": control_residues,
            "depth_nine_projected_start_count": levels[-1]["start_count"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, help="require byte-for-byte receipt equality")
    args = parser.parse_args()
    output = json.dumps(audit(), indent=2, sort_keys=True) + "\n"
    if args.check is not None:
        require(args.check.read_text() == output, "receipt mismatch")
    print(output, end="")


if __name__ == "__main__":
    main()
