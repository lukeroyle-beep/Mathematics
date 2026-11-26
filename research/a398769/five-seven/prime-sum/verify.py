#!/usr/bin/env python3
"""Verify retained bindings and arithmetic; full enumeration is a separate command."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def check_bindings(directory, manifest):
    for name, digest in manifest.items():
        require(hashlib.sha256((directory / name).read_bytes()).hexdigest() == digest,
                'artifact changed: ' + name)
    return len(manifest)


def main():
    index = json.loads((HERE / 'verification.json').read_text())
    count = check_bindings(HERE, index['artifact_sha256'])
    inherited = HERE.parent / 'trillion-witness'
    old = json.loads((inherited / 'verification.json').read_text())
    old_count = check_bindings(inherited, old['artifact_sha256'])
    checks = [('prime_density_checks.py', 'prime-density-checks.json'),
              ('global_checks.py', 'global-checks.json'),
              ('independent_checks.py', 'independent_checks.json'),
              ('archive_audit.py', 'evidence/archive-audit.json')]
    for program, receipt in checks:
        observed = json.loads(subprocess.check_output([sys.executable, str(HERE / program)]))
        expected = json.loads((HERE / receipt).read_text())
        if program == 'archive_audit.py':
            require(observed.pop('enumerations') == {'mode': 'not_rerun', 'outputs': {}},
                    'default archive verification scope changed')
            expected.pop('enumerations')
        require(observed == expected, 'arithmetic receipt changed: ' + program)
    print(json.dumps({'status': 'PASS', 'new_artifact_bindings': count,
                      'inherited_PR21_artifact_bindings': old_count,
                      'arithmetic_checkers': len(checks),
                      'archive_candidates_checked': 74601,
                      'enumerations_rerun_by_this_command': False,
                      'global_target': 'UNRESOLVED'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
