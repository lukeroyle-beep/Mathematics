#!/usr/bin/env python3
"""Independent complete modular audit; no imports from project arithmetic.

The derivative is calculated by a finite difference modulo 343**2, not by
calling or copying a primary derivative evaluator. Every check uses explicit
exceptions so that python3 -O retains exactly the same acceptance predicate.
"""

from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def source_hashes():
    files = [Path(__file__).resolve()] + [
        HERE.parent / "power-three" / name
        for name in ("README.md", "INDIVIDUAL.md", "THREE_LENGTH.md", "REVIEW.md")
    ]
    return {
        path.relative_to(ROOT).as_posix(): sha256(path.read_bytes()).hexdigest()
        for path in files
    }


def vp(n, p):
    require(n != 0, "valuation of zero is not a finite certificate")
    count = 0
    while n % p == 0:
        count += 1
        n //= p
    return count


def parameters(u):
    a = 31 + 6 * u
    d = 3 ** (a - 2)
    require((9 * d + 4) % 7 == 0, "nonintegral length")
    length = (9 * d + 4) // 7
    next_length = (9 * 729 * d + 4) // 7
    require(next_length - length == 936 * d, "length difference")
    require((d - 5) % 7 == 0, "d residue")
    w = (d - 5) // 7
    require(w % 6 == 4, "w residue")
    require(length == 9 * w + 7, "first affine length")
    require(next_length == 6561 * w + 4687, "second affine length")
    return d, length, next_length, w


def transition(u, modulus):
    d, length, next_length, _ = parameters(u)
    return (
        (7 * pow(10, length, modulus) - 25) % modulus,
        (7 * pow(10, next_length, modulus) - 25) % modulus,
        pow(10, 2 * d, modulus),
    )


def polynomial(k):
    # Expand the stated polynomial into its four monomials; no derivative
    # coefficients or predicted residues are inserted here.
    result = {}
    for power, coefficient in (
        (6561, 7 * 10**4687),
        (0, -25),
        (14 * k + 9, -7 * 10 ** (10 * k + 7)),
        (14 * k, 25 * 10 ** (10 * k)),
    ):
        result[power] = result.get(power, 0) + coefficient
    return {power: coefficient for power, coefficient in result.items() if coefficient}


def evaluate(poly, x, modulus):
    return sum(coefficient * pow(x, power, modulus) for power, coefficient in poly.items()) % modulus


def run():
    require(next(t for t in range(1, 7) if pow(10, t, 7) == 1) == 6, "order modulo 7")
    require(vp(10**6 - 1, 7) == 1, "order lifting seed")
    require(vp(729**7 - 1, 7) == 2, "seven-start period seed")

    transitions = []
    all_sets = []
    for u in range(7):
        left, right, multiplier = transition(u, 343)
        # Every k in the actual-position superset, including both endpoints.
        surviving = [k for k in range(469) if left * pow(multiplier, k, 343) % 343 == right]
        all_sets.append(surviving)
        require(transition(u + 7, 343) == (left, right, multiplier), "period spot check")
        transitions.append({"u": u, "U": left, "U_next": right, "G": multiplier, "k": surviving})
    candidates = all_sets[0]
    require(all(row == candidates for row in all_sets), "dependence on u residue")
    require(candidates == list(range(42, 469, 49)), "claimed residue class not reproduced")

    # 10^w modulo 343 has period 294. Exactly 49 of those w classes are 4 mod6.
    eligible_w = list(range(4, 294, 6))
    require(len(eligible_w) == 49, "eligible-class count")
    require(pow(10, 294, 343) == 1, "derivative period")
    derivative_rows = []
    modulus = 343**2
    for k in candidates:
        poly = polynomial(k)
        require(max(poly) == 6561, "degree")
        for w in eligible_w:
            x = pow(10, w, modulus)
            h0 = evaluate(poly, x, modulus)
            h1 = evaluate(poly, x + 343, modulus)
            numerator = (h1 - h0) % modulus
            require(numerator % 343 == 0, "finite-difference exact division")
            derivative = numerator // 343
            require(derivative == 49, "derivative is not 49 modulo 343")
            derivative_rows.append({"k": k, "w_mod_294": w, "derivative_mod_343": derivative})

    # Evaluate the two sides independently on actual admissible lengths.
    # These are identity checks, not claims that s=3 is sum compatible.
    moduli = [343, 2401, 7**8, 3**12, 101, 1009]
    identity_checks = 0
    for u in range(14):
        d, length, next_length, w = parameters(u)
        for k in candidates:
            s = 3
            s_next = s + 2 * d * k
            require(s < length and s_next < next_length, "identity-test positions not actual")
            for m in moduli:
                f = (7 * pow(10, length, m) - 18 * pow(10, s, m) - 25) % m
                f_next = (7 * pow(10, next_length, m) - 18 * pow(10, s_next, m) - 25) % m
                direct = (f_next - pow(10, 2 * d * k, m) * f) % m
                eliminated = evaluate(polynomial(k), pow(10, w, m), m)
                require(direct == eliminated, "eliminant identity mismatch")
                identity_checks += 1

    # Positivity is proved symbolically in ELIMINANT_REVIEW.md. The exact
    # endpoint predicates below record the complete integer k interval used.
    for k in range(469):
        require(468 - k >= 0 and k >= 0, "negative exponent in positivity proof")
        require(468 - k > 0 or k > 0, "both positive summands vanish")

    return {
        "schema": "a398769-power-three-pair-independent-modular-v1",
        "source_sha256": source_hashes(),
        "depth_three": {
            "modulus": 343,
            "u_period": 7,
            "k_inclusive_bounds": [0, 468],
            "tests": 7 * 469,
            "rows": transitions,
            "surviving_k": candidates,
        },
        "derivative": {
            "method": "(H(x+343)-H(x))/343 modulo343, calculated modulo343^2",
            "w_period": 294,
            "eligible_w_mod_6": 4,
            "eligible_classes": 49,
            "tests": len(derivative_rows),
            "rows": derivative_rows,
        },
        "eliminant_identity_modular_checks": identity_checks,
        "identity_moduli": moduli,
        "positivity_k_inclusive_bounds": [0, 468],
        "result": "PASS",
    }


def main():
    result = run()
    encoded = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if len(sys.argv) == 3 and sys.argv[1] == "--check":
        require(Path(sys.argv[2]).read_text() == encoded, "retained receipt differs")
        print("PASS: complete independent modular receipt and source bindings")
    elif len(sys.argv) == 1:
        print(encoded, end="")
    else:
        raise SystemExit("usage: independent_modular.py [--check RECEIPT.json]")


if __name__ == "__main__":
    main()
