#!/usr/bin/env python3
"""Independent exact arithmetic controls for proportional position bounds.

No project proof/checker module is imported. These finite controls do not
prove the external logarithm theorem or certify new exhaustive lengths.
All checks remain active under Python -O. Python standard library only.
"""

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import gcd, isqrt, prod
from pathlib import Path


N = 10_000_000


def require(condition, description):
    if not condition:
        raise ArithmeticError(description)


def log_enclosure(value, terms=32):
    """Exact atanh series, range reduced to [1,2], with geometric tail."""
    value = Q(value)
    require(value > 0, "positive logarithm argument")
    if value < 1:
        lo, hi = log_enclosure(1 / value, terms)
        return -hi, -lo
    power = 0
    while value > 2:
        value /= 2
        power += 1

    def unit_interval(x):
        z = (x - 1) / (x + 1)
        require(0 <= z <= Q(1, 3), "range reduction")
        lower = 2 * sum((z ** (2*j+1) / (2*j+1)
                         for j in range(terms)), Q(0))
        tail = 2*z ** (2*terms+1) / ((2*terms+1)*(1-z*z))
        return lower, lower + tail

    lo, hi = unit_interval(value)
    lo2, hi2 = unit_interval(Q(2))
    return lo + power*lo2, hi + power*hi2


def constants():
    lo7, hi7 = log_enclosure(7)
    lo10, hi10 = log_enclosure(10)
    require(Q("1.94591014") < lo7 < hi7 < Q("1.94591015"),
            "log7 enclosure")
    require(Q("2.30258509") < lo10 < hi10 < Q("2.30258510"),
            "log10 enclosure")
    require(168*hi10**2/lo7**4 < 63, "BL prefactor below 63")
    require(10*hi7 < Q("19.5"), "degree-one fixed term")
    require(5*hi7 < 10, "degree-at-least-two fixed term")
    # Coarse rational inputs prevent enormous nested-log fractions. Their
    # directions have just been independently certified.
    require(Q("2.3") < lo10 and hi7 < Q("1.946"), "coarse inputs")
    loglog7_hi = log_enclosure(Q("1.946"))[1]
    first_entries = {}
    for name, numerator, ceiling in [
        ("ends", Q(25001), Q(11)),
        ("midpoint", Q("30001.5"), Q("10.6")),
        ("thirds", Q(100002), Q(12)),
        ("fifths", Q(2_000_000, 7)+1, Q(13)),
    ]:
        upper = log_enclosure(numerator/Q("2.3"))[1] + loglog7_hi + Q(2, 5)
        require(upper < ceiling, name + " first maximum entry")
        first_entries[name] = str(ceiling)

    c_edge = 63*Q("19.5")**2
    c_mid = 63*8*Q("10.6")**2
    c_third = 63*27*12**2
    c_fifth = 63*125*13**2
    require(c_mid > 63*20**2 and c_third > 63*20**2
            and c_fifth > 63*20**2, "degree-one fallback dominated")
    affine = {
        "ends": (c_edge/25000, 1+c_edge, Q(1574965, 4)),
        "midpoint": (c_mid/60000, 2*c_mid, Q(11212478, 25)),
        "thirds": (Q(c_third, 300000), 2*c_third, Q(1345310)),
        "fifths": (Q(7*c_fifth, 10_000_000), Q(0), Q(683873)),
    }
    margins = {}
    for name, (slope, intercept, expected) in affine.items():
        margin = N-2-(slope*N+intercept)
        require(0 < slope < 1 and margin == expected > 0,
                name + " strict affine comparison")
        margins[name] = {"slope": str(slope), "margin_at_N": str(margin),
                         "intercept": str(intercept)}
    require(Q(165) < Q(N, 60000) < 167, "midpoint all-length strip")
    require(Q(7*c_fifth, 10_000_000) == Q(74529, 80000), "fifths slope")
    # A fixed H=181 sharpens the all-length midpoint strip to |d|<=179.
    # At N the degree-two b' is bounded by (N+360)/(362*log10).
    strip_m = Q("10.46")
    strip_b_upper = (Q(N+179, 2*181)+Q(1, 2))/Q("2.3")
    require(log_enclosure(strip_b_upper)[1]+loglog7_hi+Q(2, 5) < strip_m,
            "179-strip degree-two logarithm maximum")
    strip_c = 504*181*strip_m**2
    require(strip_c == Q(6238102374, 625) and N-2-strip_c == Q(11896376, 625) > 0,
            "179-strip strict endpoint")
    require(2*strip_c/(strip_m*N) == Q(5963769, 31250000) < 1,
            "179-strip derivative at N")
    require(strip_m > 1, "179-strip derivative decreases beyond N")
    # Since (L+c)/(N+c)<=L/N for c>=0 and L>=N, each first
    # maximum entry increases by at most log(L/N). The rational-root
    # fallback is dominated by the same degree-two envelope.
    rational_b_upper = (Q(N+179, 2*181)+1)/Q("2.3")
    require(log_enclosure(rational_b_upper)[1]+loglog7_hi+Q(2, 5) < 20,
            "179-strip degree-one logarithm maximum")
    require(63*181*20**2 < strip_c and 20 > strip_m,
            "179-strip rational-root fallback dominated")
    # For both fifths, exponent span+2 <= |delta|/5+6, and at N:
    require(Q(N, 10_000_000)+6 == Q(7*N, 10_000_000), "fifths height endpoint")
    # Dependent-root elementary comparison; the quotient of successive
    # powers of seven is 7, while (L+1)/L <= 6/5 on L>=5.
    require(6*5 < 7**(5-3) and Q(6, 5) < 7,
            "dependent-case exponential comparison")
    return {"log_terms": 32, "first_entries_strictly_below": first_entries,
            "affine_comparisons": margins,
            "fixed_midpoint_strip": {"absolute_offset_at_most": 179,
                                     "height_parameter": 181,
                                     "maximum_at_N": str(strip_m),
                                     "valuation_envelope_at_N": str(strip_c),
                                     "strict_margin_at_N": str(N-2-strip_c),
                                     "derivative_upper_bound": str(2*strip_c/(strip_m*N))}}


