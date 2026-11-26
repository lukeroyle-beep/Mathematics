#!/usr/bin/env python3
"""Independent exact arithmetic on the retained archive; no project imports.

Does not rerun either complete enumeration and does not certify omitted pairs.
Run from any directory. All checks remain enabled under python -O.
"""
import csv
import hashlib
import io
import json
from collections import Counter
from math import prod
from pathlib import Path
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE.parent / 'prime-sum/evidence/trillion-evidence.zip'
ZIP_HASH = 'b657f158d6362c77c570b87c3c193fe54c6f3c385889379edf5bf79b71f05c0a'
CSV_HASH = '919c091c978ee1e6011f9239fadbba675985714f286d8dcffa1a29ed043cf8e4'
PREFIX = 'A398769-research/'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sevens(length, modulus):
    """Return (value, decimal shift) of a repeated-seven word, by doubling.

    Appending word b to a has value a.value*b.shift+b.value. Neither
    division by 9 nor any inverse is used, including when 3 divides modulus.
    """
    value, shift = 0, 1
    block, power = 7 % modulus, 10 % modulus
    while length:
        if length & 1:
            value = (value * power + block) % modulus
            shift = shift * power % modulus
        block = block * (power + 1) % modulus
        power = power * power % modulus
        length //= 2
    return value, shift


def decimal_word_mod(L, i, modulus):
    prefix, _ = sevens(L - i - 1, modulus)
    middle, shift = sevens(i - 1, modulus)
    value = (10 * prefix + 5) % modulus
    value = (value * shift + middle) % modulus
    return (10 * value + 5) % modulus


def sparse_f_mod(L, i, modulus):
    return (7 * pow(10, L, modulus) - 18 * pow(10, i, modulus) - 25) % modulus


def literal_word(L, i):
    return '7' * (L - i - 1) + '5' + '7' * (i - 1) + '5'


def original_predicate(word):
    digits = list(map(int, word))
    return int(word) % (sum(digits) * prod(digits)) == 0


def controls():
    require(original_predicate('135'), 'nonzero original PS-divisor positive')
    require(not original_predicate('137'), 'original PS-divisor negative')
    comparisons = 0
    for L in range(5, 102, 2):
        for i in range(3, L):
            word = literal_word(L, i)
            n, S, P = int(word), sum(map(int, word)), prod(map(int, word))
            F = 7 * 10**L - 18 * 10**i - 25
            require((S, P, 9*n) == (7*L-4, 25*7**(L-2), F), 'literal identities')
            require(original_predicate(word) == (F % (225*S*7**(L-2)) == 0), 'full divisor')
            require(original_predicate(word) == (S % 5 != 0 and F % (9*S) == 0 and F % 7**(L-2) == 0), 'eligible equivalence')
            for modulus in (S, 9*S, 7**28, 125, 2, 3, 9, 27):
                require(decimal_word_mod(L, i, modulus) == n % modulus, 'word concatenation control')
                require(sparse_f_mod(L, i, modulus) == 9*n % modulus, 'sparse formula control')
                comparisons += 1
    positive = []
    # Composite S=423=9*47, plus prime S=1151; neither is a full witness.
    for L, i in ((61, 57), (165, 33)):
        S = 7*L-4
        n = int(literal_word(L, i))
        require(n % S == 0 and sparse_f_mod(L, i, 9*S) == 0, 'full digit-sum positive')
        require(not original_predicate(literal_word(L, i)), 'sum positive is not witness')
        positive.append({'L': L, 'i': i, 'S': S, 'n_mod_S': n % S,
                         'F_mod_9S': sparse_f_mod(L, i, 9*S)})
    L, i = 313, 51
    S = 7*L-4
    n = int(literal_word(L, i))
    require(S == 3**7 and S % 5 != 0, 'factor-nine eligible control')
    require(sparse_f_mod(L, i, S) == 0 and n % S != 0, 'lost factor-nine negative')
    require(sparse_f_mod(L, i, 9*S) == 9 * (n % S), 'exact factor-nine residue')
    return {'original_PS_positive': 135, 'original_PS_negative': 137,
            'literal_modular_comparisons': comparisons,
            'full_digit_sum_positives': positive,
            'factor_nine_negative': {'L': L, 'i': i, 'S': S,
                                    'F_mod_S': sparse_f_mod(L, i, S),
                                    'n_mod_S': n % S,
                                    'F_mod_9S': sparse_f_mod(L, i, 9*S)}}


