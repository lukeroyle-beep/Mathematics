#!/usr/bin/env python3
"""Independent review arithmetic. No implementation imports; checks survive -O.

Repunit residues use pow(10,L,9*m), followed by exact division by nine.
This differs from archive_control.py's decimal-word concatenation.
The receipt's implementation_commit and bindings are read from Git when --commit
is supplied. No complete archive enumeration is rerun by this program.
"""
import argparse
import csv
from collections import Counter
from fractions import Fraction as Q
import hashlib
import io
import json
from math import prod
from pathlib import Path
import subprocess
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PREFIX = 'research/a398769/five-seven/explicit-length/'


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def hash_bytes(data):
    return hashlib.sha256(data).hexdigest()


def repunit_word(L, i, modulus):
    residue = pow(10, L, 9*modulus)
    require(residue % 9 == 1, 'repunit division precision')
    repunit = (residue-1)//9
    return (7*repunit-2-2*pow(10, i, modulus)) % modulus


def literal(L, i):
    return '7'*(L-i-1)+'5'+'7'*(i-1)+'5'


def valuation(value, p):
    require(value != 0, 'finite valuation input')
    t = 0
    while value % p == 0:
        value //= p
        t += 1
    return t, value % p


def polynomial(coefficients, x):
    total = 0
    for coefficient in reversed(coefficients):
        total = total*x+coefficient
    return total


def log_interval(x, terms=40):
    z = (x-1)/(x+1)
    require(0 <= z < 1, 'log series domain')
    lo = 2*sum((z**(2*j+1)/Q(2*j+1) for j in range(terms)), Q(0))
    hi = lo+2*z**(2*terms+1)/(Q(2*terms+1)*(1-z*z))
    return lo, hi


def arithmetic_controls():
    # Independent expanded polynomials, rather than copying implementation R.
    moving = [253, 756, 756, 16380, 100800, 153216, 68544]
    square = [253, 756, 756, 252, 0, 0, 504, 1008, 756, 504, 252]
    require(all(c >= 0 for c in moving+square), 'nonnegative coefficients')
    r15, r16 = polynomial(moving, 15), polynomial(moving, 16)
    r19, r20 = polynomial(square, 19), polynomial(square, 20)
    require(r15+2 == 902265864195, 'moving endpoint')
    require(6*7**13 < r15+2 < 1000002000000, 'moving prior band and B')
    require(r16+1 < 6*7**14, 'moving first excluded band')
    require(17**6 < 2*16**6, 'moving induction growth')
    require(r19+2 == 1721427606158403, 'square tightened endpoint')
    require(6*7**17 < r19+2, 'square prior band')
    require(r20+1 < 6*7**18, 'square first excluded band')
    require(6**10 < 7*5**10, 'square induction growth')

    lo2, hi2 = log_interval(Q(2))
    lo74, hi74 = log_interval(Q(7, 4))
    lo54, hi54 = log_interval(Q(5, 4))
    lo7, hi7 = lo74+2*lo2, hi74+2*hi2
    lo10, hi10 = lo54+3*lo2, hi54+3*hi2
    require(168*hi10**2 < 63*lo7**4, 'Bugeaud-Laurent coefficient')
    require(Q(3, 2) < lo7 < hi7 < 2, 'log7 enclosure')
    require(2 < lo10 < hi10 < Q(5, 2), 'log10 enclosure')
    require(Q(1, 2) < lo2 < hi2 < 1, 'log2 enclosure')
    require((8*30**6)**2*3**9 < 10**24, 'real logarithm coefficient')
    require(48**6*3*4*8 < 2*10**12, 'two-adic logarithm coefficient')
    require(12*10**12*43 < 10**16, 'real x endpoint')
    require(8*10**12*101 < 10**16, 'two-adic x endpoint')
    require(57*10**16 < 10**18, 'q0 cutoff constant')
    require(7**10 < 10**9, 'insufficient saving exponent')
    for m in range(1, 101):
        require(10+45*m+2*m*m <= 57*m*m, 'q0 polynomial endpoint')
    # General persistence is proved separately by
    # 57m^2-(10+45m+2m^2)=(m-1)(55m+10), not by the finite loop.

    cut = 444444444445
    require(1575*cut < 700000000000900 <= 1575*(cut+1), 'conditional strict cutoff')
    band = 3301587301587
    require(52*10**14-(1575*band-900) == 1375, 'decimal band end')
    require(52*10**14-(1575*(band+1)-900) == -200, 'decimal next band')
    return {'moving_R15': r15, 'moving_R16': r16, 'moving_U': r15+2,
            'square_R19': r19, 'square_R20': r20, 'square_U': r19+2,
            'q0_U0': 10**18-1, 'q0_U100': 10**18*101**2-1,
            'decimal_conditional_cutoff': cut, 'decimal_equivalence_band_end': band,
            'rational_log_checks': 'PASS'}


