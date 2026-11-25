#!/usr/bin/env python3
"""Exact arithmetic supporting PROOF.md; no floating point or assert checks."""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def valuation7(value):
    value = Q(value)
    require(value != 0, "the valuation of zero is not finite")
    numerator, denominator = abs(value.numerator), value.denominator
    result = 0
    while numerator % 7 == 0:
        numerator //= 7
        result += 1
    while denominator % 7 == 0:
        denominator //= 7
        result -= 1
    return result


def log_small(x, terms=32):
    """Rational enclosure from 2 atanh((x-1)/(x+1)), 1 <= x <= 2."""
    x = Q(x)
    require(1 <= x <= 2, "log_small domain")
    z = (x - 1) / (x + 1)
    lower = 2 * sum((z ** (2*k+1) / (2*k+1)
                     for k in range(terms)), Q(0))
    tail = 2*z**(2*terms+1) / ((2*terms+1)*(1-z*z))
    return lower, lower + tail


def log_bounds(x):
    x = Q(x)
    require(x >= 1, "log_bounds domain")
    twos = 0
    while x > 2:
        x /= 2
        twos += 1
    lo, hi = log_small(x)
    lo2, hi2 = log_small(Q(2))
    return lo + twos*lo2, hi + twos*hi2


def outward_decimal_interval(lo, hi, places=12):
    scale = 10**places
    a = lo.numerator * scale // lo.denominator
    b = -((-hi.numerator * scale) // hi.denominator)
    return [f"{a // scale}.{a % scale:0{places}d}",
            f"{b // scale}.{b % scale:0{places}d}"]


def cleared_polynomial(r, s, x):
    m = min(0, s)
    return (7*10**(r-m)*x**12 - 18*10**(s-m)*x**5
            - 25*10**(-m))


def polynomial_mod(r, s, x, modulus):
    m = min(0, s)
    return (7*pow(10, r-m, modulus)*pow(x, 12, modulus)
            - 18*pow(10, s-m, modulus)*pow(x, 5, modulus)
            - 25*pow(10, -m, modulus)) % modulus


def main():
    n = 10**9
    lo7, hi7 = log_bounds(Q(7))
    lo10, hi10 = log_bounds(Q(10))
    prefactor_upper = 168*hi10**2/lo7**4
    require(prefactor_upper < 63, "Bugeaud--Laurent prefactor")
    q_over_h = Q(n, 168)
    bprime_upper = (q_over_h + 1) / lo10
    log_bprime_upper = log_bounds(bprime_upper)[1]
    log_log7_upper = log_bounds(hi7)[1]
    first_entry_upper = log_bprime_upper + log_log7_upper + Q(2, 5)
    require(first_entry_upper < 16, "first entry of logarithmic maximum")
    require(10*hi7 < 20, "second entry of logarithmic maximum")
    require(max(first_entry_upper, 10*hi7, Q(10)) < 20,
            "all entries below the chosen T=20")
    slope = Q(63*12**3*14*20**2, n)
    require(slope == Q("0.6096384"), "displayed coefficient")
    require(slope < 1, "strictly sublinear bound")
    margin = (1-slope)*n-2
    require(margin == 390361598 and margin > 0, "threshold margin")
    height_margin = Q(14)-Q(1, 12)-13
    require(height_margin == Q(11, 12) and height_margin > 0,
            "height enlargement at threshold")
    require(Q(14, n) < 1, "H<L")
    require(2*5 < 7**(5-3), "dependent size induction base")
    require(4 < 14, "2(L+1)<=4L<14L for L>=1")

    identities = positive_depth = root_lifts = 0
    signs = {"negative": 0, "zero": 0, "positive": 0}
    positive_depth_signs = {key: 0 for key in signs}
    for length in range(5, 242, 2):
        q, r = divmod(length, 12)
        for position in range(3, length):
            s = position-5*q
            delta = 12*position-5*length
            require(delta == 12*s-5*r and delta % 2 == 1,
                    "offset identity and odd parity")
            m = min(0, s)
            w = max(0, r, s)-m
            require(w+2 <= Q(abs(delta), 12)+13, "coefficient span")
            f = 7*10**length - 18*10**position - 25
            x = 10**q
            require(f > 0, "positivity")
            require(cleared_polynomial(r, s, x) == 10**(-m)*f,
                    "cleared polynomial identity")
            require(abs(delta) > Q(length, n), "empty small strip")
            identities += 1
            sign = "negative" if s < 0 else "positive" if s > 0 else "zero"
            signs[sign] += 1
            if f % 7:
                continue
            positive_depth += 1
            positive_depth_signs[sign] += 1
            derivative = (-90*pow(10, s-m, 7)*pow(x, 4, 7)) % 7
            require(derivative != 0, "simple root")
            alpha = x % 7
            modulus = 7
            require(polynomial_mod(r, s, alpha, modulus) == 0,
                    "initial root")
            for depth in range(2, 7):
                candidates = [alpha + digit*modulus for digit in range(7)]
                new_modulus = modulus*7
                roots = [a for a in candidates
                         if polynomial_mod(r, s, a, new_modulus) == 0]
                require(len(roots) == 1, "unique Hensel lift")
                alpha = roots[0]
                require((f % new_modulus == 0) ==
                        (x % new_modulus == alpha), "root-distance identity")
                modulus = new_modulus
                root_lifts += 1
    require(all(value > 0 for value in positive_depth_signs.values()),
            "positive-depth controls include all signs of s")

    lte_checks = 0
    for d in range(1, 13):
        for a in (1, 7, 49):
            y = 1+7*a
            require(valuation7(y**(6*d)-1) ==
                    valuation7(y-1)+valuation7(d), "principal-unit LTE")
            lte_checks += 1
    for exponent in (-49, -7, -1, 1, 7, 49):
        require(valuation7(Q(10)**(6*exponent)-1) ==
                1+valuation7(exponent), "signed exponent LTE")
        lte_checks += 1
    require(valuation7(10**6-1) == 1, "base-ten LTE constant")
    require(valuation7(7*10**23-18*10**15-25) == 2,
            "nonzero positive-depth control")
    require((7*pow(10, 23, 343)-18*pow(10, 15, 343)-25) % 343 == 245,
            "nonzero residue control")

    rejected = 0
    for operation in (lambda: require(False, "explicit failure control"),
                      lambda: valuation7(0),
                      lambda: log_bounds(Q(1, 2)),
                      lambda: require(slope == Q("0.6096385"),
                                      "altered coefficient")):
        try:
            operation()
        except ValueError:
            rejected += 1
        else:
            raise ValueError("negative control was not rejected")
    print(json.dumps({
        "verdict": "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "arithmetic": "exact integers and fractions; no floating point",
        "log7_interval": outward_decimal_interval(lo7, hi7),
        "log10_interval": outward_decimal_interval(lo10, hi10),
        "prefactor_upper_below": 63,
        "first_maximum_entry_upper_below": 16,
        "first_maximum_entry_upper_rounded_outward":
            outward_decimal_interval(first_entry_upper, first_entry_upper)[1],
        "ten_log7_upper_below": 20,
        "T": 20,
        "q_over_H_upper": str(q_over_h),
        "height_margin_at_threshold": str(height_margin),
        "slope": str(slope),
        "slope_exact_decimal": "0.6096384",
        "strict_margin_at_threshold": str(margin),
        "control_length_range": [5, 241],
        "control_lengths": "odd, all positions 3<=i<L",
        "polynomial_identities": identities,
        "s_signs": signs,
        "positive_depth_cases": positive_depth,
        "positive_depth_s_signs": positive_depth_signs,
        "hensel_comparisons_through_depth_6": root_lifts,
        "lte_checks_including_D7_and_negative_exponents": lte_checks,
        "nonzero_control": {"L": 23, "i": 15, "v7_F": 2, "F_mod343": 245},
        "negative_controls_rejected": rejected,
        "scope": "arithmetic and bounded controls, not an all-length computation"
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
