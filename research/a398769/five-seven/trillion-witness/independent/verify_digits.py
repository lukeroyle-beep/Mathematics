#!/usr/bin/env python3
"""Independent original-digit checks; standard library only, no discovery imports."""
import argparse
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def concatenate(left, right, modulus):
    """Represent a decimal block by (10**length mod modulus, value mod modulus)."""
    p, v = left
    q, w = right
    return p*q % modulus, (v*q+w) % modulus


def repeat_digit(digit, count, modulus):
    require(type(digit) is int and 0 <= digit <= 9, 'bad digit')
    require(type(count) is int and count >= 0, 'bad repetition count')
    require(type(modulus) is int and modulus > 0, 'bad modulus')
    value = (1 % modulus, 0)
    block = (10 % modulus, digit % modulus)
    while count:
        if count & 1:
            value = concatenate(value, block, modulus)
        block = concatenate(block, block, modulus)
        count //= 2
    return value


def runs_for_pair(length, position):
    require(type(length) is int and type(position) is int, 'integers required')
    require(length >= 5 and length % 2 == 1 and 3 <= position < length,
            'require odd L >= 5 and 3 <= i < L')
    return [(7, length-position-1), (5, 1), (7, position-1), (5, 1)]


def describe(runs):
    length = sum(count for _, count in runs)
    total = sum(digit*count for digit, count in runs)
    counts = {}
    positions = []
    cursor = 0
    for digit, count in reversed(runs):
        counts[digit] = counts.get(digit, 0)+count
        if digit == 5:
            require(count == 1, 'each five must be a singleton block')
            positions.append(cursor)
        cursor += count
    require(counts.get(5) == 2 and set(counts) == {5, 7}, 'bad digit counts')
    return {'length': length, 'digit_sum': total,
            'digit_counts': {'5': counts[5], '7': counts[7]},
            'digit_product': {'coefficient': 5**counts[5], 'base': 7,
                              'exponent': counts[7]},
            'five_positions_from_units': positions,
            'decimal_runs_most_significant_first':
                [{'digit': d, 'count': c} for d, c in runs]}


def original_residue(runs, modulus):
    value = (1 % modulus, 0)
    for digit, count in runs:
        value = concatenate(value, repeat_digit(digit, count, modulus), modulus)
    return value[1]


def order_depth(length):
    depth, order = 1, 6
    while order <= length:
        depth += 1
        order *= 7
    return depth


def seven_certificate(runs, limit):
    require(type(limit) is int and 1 <= limit <= 100000, 'depth limit must be 1..100000')
    stages = []
    depth = 1
    while True:
        residue = original_residue(runs, 7**depth)
        stages.append({'exponent': depth, 'n_residue': residue})
        if residue:
            valuation = 0
            while residue % 7 == 0:
                residue //= 7
                valuation += 1
            failure_modulus = 7**(valuation+1)
            failure_residue = original_residue(runs, failure_modulus)
            require(failure_residue != 0 and failure_residue % (7**valuation) == 0,
                    'inconsistent first failed power')
            return {'kind': 'exact_valuation', 'greatest_certified_depth': valuation,
                    'first_failed_exponent': valuation+1,
                    'n_mod_first_failed_power': failure_residue,
                    'stages': stages}
        if depth == limit:
            return {'kind': 'lower_bound', 'greatest_certified_depth': depth,
                    'first_failed_exponent': None, 'stages': stages}
        depth = min(depth*2, limit)


def verify(length, position, max_depth=256):
    runs = runs_for_pair(length, position)
    record = describe(runs)
    require(record['length'] == length and
            record['five_positions_from_units'] == [0, position], 'run reconstruction')
    total = record['digit_sum']
    sum_residue = original_residue(runs, total)
    five_residue = original_residue(runs, 125)
    require(five_residue % 25 == 0 and five_residue != 0, 'expected exactly two factors of five')
    needed = record['digit_product']['exponent']
    require(type(max_depth) is int and 1 <= max_depth <= 100000, 'depth limit must be 1..100000')
    certificate = seven_certificate(runs, min(max_depth, needed))
    lower_depth = certificate['greatest_certified_depth']
    sum_pass = sum_residue == 0
    five_filter_pass = total % 5 != 0
    if not sum_pass or not five_filter_pass or certificate['kind'] == 'exact_valuation':
        verdict = 'REJECTED'
    elif lower_depth >= needed:
        verdict = 'VERIFIED WITNESS'
    else:
        verdict = 'CANDIDATE AWAITING FULL VERIFICATION'
    record.update({'input_pair': [length, position], 'verdict': verdict,
                   'above_trillion': length > 10**12,
                   'K': order_depth(length), 'n_mod_digit_sum': sum_residue,
                   'nine_n_mod_nine_digit_sum': 9*sum_residue,
                   'digit_sum_pass': sum_pass, 'five_not_dividing_sum': five_filter_pass,
                   'n_mod_125': five_residue, 'exact_v5': 2,
                   'seven': certificate, 'required_seven_depth': needed,
                   'outstanding_seven_exponents':
                       [lower_depth+1, needed] if certificate['kind'] == 'lower_bound' and lower_depth < needed else [],
                   'full_seven_condition_proved': lower_depth >= needed})
    return record


