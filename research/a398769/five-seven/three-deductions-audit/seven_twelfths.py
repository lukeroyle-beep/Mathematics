#!/usr/bin/env python3
"""Exact arithmetic and bounded controls for the seven-twelfths proof.

No imported audit code, floating point, or assert-based acceptance checks.
The rational log enclosure reproduces the inherited series independently.
"""
from fractions import Fraction as Rat
from hashlib import sha256
from math import comb
from pathlib import Path
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def v7(value):
    value = Rat(value)
    need(value != 0, "finite valuation requires a nonzero argument")
    numerator, denominator = abs(value.numerator), value.denominator
    result = 0
    while numerator % 7 == 0:
        numerator //= 7
        result += 1
    while denominator % 7 == 0:
        denominator //= 7
        result -= 1
    return result


def log_interval(value):
    """Enclose log(value) using rational 2*atanh and a positive tail."""
    value = Rat(value)
    need(value >= 1, "log interval domain")

    def small(x):
        z = (x-1)/(x+1)
        partial = 2*sum((z**(2*j+1)/(2*j+1) for j in range(36)), Rat(0))
        tail = 2*z**73/(73*(1-z*z))
        return partial, partial+tail

    twos = 0
    while value > 2:
        value /= 2
        twos += 1
    low, high = small(value)
    low2, high2 = small(Rat(2))
    return low+twos*low2, high+twos*high2


