#!/usr/bin/env python3
"""Recheck source bindings, reviewed implementation, and deterministic receipts."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    baseline = json.loads((HERE/'baseline.json').read_text())
    for source in baseline['required_inputs_and_review']:
        data = subprocess.check_output(['git', 'show', source['ref']+':'+source['path']], cwd=ROOT)
        require(len(data) == source['bytes'] and digest(data) == source['sha256'],
                'source binding: '+source['path'])
    review = json.loads((HERE/'independent-review.json').read_text())
    commit = review['implementation_commit']
    require(commit and review['status'] == 'PASS', 'reviewed implementation exists')
    for name, expected in review['artifact_sha256'].items():
        data = (ROOT/name).read_bytes()
        require(digest(data) == expected, 'reviewed artifact: '+name)
        require(data == subprocess.check_output(['git', 'show', commit+':'+name], cwd=ROOT),
                'reviewed commit: '+name)
    cases = [('checks.py', 'checks.json', []),
             ('archive_control.py', 'archive-control.json', []),
             ('independent_review.py', 'independent-review.json', ['--commit', commit])]
    for program, receipt, arguments in cases:
        expected = (HERE/receipt).read_bytes()
        for flags in ([], ['-O']):
            data = subprocess.check_output([sys.executable, *flags, str(HERE/program), *arguments], cwd=ROOT)
            require(data == expected, 'reproduction: '+program+' '+str(flags))
    print(json.dumps({'status':'PASS','starting_main':baseline['starting_main'],
        'reviewed_implementation':commit,'input_bindings':len(baseline['required_inputs_and_review']),
        'reviewed_artifacts':len(review['artifact_sha256']),'checker_runs':6,
        'archive_pairs_independently_checked':74601,'full_sum_passes':0,
        'complete_enumerations_rerun':False,'adjacent_interval_rerun':False,
        'global_U':None,'global_target':'UNRESOLVED','new_whole_lengths':0},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
