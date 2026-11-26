#!/usr/bin/env python3
"""Independent exact-arithmetic checks; standard library only.

No sibling checker is imported.  All checks survive python3 -O.  The
literal-word domain is a regression test, not a new large-length search.
The exponential enclosure uses a positive Taylor sum and a geometric
upper bound on its tail.  No floating-point comparison is authoritative.
"""

from fractions import Fraction as Q
from hashlib import sha256
import json
from math import prod
from pathlib import Path


B = 1_000_002_000_000
N = 10**12


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def valuation(value, prime):
    require(value != 0, "valuation of zero")
    exponent = 0
    while value % prime == 0:
        value //= prime
        exponent += 1
    return exponent


def exp_interval(x, terms):
    """Enclose exp(x), x>0, using terms of degree zero through terms.

    The first omitted term is x**(terms+1)/(terms+1)!.  Subsequent
    ratios are at most x/(terms+2), so the geometric sum bounds the
    omitted positive tail from above.
    """
    require(x > 0 and terms >= 0 and x < terms + 2, "exp inputs")
    term = Q(1)
    lower = term
    for k in range(1, terms + 1):
        term *= x / k
        lower += term
    first_omitted = term * x / (terms + 1)
    upper = lower + first_omitted / (1 - x / (terms + 2))
    return lower, upper


def numerical_checks():
    e1_lo, e1_hi = exp_interval(Q(1), 32)
    e16_lo, e16_hi = exp_interval(Q(8, 5), 32)
    e2_lo, e2_hi = exp_interval(Q(2), 32)
    e22_lo, e22_hi = exp_interval(Q(22), 100)
    e2303_lo, e2303_hi = exp_interval(Q(2303, 1000), 40)
    e42_lo, e42_hi = exp_interval(Q(21, 5), 40)
    require(2 < e1_lo < e1_hi < 3, "2 < e < 3")
    require(e16_hi < 5, "ln 5 > 8/5")
    require(e2_lo > 7, "ln 7 < 2, ln 5 < 2")
    require(e22_lo > 2 * 10**9 + 1, "ln(2e9+1) < 22")
    require(e2303_lo > 10, "ln 10 < 2303/1000")
    require(e42_lo > 63, "ln 63 < 21/5")

    # ln7>1 since e<3<7; hence 1/ln7<1.  Under H=L/1e9,
    # t<2L gives b'<2e9+1.  ln ln5<1 since ln5<2<e.
    coefficient_upper = Q(120 * 2) / Q(8, 5)**4
    maximum_first_upper = Q(22) + 1 + Q(2, 5)
    require(coefficient_upper < 48, "coefficient strict bound")
    require(maximum_first_upper < 24, "first maximum branch")
    require(10 * Q(2) < 24 and 10 < 24, "remaining branches")
    require(Q(N, 10**9) > 2, "height floor for H")

    slope_gap = Q(1, 25000) - Q(48 * 24**2, 10**9)
    require(slope_gap == Q(193, 15625000), "slope gap")
    require(slope_gap * N > 2, "strict i-2 comparison for L>=N")
    require(B >= N, "inherited endpoint exceeds proof threshold")
    polynomial_margin = Q(N, 10**9) - Q(21, 5) - 36 * 12 * Q(2303, 1000)
    require(polynomial_margin == Q(113, 125), "polynomial base margin")
    require(polynomial_margin > 0, "polynomial base strict")
    derivative_lower = Q(1, 10**9) - Q(36, N)
    require(derivative_lower > 0, "polynomial persistence derivative")

    # For L>=5, 49**L>7*10**L; ratio grows by 49/10>1.
    require(49**5 > 7 * 10**5 and 49 > 10, "t<2L size proof")
    # The full-witness lower valuation t>=L-2 gives the exact upper
    # A=F/(25*7**t)<(343/25)*(10/7)**L.
    require(Q(7 * 7**2, 25) == Q(343, 25), "A upper coefficient")
    return {
        "method": "positive exponential Taylor sums plus geometric upper tails",
        "exp_degree_limits": {"1": 32, "8/5": 32, "2": 32, "22": 100,
                              "2303/1000": 40, "21/5": 40},
        "coefficient_rational_upper": str(coefficient_upper),
        "first_maximum_branch_upper": str(maximum_first_upper),
        "other_maximum_branch_upper": [20, 10],
        "slope_gap": str(slope_gap),
        "slope_gap_at_1e12_minus_2": str(slope_gap * N - 2),
        "polynomial_base_margin": str(polynomial_margin),
        "polynomial_derivative_lower_at_1e12": str(derivative_lower),
        "inherited_endpoint": B,
    }