def self_test():
    comparisons = 0
    positive_sum = []
    factor_nine = []
    largest_valuation = None
    for length in range(5, 66, 2):
        for position in range(3, length):
            word = '7'*(length-position-1)+'5'+'7'*(position-1)+'5'
            number = int(word)
            total = sum(map(int, word))
            product = 1
            for digit in word:
                product *= int(digit)
            runs = runs_for_pair(length, position)
            record = describe(runs)
            require(record['digit_sum'] == total, 'literal sum')
            require(record['digit_product']['coefficient'] *
                    record['digit_product']['base']**record['digit_product']['exponent']
                    == product, 'literal product')
            require(record['five_positions_from_units'] ==
                    [j for j, d in enumerate(reversed(word)) if d == '5'], 'literal positions')
            for modulus in (1, 3, 9, 25, 125, total, 9*total, 7, 49, 343, 7**8, product*total):
                require(original_residue(runs, modulus) == number % modulus, 'literal residue')
                comparisons += 1
            checked = verify(length, position, max_depth=64)
            depth = 0
            quotient = number
            while quotient % 7 == 0:
                quotient //= 7
                depth += 1
            require(checked['seven']['kind'] == 'exact_valuation', 'small control rejected before cap')
            require(checked['seven']['greatest_certified_depth'] == depth, 'literal seven valuation')
            require((checked['verdict'] == 'VERIFIED WITNESS') == (number % (product*total) == 0),
                    'literal original predicate')
            if not largest_valuation or depth > largest_valuation['depth']:
                largest_valuation = {'L': length, 'i': position, 'depth': depth}
            if number % total == 0 and len(positive_sum) < 5:
                positive_sum.append({'L': length, 'i': position, 'n': number,
                                     'S': total, 'v7': depth, 'S_divisible_by_3': total % 3 == 0})
            if (9*number) % total == 0 and number % total != 0 and len(factor_nine) < 5:
                factor_nine.append({'L': length, 'i': position, 'n': number,
                                    'S': total, 'n_mod_S': number % total})
    # Reduced-domain control: 3|i, i odd, and 5 does not divide S.
    length, position = 313, 51
    word = '7'*(length-position-1)+'5'+'7'*(position-1)+'5'
    number = int(word)
    total = sum(map(int, word))
    require((9*number) % total == 0 and number % total != 0 and total % 5 != 0,
            'targeted factor-nine trap')
    checked = verify(length, position)
    require(not checked['digit_sum_pass'] and checked['n_mod_digit_sum'] == number % total,
            'factor-nine trap independently rejected')
    factor_nine.append({'L': length, 'i': position, 'S': total,
                        'n_mod_S': number % total, 'nine_n_mod_S': 9*number % total,
                        'nine_n_mod_nine_S': 9*number % (9*total)})
    require(bool(positive_sum), 'nonzero sum-compatible controls required')
    require(bool(factor_nine), 'factor-nine negative controls required')
    positive = verify(61, 57)
    require(positive['digit_sum_pass'] and positive['five_not_dividing_sum'] and
            positive['seven']['greatest_certified_depth'] == 1, 'reduced-domain positive sum control')
    capped = verify(61, 57, 1)
    require(capped['verdict'] == 'CANDIDATE AWAITING FULL VERIFICATION' and
            capped['outstanding_seven_exponents'] == [2, 59], 'cap must not imply witness')
    positive_sum.append({'L': 61, 'i': 57, 'S': positive['digit_sum'],
                        'v7': 1, 'S_divisible_by_3': True, 'five_not_dividing_sum': True})
    rejected = 0
    for pair in [(4, 3), (5, 2), (5, 5), (5.0, 3)]:
        try:
            verify(*pair)
        except ValueError:
            rejected += 1
    require(rejected == 4, 'invalid pair guard count')
    # A tiny cap must remain explicitly incomplete for a sum-compatible control,
    # if such a control passes one seven-adic power; otherwise check the helper.
    lower = seven_certificate(runs_for_pair(39, 3), 1)
    require(lower['kind'] == 'lower_bound' and lower['greatest_certified_depth'] == 1,
            'bounded certificate scope')
    return {'status': 'PASS', 'literal_lengths_inclusive': [5, 65],
            'literal_length_step': 2, 'literal_modulus_comparisons': comparisons,
            'positive_digit_sum_controls': positive_sum,
            'factor_nine_negative_controls': factor_nine,
            'largest_literal_valuation': largest_valuation,
            'invalid_inputs_rejected': rejected, 'bounded_depth_control': lower,
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pair', nargs=2, type=int, action='append', metavar=('L', 'i'))
    parser.add_argument('--pairs-json', type=Path,
                        help='JSON list of [L,i] only; no claimed residues accepted')
    parser.add_argument('--max-depth', type=int, default=256)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        require(not args.pair and args.pairs_json is None, 'self-test takes no pair input')
        result = self_test()
    else:
        pairs = args.pair or []
        if args.pairs_json is not None:
            loaded = json.loads(args.pairs_json.read_text())
            require(type(loaded) is list, 'pair file must be a JSON list')
            for pair in loaded:
                require(type(pair) is list and len(pair) == 2, 'each input must be [L,i] only')
            pairs += loaded
        require(bool(pairs), 'supply --pair or --pairs-json or --self-test')
        result = {'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'verification_method': 'original_decimal_block_concatenation',
                  'max_depth': args.max_depth,
                  'pairs': [verify(*pair, max_depth=args.max_depth) for pair in pairs]}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
