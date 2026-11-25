#!/usr/bin/env python3
"""Independent exact quotient and digit-block checks; imports no search code.

This checks bounded controls and one huge digit-sum-only pair. It does not
prove a global cutoff or exclude that huge pair's entire length.
"""
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def valuation(n, p):
    require(n > 0, "valuation requires a positive integer")
    count = 0
    while n % p == 0:
        n //= p
        count += 1
    return count


def extract(length, a):
    modulus = 10**((length + 1)//2)//25
    candidates = [(7*10**length)//(25*a), (-pow(a, -1, modulus)) % modulus]
    accepted = []
    for q in set(candidates):
        if q <= 0:
            continue
        b = a*q+1
        i = valuation(b, 5)+2
        if not (3 <= i < length and i % 6 == 3 and length-i >= 2):
            continue
        if valuation(b, 2) != i+1:
            continue
        if 25*a*q == 7*10**length-18*10**i-25:
            accepted.append((i, q))
    return candidates, sorted(accepted)


def append_repeated_digit(n, digit, count, modulus):
    # Binary composition acts directly on the accumulated decimal prefix.
    multiplier, addition = 10 % modulus, digit % modulus
    while count:
        if count & 1:
            n = (n*multiplier+addition) % modulus
        multiplier, addition = (multiplier*multiplier % modulus,
                                addition*(multiplier+1) % modulus)
        count //= 2
    return n


def digit_blocks(length, position, modulus):
    n = append_repeated_digit(0, 7, length-position-1, modulus)
    n = (10*n+5) % modulus
    n = append_repeated_digit(n, 7, position-1, modulus)
    return (10*n+5) % modulus


def main():
    pairs = lengths = block_comparisons = 0
    for length in range(5, 302, 2):
        s = 7*length-4
        if s % 5 == 0:
            continue
        lengths += 1
        a = 9*7**(length-2)*s
        r = (length-1)//2
        modulus = 10**(r+1)//25
        require(math.gcd(a, modulus) == 1, "candidate inverse domain")
        require(Fraction(7*10**length, 25*a*modulus)
                == Fraction(49, 9*s)*Fraction(10, 49)**r < 1,
                "exact X/K bound")
        expected = []
        for i in range(3, length, 6):
            digits = "7"*(length-i-1)+"5"+"7"*(i-1)+"5"
            number = int(digits)
            actual_digits = list(map(int, digits))
            product, digit_sum = math.prod(actual_digits), sum(actual_digits)
            require(s == digit_sum and 25*a == 9*product*s, "actual P,S")
            if i <= r:
                require(Fraction(18*10**i+25, 25*a)
                        <= Fraction(301, 225*s)*Fraction(10, 49)**r < 1,
                        "small-position correction bound")
            quotient, remainder = divmod(number, product*digit_sum)
            if remainder == 0:
                expected.append((i, quotient))
            for m in (1, 3, 9, 49, 343, s):
                require(digit_blocks(length, i, m) == number % m,
                        "direct digit-block comparison")
                block_comparisons += 1
            pairs += 1
        require(extract(length, a)[1] == expected, "direct quotient equivalence")
        require(not expected, "unexpected original-problem witness")

    controls = []
    for length, i, a, q in [(7, 3, 311031, 9), (11, 9, 433015873, 63),
                            (17, 15, 556734693877551, 49)]:
        candidates, accepted = extract(length, a)
        require(accepted == [(i, q)], "synthetic positive quotient control")
        controls.append(dict(L=length, i=i, synthetic_A=a,
                             candidates=candidates, exact_q=q,
                             original_problem_witness=False))

    length, position = 121041229921, 40582608819
    s = 7*length-4
    residues = {str(m): digit_blocks(length, position, m) for m in (s, 49, 343)}
    require(s == 3**25 and residues[str(s)] == 0
            and residues["49"] == 0 and residues["343"] == 294,
            "huge digit-sum-only control from actual digit blocks")
    result = dict(method="independent exact division and decimal-block composition",
                  filtered_lengths_through_301=lengths,
                  direct_digit_pairs=pairs, block_comparisons=block_comparisons,
                  full_witnesses=[], synthetic_positive_controls=controls,
                  large_sum_only_control=dict(L=length, i=position, S=s,
                                              n_residues=residues,
                                              original_problem_witness=False,
                                              whole_length_exclusion=False),
                  global_cutoff=None, new_interval_above_10000000=None,
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
