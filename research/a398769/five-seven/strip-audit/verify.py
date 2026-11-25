#!/usr/bin/env python3
"""Reproduce new checks in both modes, compare outcomes, preserve the baseline.

No large inherited search is rerun. No essential check uses assert.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = 'b7659c9c25ef6b339ee3c1de17b1938429b9af9e'
AUDIT = '26b79b0fb5c4623e657aca40e34ba95214b5833d'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run(command):
    completed = subprocess.run(command, cwd=ROOT, capture_output=True)
    require(completed.returncode == 0,
            f'failed {command}: {completed.stderr.decode()}')
    return completed.stdout


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    run(['git', 'merge-base', '--is-ancestor', BASE, 'HEAD'])
    run(['git', 'merge-base', '--is-ancestor', AUDIT, BASE])
    baseline_paths = run(['git', 'ls-tree', '-r', '--name-only', BASE]).decode().splitlines()
    preserved = []
    for path in baseline_paths:
        if path == 'README.md':
            continue
        original = run(['git', 'show', f'{BASE}:{path}'])
        actual = (ROOT / path).read_bytes()
        require(original == actual, f'inherited file changed: {path}')
        preserved.append(path + '\t' + digest(actual) + '\n')
    require(len(preserved) == len(baseline_paths)-1, 'baseline preservation count')

    checkers = [('strip_check.py', 'strip_results.json'),
                ('modular_roots.py', 'modular_roots.json'),
                ('modular_exponents.py', 'modular_exponents.json'),
                ('review_check.py', 'review_results.json')]
    checks, objects = {}, {}
    for source, receipt in checkers:
        path = str(HERE / source)
        ordinary = run([sys.executable, path])
        optimized = run([sys.executable, '-O', path])
        require(ordinary == optimized, f'normal/-O mismatch: {source}')
        require(ordinary == (HERE / receipt).read_bytes(), f'stale receipt: {receipt}')
        value = json.loads(ordinary)
        require(value.get('status', value.get('verdict')) == 'PASS', f'non-PASS: {source}')
        objects[source] = value
        checks[source] = {'normal': 'PASS', 'optimized': 'PASS',
                          'byte_identical': True, 'receipt': receipt,
                          'receipt_sha256': digest(ordinary),
                          'source_sha256': digest((HERE / source).read_bytes())}
    roots = objects['modular_roots.py']
    exponents = objects['modular_exponents.py']
    require(roots['observed'] == exponents['observed'], 'independent modular disagreement')
    for root_row, exponent_row in zip(roots['root_lifts'], exponents['lifts']):
        require(root_row['depth'] == exponent_row['depth'], 'lift depth mismatch')
        modulus = root_row['modulus']
        require(modulus == exponent_row['modulus'], 'lift modulus mismatch')
        require([pow(10, u, modulus) for u in exponent_row['surviving_classes']] ==
                root_row['roots'], 'lift root/exponent mismatch')
    require(len(roots['root_lifts']) == len(exponents['lifts']) == 10, 'incomplete history')
    # K=k implies L<T_k; the first line position passing depth k is above T_k.
    line_early_bounds = []
    for row in exponents['lifts'][1:]:
        first_u = row['surviving_classes'][0]
        require(first_u > 0, 'least positive lift representative')
        first_length = 12*first_u+5
        require(first_length > row['period'], 'restricted line early bound')
        line_early_bounds.append({'K': row['depth'], 'T_K': row['period'],
                                  'first_depth_K_permitted_line_length': first_length})

    # Exact endpoints and their placement in the inherited coverage gap.
    centre = Fraction(5, 12)
    radius = Fraction(1, 12*10**9)
    low, high = centre-radius, centre+radius
    require(low == Fraction(4999999999, 12000000000) and
            high == Fraction(5000000001, 12000000000), 'ratio endpoints')
    require(Fraction(4000001, 10000000) < low < high < Fraction(59999, 120000),
            'new strip not contained in the stated inherited interval')

    inherited_command = str(HERE.parent / 'early-rejection' / 'verify.py')
    inherited = run([sys.executable, inherited_command])
    inherited_o = run([sys.executable, '-O', inherited_command])
    require(inherited == inherited_o, 'inherited verifier normal/-O disagreement')
    prior = json.loads(inherited)
    require(prior['status'] == 'PASS' and prior['fresh_full_runs'] == [] and
            prior['large_inherited_certificates_rerun'] is False,
            'inherited verification scope mismatch')
    required_inputs = ['proportional/COVERAGE.md', 'proportional/AUDIT.md',
                       'prime-factor-audit/PROOF.md', 'early-rejection/README.md']
    print(json.dumps({
        'status': 'PASS', 'baseline_commit': BASE, 'pr17_audit_commit': AUDIT,
        'verifier_source_sha256': digest(Path(__file__).read_bytes()),
        'baseline_tracked_files': len(baseline_paths),
        'inherited_files_byte_identical': len(preserved),
        'sole_inherited_edit': 'README.md navigation',
        'preserved_path_tab_sha256_lf_manifest_sha256': digest(''.join(preserved).encode()),
        'frozen_input_sha256': {p: digest((HERE.parent / p).read_bytes()) for p in required_inputs},
        'checks': checks, 'independent_modular_results_agree': True,
        'all_ten_root_and_exponent_lifts_agree': True,
        'observed_modular_result': roots['observed'],
        'bounded_line_t_less_than_K': {
            'admissible_line_lengths': '17 <= L < 2231854769',
            'depth_2_through_10': line_early_bounds,
            'larger_K_argument': 'K>=11 and t<10 when T_10<=L<2231854769',
            'whole_length_coverage': False},
        'new_closed_ratio_strip': [str(low), str(high)],
        'inherited_verifier': {'normal': 'PASS', 'optimized': 'PASS',
                              'byte_identical': True, 'receipt_sha256': digest(inherited),
                              'blocks_compared': prior['blocks_compared'],
                              'fresh_full_runs': [], 'large_search_rerun': False},
        'consecutive_full_witness_length_coverage_unchanged': [1, 10000000],
        'broad_E_odd_length_coverage_unchanged': [5, 9999999],
        'new_whole_length_exclusion_claimed': False,
        'new_Lean_theorem_or_build_claimed': False
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
