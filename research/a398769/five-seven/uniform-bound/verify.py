#!/usr/bin/env python3
"""Reproduce new exact controls and verify retained inherited evidence.

No ten-million search is executed. Run from any working directory.
"""
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = 'ecac4f73be7c19daff5ac931f0b7b9e2cd78b119'
AUDIT = '47f1939a4f14f774cfbc0daa1e1f8e33e9c402ea'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return sha256(data).hexdigest()


def run(command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True)
    require(result.returncode == 0, f'failed {command}: {result.stderr.decode()}')
    return result.stdout


def main():
    run(['git', 'merge-base', '--is-ancestor', BASE, 'HEAD'])
    run(['git', 'merge-base', '--is-ancestor', AUDIT, BASE])
    require(run(['git', 'diff', '--name-only', AUDIT, BASE]) == b'', 'baseline tree drift')
    parents = run(['git', 'show', '-s', '--format=%P', BASE]).decode().split()
    require(len(parents) == 2 and parents[1] == AUDIT, 'PR19 merge parents')
    paths = run(['git', 'ls-tree', '-r', '--name-only', BASE]).decode().splitlines()
    preserved = []
    for path in paths:
        if path == 'README.md':
            continue
        data = (ROOT/path).read_bytes()
        require(data == run(['git', 'show', f'{BASE}:{path}']), 'inherited change: '+path)
        preserved.append(path+'\t'+digest(data)+'\n')

    checks, reports = {}, {}
    for source, receipt in [('exact_checks.py', 'exact_results.json'),
                            ('review_check.py', 'review_results.json')]:
        normal = run([sys.executable, str(HERE/source)])
        optimized = run([sys.executable, '-O', str(HERE/source)])
        require(normal == optimized, 'normal/-O mismatch: '+source)
        require(normal == (HERE/receipt).read_bytes(), 'stale receipt: '+receipt)
        report = json.loads(normal)
        require(report['source_sha256'] == digest((HERE/source).read_bytes()), 'source identity')
        reports[source] = report
        checks[source] = {'normal': 'PASS', 'optimized': 'PASS', 'byte_identical': True,
                          'source_sha256': report['source_sha256'],
                          'receipt_sha256': digest(normal)}
    left, right = reports['exact_checks.py'], reports['review_check.py']
    for a, b in zip(left['cutoff']['base_rows'], right['cutoff']):
        require(a['K'] == b['K'] and a['quadratic_margin'] == b['target_margin'] and
                a['strong_Hensel_margin'] == b['hensel_margin'] and
                a['dependent_margin'] == b['dependent_margin'], 'independent cutoff disagreement')
    require(len(left['cutoff']['base_rows']) == len(right['cutoff']) == 2, 'cutoff row count')
    require(right['theorem4_table_floor'] == 465 and
            right['theorem4_envelope_lower_bound'] == 800, 'optimized table obstruction')
    require(left['status'] == 'PASS' and right['negative_controls_rejected'] >= 4,
            'checker status and guards')

    # Revalidate retained source-bound broad-E receipts, not their large searches.
    inherited_source = HERE.parent/'early-rejection/verify.py'
    inherited = run([sys.executable, str(inherited_source)])
    inherited_o = run([sys.executable, '-O', str(inherited_source)])
    require(inherited == inherited_o, 'inherited integrity normal/-O mismatch')
    prior = json.loads(inherited)
    require(prior['status'] == 'PASS' and prior['fresh_full_runs'] == [] and
            prior['large_inherited_certificates_rerun'] is False and
            prior['blocks_compared'] == 100, 'inherited verification scope')

    # Read both retained 100-depth records. No new line enumeration is claimed.
    depth_reports = []
    for stem in ('depth_exponents', 'depth_roots'):
        source = HERE.parent/'three-deductions-audit'/f'{stem}.py'
        receipt = source.with_suffix('.json')
        report = json.loads(receipt.read_bytes())
        require(report['source_sha256'] == digest(source.read_bytes()), 'depth source hash')
        depth_reports.append(report)
    a, b = depth_reports
    require(len(a['history']) == len(b['history']) == 100, 'retained depth history length')
    for expected, (x, y) in enumerate(zip(a['history'], b['history']), 1):
        keys = ('k', 'modulus', 'T', 'u', 'representative_L',
                'band_lower_inclusive', 'band_upper_exclusive', 'in_own_band')
        require(x['k'] == y['k'] == expected and
                {k: x[k] for k in keys} == {k: y[k] for k in keys}, 'retained depth row')
        require(pow(10, x['u'], x['modulus']) == y['root'], 'retained exponent/root residue')
    require(a['exceptions'] == b['exceptions'], 'retained exception disagreement')
    require([x['k'] for x in a['exceptions']] == [44, 56, 85, 92], 'retained qualifying depths')
    for row in a['exceptions']:
        L, i, k = row['L'], row['i'], row['k']
        S = 7*L-4
        mod = 7**(k+1)
        Fmod = (7*pow(10, L, mod)-18*pow(10, i, mod)-25) % mod
        require(Fmod == row['F_mod_7_to_k_plus_1'] and Fmod != 0 and Fmod % 7**k == 0,
                'retained exception exact valuation')
        sum_residue = (7*pow(10, L, 9*S)-18*pow(10, i, 9*S)-25) % (9*S)
        require(sum_residue == row['F_mod_9S'] != 0 and gcd(sum_residue, S) == row['gcd_F_S'] == 1,
                'retained exception full-sum rejection')
    print(json.dumps({
        'status': 'PASS', 'source_sha256': digest(Path(__file__).read_bytes()),
        'starting_commit': BASE, 'required_audited_commit': AUDIT,
        'required_commits_are_ancestors': True, 'baseline_tree_equals_audited_tree': True,
        'baseline_tracked_files': len(paths), 'inherited_files_byte_identical': len(preserved),
        'only_inherited_edit': 'README.md navigation',
        'preserved_manifest_sha256': digest(''.join(preserved).encode()),
        'checks': checks, 'independent_cutoff_rows_agree': 2,
        'inherited_integrity': {'blocks_compared': 100, 'fresh_full_runs': [],
                                'large_searches_rerun': False,
                                'normal_and_optimized_identical': True,
                                'receipt_sha256': digest(inherited),
                                'retained_depth_rows_compared': 100,
                                'exception_modular_certificates_rechecked': [44, 56, 85, 92]},
        'consecutive_whole_length_exclusion_unchanged': [1, 10000000],
        'broad_E_odd_length_coverage_unchanged': [5, 9999999],
        'restricted_minus_line_E_L_exclusive_unchanged': 6*7**99,
        'new_whole_length_coverage': [],
        'new_position_theorems': 'ANALYTIC (12), (13a)-(13c); earlier gaps not discharged',
        'broad_all_length_E': 'OPEN', 'all_length_five_seven': 'OPEN',
        'wider_digit_1_conjecture': 'OPEN', 'proposed_quadratic_bound': 'UNPROVED_UNREFUTED',
        'new_Lean_theorem_or_build': False
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
