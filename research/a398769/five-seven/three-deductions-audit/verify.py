#!/usr/bin/env python3
"""Reproduce all new exact checks in both modes and compare full receipts."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = '8677446ad39f3a8d72f3a2123c6012c012f2d271'
AUDITED = '54081b0a43beead5686aa205cce41a0b5135c03c'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def run(command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True)
    require(result.returncode == 0,
            f'command failed: {command}: {result.stderr.decode()}')
    return result.stdout


def digest(data):
    return sha256(data).hexdigest()


def main():
    run(['git', 'merge-base', '--is-ancestor', AUDITED, BASE])
    run(['git', 'merge-base', '--is-ancestor', BASE, 'HEAD'])
    require(run(['git', 'diff', '--name-only', AUDITED, BASE]) == b'',
            'unexpected change between audited head and starting main')
    parents = run(['git', 'show', '-s', '--format=%P', BASE]).decode().split()
    require(len(parents) == 2 and parents[1] == AUDITED, 'PR18 merge parents')
    paths = run(['git', 'ls-tree', '-r', '--name-only', BASE]).decode().splitlines()
    preserved = []
    for path in paths:
        if path == 'README.md':
            continue
        actual = (ROOT / path).read_bytes()
        require(run(['git', 'show', f'{BASE}:{path}']) == actual,
                f'inherited file changed: {path}')
        preserved.append(path + '\t' + digest(actual) + '\n')

    reports, checks = {}, {}
    for name, receipt_name in [('depth_exponents', 'depth_exponents'),
                               ('depth_roots', 'depth_roots'),
                               ('seven_twelfths', 'seven_twelfths'),
                               ('opposite', 'opposite'),
                               ('review_check', 'review_results')]:
        source, receipt = HERE / f'{name}.py', HERE / f'{receipt_name}.json'
        ordinary = run([sys.executable, str(source)])
        optimized = run([sys.executable, '-O', str(source)])
        require(ordinary == optimized, f'normal/-O mismatch: {name}')
        require(ordinary == receipt.read_bytes(), f'stale receipt: {name}')
        report = json.loads(ordinary)
        require(report['source_sha256'] == digest(source.read_bytes()),
                f'wrong source hash: {name}')
        if 'verdict' in report:
            require(report['verdict'] == 'PASS', f'failed verdict: {name}')
        reports[name] = report
        checks[name] = {'normal': 'PASS', 'optimized': 'PASS',
                        'byte_identical': True,
                        'source_sha256': digest(source.read_bytes()),
                        'receipt_sha256': digest(ordinary)}

    left, right = reports['depth_exponents'], reports['depth_roots']
    shared = ['k', 'modulus', 'T', 'u', 'representative_L',
              'band_lower_inclusive', 'band_upper_exclusive', 'in_own_band']
    require(len(left['history']) == len(right['history']) == 100, 'history length')
    for k, (a, b) in enumerate(zip(left['history'], right['history']), 1):
        require(a['k'] == b['k'] == k, 'missing depth')
        require({key: a[key] for key in shared} == {key: b[key] for key in shared},
                f'independent history mismatch at depth {k}')
        require(pow(10, a['u'], a['modulus']) == b['root'], 'root/exponent mismatch')
    require(left['exceptions'] == right['exceptions'], 'exception records disagree')
    require([row['k'] for row in left['exceptions']] == [44, 56, 85, 92],
            'exception depths')
    require(all(row['K'] == row['v7_F'] == row['k'] and
                row['gcd_F_S'] == 1 and row['F_mod_9S'] != 0 and row['S_mod_5'] != 0
                for row in left['exceptions']), 'exception semantics')
    require(left['coverage_L_exclusive'] == right['coverage_L_exclusive'] == 6*7**99,
            'restricted E upper endpoint')
    first = left['exceptions'][0]
    require(first['F_mod_7_to_k_plus_1'] == 3*7**44, 'first exact valuation')

    strip = reports['seven_twelfths']
    require(strip['strict_margin_at_N'] == 390361597 and
            Fraction(strip['independent_slope']) == Fraction(47628, 78125) and
            strip['independent_additive_loss'] == 1, 'strong Hensel loss')
    centre, radius = Fraction(7, 12), Fraction(1, 12*10**9)
    lower, upper = centre-radius, centre+radius
    require(lower == Fraction(6999999999, 12000000000) and
            upper == Fraction(7000000001, 12000000000), 'closed ratio endpoints')
    require(Fraction(60001, 120000) < lower < upper < Fraction(5999999, 10000000),
            'strip location in inherited open interval')
    opposite = reports['opposite']['observed']
    require(opposite['u'] == 313281594 and opposite['period'] == 1694851494 and
            opposite['least_permitted_L'] == 3759379135 > 10**9,
            'opposite modular/analytic overlap')
    review = reports['review_check']
    require(review['minus_depths_checked'] == 100 and
            review['strip']['strict_margin_at_N'] == strip['strict_margin_at_N'] and
            review['opposite_u'] == opposite['u'], 'independent review disagreement')

    inherited_path = HERE.parent / 'strip-audit' / 'verify.py'
    inherited = run([sys.executable, str(inherited_path)])
    inherited_o = run([sys.executable, '-O', str(inherited_path)])
    require(inherited == inherited_o, 'inherited verifier normal/-O mismatch')
    require(inherited == (inherited_path.parent / 'verification.json').read_bytes(),
            'inherited verification receipt changed')
    prior = json.loads(inherited)
    require(prior['status'] == 'PASS' and
            prior['inherited_verifier']['fresh_full_runs'] == [] and
            prior['inherited_verifier']['large_search_rerun'] is False,
            'inherited scope changed')
    print(json.dumps({
        'status': 'PASS', 'source_sha256': digest(Path(__file__).read_bytes()),
        'starting_main_commit': BASE, 'pr18_merge_commit': BASE,
        'audited_head': AUDITED, 'audited_head_is_ancestor': True,
        'starting_main_tree_equals_audited_head': True,
        'baseline_tracked_files': len(paths),
        'inherited_files_byte_identical': len(preserved),
        'sole_inherited_edit': 'README.md navigation',
        'preserved_path_tab_sha256_lf_manifest_sha256': digest(''.join(preserved).encode()),
        'checks': checks, 'independent_depth_rows_agree': 100,
        'independent_review': {'verdict': review['verdict'],
                               'method': review['discovery'],
                               'direct_depth5_classes_per_line':
                                   review['direct_exhaustive_depth5_classes_per_line']},
        'exceptions': left['exceptions'],
        'restricted_minus_line_E': {'L_exclusive': 6*7**99, 'all_positions_at_length': False},
        'new_closed_ratio_strip': [str(lower), str(upper)],
        'new_opposite_line_full_witness_exclusion': 'every integer u>=0',
        'full_witness_fixed_gap': 'abs(12i-5L)>=3',
        'inherited_verifier': {'normal': 'PASS', 'optimized': 'PASS',
                              'byte_identical': True, 'receipt_sha256': digest(inherited),
                              'blocks_compared': prior['inherited_verifier']['blocks_compared'],
                              'fresh_full_runs': [], 'large_search_rerun': False},
        'consecutive_whole_length_exclusion_unchanged': [1, 10000000],
        'broad_E_odd_length_coverage_unchanged': [5, 9999999],
        'new_whole_length_exclusion_claimed': False,
        'new_Lean_theorem_or_build_claimed': False,
        'all_length_five_seven_subclass': 'OPEN', 'wider_digit_1_conjecture': 'OPEN'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
