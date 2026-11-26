#!/usr/bin/env python3
"""Independent original-word arithmetic for 128 specified 3-power sums.

Standard library only.  No other checker is imported.  Decimal blocks and
tracked-power ternary lifting independently recover the sum class.  Every
check remains active under python3 -O.  The printed receipt is deterministic.
"""

from hashlib import sha256
import json
from math import prod
from pathlib import Path


BASE = "9d958f86fc81188de68af97909614e23a186df9f"
B = 1_000_002_000_000


def need(condition, message):
    if not condition:
        raise ArithmeticError(message)


def join(left, right, modulus):
    """Concatenate (10**length, value) pairs, with both entries reduced."""
    return (left[0] * right[0] % modulus,
            (left[1] * right[0] + right[1]) % modulus)


def repeat(digit, count, modulus):
    need(0 <= digit <= 9 and count >= 0 and modulus >= 1, "block inputs")
    value = (1 % modulus, 0)
    block = (10 % modulus, digit % modulus)
    while count:
        if count & 1:
            value = join(value, block, modulus)
        block = join(block, block, modulus)
        count //= 2
    return value


def word_mod(length, position, modulus):
    need(3 <= position < length, "actual position")
    value = repeat(7, length - position - 1, modulus)
    for digit, count in ((5, 1), (7, position - 1), (5, 1)):
        value = join(value, repeat(digit, count, modulus), modulus)
    return value[1]