def digits_and_number(length, position):
    require(3 <= position < length, "word position")
    digits = [7] * length
    digits[-1] = 5
    digits[length - 1 - position] = 5
    # Literal decimal word, independent of the closed formula.
    value = int("".join(str(digit) for digit in digits))
    return digits, value


def full_digit_predicate(value):
    digits = [int(c) for c in str(value)]
    denominator = sum(digits) * prod(digits)
    return denominator > 0 and value % denominator == 0


def literal_checks():
    counters = dict(words=0, digit_sum_passes=0, five_free_digit_sum_passes=0,
                    five_free_digit_sum_passes_with_3_dividing_sum=0,
                    dropped_nine_false_positives=0,
                    five_free_dropped_nine_false_positives=0,
                    depth_at_least_2=0, depth_at_least_3=0,
                    full_residual_witnesses=0)
    digest = sha256()
    examples = {}
    for length in range(5, 402, 2):
        for position in range(3, length):
            digits, number = digits_and_number(length, position)
            digit_sum, digit_product = sum(digits), prod(digits)
            literal_F = 9 * number
            require(digit_sum == 7 * length - 4, "literal digit sum")
            require(digit_product == 25 * 7**(length - 2), "literal product")
            require(literal_F == 7 * 10**length - 18 * 10**position - 25,
                    "literal F identity")
            t = valuation(literal_F, 7)
            require(valuation(literal_F, 5) == 2, "exact v5(F)")
            C = literal_F // (25 * 7**t)
            require(literal_F == 25 * C * 7**t, "seven-free factor")
            require(C > 0 and C % 5 and C % 7 and C % 3 == 0, "C units and 3 factor")
            require(25 * (C * 7**t + 1)
                    == 10**position * (7 * 10**(length-position) - 18),
                    "five-adic identity")
            require(valuation(C * 7**t + 1, 5) == position - 2,
                    "exact v5(C*7**t+1)")
            require(t < 2 * length, "literal t<2L")

            direct_full = number % (digit_product * digit_sum) == 0
            require(direct_full == (literal_F % (225 * digit_sum * 7**(length-2)) == 0),
                    "full original divisor equivalence")
            sum_pass = number % digit_sum == 0
            require(sum_pass == (literal_F % (9 * digit_sum) == 0), "retain 9S")
            conditional_full = digit_sum % 5 != 0 and sum_pass and t >= length - 2
            require(direct_full == conditional_full, "full necessary-and-sufficient predicate")

            # Extend the quotient factorization to rationals solely for testing.
            # These q values are not asserted to be integer witnesses.
            q_rational = Q(number, digit_product * digit_sum)
            seven_exponent = valuation(q_rational.numerator, 7) - valuation(q_rational.denominator, 7)
            seven_power = Q(7**seven_exponent) if seven_exponent >= 0 else Q(1, 7**(-seven_exponent))
            q0_rational = q_rational / seven_power
            require(seven_exponent == t - (length - 2), "rational quotient v7")
            require(9 * digit_sum * q0_rational == C, "rationally extended quotient identity")

            counters["words"] += 1
            counters["digit_sum_passes"] += int(sum_pass)
            counters["depth_at_least_2"] += int(t >= 2)
            counters["depth_at_least_3"] += int(t >= 3)
            counters["full_residual_witnesses"] += int(direct_full)
            if sum_pass and digit_sum % 5:
                counters["five_free_digit_sum_passes"] += 1
                if digit_sum % 3 == 0:
                    counters["five_free_digit_sum_passes_with_3_dividing_sum"] += 1
                    examples.setdefault("five_free_sum_with_3_dividing_sum", [length, position, t, digit_sum])
                if t >= 2:
                    examples.setdefault("five_free_sum_with_depth_2", [length, position, t, digit_sum])
            false_nine = literal_F % digit_sum == 0 and not sum_pass
            if false_nine:
                counters["dropped_nine_false_positives"] += 1
                if digit_sum % 5:
                    counters["five_free_dropped_nine_false_positives"] += 1
                    examples.setdefault("five_free_dropped_nine_false_positive", [length, position, t, digit_sum])
            digest.update(f"{length},{position},{t},{int(sum_pass)},{int(direct_full)}\n".encode())

    require(counters["words"] == 39800, "literal domain cardinality")
    for key in ("five_free_digit_sum_passes_with_3_dividing_sum", "depth_at_least_3",
                "five_free_dropped_nine_false_positives"):
        require(counters[key] > 0, "nonvacuous " + key)
    require(full_digit_predicate(135), "positive general full-digit control 135")
    require(not full_digit_predicate(137), "negative general full-digit control 137")
    return {
        "coverage": "all odd 5<=L<=401, all integer 3<=i<L",
        "counts": counters,
        "examples_L_i_t_S": examples,
        "pair_summary_sha256": digest.hexdigest(),
        "positive_general_full_predicate_control": 135,
        "negative_general_full_predicate_control": 137,
        "quotient_test_scope": "rational extension on literal words; no residual full witness assumed",
    }


