#!/usr/bin/env python3
"""Complete bounded-position search for S=898129*3**(193+210*t).

Only the explicitly selected t values are searched.  No inherited search code
is imported.  All integer divisibility tests retain the full digit sum.
"""
import argparse
from hashlib import sha256
import json
from math import gcd, lcm
from pathlib import Path

C = 898129
D = 56133


def require(ok, message):
    if not ok:
        raise ValueError(message)


def fmod(L, i, modulus):
    return (7*pow(10, L, modulus)-18*pow(10, i, modulus)-25) % modulus


def crt(r, m, s, n):
    g = gcd(m, n)
    require((s-r) % g == 0, 'incompatible CRT')
    q = n//g
    j = ((s-r)//g * pow(m//g, -1, q)) % q if q > 1 else 0
    W = lcm(m, n)
    return (r+m*j) % W, W


def ternary_log(target, a):
    """Precision doubling; (1+3**m*c)**d=1+3**m*c*d mod 3**(2*m)."""
    require(a >= 2 and target % 9 == 1, 'ternary log domain')
    r, m = 0, 2
    while m < a:
        new = min(a, 2*m)
        M, q, U, step = 3**new, 3**m, 3**(new-m), 3**(m-2)
        z = (target*pow(pow(10, r, M), -1, M)-1) % M
        require(z % q == 0, 'known ternary precision')
        coefficient = (pow(10, step, M)-1)//q
        digit_block = z//q * pow(coefficient, -1, U) % U
        r += step*digit_block
        m = new
        require(pow(10, r, M) == target % M, 'new ternary precision')
    require(0 <= r < 3**(a-2), 'least ternary representative')
    return r


def position_count(r, W, L):
    first = r + ((3-r+W-1)//W)*W
    count = max(0, (L-1-first)//W+1)
    return first, count


def family(t):
    a = 193+210*t
    S = C*3**a
    require((S+4) % 7 == 0, 'integral L')
    L = (S+4)//7
    require(L > 10**12 and L % 2 == 1 and S % 5 != 0, 'length domain')
    M = 3**a
    numerator = 7*pow(10, L, 9*M)-25
    require(numerator % 9 == 0, 'exact integer division by nine')
    target = (numerator//9 * pow(2, -1, M)) % M
    r3 = ternary_log(target, a)
    require(r3 % 729 == 402, 'three-adic overlap')
    r, W = crt(r3, 3**(a-2), 11337, D)
    require(W == 77*3**(a-2), 'exact sum spacing')
    require(L % D == 11248, 'length class modulo D')
    require(fmod(L, r, 9*S) == 0, 'full sum class at its representative')
    require(pow(10, W, S) == 1, 'sum class period after retaining coefficient 18')
    first, total = position_count(r, W, L)
    require(total > 0, 'nonempty actual sum-compatible positions')
    K, T = 1, 6
    while T <= L:
        K += 1
        T *= 7
    rows = []
    previous = total
    r7, T7, modulus = 3, 6, 7
    deepest = []
    for k in range(1, 100):
        require(fmod(L, r7, modulus) == 0, 'seven logarithm certificate')
        rk, Wk = crt(r, W, r7, T7)
        firstk, count = position_count(rk, Wk, L)
        require(count <= previous, 'nested survivor counts')
        rows.append(dict(depth=k, seven_residue=r7, seven_period=T7,
                         least_joint_residue=str(rk), joint_spacing=str(Wk),
                         survivors=count, rejected_at_exact_depth=k-1,
                         rejected_count=previous-count))
        if not count:
            break
        deepest = [firstk+j*Wk for j in range(count)] if count <= 20 else []
        previous = count
        next_modulus = modulus*7
        choices = [r7+j*T7 for j in range(7)
                   if fmod(L, r7+j*T7, next_modulus) == 0]
        require(len(choices) == 1, 'unique next seven-adic lift')
        r7 = choices[0]
        T7 *= 7
        modulus = next_modulus
    else:
        raise ValueError('unresolved survivor at depth 99: extend the explicit bound')
    maximum_depth = rows[-1]['depth']-1
    require(maximum_depth < K and rows[-1]['survivors'] == 0, 'all actual positions reject')
    deepest_rows = []
    for i in deepest:
        residue = fmod(L, i, 7**(maximum_depth+1))
        require(residue and residue % 7**maximum_depth == 0, 'exact rejection depth')
        require(fmod(L, i, 9*S) == 0, 'deepest actual pair full sum')
        deepest_rows.append(dict(i=str(i), F_mod_9S=0,
                                 F_mod_7_next=residue, exact_depth=maximum_depth))
    require(len(deepest_rows) == rows[-2]['survivors'], 'all deepest positions retained')
    return dict(t=t, a=a, L=str(L), S=str(S), K=K,
                sum_class_residue=str(r), sum_class_spacing=str(W),
                first_position=str(first), sum_compatible_positions=total,
                maximum_depth=maximum_depth, depths=rows,
                deepest_positions=deepest_rows, joint_K_survivors=0)


def controls():
    require(D == 3**6*7*11 and C % 3 and C % 5 and C % 7, 'fixed factor controls')
    require(pow(10, D, C) == 1, 'fixed order divides D')
    require(all(pow(10, D//p, C) != 1 for p in (3, 7, 11)), 'fixed order exactly D')
    require(7*D == 3**6*539 and pow(3, 210, 539) == 1, '210-step length progression')
    require((7*pow(10, 11248, C)-18*pow(10, 11337, C)-25) % C == 0,
            'fixed c congruence')
    require((7*pow(10, 4687, 3**10)-18*pow(10, 402, 3**10)-25) % 3**10 == 0,
            'fixed ternary overlap')
    # Separate digit-by-digit oracle on small precisions, nonzero exponents.
    checks = 0
    for a in range(2, 41):
        for expected in (0, 1, 3**(a-2)//2, 3**(a-2)-1):
            target = pow(10, expected, 3**a)
            require(ternary_log(target, a) == expected % 3**(a-2), 'known log control')
            r, step = 0, 1
            for m in range(3, a+1):
                hits = [r+j*step for j in range(3)
                        if pow(10, r+j*step, 3**m) == target % 3**m]
                require(len(hits) == 1, 'digit oracle uniqueness')
                r, step = hits[0], 3*step
            require(r == ternary_log(target, a), 'digit oracle agreement')
            checks += 1
    return dict(known_and_digit_log_controls=checks, progression_step=210)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--first-t', type=int, default=0)
    parser.add_argument('--last-t', type=int, default=31)
    args = parser.parse_args()
    require(0 <= args.first_t <= args.last_t, 'explicit t interval')
    checked = controls()
    rows = [family(t) for t in range(args.first_t, args.last_t+1)]
    histogram = {}
    for row in rows:
        for depth in row['depths']:
            key = str(depth['rejected_at_exact_depth'])
            histogram[key] = histogram.get(key, 0)+depth['rejected_count']
    print(json.dumps(dict(status='NO WITNESS IN THE STATED SEARCH',
                         source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                         family='S=898129*3**(193+210*t)',
                         first_t=args.first_t, last_t=args.last_t,
                         whole_length_samples=len(rows), contiguous_length_interval=False,
                         total_sum_compatible_positions=sum(x['sum_compatible_positions'] for x in rows),
                         exact_depth_histogram=histogram, joint_K_survivors=0,
                         controls=checked, rows=rows), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
