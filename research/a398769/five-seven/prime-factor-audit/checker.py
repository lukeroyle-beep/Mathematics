#!/usr/bin/env python3
"""Exact independent line audit. Essential checks survive Python -O.

Default: standard-library Sylvester/Bareiss determinant, deterministic Lucas
certificate verification, two complete divisor enumerations and modular tests.
--sympy adds the independent symbolic resultant cross-check.
"""

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import platform

FACTORS = {2: 7, 3: 24, 5: 25, 7: 1, 13: 1, 23: 1, 211: 1,
           1237: 1, 1289: 1, 1327: 1, 2609: 1, 7043: 1, 11399: 1,
           11831: 1, 903649: 1, 555700252411: 1, 4920652182747643: 1,
           958850750886621892231: 1, 4240701096684867281569789303: 1}
SUBSET_PRIMES = tuple(p for p in FACTORS if p not in (2, 3, 5, 7))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def multiply(a, b):
    """Ascending coefficient lists, plain integer convolution."""
    result = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result


def polynomials():
    p = [-10**5] + [0] * 6 + [1]
    q = [1]
    for _ in range(12):
        q = multiply(q, [-25, 7])
    q = [10 * x for x in q]
    q[5] -= 18**12
    return p, q


def sylvester(p, q):
    """Rows contain descending coefficients of shifted P then shifted Q."""
    m, n = len(p) - 1, len(q) - 1
    pp, qq = list(reversed(p)), list(reversed(q))
    return ([[0] * k + pp + [0] * (n - 1 - k) for k in range(n)] +
            [[0] * k + qq + [0] * (m - 1 - k) for k in range(m)])