def residue_at_next_depth(length, residue, period, depth):
    modulus = 7**(depth + 1)
    children = [residue + digit * period for digit in range(7)]
    matches = [r for r in children
               if (7 * pow(10, length, modulus) - 18 * pow(10, r, modulus) - 25) % modulus == 0]
    require(len(matches) == 1, "unique seven-adic child")
    return matches[0]


def lifting_checks():
    actual_positions = 0
    delayed_first_changes = 0
    greatest_depth = 0
    digest = sha256()
    for length in range(5, 402, 2):
        K, period = 1, 6
        while period <= length:
            K += 1
            period *= 7
        residue, running_period = 3, 6
        for depth in range(1, K):
            residue = residue_at_next_depth(length, residue, running_period, depth)
            running_period *= 7
        require(running_period == period and 0 <= residue < period, "representative range")
        if not 3 <= residue < length:
            continue
        actual_positions += 1
        _, number = digits_and_number(length, residue)
        t = valuation(9 * number, 7)
        require(t >= K, "actual representative depth")
        greatest_depth = max(greatest_depth, t)
        delayed_first_changes += int(t > K)
        original_residue = residue
        for depth in range(K, t + 1):
            next_residue = residue_at_next_depth(length, residue, running_period, depth)
            require((next_residue == residue) == (depth < t), "first change is exactly at t")
            if depth == t:
                require(next_residue >= period > length, "first change escapes actual positions")
            residue = next_residue
            running_period *= 7
        digest.update(f"{length},{original_residue},{K},{t}\n".encode())

    # Synthetic valuation controls check only the exact deadline logic.
    # They are not decimal words and are not counterexamples.
    synthetic = []
    for length in (5, 17, 101):
        for t in (length - 3, length - 2):
            value = 7**t
            first_nonzero_digit = next(j for j in range(t + 1) if (value // 7**j) % 7)
            require(first_nonzero_digit == t, "synthetic first nonzero digit")
            passes = value % 7**(length - 2) == 0
            require(passes == (t == length - 2), "L-2 is too late to reject")
            synthetic.append([length, t, passes])
    require(actual_positions > 0 and delayed_first_changes > 0, "nonzero lifting controls")
    return {"actual_positions": actual_positions,
            "first_changes_later_than_K": delayed_first_changes,
            "largest_observed_t": greatest_depth,
            "actual_position_summary_sha256": digest.hexdigest(),
            "synthetic_L_first_change_passes_seven_power": synthetic,
            "synthetic_scope": "valuation deadline arithmetic only; not decimal words"}


def main():
    result = {
        "status": "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "numerical": numerical_checks(),
        "literal_words": literal_checks(),
        "lifting": lifting_checks(),
        "coverage_limit": "regression checks only; no new whole-length endpoint or Lean proof",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
