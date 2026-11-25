#!/usr/bin/env python3
"""Fresh review: norm determinant, ascending Lucas proofs, combination enumeration.

This file imports neither checker.py nor any symbolic mathematics package.
All checks remain active with python -O. Only review_results.json is its receipt.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import comb, gcd, prod
from pathlib import Path


HERE = Path(__file__).resolve().parent


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def norm_matrix(c, a, b, h):
    """Multiply by Q in Q[X]/(X^7-10^(c+4)), columns indexed by X^j."""
    constant = 10 ** (c + 4)
    q = [10 ** max(-h, 0) * comb(b, k) * 7**k * (-25)**(b-k)
         for k in range(b + 1)]
    q[a] -= 18**b * 10 ** max(h, 0)
    matrix = [[0] * 7 for _ in range(7)]
    for column in range(7):
        for k, coefficient in enumerate(q):
            quotient, remainder = divmod(k + column, 7)
            matrix[remainder][column] += coefficient * constant**quotient
    return matrix


def rational_determinant(matrix):
    """Ordinary Gaussian elimination over Fraction, not Bareiss elimination."""
    rows = [[Fraction(entry) for entry in row] for row in matrix]
    determinant = Fraction(1)
    for column in range(len(rows)):
        pivot = next((r for r in range(column, len(rows)) if rows[r][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            determinant = -determinant
        scale = rows[column][column]
        determinant *= scale
        rows[column] = [entry / scale for entry in rows[column]]
        for r in range(column + 1, len(rows)):
            scale = rows[r][column]
            rows[r] = [x - scale*y for x, y in zip(rows[r], rows[column])]
    return determinant


def certify(payload):
    """Process increasing n: n-1 factor primes must already be proved."""
    records = sorted(payload["certificates"], key=lambda r: int(r["n"]))
    proved = set()
    for record in records:
        n = int(record["n"])
        check(n not in proved, "duplicate certificate")
        if n == 2:
            check(record["base"] is None and record["factors"] == [], "invalid 2")
        else:
            factors = [(int(p), e) for p, e in record["factors"]]
            check(all(p in proved and isinstance(e, int) and e > 0 for p, e in factors),
                  "n-1 has an unproved prime")
            check(len(factors) == len({p for p, e in factors}), "repeated factor entry")
            check(prod(p**e for p, e in factors) == n-1, "n-1 factorization")
            base = int(record["base"])
            check(1 < base < n and pow(base, n-1, n) == 1, "Lucas power")
            for p, _ in factors:
                check(gcd(pow(base, (n-1)//p, n)-1, n) == 1, "Lucas coprimality")
        proved.add(n)
    check(set(map(int, payload["roots"])) <= proved, "unproved root")
    return proved


def decimal_power(base, exponent, modulus):
    """Exponentiation by decimal Horner evaluation, independent of binary loops."""
    answer = 1
    small = [1]
    for _ in range(9):
        small.append(small[-1] * base % modulus)
    for digit in str(exponent):
        old = answer
        answer = 1
        for _ in range(10):
            answer = answer * old % modulus
        answer = answer * small[int(digit)] % modulus
    return answer


def digest(values):
    return sha256("".join(str(value) + "\n" for value in values).encode()).hexdigest()


def main():
    receipt = json.loads((HERE / "results.json").read_text())
    payload = json.loads((HERE / "primality_certificates.json").read_text())
    proved = certify(payload)
    check(len(proved) == receipt["certified_primes"] == 66, "prime certificate count")
    matrix = norm_matrix(1, 5, 12, -1)
    norm = rational_determinant(matrix)
    check(norm.denominator == 1 and norm != 0, "integral nonzero norm")
    check(norm.numerator == int(receipt["resultant"]), "norm/resultant mismatch")
    check(rational_determinant([[0, 1], [1, 0]]) == -1, "swap control")
    check(rational_determinant([[1, 2], [2, 4]]) == 0, "singular control")
    factorization = {int(p): e for p, e in receipt["factorization"].items()}
    check(set(factorization) == set(map(int, payload["roots"])), "root factors mismatch")
    check(all(p in proved for p in factorization), "unproved resultant factor")
    check(prod(p**e for p, e in factorization.items()) == abs(norm), "factor product")
    for p, expected in factorization.items():
        reduced, observed = abs(norm.numerator), 0
        while reduced % p == 0:
            reduced //= p
            observed += 1
        check(observed == expected, "factor multiplicity")
    allowed = sorted(p for p in factorization if gcd(p, 210) == 1)
    check(len(allowed) == 15 and all(factorization[p] == 1 for p in allowed),
          "eligible prime support")
    products = sorted(prod(subset) for size in range(16)
                      for subset in combinations(allowed, size))
    check(len(products) == len(set(products)) == 32768, "combination cardinality")
    eligible = [value for value in products if value % 84 == 31]
    check(len(eligible) == 1360 and min(eligible) == 17251, "line congruence set")
    check(digest(products) == receipt["subset_sha256"], "subset digest")
    check(digest(eligible) == receipt["eligible_sha256"], "eligible digest")
    survivors = [value for value in eligible if decimal_power(10, value-1, value) == 1]
    check(survivors == [int(r["S"]) for r in receipt["fermat_survivors"]]
          == [555700252411], "Fermat list")
    line_records = []
    for s in survivors + [451]:
        u = (s-31)//84
        length, position = 12*u+5, 5*u+2
        check(u >= 1 and 3 <= position < length, "actual position")
        check(7*length-4 == s and 12*position-5*length == -1, "line equality")
        check(decimal_power(10, s-1, s) == 1, "positive Fermat control")
        residues = {}
        for modulus in [s, 9*s]:
            x = decimal_power(10, length, modulus)
            y = decimal_power(10, position, modulus)
            residues[str(modulus)] = {"ten_to_L": str(x), "ten_to_i": str(y),
                                     "F": str((7*x-18*y-25) % modulus)}
        expected = (receipt["fermat_survivors"][0] if s != 451
                    else receipt["composite_control"])
        check(residues == expected["residues"], "reported residues mismatch")
        check(int(residues[str(9*s)]["F"]) != 0, "full-sum condition passes")
        line_records.append({"S": str(s), "L": str(length), "i": str(position),
                             "residues": residues})
    # Exact controls exercise the nonvanishing proof's notable cases.
    # c=3 gives P=X^7-10^7, which has rational root 10.
    # All three are compatible with L=13, i=3, p=29 and S=87.
    endpoint_controls = [(3, 0, 1, 3), (3, 1, 1, -10), (3, 3, 13, 0)]
    endpoint_results = []
    for parameters in endpoint_controls:
        value = rational_determinant(norm_matrix(*parameters))
        check(value.denominator == 1 and value != 0, "endpoint nonvanishing")
        endpoint_results.append({"c_a_b_h": list(parameters), "norm": str(value.numerator)})
    output = {"status": "PASS", "method": "7x7 quotient norm; Fraction Gaussian elimination",
              "imports_checker": False, "resultant": str(norm.numerator),
              "certified_primes": len(proved), "subset_products": len(products),
              "congruent_31_mod_84": len(eligible), "subset_sha256": digest(products),
              "eligible_sha256": digest(eligible), "fermat_survivors": list(map(str, survivors)),
              "line_records": line_records, "endpoint_controls": endpoint_results,
              "input_sha256": {name: sha256((HERE/name).read_bytes()).hexdigest()
                               for name in ["primality_certificates.json", "results.json"]},
              "review_check_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
