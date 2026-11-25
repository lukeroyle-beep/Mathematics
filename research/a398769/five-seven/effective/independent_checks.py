#!/usr/bin/env python3
"""Independent finite controls for the effective central-strip proof.

This is not an exhaustive search beyond the inherited certified interval.
No primary checker or proof-helper implementation is imported.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def valuation(value, prime):
    require(value != 0, "valuation requires nonzero input")
    count = 0
    while value % prime == 0:
        value //= prime
        count += 1
    return count


def log_interval(integer, terms=100):
    """atanh series and a positive geometric tail, using exact rationals."""
    z = Fraction(integer - 1, integer + 1)
    low = 2 * sum((z ** (2 * j + 1)) / (2 * j + 1)
                  for j in range(terms))
    tail = 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
    return low, low + tail


def main():
    l7, u7 = log_interval(7)
    l10, u10 = log_interval(10)
    require(168 * 16 * u10 ** 2 / l7 ** 4 < 1008, "BL coefficient")
    require(5 * u7 < 10, "BL fixed maximum term")
    require(6 * u10 < 14, "cutoff log upper bound")
    require(6 * l10 > 8, "cutoff active maximum branch")
    require(2 * 10**6 - 1 > 1008 * 16**2, "cutoff value")
    require(2 > Fraction(2016 * 16, 10**6), "cutoff derivative")

    # The d=1 ray checks a simple representative of the strip.
    polynomial = lambda x: 70 * x * x - 18 * x - 25
    require(polynomial(-1) > 0 > polynomial(0), "negative real root")
    require(polynomial(1) > 0 > polynomial(0), "positive real root")
    require(85**2 < 7324 < 86**2, "irreducible discriminant")
    require(70 < 10**2, "root height below log10")

    # Enumerate every possible lift, independently of a Newton implementation.
    roots = []
    root, modulus = 0, 1
    for k in range(1, 13):
        next_modulus = 7 * modulus
        lifts = [root + a * modulus for a in range(7)
                 if polynomial(root + a * modulus) % next_modulus == 0]
        require(len(lifts) == 1, "unique Hensel lift")
        root = lifts[0]
        modulus = next_modulus
        require(root % 7 == 6, "unit root residue")
        roots.append((k, modulus, root))

    histogram = Counter()
    comparisons = 0
    for i in range(3, 1001):
        length = 2 * i + 1
        # Construct the actual word from its stated digits, units position zero.
        digits = [5 if j in (0, i) else 7 for j in range(length)]
        number = 0
        for digit in reversed(digits):
            number = 10 * number + digit
        expression = 9 * number
        require(expression == 7 * 10**length - 18 * 10**i - 25,
                "digit construction versus F")
        require(expression == polynomial(10**i), "quadratic identity")
        require(sum(digits) == 7 * length - 4, "digit sum")
        require(digits.count(5) == 2, "digit product exponents")
        t = valuation(expression, 7)
        histogram[t] += 1
        for k, modulus, root in roots:
            difference = (pow(10, i, modulus) - root) % modulus
            root_distance = k if difference == 0 else valuation(difference, 7)
            require(min(t, k) == root_distance, "root valuation identity")
            comparisons += 1
    require(histogram[0] > 0 and histogram[1] > 0 and histogram[2] > 0,
            "nonvacuous positive and negative valuation controls")

    # Independent nonsquareness certificates: enumerate square residues modulo
    # small primes, rather than using the primary checker's integer square root.
    primes = [p for p in range(3, 50, 2)
              if all(p % a for a in range(2, p))]
    nonresidues = []
    strip_comparisons = 0
    strip_pairs = 0
    strip_histogram = Counter()
    for d in range(-47, 48, 2):
        magnitude = abs(d)
        if d > 0:
            a, b, c = 7 * 10**d, -18, -25
        else:
            a, b, c = 7, -18 * 10**magnitude, -25 * 10**magnitude
        discriminant = b*b - 4*a*c
        witnesses = [p for p in primes
                     if discriminant % p not in {r*r % p for r in range(p)}]
        require(witnesses, "quadratic nonresidue certificate")
        prime = witnesses[0]
        nonresidues.append([d, prime, discriminant % prime])
        q = lambda x: a*x*x + b*x + c
        if d > 0:
            require(q(-1) > 0 and q(0) < 0 and q(1) > 0,
                    "positive offset root locations")
            require(a < 10**(magnitude + 2), "positive offset height")
        else:
            require(q(-1) < 0 and q(1) < 0,
                    "negative offset root locations")
            require(-c < 10**(magnitude + 2), "negative offset height")
        root, modulus, strip_roots = 0, 1, []
        for k in range(1, 9):
            next_modulus = 7 * modulus
            lifts = [root + t * modulus for t in range(7)
                     if q(root + t * modulus) % next_modulus == 0]
            require(len(lifts) == 1, "strip unique lift")
            root, modulus = lifts[0], next_modulus
            require(root % 7 == 6, "strip unit root")
            strip_roots.append((k, modulus, root))
        for i in range(max(3, 2-d), 251):
            length = 2*i+d
            number = 0
            for j in reversed(range(length)):
                number = 10*number + (5 if j in (0, i) else 7)
            expression = 9*number
            require(expression == 7*10**length-18*10**i-25, "strip digits")
            require(q(10**i) == expression * (1 if d>0 else 10**magnitude),
                    "strip scaled quadratic identity")
            t = valuation(expression, 7)
            strip_histogram[t] += 1
            strip_pairs += 1
            for k, modulus, root in strip_roots:
                distance = (pow(10, i, modulus)-root) % modulus
                v = k if distance == 0 else valuation(distance, 7)
                require(min(t, k) == v, "strip root valuation identity")
                strip_comparisons += 1
    require(504*49 < 63*396, "strip coefficient within inherited edge bound")

    # Required inherited control, independently recomputed from decimal digits.
    control = int("".join("5" if j in (0, 15) else "7"
                          for j in reversed(range(23))))
    require((9 * control) % 49 == 0, "23,15 modulo49")
    require((9 * control) % 343 == 245, "23,15 modulo343")

    print(json.dumps({
        "status": "PASS",
        "scope": "finite proof controls, no new exhaustive interval",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "ray_positions": {"inclusive_first": 3, "inclusive_last": 1000,
                          "count": 998},
        "hensel_powers": {"inclusive_first": 1, "inclusive_last": 12},
        "root_distance_comparisons": comparisons,
        "valuation_histogram": dict(sorted(histogram.items())),
        "strip_offsets": {"inclusive_first": -47, "inclusive_last": 47,
                          "step": 2, "count": 48},
        "strip_positions": "max(3,2-d)..250 inclusive for each offset d",
        "strip_digit_pairs": strip_pairs,
        "strip_root_distance_comparisons": strip_comparisons,
        "strip_hensel_powers": {"inclusive_first": 1, "inclusive_last": 8},
        "strip_valuation_histogram": dict(sorted(strip_histogram.items())),
        "nonsquare_certificates_d_prime_residue": nonresidues,
        "exact_log_terms": 100,
        "cutoff_value_margin_lower_bound": 2 * 10**6 - 1 - 1008 * 16**2,
        "regression_23_15_F_mod_49_343": [0, 245],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