def literal_controls():
    require(135 % (prod(map(int, '135'))*sum(map(int, '135'))) == 0,
            'original predicate positive')
    require(137 % (prod(map(int, '137'))*sum(map(int, '137'))) != 0,
            'original predicate negative')
    checked, sum_passes, factor3_passes = 0, 0, 0
    for L in range(5, 202, 2):
        for i in range(3, L):
            word = literal(L, i)
            n, S, P = int(word), sum(map(int, word)), prod(map(int, word))
            F = 7*10**L-18*10**i-25
            require(9*n == F and S == 7*L-4 and P == 25*7**(L-2), 'literal reduction')
            for modulus in (S, 7**28, 27, 125):
                require(repunit_word(L, i, modulus) == n % modulus, 'literal modular control')
            original = n % (P*S) == 0
            require(original == (F % (225*S*7**(L-2)) == 0), 'exact full divisor')
            require(original == (S % 5 != 0 and n % S == 0 and n % 7**(L-2) == 0),
                    'eligible threshold')
            if S % 5 != 0 and n % S == 0:
                sum_passes += 1
                factor3_passes += S % 3 == 0
            checked += 1
    require(repunit_word(61, 57, 423) == 0, 'composite sum positive')
    require(repunit_word(165, 33, 1151) == 0, 'prime sum positive')
    require(repunit_word(313, 51, 2187) == 1944, 'factor nine negative')
    return {'literal_pairs': checked, 'eligible_sum_passes': sum_passes,
            'eligible_sum_passes_with_3_dividing_S': factor3_passes,
            'original_PS_positive': 135, 'factor_nine_negative_n_mod_S': 1944}


def archive_review():
    archive = HERE.parent/'prime-sum/evidence/trillion-evidence.zip'
    data = archive.read_bytes()
    require(hash_bytes(data) == 'b657f158d6362c77c570b87c3c193fe54c6f3c385889379edf5bf79b71f05c0a',
            'review archive identity')
    with ZipFile(io.BytesIO(data)) as z:
        raw = z.read('A398769-research/valuation/candidates.csv')
    require(hash_bytes(raw) == '919c091c978ee1e6011f9239fadbba675985714f286d8dcffa1a29ed043cf8e4',
            'review CSV identity')
    pairs = [tuple(map(int, row)) for row in csv.reader(io.StringIO(raw.decode()))]
    require(len(pairs) == len(set(pairs)) == 74601 and pairs == sorted(pairs), 'review row domain')
    histogram = Counter()
    rows_hash = hashlib.sha256()
    sum_passes, thirds, fifths = 0, 0, 0
    for L, i in pairs:
        require(5 <= L <= 10**12 and L % 2 == 1 and 3 <= i < L and i % 6 == 3, 'review pair')
        S = 7*L-4
        n_sum = repunit_word(L, i, S)
        n7 = repunit_word(L, i, 7**28)
        t, lead = valuation(n7, 7)
        require(22 <= t <= 27 and t < L-2, 'review exact depth')
        histogram[t] += 1
        sum_passes += n_sum == 0
        thirds += S % 3 == 0
        fifths += S % 5 == 0
        rows_hash.update(f'{L},{i},{n_sum},{9*n_sum},{t},{lead}\n'.encode())
    require(sum_passes == 0, 'review zero sum passes')
    receipt = json.loads((HERE/'archive-control.json').read_text())
    require(rows_hash.hexdigest() == receipt['arithmetic_rows_sha256'], 'independent arithmetic stream equality')
    require(dict(sorted(histogram.items())) == {int(k):v for k,v in receipt['exact_valuation_histogram'].items()},
            'independent histogram equality')
    return {'pairs': len(pairs), 'sum_passes': sum_passes,
            'with_3_dividing_S': thirds, 'with_5_dividing_S': fifths,
            'exact_valuation_histogram': dict(sorted(histogram.items())),
            'arithmetic_rows_sha256': rows_hash.hexdigest(),
            'complete_enumerations_rerun': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--commit')
    args = parser.parse_args()
    bindings = {}
    if args.commit:
        files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', args.commit, '--',
                                         PREFIX, 'README.md'], cwd=ROOT, text=True).splitlines()
        for file in files:
            if Path(file).name in {'independent_review.py', 'independent-review.json', 'REVIEW.md'}:
                continue
            committed = subprocess.check_output(['git', 'show', args.commit+':'+file], cwd=ROOT)
            require(committed == (ROOT/file).read_bytes(), 'reviewed commit mismatch: '+file)
            bindings[file] = hash_bytes(committed)
    result = {'status': 'PASS', 'implementation_commit': args.commit,
              'artifact_sha256': bindings, 'arithmetic': arithmetic_controls(),
              'literal_controls': literal_controls(), 'archive': archive_review(),
              'global_U': None, 'global_target': 'UNRESOLVED',
              'new_whole_length_coverage': None}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