def read_pairs():
    data = ARCHIVE.read_bytes()
    require(digest(data) == ZIP_HASH, 'archive SHA-256')
    with ZipFile(io.BytesIO(data)) as z:
        require(z.testzip() is None, 'archive CRC')
        names = z.namelist()
        require(len(names) == len(set(names)) == 28, 'archive member uniqueness/count')
        manifest_name = PREFIX + 'SHA256SUMS.txt'
        seen = set()
        for line in z.read(manifest_name).decode().splitlines():
            expected, relative = line.split(maxsplit=1)
            name = PREFIX + relative
            require(name not in seen and digest(z.read(name)) == expected, 'manifest member hash')
            seen.add(name)
        require(seen | {manifest_name} == set(names), 'complete manifest coverage')
        raw = z.read(PREFIX + 'valuation/candidates.csv')
    require(digest(raw) == CSV_HASH, 'canonical candidate CSV SHA-256')
    rows = list(csv.reader(io.StringIO(raw.decode('ascii'))))
    require(all(len(row) == 2 for row in rows), 'CSV arity')
    pairs = [tuple(map(int, row)) for row in rows]
    require(len(pairs) == len(set(pairs)) == 74601, 'retained-pair uniqueness/count')
    require(pairs == sorted(pairs), 'canonical ordering')
    return pairs, len(data), len(seen)


def inherited_bindings():
    result = {}
    for name in ('prime-sum', 'trillion-witness'):
        directory = HERE.parent / name
        raw = (directory / 'verification.json').read_bytes()
        manifest = json.loads(raw)['artifact_sha256']
        for relative, expected in manifest.items():
            require(digest((directory / relative).read_bytes()) == expected,
                    'inherited artifact binding: ' + name + '/' + relative)
        result[name] = {'manifest_sha256': digest(raw),
                        'artifact_bindings_verified': len(manifest),
                        'underlying_search_rerun': False}
    return result


def main():
    bindings = inherited_bindings()
    control_receipt = controls()
    pairs, archive_bytes, manifest_members = read_pairs()
    histogram, counts = Counter(), Counter()
    sum_passes, exact27 = [], []
    residue_digest = hashlib.sha256()
    modulus = 7**28
    for L, i in pairs:
        require(5 <= L <= 10**12 and L % 2 == 1 and 3 <= i < L and i % 6 == 3, 'pair domain')
        S = 7*L - 4
        # Original decimal word and sparse expression are evaluated separately.
        n_sum = decimal_word_mod(L, i, S)
        f_sum = sparse_f_mod(L, i, 9*S)
        require(f_sum == 9*n_sum, 'same-pair full sum cross-check')
        counts['S_divisible_by_3'] += S % 3 == 0
        counts['S_divisible_by_5'] += S % 5 == 0
        counts['eligible_5_not_dividing_S'] += S % 5 != 0
        counts['weaker_F_mod_S_zero'] += f_sum % S == 0
        if n_sum == 0:
            sum_passes.append([L, i])
        n7 = decimal_word_mod(L, i, modulus)
        f7 = sparse_f_mod(L, i, modulus)
        require(f7 == 9*n7 % modulus and n7 != 0, 'seven-adic independent word check')
        t, reduced = 0, n7
        while reduced % 7 == 0:
            t += 1
            reduced //= 7
        require(22 <= t < 28, 'retained depth and exactness')
        require(t < L-2, 'full-witness rejection at actual exponent')
        histogram[t] += 1
        residue_digest.update(f'{L},{i},{n_sum},{f_sum},{t},{reduced % 7}\n'.encode('ascii'))
        if t == 27:
            exact27.append({'L': L, 'i': i, 'n_mod_S': n_sum,
                            'F_mod_9S': f_sum, 'n_div_7t_mod7': reduced % 7,
                            'F_div_7t_mod7': (f7 // 7**t) % 7})
    require(not sum_passes, 'reported zero digit-sum passes independently confirmed')
    receipt = {'status': 'PASS', 'archive_sha256': ZIP_HASH,
               'archive_bytes': archive_bytes, 'manifest_members_verified': manifest_members,
               'inherited_bindings': bindings,
               'candidate_csv_sha256': CSV_HASH, 'retained_pairs': len(pairs),
               'domain_max_L_inclusive': 10**12,
               'full_digit_sum_passes': sum_passes, 'full_digit_sum_pass_count': len(sum_passes),
               'counts': dict(sorted(counts.items())),
               'exact_valuation_histogram': dict(sorted(histogram.items())),
               'valuation_27_pairs': exact27, 'controls': control_receipt,
               'arithmetic_rows_sha256': residue_digest.hexdigest(),
               'complete_enumerations_rerun': False,
               'omitted_pair_depth_below_22': 'INHERITED_PR22',
               'coverage_through_1000002000000': 'INHERITED_PR22_PLUS_PR21',
               'new_global_bound': None, 'new_lengths_excluded': 0}
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
