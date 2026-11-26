#!/usr/bin/env python3
"""Reproduce fresh checks and audit inherited receipts, without large searches."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
FAMILY = HERE.parent
ROOT = HERE.parents[3]
BASE = '0e4dbdf9244c6b7f743d7e90ce04c91ea3d38675'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def bindings(directory, manifest):
    for name, expected in manifest.items():
        require(digest(directory/name) == expected, 'artifact changed: '+str(directory/name))
    return len(manifest)


def audit():
    baseline = json.loads((HERE/'baseline.json').read_text())
    require(baseline['starting_main'] == baseline['requested_pr25_merge'] == BASE, 'base identity')
    baseline_count = bindings(FAMILY, baseline['inherited_sha256'])
    inherited = {}
    # Binding checks only: no historical trillion-length scan is rerun.
    for folder in ['prime-sum','trillion-witness']:
        manifest = json.loads((FAMILY/folder/'verification.json').read_text())
        inherited[folder] = bindings(FAMILY/folder, manifest['artifact_sha256'])
    rc = json.loads(subprocess.check_output(
        [sys.executable, *(['-O'] if sys.flags.optimize else []), str(FAMILY/'rational-centres/verify.py')]))
    require(rc['status']=='PASS' and rc['unresolved_survivors']==[], 'rational centre receipts')
    require(rc['whole_length_endpoint']==1_000_002_000_000, 'inherited endpoint')
    require(rc['partitions_per_engine']==300 and rc['control_partitions_per_engine']==1,
            'rational centre receipt coverage')

    checks = [('checks.py','checks.json'),
              ('independent_checks.py','independent-checks.json'),
              ('obstruction_checks.py','obstruction-checks.json')]
    fresh = []
    for program, receipt in checks:
        expected = (HERE/receipt).read_bytes()
        normal = subprocess.check_output([sys.executable,str(HERE/program)])
        optimized = subprocess.check_output([sys.executable,'-O',str(HERE/program)])
        require(normal==optimized==expected, 'fresh reproduction mismatch: '+program)
        require(json.loads(normal)['status']=='PASS', 'checker status: '+program)
        fresh.append({'program':program, 'normal_and_optimized_match':True,
                      'receipt':receipt,'receipt_sha256':sha256(expected).hexdigest()})
    primary = json.loads((HERE/'checks.json').read_text())
    independent = json.loads((HERE/'independent-checks.json').read_text())
    require(primary['literal_words']['counts']['full_witnesses']==0, 'primary witness needs certification')
    require(independent['literal_words']['counts']['full_residual_witnesses']==0,
            'independent witness needs certification')
    files = ['PROOF.md','OBSTRUCTION.md','README.md','checks.py','checks.json',
             'independent_checks.py','independent-checks.json','obstruction_checks.py',
             'obstruction-checks.json','baseline.json','verify.py']
    artifacts = {name:digest(HERE/name) for name in files}
    artifacts['../../../../README.md'] = digest(ROOT/'README.md')
    return {
        'status':'PASS', 'base_main':BASE, 'baseline_bindings':baseline_count,
        'fresh_reproductions':fresh, 'artifact_sha256':artifacts,
        'inherited_receipt_bindings':inherited,
        'inherited_rational_centre_receipts':{
            'partitions_checked_per_engine':301,
            'ordered_partition_pair_digest':rc['ordered_partition_pair_digest'],
            'large_enumerations_rerun':False},
        'whole_length_endpoint_inclusive':1_000_002_000_000,
        'q0_at_most_L_pow_35_subfamily':'EXCLUDED_AT_EVERY_LENGTH',
        'new_consecutive_lengths':0, 'unrestricted_five_seven':'OPEN',
        'wider_digit_one_conjecture':'OPEN', 'full_witness_found':False,
        'new_Lean_formalization':False, 'Lean_build_performed':False,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='explicitly regenerate the compact verification receipt')
    args=parser.parse_args()
    result=audit()
    path=HERE/'verification.json'
    if args.write:
        path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        require(json.loads(path.read_text())==result, 'verification receipt mismatch')
    print(json.dumps({'status':'PASS','fresh_checkers':3,'modes':['normal','-O'],
                      'historical_large_searches_rerun':False,
                      'inherited_bindings':result['inherited_receipt_bindings'],
                      'rational_centre_receipts':602,
                      'whole_length_endpoint':result['whole_length_endpoint_inclusive']},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
