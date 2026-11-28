#!/usr/bin/env python3
"""Exact q^61>L^20 corollary and all 259 inherited finite exclusions."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
INPUTS = (
    'power-three/individuals.json',
    'power-three/individuals-independent.json',
    'power-three-pair/root-log.json',
    'power-three-pair/individual.json',
    'power-three-individual/root_log.json',
    'power-three-individual/independent_decimal.json',
)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def repeated_sevens(length, modulus):
    """Return (10^length, value of length sevens) by concatenation."""
    need(length >= 0 and modulus > 0, 'valid decimal block')
    scale, value = 1, 0
    block_scale, block_value = 10 % modulus, 7 % modulus
    while length:
        if length & 1:
            value = (value * block_scale + block_value) % modulus
            scale = scale * block_scale % modulus
        block_value = block_value * (block_scale + 1) % modulus
        block_scale = block_scale * block_scale % modulus
        length //= 2
    return scale, value


def decimal_word_mod(L, s, modulus):
    """Build 7...(L-s-1 times)...75...7(s-1 times)...75."""
    need(3 <= s < L, 'actual original decimal word')
    _, left = repeated_sevens(L-s-1, modulus)
    scale, middle = repeated_sevens(s-1, modulus)
    return (((left*10+5)*scale+middle)*10+5) % modulus


def sparse_F(L, s, modulus):
    return (7*pow(10, L, modulus)-18*pow(10, s, modulus)-25) % modulus


def run():
    first_left = 3**1585
    first_right = 7*(624000*1605**2)**61
    second_left = 3*1605**122
    second_right = 1606**122
    need(first_left > first_right, 'strict crossover at a=1585')
    need(second_left > second_right, 'strict induction ratio')
    # Independently rearranged comparison, preserving all integer factors.
    need(first_right == 7*624000**61*1605**122, 'crossover exponent arithmetic')
    need((3**1585+4)//7 > (624000*1605**2)**61, 'strict length crossover')

    data = [json.loads((BASE/name).read_text()) for name in INPUTS]
    left = data[0]['cases'] + [data[2]['case']]
    right = data[1]['cases'] + [data[3]['new_a1567']]
    left += [r for r in data[4]['cases'] if r['a'] in (1573, 1579)]
    right += [r for r in data[5]['rows'] if r['a'] in (1573, 1579)]
    expected = list(range(31, 1585, 6))
    need([r['a'] for r in left] == [r['a'] for r in right] == expected,
         'exact 259 ordered exponents below cutoff')
    need(len(expected) == 259 and expected[-1]+6 == 1585, 'finite endpoint')
    fields = ('a', 'L', 's', 'i', 't', 'first_fail_depth', 'first_fail_n_residue')

    literal_count = 0
    for L in range(4, 25):
        for s in range(3, L):
            text = '7'*(L-s-1)+'5'+'7'*(s-1)+'5'
            n = int(text)
            for modulus in (49, 343, 25*(7*L-4), 9*(7*L-4)):
                need(decimal_word_mod(L, s, modulus) == n % modulus,
                     'literal original-word block control')
            need(sum(map(int, text)) == 7*L-4, 'literal sum control')
            need(9*n == 7*10**L-18*10**s-25, 'literal sparse identity')
            literal_count += 1

    rows = []
    histogram = Counter()
    misses = 0
    for old, independent in zip(left, right):
        a, L, s = old['a'], old['L'], old['s']
        need(all(old[key] == independent[key] for key in fields),
             'independent inherited agreement at '+str(a))
        S, d = 3**a, 3**(a-2)
        need(7*L == S+4 and L > 4 and 2*d > L, 'family length')
        need(3 <= s < 2*d and s % 6 == 3, 'unique odd representative domain')
        need(sparse_F(L, s, 9*S) == 0, 'full same-position ternary condition')
        actual = s < L
        need((old['i'] is not None) == actual, 'recorded actuality')
        row = dict(a=a, actual=actual,
                   retained_pair_sha256=sha256(json.dumps(
                       {k: old[k] for k in fields}, sort_keys=True).encode()).hexdigest(),
                   F_mod_9S=0)
        if not actual:
            need(old['i'] is None and old['t'] is None and
                 old['first_fail_depth'] is None and old['first_fail_n_residue'] is None,
                 'class miss has no original-word valuation')
            row['verdict'] = 'unique joint class misses actual interval'
            misses += 1
        else:
            need(old['i'] == s, 'same actual position')
            t, depth, residue = (old['t'], old['first_fail_depth'],
                                 old['first_fail_n_residue'])
            need(type(t) is int and t >= 1 and depth == t+1 <= L-2,
                 'inclusive failure deadline')
            need(decimal_word_mod(L, s, 25*S) == 0, 'original word modulo 25S')
            seven_residues = []
            for m in range(1, depth+1):
                modulus = 7**m
                r = decimal_word_mod(L, s, modulus)
                need(9*r % modulus == sparse_F(L, s, modulus),
                     'decimal versus sparse seven residue')
                seven_residues.append(r)
            need(seven_residues == [0]*t+[residue] and
                 0 < residue < 7**depth and residue % 7**t == 0,
                 'exact valuation at actual position')
            row.update(t=t, first_fail_depth=depth,
                       first_fail_n_residue=residue, n_mod_25S=0,
                       verdict='original word fails full seven power')
            histogram[str(t)] += 1
        rows.append(row)
    need(misses == 85 and dict(histogram) == {'1':152, '2':18, '3':3, '4':1},
         'complete finite summary')
    base = next(row for row in rows if row['a'] == 31)
    deep = next(row for row in rows if row['a'] == 1231)
    need(base['t'] == 1 and base['first_fail_n_residue'] == 35, 'a31 base')
    need(deep['t'] == 4 and deep['first_fail_n_residue'] == 14406,
         'nonzero depth-four positive control')

    return dict(
        status='PASS', source_sha256=digest(Path(__file__)),
        proof_sha256=digest(HERE/'COROLLARY.md'),
        merged_valuation_proof_sha256=digest(BASE/'power-three-individual/COMMON_FACTOR.md'),
        inherited_sha256={name:digest(BASE/name) for name in INPUTS},
        statement='Every full family witness satisfies q^61 > L^20',
        valuation_bound_inherited='t < 312000*q^3*(a+20)^2',
        cutoff_a=1585,
        crossover_left=first_left, crossover_right=first_right,
        crossover_margin=first_left-first_right,
        induction_left=second_left, induction_right=second_right,
        induction_margin=second_left-second_right,
        finite_exponents=expected, finite_count=len(expected),
        finite_class_misses=misses, finite_actual_candidates=len(expected)-misses,
        finite_exact_valuation_histogram=dict(sorted(histogram.items())),
        finite_rows=rows, literal_word_controls=literal_count,
        finite_representatives='Inherited from paired receipts; freshly validated by 9S congruence and uniqueness domain',
        finite_arithmetic='Fresh original decimal-block residues and sparse F comparisons',
        large_enumeration_rerun=False, Lean_verification_performed=False,
        remaining_denominator_range='q^61 > L^20, including q=L',
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = run()
    if args.check:
        need(result == json.loads(args.check.read_text()), 'retained receipt matches fresh checks')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
