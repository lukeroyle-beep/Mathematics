#!/usr/bin/env python3
"""Exact finite checks for COMMON_FACTOR.md; no arithmetic imports.

The proof remains a mathematical argument. Receipts supply exact constant
and finite-remainder evidence, not a numerical proof for infinitely many a.
All checks use explicit exceptions and remain active with python3 -O.
"""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from math import factorial, gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def valuation(value, prime=7):
    require(value != 0, "valuation requires nonzero integer")
    result = 0
    while value % prime == 0:
        value //= prime
        result += 1
    return result


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def exponential_lower(argument, terms):
    return sum((argument**k / factorial(k) for k in range(terms+1)), Fraction(0))


def finite_remainder():
    files = [PARENT / "power-three" / name
             for name in ("individuals.json", "individuals-independent.json")]
    files.append(PARENT / "power-three-pair" / "individual.json")
    data = [json.loads(path.read_text()) for path in files]
    rows = []
    for a in range(31, 100, 6):
        old = [next(row for row in datum["cases"] if row["a"] == a)
               for datum in data[:2]]
        old.append(next(row for row in data[2]["finite_rows_including_crossing_successor"]
                        if row["a"] == a))
        fields = ("a", "L", "S", "d", "s", "i", "t", "first_fail_depth",
                  "first_fail_n_residue")
        require(all(all(row[key] == old[0][key] for key in fields) for row in old),
                f"three inherited exact rows agree at a={a}")
        row = {key: old[0][key] for key in fields}
        S, L, d, s = row["S"], row["L"], row["d"], row["s"]
        require(S == 3**a and d == 3**(a-2) and 7*L == S+4, "family data")
        require(3 <= s < 2*d and s % 6 == 3 and L < 2*d, "unique joint range")
        require((7*pow(10, L, 9*S)-18*pow(10, s, 9*S)-25) % (9*S) == 0,
                "complete same-position sum condition")
        require(pow(10, d, S) == 1 and pow(10, d//3, S) != 1, "exact ternary order")
        if s >= L:
            require(row["i"] is None and row["t"] is None, "class miss")
            row["verdict"] = "class_miss"
        else:
            t, depth = row["t"], row["first_fail_depth"]
            require(row["i"] == s and depth == t+1 <= L-2, "actual failure deadline")
            modulus = 7**depth
            F = (7*pow(10, L, modulus)-18*pow(10, s, modulus)-25) % modulus
            require(F != 0 and valuation(F) == t, "exact seven valuation")
            # Division is by nine in Z/7^depth, where nine is a unit.
            n = F * pow(9, -1, modulus) % modulus
            require(n == row["first_fail_n_residue"], "original n residue")
            row["verdict"] = "seven_power_failure"
        rows.append(row)
    require(len(rows) == 12, "all twelve exponents below 100")
    return rows, {str(path.relative_to(PARENT)): digest(path) for path in files}


def hensel_controls():
    rows = []
    # Each is a non-family polynomial with q odd, gcd(p,q)=1,
    # L=gq=1 mod6 and s=gp=39 mod42. Include depth-three cases.
    for g, p, q in ((13, 3, 7), (13, 3, 19), (53, 15, 17), (83, 3, 17)):
        require(0 < p < q and gcd(p, q) == 1 and q % 2 == 1, "reduced odd degree")
        L, s, X = g*q, g*p, 10**g
        require(L % 6 == 1 and s % 42 == 39 and p % 7 != 0, "depth-two domain")
        F = 7*X**q - 18*X**p - 25
        derivative = 7*q*X**(q-1)-18*p*X**(p-1)
        t = valuation(F)
        require(F > 0 and t >= 2 and derivative % 7 != 0, "nonzero simple-Hensel input")
        alpha, modulus = X % 7, 7
        for _ in range(t):
            next_modulus = 7*modulus
            children = [alpha + digit*modulus for digit in range(7)
                        if (7*pow(alpha+digit*modulus, q, next_modulus)
                            -18*pow(alpha+digit*modulus, p, next_modulus)-25) % next_modulus == 0]
            require(len(children) == 1, "unique simple-root digit lift")
            alpha, modulus = children[0], next_modulus
        difference = (X-alpha) % modulus
        sixth_difference = (pow(X, 6, modulus)-pow(alpha, 6, modulus)) % modulus
        require(difference != 0 and valuation(difference) == t, "exact root distance")
        require(sixth_difference != 0 and valuation(sixth_difference) == t,
                "sixth powers preserve valuation")
        rows.append({"g": g, "p": p, "q": q, "L": L, "s": s, "t": t,
                     "alpha_mod_7_to_t_plus_1": alpha, "modulus": modulus,
                     "derivative_mod7": derivative % 7,
                     "distance_residue": difference, "sixth_power_distance_residue": sixth_difference})
    return rows


def build():
    require(7*pow(10, 1, 49) % 49 == 21, "family leading term")
    require(pow(18, -1, 49)*(-4) % 49 == 27, "depth-two rearrangement")
    require(pow(10, 39, 49) == 27 and valuation(10**6-1) == 1, "order ingredients")
    order7 = next(k for k in range(1, 7) if pow(10, k, 7) == 1)
    order49 = next(k for k in range(1, 43) if pow(10, k, 49) == 1)
    require((order7, order49) == (6, 42), "exact orders")
    residues = [(21-18*pow(10, s, 49)-25) % 49 for s in range(42)]
    require([s for s in range(42) if residues[s] == 0] == [39], "entire depth-two period")

    exponential = []
    for argument, terms, target in ((Fraction(5, 2), 12, 10),
                                    (Fraction(25, 6), 16, 50),
                                    (Fraction(2), 8, 7)):
        lower = exponential_lower(argument, terms)
        require(lower > target, "strict rational exponential comparison")
        exponential.append({"argument": str(argument), "terms_through": terms,
                            "target": target, "positive_margin": str(lower-target)})
    constant = 208*15*25*4
    require(constant == 312000, "valuation constant")
    left, right = 3**100, 7*(2*constant*120**2)**4
    require(left > right, "a=100 crossover")
    induction_margin = 3*20**8 - 21**8
    require(induction_margin > 0, "all-a ratio induction")
    first_length = (3**31+4)//7
    require(6*7**15 <= first_length < 6*7**16, "first family length has K=17")
    require(17**8 < 6*7**15 and 18**8 < 7*17**8, "old exact-centre inclusion")
    finite, inherited = finite_remainder()
    bound_inputs = ["power-three/INDIVIDUAL.md", "power-three-pair/PAIR.md",
                    "power-three-pair/LOGARITHMS.md", "power-three-pair/INDIVIDUAL.md",
                    "rational-centres/ANALYTIC.md"]
    inherited.update({name: digest(PARENT/name) for name in bound_inputs})
    return {"schema": 1, "base_main": "a9edeb0a96bd56d55f3c96767f5154e69cb8ceda",
            "source_sha256": digest(Path(__file__)), "proof_sha256": digest(HERE/"COMMON_FACTOR.md"),
            "inherited_sha256": inherited, "depth_two_F_residues_mod49": residues,
            "depth_two_surviving_s_mod42": [39], "rational_exponential_checks": exponential,
            "valuation_constant": constant, "cutoff_a": 100,
            "crossover_left": left, "crossover_right": right, "crossover_margin": left-right,
            "induction_margin_3_times_20_to_8_minus_21_to_8": induction_margin,
            "first_family_length": first_length, "first_family_K": 17,
            "old_exact_centre_base_margin": 6*7**15-17**8,
            "old_exact_centre_ratio_margin": 7*17**8-18**8,
            "finite_exponents": list(range(31,100,6)), "finite_rows": finite,
            "synthetic_hensel_controls": hensel_controls(), "lean_verification_performed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(build(), indent=2, sort_keys=True)+"\n"
    if args.check:
        require(args.check.read_text() == rendered, "retained math receipt matches exact recomputation")
        print("PASS: common-factor exact constants, complete small range and Hensel controls")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