def complementary_intervals(intervals):
    intervals = sorted(intervals)
    require(intervals[0][0] == 0 and intervals[-1][1] == 1,
            "outer endpoints")
    for index, (left, right) in enumerate(intervals):
        require(left <= right, "interval orientation")
        if index:
            require(intervals[index-1][1] < left, "excluded intervals disjoint")
    return [(intervals[j][1], intervals[j+1][0])
            for j in range(len(intervals)-1)]


def interval_checks():
    original = [
        (Q(0), Q(1, 25000)),
        (Q(1, 3)-Q(1, 900000), Q(1, 3)+Q(1, 900000)),
        (Q(1, 2)-Q(1, 120000), Q(1, 2)+Q(1, 120000)),
        (Q(2, 3)-Q(1, 900000), Q(2, 3)+Q(1, 900000)),
        (1-Q(1, 25000), Q(1)),
    ]
    # Inclusive equality boundaries must be removed, not left as survivors.
    for a, b, eta, pair in [(1, 3, Q(1, 300000), original[1]),
                            (1, 2, Q(1, 60000), original[2]),
                            (2, 3, Q(1, 300000), original[3])]:
        for endpoint in pair:
            require(abs(b*endpoint-a) == eta, "original equality boundary")
    fifths = [(Q(a, 5)-Q(1, 10_000_000), Q(a, 5)+Q(1, 10_000_000))
              for a in (2, 3)]
    for a, pair in zip((2, 3), fifths):
        for endpoint in pair:
            require(abs(5*endpoint-a) == Q(1, 2_000_000),
                    "fifths equality boundary and radius")
    before = complementary_intervals(original)
    after = complementary_intervals(original + fifths)
    require(len(before) == 4 and len(after) == 6, "complement component counts")
    require(any(left < Q(2, 5) < right for left, right in before),
            "2/5 survives original five bounds")
    require(not any(left < Q(2, 5) < right for left, right in after),
            "2/5 removed by new bound")
    # An exact surviving interval, not a graphical estimate.
    gap = (Q(41, 100), Q(49, 100))
    require(any(left < gap[0] < gap[1] < right for left, right in after),
            "positive-width remaining gap")
    return {"original_open_complement": [[str(a), str(b)] for a, b in before],
            "with_fifths_open_complement": [[str(a), str(b)] for a, b in after],
            "specific_surviving_open_interval": [str(x) for x in gap]}


