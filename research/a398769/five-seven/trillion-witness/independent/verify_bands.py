#!/usr/bin/env python3
"""Verify the specified 113 by 16 sampled bands independently from original digits."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from verify_digits import order_depth, repeat_digit, require, verify
from verify_stream import verify_order


def audit(path):
    evidence = json.loads(path.read_text())
    rows = evidence['rows']
    require(len(rows) == 113*16, 'wrong sampled-band count')
    categories, depths = Counter(), Counter()
    seen_orders = set()
    strongest = None
    actual_count = 0
    for offset, row in enumerate(rows):
        K, sample = divmod(offset, 16)
        K += 16
        lower = 6*7**(K-2)+1
        upper = 6*7**(K-1)-1
        length = lower+2*((upper-lower)*sample//30)
        require(row['K'] == K and row['band_sample'] == sample and row['L'] == length,
                'sample enumeration differs')
        require(order_depth(length) == K and length > 10**12, 'wrong length band')
        position = row['i']
        period = 6*7**(K-1)
        modulus = 7**K
        verify_order(K, seen_orders)
        require(type(position) is int and 0 <= position < period and period > length,
                'noncanonical exponent representative')
        all_sevens = repeat_digit(7, length, modulus)[1]
        require((all_sevens-2-2*pow(10, position, modulus)) % modulus == 0,
                'representative fails independently derived original-digit congruence')
        actual = 3 <= position < length
        require(type(row['actual']) is bool and row['actual'] == actual, 'actual flag incorrect')
        if not actual:
            require(row['category'] == 'outside', 'outside category incorrect')
        else:
            actual_count += 1
            checked = verify(length, position, max_depth=256)
            depth_record = checked['seven']
            require(depth_record['kind'] == 'exact_valuation', 'actual depth exceeds affordable certificate')
            depth = depth_record['greatest_certified_depth']
            require(depth >= K and depth < length-2, 'depth fails expected strict rejection')
            require(row['depth'] == depth, 'discovery depth differs from original digits')
            require(row['F_mod_9S'] == checked['nine_n_mod_nine_digit_sum'], 'sum residue differs')
            require(row['F_mod_7_next'] ==
                    (9*depth_record['n_mod_first_failed_power']) % 7**(depth+1),
                    'next seven-power residue differs')
            expected = 'five' if not checked['five_not_dividing_sum'] else (
                       'joint' if checked['digit_sum_pass'] else 'sum_fail')
            require(row['category'] == expected, 'actual category incorrect')
            depths[depth] += 1
            if strongest is None or depth > strongest['seven']['greatest_certified_depth']:
                strongest = checked
        categories[row['category']] += 1
    require(dict(categories) == evidence['categories'] or
            {k:v for k,v in evidence['categories'].items() if v} == dict(categories),
            'claimed category totals differ')
    return {'status': 'PASS', 'scope': {'K_first': 16, 'K_last': 128, 'samples_per_band': 16,
            'coverage_type': 'sampled_lengths_only'}, 'rows_checked': len(rows),
            'all_representative_congruences_independently_checked': len(rows),
            'original_digit_pairs_checked': actual_count, 'categories': dict(sorted(categories.items())),
            'exact_depth_histogram': dict(sorted(depths.items())), 'strongest_original_digit_check': strongest,
            'exact_order_depths_checked': sorted(seen_orders),
            'input_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'original_digit_verifier_sha256': hashlib.sha256(Path(__file__).with_name('verify_digits.py').read_bytes()).hexdigest(),
            'discovery_module_imported': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence', type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.evidence), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
