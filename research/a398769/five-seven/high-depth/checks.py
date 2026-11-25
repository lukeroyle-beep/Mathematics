#!/usr/bin/env python3
"""Bounded high-depth representative experiment; all checks survive python -O.

Standard library only. No inherited checker is imported. The experiment is
wholly inside the already certified interval and does not extend its coverage.
"""
from collections import Counter
from hashlib import sha256
from math import gcd
from pathlib import Path
import json


LIMIT = 100001
BASE = 'b6db8703afd3d32211fd75de9ce1e34440dddfe8'


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def fmod(length, position, modulus):
    require(length >= 1 and position >= 0 and modulus >= 1, 'fmod domain')
    return (7*pow(10, length, modulus)-18*pow(10, position, modulus)-25) % modulus


def first_large_period(length):
    require(length >= 1, 'K domain')
    k, period = 1, 6
    while period <= length:
        k += 1
        period *= 7
    require(period > length and (k == 1 or period//7 <= length), 'least K')
    return k, period


def lift(length, k, representative):
    """Return the unique digit a_k and representative at k+1, exactly."""
    modulus, period = 7**k, 6*7**(k-1)
    require(k >= 1 and 0 <= representative < period, 'lift domain')
    require(fmod(length, representative, modulus) == 0, 'input not root')
    next_modulus = 7*modulus
    order_residue = pow(10, period, next_modulus)
    require((order_residue-1) % modulus == 0, 'order precision')
    coefficient = (order_residue-1)//modulus
    require(coefficient % 7 != 0, 'order did not grow by seven')
    y = 18*pow(10, representative, next_modulus)
    target = 7*pow(10, length, next_modulus)-25
    require((target-y) % modulus == 0, 'lift division not exact')
    digit = ((target-y)//modulus)*pow(y*coefficient, -1, 7) % 7
    result = representative+digit*period
    require(0 <= digit < 7 and 0 <= result < 7*period, 'lift range')
    require(fmod(length, result, next_modulus) == 0, 'lift not root')
    return digit, result


def representative_at_k(length, k):
    require(k >= 1, 'representative depth')
    representative = 3
    require(fmod(length, representative, 7) == 0, 'initial root')
    for depth in range(1, k):
        _, representative = lift(length, depth, representative)
    return representative


def exact_depth(length, position, minimum):
    """Termination here is certified by a returned nonzero next residue."""
    depth = minimum
    require(fmod(length, position, 7**depth) == 0, 'claimed minimum depth')
    while fmod(length, position, 7**(depth+1)) == 0:
        depth += 1
        # A resource guard, not an exclusion: exhausting it fails the run.
        require(depth <= 64, 'experiment precision guard exhausted')
    return depth


def order_by_recurrence(modulus):
    require(gcd(modulus, 10) == 1, 'nonunit order')
    value, order = 10 % modulus, 1
    while value != 1:
        value = 10*value % modulus
        order += 1
        require(order <= modulus, 'order recurrence failed')
    return order


def valuation_seven(value):
    require(value > 0, 'valuation needs positive integer')
    exponent = 0
    while value % 7 == 0:
        value //= 7
        exponent += 1
    return exponent


def literal_checks():
    pairs = sum_pairs = triples = saturation_lengths = 0
    saturation_histogram = Counter()
    saturation_example = None
    for length in range(5, 202, 2):
        s = 7*length-4
        k, period = first_large_period(length)
        require(k <= length-2, 'K beyond witness threshold')
        r = representative_at_k(length, k)
        literal_at_k = []
        for position in range(3, length):
            digits = '7'*(length-position-1)+'5'+'7'*(position-1)+'5'
            n = int(digits)
            require(sum(map(int, digits)) == s, 'literal sum')
            product = 1
            for digit in digits:
                product *= int(digit)
            require(product == 25*7**(length-2), 'literal product')
            f = 7*10**length-18*10**position-25
            require(f == 9*n, 'literal decimal formula')
            require((n % s == 0) == (f % (9*s) == 0), 'full sum equivalence')
            require((n % (product*s) == 0)
                    == (f % (225*s*7**(length-2)) == 0), 'full divisor equivalence')
            if s % 5:
                require(n % 25 == 0 and gcd(25, s) == 1 and s % 7 != 0,
                        'separation coprimality')
                require((n % (product*s) == 0)
                        == (f % (9*s) == 0 and f % 7**(length-2) == 0),
                        'separated witness equivalence')
            else:
                require(n % 125 != 0, 'excluded five-dividing sum')
            if n % 7**k == 0:
                literal_at_k.append(position)
            for depth in range(1, min(4, length-2)+1):
                rr = representative_at_k(length, depth)
                require((n % 7**depth == 0)
                        == ((position-rr) % (6*7**(depth-1)) == 0), 'literal depth class')
                triples += 1
            pairs += 1
            sum_pairs += n % s == 0
        require(literal_at_k == ([r] if 3 <= r < length else []),
                'sole representative versus literal words')
        if gcd(s, 10) == 1:
            d = order_by_recurrence(s)
            e = valuation_seven(d)
            require(e < k, 'sum-order saturation inequality')
            saturation_lengths += 1
            saturation_histogram[e] += 1
            if saturation_example is None or e > saturation_example['v7_order']:
                saturation_example = {'L':length,'S':s,'order_S':d,
                                      'v7_order':e,'K':k}
    # A positive full-sum control with 3 | S, and a false positive if nine is lost.
    positive = {'L':13,'i':12,'S':87,'F_mod_9S':fmod(13,12,9*87)}
    negative = {'L':151,'i':8,'S':1053,'F_mod_S':fmod(151,8,1053),
                'F_mod_9S':fmod(151,8,9*1053)}
    require(positive['F_mod_9S'] == 0, 'positive full-nine control')
    require(negative['F_mod_S'] == 0 and negative['F_mod_9S'] == 8424,
            'loss-of-nine negative control')
    return {'odd_lengths_inclusive':[5,201],'all_positions':'3 <= i < L',
            'literal_pairs':pairs,'full_sum_pairs':sum_pairs,
            'depth_class_comparisons':triples,
            'sum_order_saturation_lengths':saturation_lengths,
            'sum_order_saturation_histogram':dict(sorted(saturation_histogram.items())),
            'largest_sum_order_seven_part_control':saturation_example,
            'three_divisible_positive':positive,'loss_of_nine_negative':negative}


def boundary_checks():
    rows = []
    for k in range(1, 9):
        period = 6*7**(k-1)
        require(first_large_period(period-1)[0] == k, 'left period endpoint')
        require(first_large_period(period)[0] == k+1, 'strict period endpoint')
        require(first_large_period(period+1)[0] == k+1, 'right period endpoint')
        rows.append({'k':k,'T':period,'K_at_T_minus_1':k,
                     'K_at_T':k+1,'K_at_T_plus_1':k+1})
    require(first_large_period(5) == (1,6), 'L=5 boundary')
    return rows


def order_checks():
    rows = []
    for k in range(1, 14):
        modulus, period = 7**k, 6*7**(k-1)
        primes = (2,3) if k == 1 else (2,3,7)
        residues = {str(p):pow(10,period//p,modulus) for p in primes}
        require(pow(10,period,modulus) == 1, 'period not an order')
        require(all(r != 1 for r in residues.values()), 'order not exact')
        rows.append({'k':k,'T':period,'proper_prime_divisor_residues':residues})
    return rows


def saturation_controls():
    rows = []
    for length, expected_order in ((13,28),(85,98),(589,686)):
        s = 7*length-4
        d = order_by_recurrence(s)
        e = valuation_seven(d)
        k, period = first_large_period(length)
        require(d == expected_order and e == k-1, 'sharp saturation control')
        rows.append({'L':length,'S':s,'order_S':d,'v7_order':e,
                     'K':k,'T_K':period,'attains_e_equals_K_minus_1':True})
    return rows


def bounded_experiment():
    counts = Counter({'actual_5_free_passing_full_sum':0})
    by_k, runs, depths = Counter(), Counter(), Counter()
    digest = sha256()
    survivors = []
    best = best_five_free = None
    for length in range(5, LIMIT+1, 2):
        k, period = first_large_period(length)
        require(k <= length-2, 'K threshold')
        r = representative_at_k(length, k)
        by_k[k] += 1
        counts['odd_lengths'] += 1
        if not 3 <= r < length:
            counts['outside_actual_interval'] += 1
            digest.update(f'{length}:{k}:{r}:{period}:-:-\n'.encode('ascii'))
            continue
        s = 7*length-4
        depth = exact_depth(length, r, k)
        residue = fmod(length, r, 9*s)
        digest.update(f'{length}:{k}:{r}:{period}:{depth}:{residue}\n'.encode('ascii'))
        counts['actual_representatives'] += 1
        runs[depth-k] += 1
        depths[depth] += 1
        for level in range(k, depth):
            digit, rr = lift(length, level, r)
            require(digit == 0 and rr == r, 'zero-run correspondence')
        digit, rr = lift(length, depth, r)
        require(digit != 0 and rr >= length, 'escape correspondence')
        require(depth <= length-3, 'bounded experiment reached witness threshold')
        row = {'L':length,'i':r,'K':k,'T_K':period,'depth':depth,
               'zero_lifts_after_K':depth-k,'first_nonzero_lift_index':depth,
               'first_nonzero_lift_digit':digit,'escaped_representative':rr,
               'F_mod_9S':residue,'F_mod_7_to_depth_plus_1':fmod(length,r,7**(depth+1))}
        if best is None or depth-k > best['zero_lifts_after_K']:
            best = row
        if s % 5 and (best_five_free is None
                         or depth-k > best_five_free['zero_lifts_after_K']):
            best_five_free = row
        if s % 5 == 0:
            counts['actual_with_5_dividing_S'] += 1
        elif residue:
            counts['actual_5_free_failing_full_sum'] += 1
        else:
            counts['actual_5_free_passing_full_sum'] += 1
            survivors.append(row)
    require(counts['odd_lengths'] == 49999, 'odd-length coverage endpoints')
    require(sum(by_k.values()) == counts['odd_lengths'], 'K coverage')
    require(counts['outside_actual_interval']+counts['actual_representatives']
            == counts['odd_lengths'], 'actual coverage')
    require(sum(runs.values()) == counts['actual_representatives'], 'zero-run coverage')
    require(sum(counts[name] for name in ('actual_with_5_dividing_S',
            'actual_5_free_failing_full_sum','actual_5_free_passing_full_sum'))
            == counts['actual_representatives'], 'sum coverage')
    return {'odd_lengths_inclusive':[5,LIMIT],
            'counts':dict(sorted(counts.items())),
            'lengths_by_K':dict(sorted(by_k.items())),
            'all_actual_zero_run_histogram':dict(sorted(runs.items())),
            'all_actual_depth_histogram':dict(sorted(depths.items())),
            'full_sum_survivors':survivors,'longest_zero_run_control':best,
            'longest_5_free_zero_run_control':best_five_free,
            'ordered_length_representative_sha256':digest.hexdigest(),
            'digest_format':'ASCII L:K:r_K:T_K:depth:F_mod_9S\\n; last two fields - outside actual interval',
            'scope':'bounded diagnostic inside inherited coverage; no extension or all-length inference'}


def run():
    return {'status':'passed','base_commit':BASE,
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'boundary_checks':boundary_checks(),'order_checks':order_checks(),
            'literal_checks':literal_checks(),'saturation_controls':saturation_controls(),
            'bounded_experiment':bounded_experiment()}


if __name__ == '__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
