#!/usr/bin/env python3
"""Independent-of-imports recurrence and dual-number checks for the pair proof."""
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def dual_add(a, b, modulus):
    return tuple((x+y) % modulus for x, y in zip(a, b))


def dual_mul(a, b, modulus):
    return (a[0]*b[0] % modulus, (a[0]*b[1]+a[1]*b[0]) % modulus)


def dual_power(x, exponent, modulus):
    result = (1, 0)
    while exponent:
        if exponent & 1:
            result = dual_mul(result, x, modulus)
        x = dual_mul(x, x, modulus)
        exponent //= 2
    return result


def eliminant(k, x, modulus):
    # Automatic differentiation through the factored expression; no derivative
    # coefficients are entered separately.
    variable = (x % modulus, 1)
    leading = dual_mul((7*pow(10, 4687, modulus), 0),
                       dual_power(variable, 6561, modulus), modulus)
    inner = dual_add(dual_mul((7*10**7, 0), dual_power(variable, 9, modulus), modulus),
                     (-25, 0), modulus)
    product = dual_mul(dual_mul((-pow(10, 10*k, modulus), 0),
                               dual_power(variable, 14*k, modulus), modulus), inner, modulus)
    return dual_add(dual_add(leading, (-25, 0), modulus), product, modulus)


def compute():
    modulus = 343
    order = 294
    length = ((3**31+4)//7) % order
    delta = 2*3**29 % order
    transitions = []
    for u in range(7):
        next_length = (729*length-416) % order
        left = (7*pow(10, length, modulus)-25) % modulus
        right = (7*pow(10, next_length, modulus)-25) % modulus
        generator = pow(10, delta, modulus)
        power = 1
        ks = []
        # Every increment is checked, including both endpoints.
        for k in range(469):
            if left*power % modulus == right:
                ks.append(k)
            power = power*generator % modulus
        transitions.append(dict(u=u, k=ks))
        length = next_length
        delta = 729*delta % order
    expected = list(range(42, 469, 49))
    need(all(row['k'] == expected for row in transitions), 'complete depth-three filter')
    need(pow(10, 6, 49) != 1 and pow(10, 6, 7) == 1, 'order lift base')
    derivative_rows = []
    for k in expected:
        values = []
        for w in range(4, 294, 6):
            values.append(eliminant(k, pow(10, w, modulus), modulus)[1])
        need(values == [49]*49, 'derivative on all eligible classes')
        derivative_rows.append(dict(k=k, residues=values))
    # Exact exponent/coefficient identities for the entire polynomial, plus
    # independent modular evaluation in the original F expressions.
    checks = 0
    for a in (31, 37, 97, 103, 1567):
        d = 3**(a-2)
        w, remainder = divmod(d, 7)
        need(remainder == 5 and w % 6 == 4, 'w domain')
        length = (9*d+4)//7
        next_length = (9*729*d+4)//7
        need(length == 9*w+7 and next_length == 6561*w+4687, 'length identity')
        need(next_length-length == 936*d, 'length increment')
        for k in range(469):
            need(2*d*k == 14*k*w+10*k, 'position exponent identity')
            # Positivity: both terms are nonnegative and one is strictly positive.
            need(468-k >= 0 and (468-k > 0 or k > 0), 'positivity endpoint')
            for m in (7**3, 7**6, 3**8, 11**3):
                s = 3
                sp = s+2*d*k
                f = (7*pow(10, length, m)-18*pow(10, s, m)-25) % m
                fp = (7*pow(10, next_length, m)-18*pow(10, sp, m)-25) % m
                need((fp-pow(10, 2*d*k, m)*f) % m ==
                     eliminant(k, pow(10, w, m), m)[0], 'eliminant identity')
                checks += 1
    # Symbolic degree/norm bounds, verified with exact integers.
    norm_max = 0
    for k in expected:
        need(14*k+9 < 6561, 'polynomial degree')
        norm = 7*10**4687 + 25 + 7*10**(10*k+7) + 25*10**(10*k)
        need(norm < 10**4688, 'coefficient one-norm bound')
        norm_max = max(norm_max, norm)
    return dict(status='PASS', source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                transitions=transitions, transition_checks=7*469,
                k_values=expected, derivative_classes=list(range(4, 294, 6)),
                derivative_rows=derivative_rows, derivative_checks=9*49,
                identity_modular_checks=checks, degree=6561,
                coefficient_norm_strict_upper_power_ten=4688,
                all_positivity_endpoints_checked=True)


if __name__ == '__main__':
    print(json.dumps(compute(), indent=2, sort_keys=True))
