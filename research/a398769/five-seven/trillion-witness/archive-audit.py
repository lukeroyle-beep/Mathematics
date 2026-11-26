#!/usr/bin/env python3
"""Fresh original-decimal controls; imports no discovery or inherited checker.

The named trillion-length archive was unavailable. These are targeted controls
from current main, not a rerun or certification of either large finite range.
All modular evaluations concatenate runs, without F or division by nine.
"""
import hashlib
import json
from pathlib import Path


def require(value, message):
    if not value:
        raise ValueError(message)


def join(left, right, modulus):
    """(value, 10**length) for the concatenation of two decimal words."""
    x, p = left
    y, q = right
    return ((x * q + y) % modulus, p * q % modulus)


def run(digit, length, modulus):
    require(0 <= digit <= 9 and length >= 0 and modulus > 0, 'run domain')
    result, power = (0, 1 % modulus), (digit % modulus, 10 % modulus)
    while length:
        if length & 1:
            result = join(result, power, modulus)
        power = join(power, power, modulus)
        length //= 2
    return result


def description(L, i):
    require(L % 2 == 1 and L >= 5 and 3 <= i < L, 'pair domain')
    return [(7, L-i-1), (5, 1), (7, i-1), (5, 1)]


def read_description(blocks):
    length = digit_sum = 0
    product = {}
    fives = []
    for digit, count in reversed(blocks):
        require(digit in (5, 7) and count >= 0, 'digit specification')
        if digit == 5:
            fives.extend(range(length, length+count))
        length += count
        digit_sum += digit * count
        product[digit] = product.get(digit, 0) + count
    return length, digit_sum, product, fives


def decimal_residue(blocks, modulus):
    value = (0, 1 % modulus)
    for digit, count in blocks:
        value = join(value, run(digit, count, modulus), modulus)
    return value[0]


def inspect_pair(L, i, cap=128):
    blocks = description(L, i)
    length, S, P, fives = read_description(blocks)
    require(length == L and fives == [0, i], 'derived positions and length')
    require(P == {5: 2, 7: L-2} and S == 7*L-4, 'derived sum and product')
    period, K = 6, 1
    while period <= length:
        period *= 7
        K += 1
    sum_residue = decimal_residue(blocks, S)
    modulus = 1
    depth = None
    for k in range(1, cap+1):
        modulus *= 7
        residue = decimal_residue(blocks, modulus)
        if residue:
            depth = k-1
            break
    require(depth is not None, 'control has not failed by configured cap')
    require(residue % (7**depth) == 0, 'exact valuation endpoint')
    require(decimal_residue(blocks, 125) == 25, 'exactly two factors of five')
    return {
        'L': length, 'i': i, 'blocks': blocks, 'five_positions': fives,
        'S': S, 'P_factorization': [[p, e] for p, e in sorted(P.items())],
        'K': K, 'n_mod_S': sum_residue,
        'F_mod_9S_derived_from_n': 9*sum_residue,
        'exact_v7_n': depth, 'first_failed_modulus': modulus,
        'n_mod_first_failed_modulus': residue,
        'F_mod_first_failed_modulus_derived_from_n': (9*residue) % modulus,
        'full_witness_rejected': depth < length-2 or sum_residue != 0,
    }


def main():
    literal_count = 0
    for L in range(5, 102, 2):
        for i in range(3, L):
            blocks = description(L, i)
            literal = int(''.join(str(d)*m for d, m in blocks))
            for modulus in (1, 7, 49, 125, 9*(7*L-4), 7**8):
                require(decimal_residue(blocks, modulus) == literal % modulus,
                        'literal decimal cross-check')
                literal_count += 1
    inputs = [
        ('retained_five_zero_lifts', 69489, 40323, 11),
        ('retained_sum_compatible_family',
         15582704697570091495948156638491914590405161120787807516829906317314612303918977615165179656913553,
         6477065490626893175017379503058848761317334778884442403179846853582090755525695000140054741394429, 4),
        ('retained_depth_44', 3955567925893426973231046645818352161,
         1648153302455594572179602769090980067, 44),
        ('retained_depth_56', 119370568731057982371060322997782242271333208681,
         49737736971274159321275134582409267613055503617, 56),
        ('retained_depth_85', 232355213189479324642841163179368518745758138259880936147570942319340913,
         96814672162283051934517151324736882810732557608283723394821225966392047, 85),
        ('retained_depth_92', 371682098545327426599885149975293409551010717126756268211295464073101642711793,
         154867541060553094416618812489705587312921132136148445088039776697125684463247, 92),
    ]
    controls = []
    for label, L, i, expected_depth in inputs:
        row = inspect_pair(L, i)
        require(row['exact_v7_n'] == expected_depth, 'retained depth claim')
        row['label'] = label
        controls.append(row)
    family = controls[1]
    require(family['n_mod_S'] == 0, 'nonzero full-sum positive control')
    blocks = description(family['L'], family['i'])
    require(decimal_residue(blocks, 25*7**4*family['S']) == 0,
            'joint sum and depth-four positive control')
    require(controls[0]['F_mod_9S_derived_from_n'] == 2218743,
            'retained zero-run sum rejection')
    for row in controls[2:]:
        require(row['K'] == row['exact_v7_n'] and row['n_mod_S'] != 0,
                'high-depth controls fail full sum')
    nine_control = inspect_pair(313, 51)
    require(nine_control['S'] == 2187 and nine_control['n_mod_S'] == 1944,
            'factor-nine negative control')
    require(nine_control['F_mod_9S_derived_from_n'] % nine_control['S'] == 0,
            'dropping nine would accept negative control')
    rejected_mutations = 0
    for check in (
        lambda: require(family['exact_v7_n'] >= family['L']-2, 'false full witness'),
        lambda: require(nine_control['n_mod_S'] == 0, 'dropped nine'),
        lambda: description(1000000000001, 1000000000001),
    ):
        try:
            check()
        except ValueError:
            rejected_mutations += 1
    require(rejected_mutations == 3, 'negative controls exercised')
    family_counts = []
    for depth, bound in ((4, 154), (5, 22), (6, 4), (7, 1)):
        denominator = 154*7**(depth-1)
        require(9*898129+1 < bound*denominator, 'uniform class count bound')
        family_counts.append({'depth': depth, 'at_most_actual_positions': bound,
                              'ratio_upper_numerator': 9*898129+1,
                              'ratio_upper_denominator': denominator})
    print(json.dumps({
        'status': 'PASS', 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'method': 'binary concatenation monoid of original decimal runs',
        'uses_F_formula': False, 'imports_discovery_code': False,
        'literal_modular_comparisons': literal_count,
        'controls': controls, 'factor_nine_control': nine_control,
        'rejected_mutations': rejected_mutations,
        'fixed_family_class_count_bounds': family_counts,
        'named_trillion_attachments_found': [],
        'named_attachment_search_locations': [
            '/Users/lukesmacminim41/Documents/ChatGPT/Mathematics',
            '/Users/lukesmacminim41/Downloads'],
        'archive_controls_rerun': False,
        'large_exhaustive_searches_rerun': False,
        'new_contiguous_coverage': [],
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
