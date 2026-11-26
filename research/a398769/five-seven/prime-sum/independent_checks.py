#!/usr/bin/env python3
"""Independent literal polynomial / original-decimal audit. No project imports."""
import json
from math import isqrt, prod


def require(ok, message):
    if not ok:
        raise ValueError(message)


def prime(p):
    return p >= 2 and all(p % q for q in range(2, isqrt(p) + 1))


def word(L, i):
    return '7' * (L - i - 1) + '5' + '7' * (i - 1) + '5'


def original(s):
    return int(s) % (sum(map(int, s)) * prod(map(int, s))) == 0


def main():
    require(original('135'), 'original predicate positive control')
    require(not original('137'), 'original predicate negative control')
    literal_count = 0
    for L in range(5, 202, 2):
        for i in range(3, L):
            s = word(L, i)
            n, S, P = int(s), sum(map(int, s)), prod(map(int, s))
            F = 7 * 10**L - 18 * 10**i - 25
            require(9 * n == F and S == 7 * L - 4 and P == 25 * 7**(L - 2), 'decimal identity')
            require(n % 125 == 25, 'exact five valuation')
            require(original(s) == (F % (225 * S * 7**(L - 2)) == 0), 'full divisor')
            require(original(s) == (S % 5 != 0 and F % (9 * S) == 0 and F % 7**(L - 2) == 0), 'joint divisor')
            if F % 7 == 0:
                require(i % 6 == 3, 'position class')
            literal_count += 1

    roots = {}
    prime_rows = 0
    for p in range(31, 3001, 14):
        if not prime(p):
            continue
        L = (p + 4) // 7
        # Direct exhaustive polynomial evaluation, without a root-extraction formula.
        ys = [y for y in range(p) if pow(y, 7, p) == pow(10, 5, p)]
        require(len(ys) == 1 and ys[0] == pow(10, L, p), 'unique fixed Y')
        hs = [x for x in range(p) if (pow(180 * x*x + 25, 7, p) - pow(7, 7, p)*pow(10, 5, p)) % p == 0]
        gs = [z for z in range(p) if (pow(18000 * pow(z, 6, p) + 25, 7, p) - pow(7, 7, p)*pow(10, 5, p)) % p == 0]
        A = (7 * ys[0] - 25) * pow(180, -1, p) % p
        B = (7 * ys[0] - 25) * pow(18000, -1, p) % p
        require(hs == [x for x in range(p) if x*x % p == A], 'H root equivalence')
        require(gs == [z for z in range(p) if pow(z, 6, p) == B], 'G root equivalence')
        require(not gs or hs, 'sextic implies quadratic')
        if p in (31, 59, 199, 283):
            roots[str(p)] = {'L': L, 'Y': ys[0], 'A': A, 'B': B, 'H_roots': hs, 'G_roots': gs}
        prime_rows += 1
    require(roots['31']['H_roots'] == [], '31 control')
    require(roots['59']['H_roots'] == [26, 33], '59 control')
    require(pow(roots['199']['B'], 33, 199) == 107, '199 sextic character')
    require(pow(107, 6, 199) == 1 and all(pow(107, d, 199) != 1 for d in (1, 2, 3)), 'primitive character')
    require(pow(roots['283']['B'], 47, 283) == 1, '283 sextic character')

    # Full sum positives: original decimal arithmetic supplies the predicate.
    sum_passes = []
    for p in range(31, 5001, 14):
        if not prime(p):
            continue
        L = (p + 4) // 7
        for i in range(3, L, 6):
            n = int(word(L, i))
            if n % p:
                continue
            y = pow(10, L, p)
            x = pow(10, (i - 1) // 2, p)
            z = pow(10, (i - 3) // 6, p)
            require((180*x*x + 25 - 7*y) % p == 0, 'necessary square root at actual pair')
            require((18000*pow(z, 6, p) + 25 - 7*y) % p == 0, 'necessary sixth root at actual pair')
            t, v = 0, n
            while v % 7 == 0:
                v //= 7
                t += 1
            require(t < L - 2 and not original(word(L, i)), 'necessary passes are not witnesses')
            sum_passes.append([L, i, p, t])
    require(sum_passes == [[165, 33, 1151, 1], [195, 15, 1361, 1], [365, 225, 2551, 2], [605, 213, 4231, 1]], 'sum-compatible controls')
    print(json.dumps({'literal_pairs': literal_count, 'polynomial_prime_range': [31, 3000], 'prime_rows': prime_rows, 'roots': roots, 'full_sum_control_prime_limit': 5000, 'full_sum_passes_L_i_S_t': sum_passes, 'original_predicate_positive': 135, 'status': 'PASS'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
