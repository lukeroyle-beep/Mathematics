#!/usr/bin/env python3
"""Exact whole-length audit; Python 3.9+, standard library, checks survive -O.

Direct modular-power path, independent of independent_blocks.py and inherited
checkers. Inputs are the two unchanged appendix positions in SUBMISSION.txt.
No giant decimal integer or power 10**L is constructed for either appendix.
"""
from collections import Counter
from hashlib import sha256
from math import gcd, isqrt, lcm
from pathlib import Path
import json
import re


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def fmod(length, position, modulus):
    return (7 * pow(10, length, modulus)
            - 18 * pow(10, position, modulus) - 25) % modulus


def v7(residue):
    require(residue != 0, 'valuation precision exhausted')
    depth = 0
    while residue % 7 == 0:
        residue //= 7
        depth += 1
    return depth


def prime(n):
    return n >= 2 and all(n % q for q in range(2, isqrt(n) + 1))


def factor(n):
    result = {}
    q = 2
    while q * q <= n:
        while n % q == 0:
            result[q] = result.get(q, 0) + 1
            n //= q
        q += 1
    if n > 1:
        result[n] = result.get(n, 0) + 1
    return result


def certify_order(modulus, order, factors):
    product = 1
    for p, exponent in factors.items():
        require(prime(p), 'order factor is not prime')
        product *= p ** exponent
    require(product == order, 'incomplete order factorization')
    require(pow(10, order, modulus) == 1, 'not an exponent period')
    proper = {str(p): str(pow(10, order // p, modulus)) for p in factors}
    require(all(int(x) != 1 for x in proper.values()), 'order is not minimal')
    return {'modulus': str(modulus), 'order': str(order),
            'factorization': factors, 'at_order': 1,
            'at_order_divided_by_prime': proper}


def small_literal_checks():
    """Literal words test the sum coset and joint-depth class exhaustively."""
    pairs = classes = pairs_with_three = joint = 0
    three_control = None
    for length in range(5, 402, 2):
        s = 7 * length - 4
        if gcd(s, 10) != 1:
            continue
        d, value = 1, 10 % s
        while value != 1:
            d += 1
            value = 10 * value % s
        positions, depths = [], {}
        for position in range(3, length):
            n = int('7' * (length-position-1) + '5'
                    + '7' * (position-1) + '5')
            f = 7 * 10 ** length - 18 * 10 ** position - 25
            require(f == 9*n, 'literal decimal reduction')
            require((n % s == 0) == (f % (9*s) == 0), 'full sum lost nine')
            if n % s == 0:
                positions.append(position)
                depths[position] = v7(n)
            pairs += 1
            pairs_with_three += (s % 3 == 0)
        if not positions:
            continue
        classes += 1
        seed = positions[0]
        require(positions == [j for j in range(3, length) if (j-seed) % d == 0],
                'literal sum-class mismatch')
        if s % 3 == 0 and three_control is None:
            three_control = {'L': length, 'S': s, 'd': d, 'positions': positions}
        for k in range(1, 5):
            qualified = [j for j in positions if depths[j] >= k]
            if qualified:
                gap = lcm(d, 6 * 7 ** (k-1))
                expected = [j for j in range(3, length) if (j-qualified[0]) % gap == 0]
                require(qualified == expected, 'literal joint class mismatch')
                joint += 1
    require(three_control is not None, 'missing three-divisible positive control')
    return {'odd_lengths_inclusive': [5, 401], 'positions': 'all 3 <= i < L',
            'filter': 'gcd(7L-4,10)=1', 'literal_pairs': pairs,
            'literal_pairs_with_3_dividing_S': pairs_with_three,
            'nonempty_sum_classes': classes, 'nonempty_joint_classes_k_1_to_4': joint,
            'three_divisible_positive_control': three_control}


def grid_controls():
    length = 1290643
    table = {str(i): fmod(length, i, 49) for i in range(3, 42, 6)}
    require(table == {'3': 28, '9': 7, '15': 35, '21': 14,
                      '27': 42, '33': 21, '39': 0}, 'seven-lift table')
    rows = []
    for m in range(2):
        for j in range(2):
            a, b = 12 + 84*m, 1 + 42*j
            s = 3**a * 17**b
            length = (s+4)//7
            d = 16*3**(a-2)*17**(b-1)
            require(7*length == s+4 and length % 2 == 1, 'grid length')
            require((s-9034497) % 2352 == 0 and length % 42 == 25,
                    'grid freezing')
            require(d % 42 == 36 and d < length < 2*d and 7*d > length,
                    'grid spacing')
            require([fmod(length, x, 49) for x in (15,9,3)] == [35,7,28],
                    'depth-one neighbour residues')
            rows.append({'m': m, 'j': j, 'L_mod_42': length % 42,
                         'd_mod_42': d % 42, 'd_less_L_less_2d': True,
                         '7d_greater_L': True})
    return {'A': 84, 'B': 42, 'chosen_e': 9,
            'all_lifts_F_mod_49': table, 'grid_controls': rows,
            'neighbour_i_mod_42': [15,9,3], 'neighbour_F_mod_49': [35,7,28],
            'scope': 'finite controls; arbitrary-grid and density proofs in PROOF.md'}


def example(a, p, b, k, position):
    s = 3**a * p**b
    length, rem = divmod(s+4, 7)
    require(rem == 0 and length % 2 == 1 and length > k+2, 'length domain')
    require(prime(p), 'nonprime appendix factor')
    base_order = 16 if p == 17 else 56133
    base_factors = factor(base_order)
    base_certificate = certify_order(p, base_order, base_factors)
    lift_residue = pow(10, base_order, p*p)
    require((lift_residue-1) % p == 0 and lift_residue != 1, 'order lift obstruction')
    lifted_order = base_order * p**(b-1)
    lifted_factors = dict(base_factors)
    if b > 1:
        lifted_factors[p] = b-1
    lifted_certificate = certify_order(p**b, lifted_order, lifted_factors)
    three_order = 3**(a-2)
    d = lcm(three_order, lifted_order)
    factors = ({2:4, 3:a-2, 17:b-1} if p == 17
               else {3:a-2, 7:1, 11:1, p:b-1})
    s_certificate = certify_order(s, d, factors)
    require(fmod(length, position, 225*s*7**k) == 0, 'supplied depth divisibility')
    next_residue = fmod(length, position, 7**(k+1))
    require(v7(next_residue) == k, 'supplied exact depth')
    require(41*length < 100*position < 42*length, 'supplied strict interval')
    lo = -((position-3)//d)
    hi = (length-1-position)//d
    first, last = position+lo*d, position+hi*d
    require(3 <= first <= last < length, 'actual endpoints')
    require(first-d < 3 and last+d >= length, 'endpoints not exhaustive')
    hist, parity = Counter(), {'even':Counter(), 'odd':Counter()}
    digest = sha256()
    maxima = []
    max_depth = -1
    modulus = 7**12
    for h in range(lo, hi+1):
        j = position+h*d
        # Fresh direct modular powers at every representative, not a recurrence
        # that merely assumes the spacing theorem to pass the sum condition.
        require(fmod(length,j,9*s) == 0, 'sum divisibility at enumerated position')
        depth = v7(fmod(length,j,modulus))
        hist[depth] += 1
        parity['odd' if j % 2 else 'even'][depth] += 1
        if depth > max_depth:
            max_depth, maxima = depth, []
        if depth == max_depth:
            maxima.append(str(j))
        digest.update(f'{j}:{depth}\n'.encode())
    require(max_depth == k and max_depth < length-2, 'whole-length depth maximum')
    expected = {4:1} if p == 17 else {0:7499,2:6427,3:918,4:131,5:19,6:2,7:1}
    require(dict(hist) == expected, 'unexpected valuation histogram')
    require((lo,hi) == ((0,0) if p == 17 else (-6195,8801)), 'signed endpoint control')
    return {'a':a,'p':p,'b':b,'k':k,'S':str(s),'L':str(length),'i':str(position),
            'order_prime_certificate':base_certificate,
            'order_lift':{'mod_p_squared':str(lift_residue),
                          'coefficient_after_division_by_p':(lift_residue-1)//p,
                          'certificate_at_power_b':lifted_certificate},
            'order_S_certificate':s_certificate,'d':str(d),
            'least_sum_class_residue':str(position % d),
            'signed_h_min':lo,'signed_h_max':hi,'positions':hi-lo+1,
            'first_position':str(first),'last_position':str(last),
            'previous_position':str(first-d),'next_position':str(last+d),
            'F_mod_225S7k':0,'F_mod_7_to_k_plus_1':next_residue,
            'interval_margins':{'100i_minus_41L':str(100*position-41*length),
                                '42L_minus_100i':str(42*length-100*position)},
            'valuation_histogram':dict(sorted(hist.items())),
            'parity_histograms':{t:dict(sorted(v.items())) for t,v in parity.items()},
            'maximum_depth':max_depth,'maximal_positions':maxima,
            'valuation_precision':12,'ordered_position_depth_sha256':digest.hexdigest(),
            'whole_length_excluded':True}


def run():
    source = Path(__file__).resolve().parent.parent/'fixed-depth'/'SUBMISSION.txt'
    positions = [int(x) for x in re.findall(r'^\d{100,}$', source.read_text(), re.M)]
    require(len(positions) == 2, 'expected exactly two supplied appendix positions')
    return {'status':'passed','base_commit':'022e8120d0af98030b60bdda117b45fbfdba0543',
            'submission_sha256':sha256(source.read_bytes()).hexdigest(),
            'literal_checks':small_literal_checks(),'depth_one_controls':grid_controls(),
            'examples':[example(164,17,41,4,positions[0]),
                        example(103,898129,21,7,positions[1])],
            'scope':'Two complete isolated lengths; finite controls do not prove density.'}


if __name__ == '__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
