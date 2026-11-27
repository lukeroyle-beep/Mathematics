#!/usr/bin/env python3
"""Reapply the inherited Newton/log method, explicitly separate from fresh blocks.

This adapter is reuse, not a newly authored independent arithmetic engine.
Its arithmetic source is bound by hash and by the aggregate base archive.
"""
import importlib.util
from hashlib import sha256
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'power-three'/'individuals.py'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    spec = importlib.util.spec_from_file_location('inherited_root_log', SOURCE)
    inherited = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(inherited)
    theta, C, kappa = inherited.parameters(1568)
    theta2, C2, kappa2 = inherited.parameters(1569)
    need(theta2 % 3**1570 == theta and C2 % 3**1568 == C and
         kappa2 % 3**1566 == kappa, 'precision stability')
    row = inherited.member(1567, theta, kappa)
    fresh_path = HERE/'individual.json'
    fresh = json.loads(fresh_path.read_text())['new_a1567']
    for key in ('a', 'L', 'S', 'd', 'D', 's', 'i', 't',
                'first_fail_depth', 'first_fail_n_residue'):
        need(row[key] == fresh[key], 'independent original blocks disagree: '+key)
    need(row['t'] == 1 and row['first_fail_n_residue'] == 7, 'new individual verdict')
    print(json.dumps(dict(status='PASS', source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                         inherited_source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
                         compared_receipt_sha256=sha256(fresh_path.read_bytes()).hexdigest(),
                         method='explicit reuse of PR28 Newton root and modular logarithm',
                         precisions=[1568,1569], case=row), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