def ternary_log(target, exponent):
    """Solve 10**r=target mod3**exponent, 0<=r<3**(exponent-2).

    LTE gives v3(10**(3**k)-1)=k+2.  The tracked base is this
    power modulo the final modulus, and each next digit is obtained from
    the nonzero coefficient of 3**(k+2), without testing candidate pow().
    """
    modulus = 3**exponent
    need(exponent >= 3 and target % 9 == 1, "principal-unit input")
    target %= modulus
    residue, current, base = 0, 1, 10
    step, scale = 1, 9
    for _ in range(exponent - 2):
        need((target - current) % scale == 0, "log invariant")
        need((base - 1) % scale == 0, "base valuation invariant")
        coefficient = current * ((base - 1) // scale) % 3
        need(coefficient in (1, 2), "nonsingular ternary digit")
        # Both nonzero elements of F_3 are their own inverses.
        digit = ((target - current) // scale * coefficient) % 3
        residue += digit * step
        current = current * (base**digit) % modulus
        base = base**3 % modulus
        step *= 3
        scale *= 3
    need(current == target and 0 <= residue < step, "complete log")
    need(pow(10, residue, modulus) == target, "independent log readback")
    need(step == 3**(exponent - 2), "log period")
    return residue


def sum_class(a):
    need(a >= 7 and a % 6 == 1, "admissible exponent")
    S = 3**a
    need((S + 4) % 7 == 0, "integral length")
    L = (S + 4) // 7
    need(L % 2 == 1 and S % 5 != 0, "length and five eligibility")
    d, D = 3**(a - 2), 2 * 3**(a - 2)
    need(D > L, "at most one actual position")
    need(pow(10, d, S) == 1 and pow(10, d // 3, S) != 1,
         "exact order is the asserted power of three")
    seven_word = repeat(7, L, S)[1]
    target = (seven_word - 2) * ((S + 1) // 2) % S
    residue = ternary_log(target, a)
    need(residue % 3 == 0, "sum class compatible with 3 mod6")
    # d is odd and a multiple of three.  Exactly one of r,r+d is odd.
    r = residue if residue % 2 else residue + d
    need(0 <= r < D and r % 6 == 3, "canonical combined class")
    s = r if r >= 3 else r + D
    return a, L, S, d, D, r, s


def case(a):
    a, L, S, d, D, r, s = sum_class(a)
    i = s if s < L else None
    result = dict(a=a, L=L, S=S, d=d, D=D, class_residue=r, s=s,
                  i=i, t=None, first_fail_depth=None,
                  first_fail_n_residue=None)
    if i is None:
        return result
    need(word_mod(L, i, S) == 0, "original word sum pass")
    need(word_mod(L, i, 25 * S) == 0, "complete non-seven divisor")
    # Independent readback at 9S detects cancellation of nine mistakes.
    need((7 * pow(10, L, 9*S) - 18 * pow(10, i, 9*S) - 25) % (9*S) == 0,
         "F must retain full factor nine")
    modulus = 1
    for depth in range(1, min(L - 2, 4096) + 1):
        modulus *= 7
        value = word_mod(L, i, modulus)
        if value:
            need(depth <= L - 2, "failure before witness threshold")
            result.update(t=depth - 1, first_fail_depth=depth,
                          first_fail_n_residue=value)
            return result
    # Never silently turn a resource limit into an exclusion certificate.
    raise ArithmeticError(f"a={a}: no first failure certified; investigate as survivor")


def valuation(number, prime):
    need(number > 0, "positive valuation input")
    answer = 0
    while number % prime == 0:
        answer += 1
        number //= prime
    return answer


def controls():
    count = 0
    sum_passes = 0
    sum_three_passes = 0
    nine_negative = None
    digest = sha256()
    for L in range(5, 322, 2):
        for i in range(3, L):
            digits = [7] * L
            digits[-1] = 5
            digits[L-i-1] = 5
            word = "".join(map(str, digits))
            number = int(word)
            S, P = sum(digits), prod(digits)
            F = 7*10**L - 18*10**i - 25
            need(S == 7*L-4 and P == 25*7**(L-2), "literal digit quantities")
            need(F == 9*number, "literal F")
            need(valuation(F, 5) == 2, "five valuation")
            need((number % (P*S) == 0) == (F % (225*S*7**(L-2)) == 0),
                 "original full predicate")
            need((number % S == 0) == (F % (9*S) == 0), "complete sum predicate")
            if number % S == 0:
                sum_passes += 1
                if S % 3 == 0 and S % 5:
                    sum_three_passes += 1
            if nine_negative is None and i % 6 == 3 and S % 3 == 0 and S % 5 and F % S == 0 and number % S:
                nine_negative = dict(L=L, i=i, word=word, S=S,
                                     F_mod_S=0, F_mod_9S=F % (9*S), n_mod_S=number % S)
            for modulus in (1, 7, 49, 343, 2401, S, 9*S, 25*S):
                need(word_mod(L, i, modulus) == number % modulus, "literal block readback")
            digest.update(f"{L},{i},{number % S},{valuation(number, 7)}\n".encode())
            count += 1
    need(sum_passes > 0 and sum_three_passes > 0 and nine_negative is not None,
         "nonzero literal controls")
    log_cases = 0
    for a in range(3, 8):
        for e in range(3**(a-2)):
            need(ternary_log(pow(10, e, 3**a), a) == e, "exhaustive small log")
            log_cases += 1
    # a=7 permits exhaustive enumeration of all original actual words.
    row = case(7)
    actual = [i for i in range(3, row['L'])
              if i % 6 == 3 and word_mod(row['L'], i, row['S']) == 0]
    need(actual == [row['i']], "complete small class enumeration")
    # Abstract positive F, not claimed to be decimal-word examples.
    # They test both sides of the inclusive lift deadline independently
    # of whether a full word satisfying the sum condition exists.
    deadline = []
    for L in (9, 11, 15):
        K, T = 1, 6
        while T <= L:
            K, T = K+1, T*7
        for t in (L-3, L-2, L-1):
            F = 7**t
            zero_run = all(F % 7**(j+1) == 0 for j in range(K, L-2))
            need(zero_run == (t >= L-2), "inclusive zero-run deadline")
            need(F % 7**t == 0 and F % 7**(t+1) != 0, "first failing power")
            deadline.append(dict(L=L, K=K, t=t, first_change_index=t,
                                 survives_through_L_minus_2=zero_run))
    return dict(literal_words=count, literal_digest=digest.hexdigest(),
                sum_passes=sum_passes, sum_passes_with_3_dividing_S_and_5_free=sum_three_passes,
                factor_nine_negative=nine_negative, small_log_cases=log_cases,
                exhaustive_a7=row, abstract_deadline_controls=deadline)


def main():
    tested_controls = controls()
    control = case(25)
    need((control['L'], control['i'], control['t']) ==
         (121041229921, 40582608819, 2), "inherited positive control recovered")
    cases = [case(31 + 6*u) for u in range(128)]
    compatibility = []
    for old, new in zip([control] + cases[:-1], cases):
        a, L, S = old['a'], old['L'], old['S']
        need(new['a'] == a+6 and new['L']-L == 104*S, "length recurrence")
        modulus = 9*S
        old_power, new_power = pow(10, L, modulus), pow(10, new['L'], modulus)
        need(old_power == new_power, "ten-power recurrence at 3**(a+2)")
        need(new['class_residue'] % old['D'] == old['class_residue'], "sum class reduction")
        compatibility.append(dict(a=a, next_a=a+6, power_mod_3_a_plus_2=old_power,
                                  reduced_class=new['class_residue'] % old['D']))
    hits = [row for row in cases if row['i'] is not None]
    histogram = {}
    for row in hits:
        histogram[str(row['t'])] = histogram.get(str(row['t']), 0) + 1
    need(cases[0]['L'] > B, "requested range above inherited endpoint")
    result = dict(schema=1, implementation="independent decimal-block and tracked-power lift",
                  source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  base_commit=BASE, inherited_endpoint=B,
                  specified_exponents=dict(start=31, step=6, count=128, last=793),
                  summary=dict(cases=128, actual_positions=len(hits), misses=128-len(hits),
                               valuation_histogram=histogram, witnesses=0,
                               first_length=cases[0]['L'], last_length=cases[-1]['L']),
                  controls=tested_controls, inherited_control=control,
                  compatibility=compatibility, cases=cases)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
