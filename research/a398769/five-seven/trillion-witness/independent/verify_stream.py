#!/usr/bin/env python3
"""Audit complete TSV/gzip certificates using independently derived original digits."""
import argparse
from collections import Counter
import csv
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

from verify_digits import (concatenate, describe, order_depth, original_residue,
                           repeat_digit, require, runs_for_pair)

HEADER = ['L', 'K', 'r', 'category', 'depth', 'F_mod_9S', 'F_mod_7_next', 'next_lift']


def verify_order(depth, seen):
    if depth in seen:
        return
    modulus = 7**depth
    order = 6*7**(depth-1)
    require(pow(10, order, modulus) == 1, 'claimed order not a period')
    for prime in [2, 3] + ([7] if depth > 1 else []):
        require(pow(10, order//prime, modulus) != 1, 'period not exact order')
    seen.add(depth)


def read_stream(path, start, stop):
    require(start >= 5 and start % 2 == 1 and stop >= start and stop % 2 == 1,
            'odd valid inclusive endpoints required')
    raw_hash = hashlib.sha256()
    reader_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    digit_hash = hashlib.sha256(Path(__file__).with_name('verify_digits.py').read_bytes()).hexdigest()
    categories, depths, lift_digits = Counter(), Counter(), Counter()
    seen_orders = set()
    reps = sum_pass = outside = 0
    maximum = None
    count = 0
    previous_length = previous_K = previous_sevens = None
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt', newline='') as source:
        header = source.readline()
        raw_hash.update(header.encode())
        require(header.rstrip('\n').split('\t') == HEADER, 'certificate header differs')
        for line in source:
            raw_hash.update(line.encode())
            fields = line.rstrip('\n').split('\t')
            require(len(fields) == len(HEADER), 'wrong row width')
            length, K, position = map(int, fields[:3])
            category = fields[3]
            expected_length = start+2*count
            require(length == expected_length and length <= stop, 'gap, duplicate or extra length')
            count += 1
            computed_K = order_depth(length)
            require(K == computed_K, 'wrong K')
            modulus = 7**K
            period = 6*7**(K-1)
            verify_order(K, seen_orders)
            require(0 <= position < period and period > length, 'representative outside canonical range')
            # The all-seven word is computed initially by concatenation, then
            # extended by the literal decimal suffix 77 at each next length.
            if previous_length is not None and previous_K == K:
                all_sevens = (100*previous_sevens+77) % modulus
            else:
                all_sevens = repeat_digit(7, length, modulus)[1]
            previous_length, previous_K, previous_sevens = length, K, all_sevens
            # Replacing the units and position-r digits subtracts 2 and 2*10^r.
            # For r outside the word this is only an exponent-congruence check.
            residue = (all_sevens-2-2*pow(10, position, modulus)) % modulus
            require(residue == 0, 'representative does not solve original-digit congruence')
            categories[category] += 1
            actual = 3 <= position < length
            if not actual:
                require(category == 'outside' and fields[4:] == ['-']*4,
                        'bad outside row')
                outside += 1
                continue
            require(category in ('five', 'sum_fail', 'joint'), 'bad actual category')
            reps += 1
            depth, claimed_sum, claimed_next, next_digit = map(int, fields[4:])
            require(K <= depth < length-2, 'exact rejecting depth does not reject full condition')
            require(1 <= next_digit <= 6, 'first nonzero lift digit must be 1..6')
            runs = runs_for_pair(length, position)
            derived = describe(runs)
            total = derived['digit_sum']
            require(derived['five_positions_from_units'] == [0, position], 'wrong original positions')
            sum_residue = original_residue(runs, total)
            require(claimed_sum == 9*sum_residue, 'sum residue differs from original number')
            expected_category = 'five' if total % 5 == 0 else ('sum_fail' if sum_residue else 'joint')
            require(category == expected_category, 'category differs from original divisor tests')
            sum_pass += sum_residue == 0
            next_modulus = 7**(depth+1)
            n_residue = original_residue(runs, next_modulus)
            require(n_residue != 0 and n_residue % (7**depth) == 0, 'incorrect exact seven valuation')
            require(claimed_next == (9*n_residue) % next_modulus, 'next-power residue differs')
            # Independently check all seven exponent lifts by replacing the
            # indicated digit of the all-seven polynomial. This is permitted
            # for exponents beyond the word only as a congruence check.
            next_period = 6*7**(depth-1)
            all_sevens_next = repeat_digit(7, length, next_modulus)[1]
            base_power = pow(10, position, next_modulus)
            jump = pow(10, next_period, next_modulus)
            hits = []
            for digit in range(7):
                if (all_sevens_next-2-2*base_power) % next_modulus == 0:
                    hits.append(digit)
                base_power = base_power*jump % next_modulus
            require(hits == [next_digit], 'wrong or nonunique nonzero lift')
            verify_order(depth+1, seen_orders)
            depths[depth] += 1
            lift_digits[next_digit] += 1
            if maximum is None or depth > maximum['depth']:
                maximum = {'L': length, 'i': position, 'depth': depth,
                           'n_mod_7_next': n_residue,
                           'nine_n_mod_7_next': claimed_next,
                           'n_mod_S': sum_residue, 'next_lift': next_digit}
            if count % 100000 == 0:
                print(f'checked {count} complete length rows', file=sys.stderr, flush=True)
    require(count == (stop-start)//2+1, 'truncated certificate')
    return {'status': 'PASS', 'start_odd_inclusive': start, 'stop_odd_inclusive': stop,
            'length_step': 2, 'rows_checked': count,
            'all_representative_congruences_independently_checked': count,
            'original_digit_pairs_checked': reps, 'outside_representatives': outside,
            'categories': dict(sorted(categories.items())),
            'exact_depth_histogram': dict(sorted(depths.items())),
            'first_nonzero_lift_histogram': dict(sorted(lift_digits.items())),
            'digit_sum_pass_including_five_rejections': sum_pass,
            'all_seven_lifts_checked_per_actual_pair': True,
            'maximum_exact_depth_example': maximum,
            'exact_order_depths_checked': sorted(seen_orders),
            'uncompressed_tsv_sha256': raw_hash.hexdigest(),
            'stream_verifier_sha256': reader_hash, 'original_digit_verifier_sha256': digit_hash,
            'discovery_module_imported': False,
            'scope': 'all odd lengths in the stated interval; even lengths excluded by parity'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--start', required=True, type=int)
    parser.add_argument('--stop', required=True, type=int)
    args = parser.parse_args()
    print(json.dumps(read_stream(args.certificate, args.start, args.stop), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
