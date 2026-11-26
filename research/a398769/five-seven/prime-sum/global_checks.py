#!/usr/bin/env python3
"""Exact controls for GLOBAL.md; finite controls do not prove its theorems."""

from fractions import Fraction
from hashlib import sha256
from math import factorial
from pathlib import Path
import json


def require(condition, label):
    if not condition:
        raise ValueError(label)


def exp_lower(x, degree):
    return sum((x**k / factorial(k) for k in range(degree + 1)), Fraction())


def valuation(n, p):
    require(n != 0, "zero valuation input")
    n = abs(n)
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def conditional_cutoff(c):
    require(c >= 1, "C domain")
    n = 0
    c = Fraction(c)
    rhs = c**6 * 7**17
    while Fraction(117649, 100000)**n < rhs:
        n += 1
    require(Fraction(117649, 100000)**n >= rhs, "cutoff endpoint")
    require(n == 0 or Fraction(117649, 100000)**(n-1) < rhs,
            "cutoff minimality")
    return n


def main():
    # Positive Taylor terms prove all lower exponential bounds used below.
    require(exp_lower(Fraction(2), 5) > 7, "log7<2")
    require(exp_lower(Fraction(5, 2), 6) > 10, "log10<5/2")
    require(exp_lower(Fraction(3, 2), 3) > 3, "log3<3/2")
    require(exp_lower(Fraction(1), 3) == Fraction(8, 3), "e>8/3")
    require(Fraction(8, 3)**40 > 4*10**16, "log(4*10^16)<40")
    # e<11/4: sum through degree 4, plus tail <= (1/5!)/(1-1/6).
    e_upper = exp_lower(Fraction(1), 4) + Fraction(1, factorial(5))*Fraction(6, 5)
    require(e_upper < Fraction(11, 4), "e<11/4")
    require(e_upper**3 < 7**2, "log7>3/2")
    require(Fraction(11, 4)**2 < 10, "log10>2")
    require(81**2*3 < 141**2, "3^(9/2)<141")
    require(8*30**6*141 < 10**12, "Matveev coefficient")
    require(48**6*3*4*8 < 2*10**12, "Yu coefficient")
    require(12*10**12*41 < 10**16, "real threshold")
    require(8*10**12*100 < 10**16, "two-adic threshold")
    require(7**10 < 10**9, "needed exponent is below 9/10")
    require(Fraction(1)-Fraction(1, 3*10**16) > Fraction(9, 10),
            "proved exponent is insufficient")

    # Original decimal words independently check all algebraic forms and
    # exact two-adic valuations on a declared small rectangle.
    pairs = 0
    case_counts = {"i_le_half": 0, "i_ge_half": 0}
    seven_positive = 0
    for length in range(5, 257):
        for position in range(3, length):
            word = "7"*(length-position-1)+"5"+"7"*(position-1)+"5"
            number = int(word)
            f = 7*10**length-18*10**position-25
            require(f == 9*number, "original word")
            require(sum(map(int, word)) == 7*length-4, "digit sum")
            require(10**length < f < 7*10**length, "size")
            t = valuation(number, 7)
            m = f//7**t
            require(m % 7 != 0 and f == 7**t*m, "exact factorization")
            require(t < 2*length, "t size")
            real_form = Fraction(7**t*m, 7*10**length)-1
            require(real_form == -Fraction(18*10**position+25, 7*10**length),
                    "real form identity")
            padic_form = -Fraction(7**t*m, 25)-1
            require(padic_form == -Fraction(10**position*(7*10**(length-position)-18), 25),
                    "signed two-adic form identity")
            v2 = valuation(padic_form.numerator, 2)-valuation(padic_form.denominator, 2)
            require(v2 == position+(2 if length-position == 1 else 1),
                    "exact two-adic valuation")
            if 2*position <= length:
                case_counts["i_le_half"] += 1
                require(real_form**2*10**length < 9, "real form upper bound")
            if 2*position >= length:
                case_counts["i_ge_half"] += 1
                require(2*v2 >= length, "two-adic lower bound")
            if t:
                seven_positive += 1
                require(position % 6 == 3, "necessary position residue")
            pairs += 1

    cutoffs = {str(c): conditional_cutoff(c) for c in (1, 25, 10**6)}
    require(cutoffs == {"1": 204, "25": 323, "1000000": 714}, "cutoff values")
    # Domain and mutation controls must run under python -O too.
    rejected = 0
    for mutant in (lambda: conditional_cutoff(0),
                   lambda: require(117649 == 7**5, "wrong base power"),
                   lambda: require(cutoffs["1"] == 203, "wrong cutoff")):
        try:
            mutant()
        except ValueError:
            rejected += 1
    require(rejected == 3, "negative controls")
    print(json.dumps({
        "schema": 1,
        "scope": "exact finite controls, not a search above the inherited baseline",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "original_decimal_pairs": pairs,
        "lengths_inclusive": [5, 256],
        "positions": "every integer 3<=i<L",
        "case_counts": case_counts,
        "positive_seven_valuation_controls": seven_positive,
        "conditional_5_over_6_cutoffs": cutoffs,
        "5_over_6_bound_proved": False,
        "proved_signed_bound": {"C": 25, "exponent": "1-1/(3*10^16)", "starting_length": 5},
        "new_whole_length_coverage": None,
        "negative_controls_rejected": rejected,
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
