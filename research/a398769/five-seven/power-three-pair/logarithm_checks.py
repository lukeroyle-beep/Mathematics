#!/usr/bin/env python3
"""Independent finite checks for LOGARITHMS.md; no shared arithmetic imports."""
import argparse
from fractions import Fraction
import hashlib
import json
from math import factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent
KS = tuple(range(42, 435, 49))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def valuation(n, prime=7):
    require(n != 0, "valuation must be finite")
    result = 0
    while n % prime == 0:
        n //= prime
        result += 1
    return result


def polynomial(k, x, modulus, derivative=False):
    # Expanded coefficients, evaluated independently term by term.
    terms = ((6561, 7, 4687), (14*k+9, -7, 10*k+7),
             (14*k, 25, 10*k), (0, -25, 0))
    value = 0
    for degree, factor, exponent in terms:
        if derivative:
            if degree == 0:
                continue
            factor *= degree
            degree -= 1
        value += factor * pow(10, exponent, modulus) * pow(x, degree, modulus)
    return value % modulus


def compute():
    require(pow(3, 29, 42) == 33 and pow(3, 6, 42) == 15,
            "initial residue arithmetic")
    require(33*pow(3, 6, 42) % 42 == 33, "w residue induction")
    require((33-5)//7 == 4, "w residue class")
    require(valuation(10**6-1) == 1, "exact initial order lift")
    require(next(j for j in range(1, 295) if pow(10, j, 343) == 1) == 294,
            "full order modulo343")

    derivative_rows = []
    norm_rows = []
    hensel_rows = []
    for k in KS:
        derivative_values = [polynomial(k, pow(10, w, 343), 343, True)
                             for w in range(4, 294, 6)]
        require(len(derivative_values) == 49 and set(derivative_values) == {49},
                "complete derivative classes")
        derivative_rows.append({"k": k, "w_classes": list(range(4, 294, 6)),
                                "derivative_mod343": derivative_values})
        norm = 7*10**4687+7*10**(10*k+7)+25*10**(10*k)+25
        require(norm < 10**4688, "coefficient norm")
        require(14*k+9 < 6561 and 0 < 14*k < 14*k+9, "degree and distinctness")
        norm_rows.append({"k": k, "degree": 6561, "norm_below_10_power": 4688,
                          "norm_sha256": hashlib.sha256(norm.to_bytes(
                              (norm.bit_length()+7)//8, "big")).hexdigest()})

        # Discover a nonzero strong-Hensel control rather than seed a result.
        precision = 12
        modulus = 7**precision
        found = None
        for w in range(4, 6*2401, 6):
            x = pow(10, w, modulus)
            value = polynomial(k, x, modulus)
            if value and 5 <= valuation(value) < 10:
                found = (w, x, valuation(value))
                break
        require(found is not None, "positive strong-Hensel control")
        w, x, t = found
        alpha = x % 7**3
        require(polynomial(k, alpha, 7**5) == 0, "initial precision")
        for exponent in range(3, 11):
            lifts = [alpha+j*7**exponent for j in range(7)
                     if polynomial(k, alpha+j*7**exponent, 7**(exponent+3)) == 0]
            require(len(lifts) == 1, "unique digit with derivative loss two")
            alpha = lifts[0]
        require(polynomial(k, alpha, 7**13) == 0, "final root precision")
        q = valuation((alpha-x) % 7**11)
        require(q == t-2 and q >= 3, "exact Hensel valuation loss")
        require(polynomial(k, alpha, 343, True) == 49, "root derivative")
        sixth_difference = (pow(x, 6, 7**11)-pow(alpha, 6, 7**11)) % 7**11
        require(valuation(sixth_difference) == q, "sixth powers preserve distance")
        hensel_rows.append({"k": k, "w": w, "t": t, "q": q,
                            "alpha_mod7_power11": alpha,
                            "polynomial_zero_mod7_power": 13})

    exp_7_over_3_lower = sum((Fraction(7, 3)**j/Fraction(factorial(j)))
                           for j in range(11))
    exp_2_lower = sum(Fraction(2**j, factorial(j)) for j in range(6))
    # e=sum1/j! < 1+1+sum_{j>=2}1/2^(j-1)=3, strictly.
    require(exp_7_over_3_lower > 10, "log10<7/3")
    require(exp_2_lower > 7, "log7<2")
    require(6*4688*Fraction(7, 3) == 65632 < 70000, "root sixth-power height")
    require(6*Fraction(7, 3) == 14 < 15, "ten sixth-power height")
    constant = 832*6561**4*15*70000
    require(constant == 1618798436980968297600000, "explicit constant")
    require(constant+2 < 10**30, "loose bound")
    require(6561*4688 < 10**8, "dependence integer magnitude")

    left = 3**100
    right = 7*10**30*120**2+10
    require(left > right, "crossover initial exact inequality")
    # Symbolic coefficient arrays for 3(a+20)^2-(a+21)^2.
    quadratic = [3*400-441, 3*40-42, 3-1]
    require(quadratic == [759, 78, 2] and all(v > 0 for v in quadratic),
            "crossover induction polynomial")
    require(10**30*400 > 27 and 40*10**30 > 2,
            "dependent bound for all a>=0 by positive coefficients")

    return {
        "schema": "a398769-pair-logarithms-v1",
        "source_pdf": {
            "url": "https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf",
            "bytes": 271382,
            "sha256": "554bb384df62538fa11fcf6ab74976e772156c9d3ca4022e2128d48e3632128d",
            "formula": "Corollary2 printed page5; definitions printed pages2-4",
            "download_audit_date": "2026-11-27",
        },
        "bindings": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                     for name in ("LOGARITHMS.md", "logarithm_checks.py")},
        "derivative_rows": derivative_rows,
        "derivative_cases": 9*49,
        "norm_rows": norm_rows,
        "strong_hensel_controls": hensel_rows,
        "exponential_lower_bounds": {
            "exp_7_over3": str(exp_7_over_3_lower), "exp2": str(exp_2_lower)},
        "height_ceiling_alpha6": 65632,
        "independent_constant": constant,
        "crossover": {"a": 100, "left": str(left), "right": str(right),
                      "positive_gap": str(left-right),
                      "induction_coefficients_ascending": quadratic},
        "finite_starts_below_cutoff": list(range(31, 100, 6)),
        "assertions_removable": False,
        "lean_verification": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--source-pdf", type=Path,
                        help="Also recheck exact downloaded primary PDF bytes")
    args = parser.parse_args()
    result = compute()
    if args.source_pdf:
        data = args.source_pdf.read_bytes()
        require(len(data) == result["source_pdf"]["bytes"], "primary PDF byte count")
        require(hashlib.sha256(data).hexdigest() == result["source_pdf"]["sha256"],
                "primary PDF hash")
    encoded = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.check:
        require(args.check.read_text() == encoded, "source-bound receipt mismatch")
    print(encoded, end="")


if __name__ == "__main__":
    main()