def evaluate(coefficients, x):
    result = 0
    for coefficient in reversed(coefficients):
        result = result*x+coefficient
    return result


def polynomial_forms(length, position):
    """Return independent cleared coefficients, k, clearing power, offsets."""
    d = length-2*position
    e = max(0, -d)
    yield "midpoint", (-25*10**e, -18*10**e, 7*10**(d+e)), position, e, d
    for label, k, middle_degree in [("one_third", position, 1),
                                     ("two_thirds", length-position, 2)]:
        d = length-3*k
        e = max(0, -d)
        coefficients = [-25*10**e, 0, 0, 7*10**(d+e)]
        coefficients[middle_degree] = -18*10**(e if middle_degree == 1 else d+e)
        yield label, tuple(coefficients), k, e, d
    k, r = divmod(length, 5)
    for a in (2, 3):
        s = position-a*k
        e = -min(0, r, s)
        coefficients = [-25*10**e, 0, 0, 0, 0, 7*10**(r+e)]
        coefficients[a] = -18*10**(s+e)
        delta = 5*position-a*length
        span = max(0, r, s)-min(0, r, s)
        require(Q(span) <= Q(abs(delta), 5)+4, "fifth exponent-span bound")
        require(sum(abs(c) for c in coefficients) <= 50*10**span,
                "fifth coefficient sum bound")
        yield str(a)+"_fifths", tuple(coefficients), k, e, delta


def polynomial_checks():
    identities = Counter()
    signs = {name: Counter() for name in
             ("midpoint", "one_third", "two_thirds", "2_fifths", "3_fifths")}
    positive_controls = Counter()
    hensel_comparisons = Counter()
    valuation_counts = Counter()
    decimal_pairs = 0
    for length in range(5, 122, 2):
        for position in range(3, length):
            digits = [5 if j in (0, position) else 7 for j in reversed(range(length))]
            number = 0
            for digit in digits:
                number = 10*number+digit
            f = 7*10**length-18*10**position-25
            p, s = prod(digits), sum(digits)
            require(f == 9*number and p == 25*7**(length-2) and s == 7*length-4,
                    "direct decimal and digit statistics")
            require((number % (p*s) == 0) == (f % (9*p*s) == 0),
                    "exact full divisor equivalence")
            require(number % (p*s) != 0, "unexpected small full witness")
            decimal_pairs += 1
            value, exponent = f, 0
            while value % 7 == 0:
                value //= 7
                exponent += 1
            valuation_counts[exponent] += 1
            for name, coefficients, k, e, offset in polynomial_forms(length, position):
                require(evaluate(coefficients, 10**k) == 10**e*f,
                        name + " cleared polynomial identity")
                identities[name] += 1
                signs[name]["negative" if offset < 0 else "positive" if offset > 0 else "zero"] += 1
                if f % 7:
                    continue
                positive_controls[name] += 1
                root = pow(10, k, 7)
                derivative = tuple(j*coefficients[j] for j in range(1, len(coefficients)))
                require(root != 0 and evaluate(coefficients, root) % 7 == 0,
                        name + " unit root")
                require(evaluate(derivative, root) % 7 != 0, name + " simple root")
                modulus = 7
                for power in range(1, 7):
                    if power > 1:
                        lifts = [root+j*modulus for j in range(7)
                                 if evaluate(coefficients, root+j*modulus) % (7*modulus) == 0]
                        require(len(lifts) == 1, name + " unique Hensel lift")
                        root, modulus = lifts[0], 7*modulus
                    require((pow(10, k, modulus)-root) % modulus == 0
                            if exponent >= power else (pow(10, k, modulus)-root) % modulus != 0,
                            name + " root-distance valuation identity")
                    hensel_comparisons[name] += 1
    require(decimal_pairs == 3540 and all(n == 3540 for n in identities.values()),
            "all positions and exact counts")
    require(all(v["negative"] > 0 and v["positive"] > 0 for v in signs.values()),
            "both offset signs exercised")
    require(valuation_counts[0] > 0 and valuation_counts[1] > 0
            and valuation_counts[2] > 0, "positive and negative modular controls")
    require(all(n == 610 for n in positive_controls.values()), "positive control counts")
    # Check nonsquareness on the enlarged midpoint strip independently of the
    # symbolic proof; this finite list has no claim to length coverage.
    for d in range(-179, 180, 2):
        e = max(0, -d)
        discriminant = (18*10**e)**2 + 700*10**(d+2*e)
        root = isqrt(discriminant)
        require(root*root < discriminant < (root+1)**2, "midpoint nonsquare")
    regression = 7*10**23-18*10**15-25
    require(regression % 49 == 0 and regression % 343 == 245, "23,15 regression")
    # Sum-only is a genuine positive control; it is not a full witness.
    f = 7*10**7-18*10**3-25
    require(f % (9*(7*7-4)) == 0 and f % (225*7**5*(7*7-4)) != 0,
            "sum-only positive control rejected by full divisor")
    f = 7*10**313-18*10**51-25
    require(f % (7*313-4) == 0 and f % (9*(7*313-4)) == 17496,
            "S divides F is weaker than S divides n")
    return {"lengths": "odd 5 through 121 inclusive", "positions": "every 3 <= i < L",
            "decimal_pairs": decimal_pairs, "polynomial_identities": dict(identities),
            "offset_signs": {k: dict(v) for k, v in signs.items()},
            "positive_mod7_controls": dict(positive_controls),
            "root_distance_comparisons_powers_1_through_6": dict(hensel_comparisons),
            "valuation_histogram": dict(sorted(valuation_counts.items())),
            "nonsquare_midpoint_discriminants": 180,
            "regression_23_15_mod49_mod343": [0, 245],
            "sum_only_control": [7, 3], "factor9_negative_control": [313, 51]}