def determinant(matrix):
    """Fraction-free Bareiss elimination; every division is checked exact."""
    n = len(matrix)
    require(n > 0 and all(len(row) == n for row in matrix), "square matrix")
    a = [row[:] for row in matrix]
    sign, previous = 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot_row = next((j for j in range(k + 1, n) if a[j][k]), None)
            if pivot_row is None:
                return 0
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = pivot * a[i][j] - a[i][k] * a[k][j]
                quotient, remainder = divmod(numerator, previous)
                require(remainder == 0, "Bareiss division is not exact")
                a[i][j] = quotient
        for i in range(k + 1, n):
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def verify_certificates(payload, roots):
    """Prove primes recursively by the full factorization of n-1.

    For every certified prime q|n-1 the witness has a^(n-1)=1 mod n and
    gcd(a^((n-1)/q)-1,n)=1. Thus every prime divisor r of n has n-1|r-1,
    so r>=n and n is prime. Recursion bottoms out at 2.
    """
    records = {}
    for record in payload["certificates"]:
        n = int(record["n"])
        require(n not in records, "duplicate certificate")
        records[n] = record
    verified, visiting = set(), set()

    def verify(n):
        if n in verified:
            return
        require(n >= 2 and n in records, "missing certificate or invalid integer")
        require(n not in visiting, "certificate cycle")
        visiting.add(n)
        record = records[n]
        if n == 2:
            require(record["base"] is None and record["factors"] == [], "base case")
        else:
            a = int(record["base"])
            require(1 < a < n, "invalid Lucas base")
            factors = [(int(p), e) for p, e in record["factors"]]
            require(len({p for p, _ in factors}) == len(factors), "duplicate n-1 factor")
            require(all(isinstance(e, int) and e > 0 and 2 <= p < n
                        for p, e in factors), "invalid n-1 factor")
            require(math.prod(p**e for p, e in factors) == n - 1, "incomplete n-1 factorization")
            for p, _ in factors:
                verify(p)
            require(pow(a, n - 1, n) == 1, "failed Lucas power")
            for p, _ in factors:
                require(math.gcd(pow(a, (n - 1) // p, n) - 1, n) == 1,
                        "failed Lucas gcd")
        visiting.remove(n)
        verified.add(n)

    require(set(map(int, payload["roots"])) == set(roots), "wrong certificate roots")
    for n in roots:
        verify(n)
    require(verified == set(records), "unused certificate entries")
    return sorted(verified)


def check_factorization(resultant, factors):
    require(abs(resultant) == math.prod(p**e for p, e in factors.items()),
            "factorization product mismatch")
    remainder = abs(resultant)
    observed = {}
    for p, expected in sorted(factors.items()):
        exponent = 0
        while remainder % p == 0:
            remainder //= p
            exponent += 1
        require(exponent == expected, f"multiplicity mismatch for {p}")
        observed[str(p)] = exponent
    require(remainder == 1, "unfactored cofactor")
    return observed


def subsets_by_masks(primes):
    output = []
    for mask in range(1 << len(primes)):
        value = 1
        for k, prime in enumerate(primes):
            if mask & (1 << k):
                value *= prime
        output.append(value)
    return sorted(output)


def subsets_by_recursion(primes):
    def visit(k, product):
        if k == len(primes):
            yield product
        else:
            yield from visit(k + 1, product)
            yield from visit(k + 1, product * primes[k])
    return sorted(visit(0, 1))


def modular_power(base, exponent, modulus):
    """Independent square-and-multiply for cross-checking Python pow."""
    result = 1
    while exponent:
        if exponent & 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent //= 2
    return result % modulus


def repunit_mod(length, modulus):
    """Return sum(10^j,j=0..length-1) by divide-and-conquer concatenation."""
    power, repunit = 1, 0
    for digit in bin(length)[2:]:
        repunit = repunit * (1 + power) % modulus
        power = power * power % modulus
        if digit == "1":
            repunit = (10 * repunit + 1) % modulus
            power = 10 * power % modulus
    return repunit


def line_record(s):
    require(s % 84 == 31, "not on line")
    u = (s - 31) // 84
    length, position = 12 * u + 5, 5 * u + 2
    require(u >= 1 and 3 <= position < length, "not an actual position")
    require(12 * position - 5 * length == -1 and 7 * length - 4 == s,
            "line parameters")
    require(length % 2 == 1 and s % 5 != 0, "line domain")
    residues = {}
    for modulus in (s, 9 * s):
        x, z = pow(10, length, modulus), pow(10, position, modulus)
        require(x == modular_power(10, length, modulus), "power L disagreement")
        require(z == modular_power(10, position, modulus), "power i disagreement")
        residues[str(modulus)] = {"ten_to_L": str(x), "ten_to_i": str(z),
                                  "F": str((7 * x - 18 * z - 25) % modulus)}
    # n is the length-L all-seven word minus two at positions zero and i.
    n_mod_s = (7 * repunit_mod(length, s) - 2 * modular_power(10, position, s) - 2) % s
    require(9 * n_mod_s == int(residues[str(9 * s)]["F"]), "repunit F disagreement")
    return {"S": str(s), "u": str(u), "L": str(length), "i": str(position),
            "fermat_residue": str(pow(10, s - 1, s)), "residues": residues}


def digest_integers(values):
    return hashlib.sha256("".join(f"{n}\n" for n in values).encode("ascii")).hexdigest()


def must_reject(action, label):
    try:
        action()
    except ValueError:
        return label
    raise ValueError(f"negative self-check accepted: {label}")


def self_checks(payload, resultant):
    require(determinant([[0, 1], [1, 0]]) == -1, "row-swap determinant control")
    require(determinant([[1, 2], [2, 4]]) == 0, "singular determinant control")
    require(determinant(sylvester([-2, 1], [-3, 1])) == -1, "resultant sign control")
    bad = copy.deepcopy(payload)
    next(r for r in bad["certificates"] if r["n"] == "13")["base"] = "3"
    outcomes = [must_reject(lambda: verify_certificates(bad, FACTORS), "failed Lucas gcd")]
    incomplete = copy.deepcopy(payload)
    next(r for r in incomplete["certificates"] if r["n"] == "13")["factors"].pop()
    outcomes.append(must_reject(lambda: verify_certificates(incomplete, FACTORS),
                                "incomplete n-1 factorization"))
    bad_factors = dict(FACTORS)
    bad_factors[3] -= 1
    outcomes.append(must_reject(lambda: check_factorization(resultant, bad_factors),
                                "missing factor multiplicity"))
    outcomes.append(must_reject(lambda: check_factorization(resultant + 1, FACTORS),
                                "perturbed resultant"))
    return outcomes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sympy", action="store_true", help="cross-check with SymPy resultant")
    args = parser.parse_args()
    certificate_path = Path(__file__).with_name("primality_certificates.json")
    certificate_bytes = certificate_path.read_bytes()
    payload = json.loads(certificate_bytes)
    certified = verify_certificates(payload, FACTORS)
    p, q = polynomials()
    matrix = sylvester(p, q)
    resultant = determinant(matrix)
    require(resultant != 0, "zero resultant")
    factorization = check_factorization(resultant, FACTORS)
    symbolic = None
    if args.sympy:
        import sympy
        x = sympy.Symbol("X")
        # Construct independently, without using the coefficient lists above.
        symbolic_resultant = int(sympy.resultant(x**7 - 10**5,
                                  10 * (7*x - 25)**12 - 18**12 * x**5, x))
        require(symbolic_resultant == resultant, "independent resultants disagree")
        symbolic = {"version": sympy.__version__, "resultant_matches": True}
    masks, recursive = subsets_by_masks(SUBSET_PRIMES), subsets_by_recursion(SUBSET_PRIMES)
    require(masks == recursive, "independent divisor lists disagree")
    require(len(masks) == len(set(masks)) == 32768, "subset count")
    eligible = [s for s in masks if s % 84 == 31]
    require(len(eligible) == 1360, "congruence count")
    require(all(s > 31 and (s - 31) // 84 >= 1 for s in eligible),
            "congruence list includes a non-actual line parameter")
    survivors = [s for s in eligible if pow(10, s - 1, s) == 1]
    survivors_independent = [s for s in recursive if s % 84 == 31 and
                            modular_power(10, s - 1, s) == 1]
    require(survivors == survivors_independent, "Fermat enumerations disagree")
    require(survivors == [555700252411], "survivor list")
    survivor_records = [line_record(s) for s in survivors]
    record = survivor_records[0]
    require((int(record["L"]), int(record["i"])) == (79385750345, 33077395977),
            "reported survivor L/i")
    require(record["residues"][record["S"]] == {
        "ten_to_L": "79923024499", "ten_to_i": "166905216978", "F": "333668527919"},
        "reported survivor residues")
    require(all(int(r["residues"][str(9 * int(r["S"]))]["F"]) != 0
                for r in survivor_records), "line exclusion fails")
    require(451 == 11 * 41, "composite control factorization")
    require(all(all(n % d for d in range(2, math.isqrt(n) + 1)) for n in (11, 41)),
            "composite control factor primality")
    control = line_record(451)
    require((control["L"], control["i"], control["fermat_residue"]) == ("65", "27", "1"),
            "composite control parameters/Fermat")
    require(control["residues"]["4059"]["F"] == "2241", "composite control F")
    # Boundary u=0 is not an actual position; both parities occur for u>=1.
    require((12 * 0 + 5, 5 * 0 + 2) == (5, 2), "line boundary")
    require({(5 * u + 2) % 2 for u in (1, 2)} == {0, 1}, "position parities")
    output = {"status": "PASS", "python_version": platform.python_version(),
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "integer_arithmetic": "Python arbitrary precision; no floating point",
              "sylvester_dimension": len(matrix), "resultant": str(resultant),
              "factorization": factorization, "certified_primes": len(certified),
              "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
              "sympy_crosscheck": symbolic,
              "subset_products": len(masks), "subset_sha256": digest_integers(masks),
              "congruent_31_mod_84": len(eligible), "eligible_sha256": digest_integers(eligible),
              "minimum_eligible_S": str(min(eligible)),
              "minimum_eligible_u": str((min(eligible) - 31) // 84),
              "fermat_survivors": survivor_records, "composite_control": control,
              "negative_self_checks": self_checks(payload, resultant)}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