def outward(low, high, places=12):
    scale = 10**places
    low_int = low.numerator*scale//low.denominator
    high_int = -((-high.numerator*scale)//high.denominator)
    return [f"{low_int//scale}.{low_int%scale:0{places}d}",
            f"{high_int//scale}.{high_int%scale:0{places}d}"]


def coefficients(r, s):
    m = min(0, s)
    result = [0]*13
    result[0] = -25*10**(-m)
    result[7] = -18*10**(s-m)
    result[12] = 7*10**(r-m)
    return result


def evaluate(coeffs, x):
    value = 0
    for coefficient in reversed(coeffs):
        value = value*x+coefficient
    return value


def derivative(coeffs, x):
    return evaluate([j*coeffs[j] for j in range(1, len(coeffs))], x)


def local_root_control(coeffs, x, t):
    """Transform Q(x+49Y)/343 to a simple-root polynomial; lift all digits.

    This does not falsely assert that Q has a unique root modulo 7^k.
    The unique p-adic root in x+49Z_7 is represented by the unique root of R.
    """
    need(t >= 3 and v7(derivative(coeffs, x)) == 1,
         "strong Hensel hypotheses")
    shifted = []
    for j in range(len(coeffs)):
        numerator = 49**j*sum(coeffs[k]*comb(k, j)*x**(k-j)
                              for k in range(j, len(coeffs)))
        need(numerator % 343 == 0, "transformed coefficients integral")
        shifted.append(numerator//343)
    need(shifted[1] % 7 != 0, "transformed derivative is a unit")
    roots = [y for y in range(7) if evaluate(shifted, y) % 7 == 0]
    need(len(roots) == 1, "all initial transformed roots")
    modulus = 7
    count = 0
    for depth in range(1, 7):
        if depth > 1:
            roots = [y+d*modulus for y in roots for d in range(7)
                     if evaluate(shifted, y+d*modulus) % (7*modulus) == 0]
            modulus *= 7
        need(len(roots) == 1, "unique transformed lift")
        alpha = x+49*roots[0]
        need(evaluate(coeffs, alpha) % (343*modulus) == 0,
             "lifted Q root congruence")
        need(v7(derivative(coeffs, alpha)) == 1,
             "derivative valuation preserved")
        if depth > t-3:
            need(v7(x-alpha) == t-1, "exact root distance loses one unit")
        count += 1
    return count


def main():
    n = 10**9
    lo7, hi7 = log_interval(7)
    lo10, hi10 = log_interval(10)
    prefactor = 168*hi10**2/lo7**4
    need(prefactor < 63, "logarithmic prefactor")
    bprime = (Rat(n, 168)+1)/lo10
    first = log_interval(bprime)[1]+log_interval(hi7)[1]+Rat(2, 5)
    need(first < 16, "first logarithmic maximum entry")
    need(10*hi7 < 20 and max(first, 10*hi7, Rat(10)) < 20,
         "all three maximum entries")
    slope = Rat(63*12**3*14*20**2, n)
    need(slope == Rat("0.6096384"), "claimed coefficient")
    margin = (1-slope)*n-3
    need(margin == 390361597 and margin > 0, "margin for 1+slope*L")
    need(Rat(14)-Rat(1, 12)-13 == Rat(11, 12), "height enlargement")
    need(14*lo10 > hi7 and lo10 > hi7, "height parameter lower bounds")
    need(Rat(14, n) < 1, "H<L")
    need(2*6 < 7**(6-4), "dependent branch induction base L=6")
    need(4 < 14, "2(L+1)<=4L<7(2L) for L>=1")

    span_checks = 0
    for r in range(12):
        for s in range(-100, 101):
            m = min(0, s)
            w = max(0, r, s)-m
            delta = 12*s-7*r
            need(w+2 <= Rat(abs(delta), 12)+13, "both-sign span")
            need(sum(abs(c) for c in coefficients(r, s)) <= 50*10**w,
                 "coefficient l1 bound")
            span_checks += 1

    identities = positive = strong = root_checks = 0
    signs = {"negative": 0, "zero": 0, "positive": 0}
    depth_signs = dict(signs)
    strong_signs = dict(signs)
    depth_histogram = {}
    positive_controls = []
    for length in range(5, 242, 2):
        q, r = divmod(length, 12)
        x = 10**q
        for position in range(3, length):
            s = position-7*q
            m = min(0, s)
            delta = 12*position-7*length
            sign = "negative" if s < 0 else "positive" if s > 0 else "zero"
            signs[sign] += 1
            coeffs = coefficients(r, s)
            f = 7*10**length-18*10**position-25
            need(f > 0, "nonzero F")
            need(delta == 12*s-7*r and delta % 2 == 1, "odd offset")
            need(abs(delta) > Rat(length, n), "empty small strip")
            need(evaluate(coeffs, x) == 10**(-m)*f, "Q(x) identity")
            deriv = derivative(coeffs, x)
            need(x*deriv == 7*10**(-m)*(f+5*10**length+25),
                 "derivative identity")
            need(deriv % 7 == 0, "simple-root criterion does not apply")
            identities += 1
            t = v7(f)
            depth_histogram[t] = depth_histogram.get(t, 0)+1
            if t:
                positive += 1
                depth_signs[sign] += 1
                need(v7(deriv) == 1, "odd-L derivative valuation exactly one")
            if t >= 3:
                strong += 1
                strong_signs[sign] += 1
                root_checks += local_root_control(coeffs, x, t)
                if (length, position) in ((17, 15), (81, 3), (233, 183)):
                    positive_controls.append({"L": length, "i": position,
                        "s": s, "v7_F": t, "v7_Qprime": v7(deriv),
                        "root_distance": t-1, "F_mod_next_power": f % 7**(t+1)})
    need(all(depth_signs.values()), "positive-depth cases include all s signs")
    need(strong_signs["negative"] > 0 and strong_signs["positive"] > 0,
         "strong Hensel controls include both signs")
    need(len(positive_controls) == 3, "positive controls observed")

    # LTE checks retain the degree-seven subtraction, including signed h.
    lte = 0
    for d in range(1, 13):
        for a in (1, 7, 49):
            y = 1+49*a
            need(v7(y**(6*d)-1) == v7(y-1)+v7(d), "principal unit LTE")
            lte += 1
    for h in (-49, -7, -1, 1, 7, 49):
        need(v7(Rat(10)**(6*h)-1) == 1+v7(h), "signed base-ten LTE")
        lte += 1
    need(v7(10**6-1) == 1, "base-ten valuation")
    for d in (1, 7):
        # Synthetic LTE identity with alpha=10^3 and q-3=6*49.
        # d=7 tests the subtraction algebra; it is not alpha's field degree.
        q, j = 3+6*49, 3*d
        t = 1+v7(10**q-10**3)
        need(t == 2+v7(d*q-j)-v7(d), "dependent identity with loss and D7")
        lte += 1

    rejected = 0
    for operation in (
        lambda: need(False, "explicit negative guard"),
        lambda: v7(0),
        lambda: log_interval(Rat(1, 2)),
        lambda: need(margin == 390361598, "omitted Hensel loss"),
        lambda: need(v7(derivative(coefficients(8, 3), 1)) == 1,
                     "dropping odd-L hypothesis at L=8,i=3"),
    ):
        try:
            operation()
        except ValueError:
            rejected += 1
        else:
            raise ValueError("negative control unexpectedly passed")

    print(json.dumps({
        "verdict": "PASS", "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "arithmetic": "exact integers and rational enclosures",
        "log7_interval": outward(lo7, hi7), "log10_interval": outward(lo10, hi10),
        "prefactor_strict_upper": 63, "first_maximum_entry_upper": outward(first, first)[1],
        "maximum_strict_upper": 20, "height_margin_at_N": "11/12",
        "independent_slope": str(slope), "independent_slope_decimal": "0.6096384",
        "independent_additive_loss": 1, "strict_margin_at_N": int(margin),
        "dependent_valuation_formula": "t=2+v7(D*q-j)-v7(D)",
        "dependent_size_induction_start": 6,
        "span_controls": span_checks, "control_odd_L": [5, 241],
        "control_position_domain": "every 3<=i<L", "polynomial_and_derivative_identities": identities,
        "offset_signs": signs, "positive_depth_cases": positive,
        "positive_depth_signs": depth_signs, "depth_histogram": depth_histogram,
        "strong_Hensel_cases": strong, "strong_Hensel_signs": strong_signs,
        "transformed_root_comparisons": root_checks, "positive_controls": positive_controls,
        "LTE_checks": lte, "negative_controls_rejected": rejected,
        "scope": "exact constants and bounded controls supporting the proof, not length exhaustion"
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