def gap_family_checks():
    """Finite controls for the irrational-centre obstruction proof.

    These do not claim full digit-sum or growing-power survivors. The
    universally quantified gap follows from the documented rational-distance
    and height inequalities, not from this finite sample of denominators.
    """
    period = 6*5*11*13*37*101
    require(period == 16_031_730 > N, "gap family period")
    rows = []
    compared = 0
    for j in (1, 2, 3, 10, 100, 10000):
        length = 1+period*j
        floor_x = isqrt(2*length*length)-length
        position = 39+42*((floor_x-18)//42)
        require(length % 6 == 1 and position % 42 == 39
                and 3 <= position < length, "family elementary congruences")
        require(all(length % prime == 1 for prime in (5, 11, 13, 37, 101)),
                "family full-divisor length filters")
        require((7*pow(10, length, 49)-18*pow(10, position, 49)-25) % 49 == 0,
                "family modulo49 positive control")
        require(Q(41, 100) < Q(position, length) < Q(42, 100),
                "family lies in surviving interval")
        require((position+length-21)**2 < 2*length**2 < (position+length+21)**2,
                "family irrational distance below 21/L")
        for b in range(2, 101):
            if 12600*b**3 >= length:
                continue
            require(length > 168*b*b, "applicable baseline implies rounding threshold")
            require(Q(21, length) < Q(1, 8*b*b), "rounding loss below 1/(8b^2)")
            require(Q(1, 8*b*b) > Q(1, 6300*b**3),
                    "Diophantine gap exceeds universal-majorant radius")
            for a in range(1, b):
                if gcd(a, b) != 1:
                    continue
                # 2b^2-(a+b)^2 is a nonzero integer. The algebraic
                # conjugate denominator is <4 since 0<a/b<1.
                require(2*b*b != (a+b)**2, "irrationality integer control")
                require(abs(Q(position, length)-Q(a, b)) > Q(1, 6300*b**3),
                        "sample pair outside universal-majorant covering width")
                compared += 1
        rows.append({"length": length, "position": position})
    return {"period": period, "sample_pairs": rows,
            "denominators_checked": "2 through 100 when 12600*b^3 < L",
            "rational_centres_compared": compared,
            "scope": "congruence and majorant controls only; full divisibility not asserted"}


def main():
    result = {"status": "PASS", "scope": "independent finite controls; no new exhaustive lengths",
              "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "constants": constants(), "intervals": interval_checks(),
              "polynomials": polynomial_checks(), "gap_family": gap_family_checks()}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
