#!/usr/bin/env python3
"""Independent finite controls for the proved W-isometry; no research imports."""
import hashlib
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def v7(n):
    require(n != 0, "valuation of zero")
    t = 0
    while n % 7 == 0:
        n //= 7
        t += 1
    return t


def wmod(length, start, step, j, modulus):
    return (7 * pow(10, length, modulus)
            - 18 * pow(10, start + step * j, modulus) - 25) % modulus


def run():
    counts = dict(difference_pairs=0, children=0, exhaustive_classes=0,
                  coefficient_controls=0, boundary_controls=0)
    roots = []
    # Starts need only be 3 mod6 for this seven-adic theorem. These synthetic
    # starts are deliberately NOT claimed to be ternary representatives.
    for a in (37, 43, 49, 97, 1231, 1579, 1585, 1591, 1597):
        D = 3 ** (a - 8)
        length = (3 ** a + 4) // 7
        step = 2 * D
        require(D % 7 == 5 and (D // 3) % 7 == 4, "D coefficients")
        require((pow(10, step, 49) - 1) % 49 == 28,
                "step coefficient must be 4 after division by seven")
        for start in (3, 9, 39, 123, 2 * D - 3):
            require(start % 6 == 3 and 3 <= start < 2 * D, "start domain")
            K = (length - 1 - start) // step
            require(K in (467, 468), "range bound")
            require(start + step * K <= length - 1
                    < start + step * (K + 1), "floor endpoints")
            counts['boundary_controls'] += 1
            require(wmod(length, start, step, 0, 7) == 0, "depth one")
            for h in range(11):
                modulus = 7 ** (h + 3)
                difference = (wmod(length, start, step, 7 ** h, modulus)
                              - wmod(length, start, step, 0, modulus)) % modulus
                require(v7(difference) == h + 1, "deep difference identity")
                counts['difference_pairs'] += 1
            for i in range(32):
                for j in range(i):
                    exact_t = 1 + v7(i - j)
                    modulus = 7 ** (exact_t + 1)
                    difference = (wmod(length, start, step, i, modulus)
                                  - wmod(length, start, step, j, modulus)) % modulus
                    require(v7(difference) == exact_t, "difference identity")
                    counts['difference_pairs'] += 1
            j = 0
            sequence = [j]
            for m in range(1, 12):
                modulus = 7 ** (m + 1)
                old = wmod(length, start, step, j, modulus)
                require(old % (7 ** m) == 0, "old root")
                carry = old // (7 ** m)
                digit = (-4 * carry) % 7
                passing = []
                for c in range(7):
                    value = wmod(length, start, step, j + c * 7 ** (m - 1), modulus)
                    require(value == (old + 2 * c * 7 ** m) % modulus,
                            "coefficient differs from direct child")
                    if value == 0:
                        passing.append(c)
                    counts['children'] += 1
                    counts['coefficient_controls'] += 1
                require(passing == [digit], "unique child")
                j += digit * 7 ** (m - 1)
                sequence.append(j)
                if m < 5:
                    period = 7 ** m
                    all_roots = [z for z in range(period)
                                 if wmod(length, start, step, z, modulus) == 0]
                    require(all_roots == [j], "full class enumeration")
                    counts['exhaustive_classes'] += period
            roots.append(dict(a=a, synthetic_start=str(start),
                              K=K, j_by_depth=sequence))
    require(any(row['j_by_depth'][4] != 0 for row in roots),
            "nonzero surviving-root positive controls missing")
    # These do not certify membership of any actual kappa prefix. They check
    # the elementary inequalities for the three constant-block classes.
    block_controls = []
    for a in (61, 97, 1231, 1597, 10003):
        for increment, constant, multiplier, additive in (
                (0, 3528, 504, 1), (468, 2268, 324, 0),
                (234, 38304, 5472, 0)):
            h = next(h for h in range(1, (a - 31) // 6 + 1)
                     if 9 * 729 ** h >= constant * (a + 20) ** 2 + 1)
            T = 3 ** (a - 6 * h - 2)
            L = (3 ** a + 4) // 7
            require(T > 17, "block domain")
            require(additive + multiplier * T * (a + 20) ** 2 < L - 2,
                    "strict block comparison")
            old_L = (9 * T + 4) // 7
            shift = 2 * T * increment * (729 ** h - 1) // 728
            for old_s in (3, 2 * T - 3):
                new_s = old_s + shift
                if increment == 0:
                    require(new_s == old_s, "zero run")
                elif increment == 468:
                    require(L - new_s == old_L - old_s, "gap run")
                else:
                    require(L - 2 * new_s == old_L - 2 * old_s, "central run")
                    require(7 * (abs(old_L - 2 * old_s) + 2) < 19 * T,
                            "central offset bound")
            block_controls.append(dict(a=a, h=h, increment=increment,
                                       sufficient_only=True))
    return dict(schema=1, status='PASS', counts=counts, roots=roots,
                block_inequality_controls=block_controls,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                scope='Finite controls; universal claims are proved in ONE_STEP.md, '
                      'not inferred from these samples.')


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
