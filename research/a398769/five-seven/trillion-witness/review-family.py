#!/usr/bin/env python3
"""Independent complete class/count audit of the 32 family lengths.

No discovery code is imported. Full-sum residues concatenate original
decimal blocks. Seven-adic classes are lifted from the sum class itself,
not by a separately computed logarithm followed by the discovery CRT.
"""
import hashlib
import json
from math import gcd, lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise ValueError(message)


def original_word(L, i, modulus):
    require(L >= 5 and 3 <= i < L, 'original word domain')
    value = 0
    for digit, count in ((7, L-i-1), (5, 1), (7, i-1), (5, 1)):
        # The power residue is 1 modulo 9, so this is exact integer
        # division. It evaluates this run, not the discovery F formula.
        residue = pow(10, count, 9*modulus)
        run = digit*((residue-1)//9) % modulus
        value = (value*(residue % modulus)+run) % modulus
    return value


def small_seven_word(L, i, k):
    """Same original word; reduce run lengths by its proved monoid period."""
    modulus = 7**k
    period = 6*7**(k-1)
    # i can be an unbounded exponent class; take a congruent actual
    # position so every evaluated word still has two distinct fives.
    i = 3+(i-3) % period
    require(i < L, 'bounded surrogate original position')
    value = 0
    for digit, count in ((7, L-i-1), (5, 1), (7, i-1), (5, 1)):
        residue = pow(10, count % period, 9*modulus)
        value = (value*(residue % modulus)+digit*((residue-1)//9)) % modulus
    return value


def count_class(r, modulus, L):
    return (L-1-r)//modulus - (2-r)//modulus


def main():
    path = HERE/'families/results.json'
    raw = path.read_bytes()
    data = json.loads(raw)
    source = HERE/'families/search_families.py'
    require(data['source_sha256'] == hashlib.sha256(source.read_bytes()).hexdigest(),
            'receipt source identity')
    require(data['first_t'] == 0 and data['last_t'] == 31, 'fixed reviewed endpoints')
    require(len(data['rows']) == 32, 'every family parameter present')
    c, d = 898129, 56133
    require(gcd(c, 630) == 1 and d == 3**6*7*11, 'coprimality and order factors')
    require(pow(10, d, c) == 1 and all(pow(10, d//p, c) != 1 for p in (3, 7, 11)),
            'exact fixed order')
    require(pow(3, 210, 539) == 1 and 7*d == 3**6*539,
            'enlarged progression')
    # Fresh small original-word checks of this different run evaluator.
    small_checks = 0
    for L in range(5, 62, 2):
        for i in range(3, L):
            literal = int('7'*(L-i-1)+'5'+'7'*(i-1)+'5')
            for modulus in (7, 49, 125, 2187, 9*(7*L-4)):
                require(original_word(L, i, modulus) == literal % modulus, 'literal run oracle')
                small_checks += 1
    # Run monoid period: 10^T=1 mod 7^k and 9 is invertible there.
    # Checking mod 9*7^k avoids invoking any cancellation in code.
    for k in range(1, 13):
        require(pow(10, 6*7**(k-1), 9*7**k) == 1, 'run monoid period')
    rows, histogram = [], {}
    previous_three_residue, previous_three_period = None, None
    nested_three_checks = 0
    for expected_t, row in enumerate(data['rows']):
        require(row['t'] == expected_t and row['a'] == 193+210*expected_t,
                'parameter coverage')
        a = row['a']
        S = c*3**a
        L = (S+4)//7
        require(S+4 == 7*L and L % 2 == 1 and L > 10**12 and S % 5,
                'derived family length')
        require(str(L) == row['L'] and str(S) == row['S'], 'receipt length/sum')
        W = 77*3**(a-2)
        r = int(row['sum_class_residue'])
        require(0 <= r < W and str(W) == row['sum_class_spacing'], 'sum class canonical')
        require(3 <= r < L and r % 729 == 402, 'original sum representative and overlap')
        require(original_word(L, r, S) == 0, 'original decimal full-sum condition')
        three_period = 3**(a-2)
        three_residue = r % three_period
        if previous_three_period is not None:
            require(three_residue % previous_three_period == previous_three_residue,
                    'universal nested three-adic class')
            nested_three_checks += 1
        previous_three_residue, previous_three_period = three_residue, three_period
        # Exact ord_S(10)=lcm(d,3^(a-2))=W by coprime factors and LTE.
        require(lcm(d, 3**(a-2)) == W, 'complete sum-class period')
        previous = count_class(r, W, L)
        require(previous == row['sum_compatible_positions'], 'complete sum position count')
        require(r == int(row['first_position']), 'first actual sum position')
        original_sum_count = previous
        depth_counts = []
        for expected_k, depth in enumerate(row['depths'], start=1):
            require(depth['depth'] == expected_k, 'no omitted depth')
            T = 6*7**(expected_k-1)
            newW = lcm(W, T)
            growth = newW//W
            hits = [r+j*W for j in range(growth)
                    if small_seven_word(L, r+j*W, expected_k) == 0]
            require(len(hits) == 1, 'unique lifted sum class')
            r, W = hits[0], newW
            require(0 <= r < W, 'canonical lifted class')
            number = count_class(r, W, L)
            require(number == depth['survivors'] and str(r) == depth['least_joint_residue']
                    and str(W) == depth['joint_spacing'], 'independent exact class/count')
            require(previous-number == depth['rejected_count']
                    and depth['rejected_at_exact_depth'] == expected_k-1, 'exact rejection count')
            require(int(depth['seven_residue']) % T == r % T
                    and depth['seven_period'] == T, 'separate seven log agrees')
            histogram[str(expected_k-1)] = histogram.get(str(expected_k-1), 0)+previous-number
            previous = number
            depth_counts.append(number)
        maximum = len(depth_counts)-1
        require(previous == 0 and maximum == row['maximum_depth'], 'empty terminal class')
        period, K = 6, 1
        while period <= L:
            period *= 7
            K += 1
        require(K == row['K'] and maximum < K < L-2, 'full-witness depth impossible')
        rows.append({'t': expected_t, 'a': a, 'K': K,
                     'sum_compatible_positions': original_sum_count,
                     'survivors_by_depth': depth_counts, 'maximum_exact_depth': maximum})
    total = sum(row['sum_compatible_positions'] for row in rows)
    require(total == data['total_sum_compatible_positions'] and histogram == data['exact_depth_histogram'],
            'global complete rejection accounting')
    print(json.dumps({
        'status': 'PASS', 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'family_receipt_sha256': hashlib.sha256(raw).hexdigest(),
        'discovery_source_sha256': data['source_sha256'],
        'imports_discovery_code': False,
        'full_sum_verification': 'original decimal blocks modulo S for all 32 least sum representatives',
        'class_verification': 'enumerate extensions of previous joint class, no CRT solver or logarithm imported',
        'literal_modular_checks': small_checks,
        'nested_three_adic_class_checks': nested_three_checks,
        'whole_lengths_independently_excluded': 32,
        'contiguous_length_interval': False,
        'total_sum_compatible_positions': total,
        'exact_depth_histogram': histogram, 'rows': rows,
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
