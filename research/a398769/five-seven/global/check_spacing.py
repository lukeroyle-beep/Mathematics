#!/usr/bin/env python3
"""Non-vacuous finite arithmetic checks of the proved pairwise lemma.

This enumerates fixed-power congruences, not the growing-power problem.
It imports no other search implementation and makes no length-exclusion claim.
"""

import hashlib
import itertools
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def valuation(number):
    require(number != 0, "zero has no finite valuation")
    number = abs(number)
    answer = 0
    while number % 7 == 0:
        number //= 7
        answer += 1
    return answer


def compatible(exponent, dl, di):
    """The lemma's nonzero-difference conclusion, with its hypotheses."""
    require(dl != 0 and di != 0 and dl % 6 == 0 and di % 6 == 0,
            "inapplicable difference pair")
    a, b = 2+valuation(dl), 1+valuation(di)
    return (a == b < exponent) or min(a, b) >= exponent


def check(exponent, limit=1001):
    modulus = 7**exponent
    pairs = []
    for length in range(5, limit + 1, 2):
        for position in range(3, length, 6):
            if (7*pow(10, length, modulus)
                    - 18*pow(10, position, modulus) - 25) % modulus == 0:
                pairs.append((length, position))
    require(pairs, "missing positive congruence controls")
    ordinary = high = same_position = same_length = same_gap = 0
    examples = {}
    for left, right in itertools.combinations(pairs, 2):
        length, position = left
        other_length, other_position = right
        if (length-other_length) % 6:
            continue
        dl = length-other_length
        di = position-other_position
        if dl and di:
            a, b = 2+valuation(dl), 1+valuation(di)
            require(compatible(exponent, dl, di),
                    "pairwise valuation restriction failed")
            if min(a, b) < exponent:
                ordinary += 1
                examples.setdefault("equal_low_valuations", [left, right, a, b])
            else:
                high += 1
                examples.setdefault("both_high_valuations", [left, right, a, b])
        if di == 0:
            require(dl % (6*7**(exponent-2)) == 0,
                    "same-position spacing failed")
            same_position += 1
        if dl == 0:
            require(di % (6*7**(exponent-1)) == 0,
                    "same-length spacing failed")
            same_length += 1
        if dl == di:
            require(dl % (6*7**(exponent-1)) == 0,
                    "same-gap spacing failed")
            same_gap += 1
    require(ordinary > 0, "missing below-modulus controls")
    return dict(exponent=exponent, limit=limit, congruence_pairs=len(pairs),
                equal_low_valuations=ordinary, both_high_valuations=high,
                same_position=same_position, same_length=same_length,
                same_gap=same_gap, examples=examples)


def main():
    # A wrong pair of exponent differences must not pass the lemma filter.
    require(not compatible(3, 6, 6), "negative control was accepted")
    # Both high valuations need not be equal: omitting the threshold is false.
    require(compatible(3, 294, 294), "high-valuation control was rejected")
    require(2+valuation(294) != 1+valuation(294),
            "missing unequal-high control")
    # The actual congruence pairs (17,15), (71,57) show the required +1.
    require(valuation(42) == valuation(54)+1,
            "shifted-valuation positive control failed")
    require(valuation(42) != valuation(54),
            "wrong unshifted-valuation control was not rejected")
    result = dict(
        method="independent fixed-power enumeration and pairwise arithmetic",
        checks=[check(k) for k in (3, 4, 5)],
        global_cutoff=None,
        excludes_new_length_interval=False,
        controls=dict(incompatible_differences_rejected=[6, 6],
                      unequal_high_differences_accepted=[294, 294],
                      unshifted_valuation_equality_rejected=[54, 42]),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
