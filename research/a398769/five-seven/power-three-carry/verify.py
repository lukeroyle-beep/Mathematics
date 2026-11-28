#!/usr/bin/env python3
"""Reproduce receipts, audit scope, reject corruption, and bind preserved sources."""
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = '61a6fdfd7f4093b77be36ed0a55fbd3ebf798b7c'
PROGRAMS = [('certificates.py', 'certificates.json'),
            ('corollary_checks.py', 'corollary-checks.json'),
            ('one_step_checks.py', 'one-step-checks.json')]
DOCS = ['README.md', 'ONE_STEP.md', 'MOVING_BOUND.md', 'COROLLARY.md',
        'EXACT_CERTIFICATES.md', 'SOURCES.md']


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(c, q, w):
    need(c['status'] == q['status'] == w['status'] == 'PASS', 'receipt status')
    need([r['a'] for r in c['rows']] == [1231, 1579, 1585, 1591, 1597],
         'selected exponents')
    pilots = {1231:(377,468,720,4,14406), 1579:(205,467,119,1,14),
              1585:(450,468,922,1,28), 1591:(191,468,780,1,42),
              1597:(92,468,2255,2,294)}
    for r in c['rows']:
        a, L, sb, sa = r['a'], r['L'], r['s_b'], r['s_a']
        S, D = 3 ** a, 3 ** (a - 8)
        need(7 * L == S + 4 and r['D'] == D, 'exact length')
        need(3 <= sb < 2 * D and 3 <= sa < 1458 * D and sb % 6 == sa % 6 == 3,
             'representative domains')
        need(sa == sb + 2 * D * r['k'] and 0 <= r['k'] <= 728,
             'actual ternary increment')
        need(r['K'] == (L - 1 - sb) // (2 * D) <= 468, 'exact K')
        need(r['actual'] and r['k'] <= r['K'] and 3 <= sa < L, 'actuality')
        need((r['k'],r['K'],r['j_5'],r['t'],r['first_nonzero_n_residue']) == pilots[a],
             'selected reconstructed values')
        need((7 * pow(10,L,9*S) - 18 * pow(10,sa,9*S) - 25) % (9*S) == 0,
             'same-position factor nine')
        need(r['n_mod_25S'] == r['F_mod_9S'] == 0, 'original other factors')
        t, m = r['t'], r['first_fail_depth']
        need(m == t + 1 <= L - 2 and r['first_fail_modulus'] == 7 ** m,
             'inclusive failure deadline')
        need(r['n_residues'] == [0] * t + [r['first_nonzero_n_residue']],
             'exact valuation')
        need(not r['full_witness'], 'no proposed witness')
    expected = list(range(31, 1585, 6))
    need(q['finite_exponents'] == expected and
         [r['a'] for r in c['inherited_259']['rows']] == expected and
         [r['a'] for r in q['finite_rows']] == expected, 'complete finite remainder')
    for x, y in zip(c['inherited_259']['rows'], q['finite_rows']):
        need(x['actual'] == y['actual'], 'inherited actuality agreement')
        if x['actual']:
            need(x['t'] == y['t'] and x['first_fail_depth'] == y['first_fail_depth']
                 and x['first_nonzero_n_residue'] == y['first_fail_n_residue'],
                 'independent finite arithmetic agreement')
        else:
            need(x['t'] is None, 'miss has no valuation')
    need(q['finite_count'] == 259 and c['named_family_members_excluded'] == 262
         and c['last_family_exponent'] == 1597 and c['next_family_exponent'] == 1603,
         'family count and endpoint')
    need(c['class_misses'] == 85 and c['actual_candidates'] == 177 and
         c['valuation_histogram'] == {'1':154,'2':19,'3':3,'4':1}, 'coverage summary')
    need(q['crossover_left'] == 3**1585 and
         q['crossover_right'] == 7*(624000*1605**2)**61 and
         q['crossover_margin'] == q['crossover_left']-q['crossover_right'] > 0,
         'exact corollary crossover')
    need(q['induction_left'] == 3*1605**122 and q['induction_right'] == 1606**122
         and q['induction_margin'] == q['induction_left']-q['induction_right'] > 0,
         'exact corollary induction')
    need(c['no_depth_cap_exclusions'] and not c['Lean_verification'] and
         c['whole_length_endpoint_inclusive'] == 1000002000000 and
         c['moving_family'] == c['unrestricted_five_seven'] == c['wider_digit_one'] == 'OPEN',
         'scope boundaries')
    need(w['counts']['children'] == 45*11*7 and len(w['roots']) == 45 and
         len(w['block_inequality_controls']) == 15, 'one-step control coverage')


def corruption_controls(values):
    paths = [(0, ('rows',2,'k'), 449), (0, ('rows',1,'K'), 468),
             (0, ('rows',2,'j_5'), 450), (0, ('rows',4,'F_mod_9S'), 3),
             (0, ('no_depth_cap_exclusions',), False),
             (0, ('inherited_259','rows',0,'t'), 2),
             (1, ('finite_count',), 258), (1, ('crossover_margin',), 0),
             (2, ('counts','children'), 0)]
    for which, path, replacement in paths:
        changed = deepcopy(values)
        obj = changed[which]
        for key in path[:-1]:
            obj = obj[key]
        obj[path[-1]] = replacement
        try:
            validate(*changed)
        except (ValueError, KeyError, TypeError):
            continue
        raise ValueError('Corrupted receipt was accepted: '+str(path))
    return len(paths)


def preserved_base():
    listing = subprocess.check_output(['git','ls-tree','-r',BASE], cwd=ROOT).decode().splitlines()
    count = 0
    for line in listing:
        metadata, name = line.split('\t', 1)
        mode, kind, expected = metadata.split()
        need(kind == 'blob' and mode in ('100644','100755'), 'ordinary inherited source')
        data = (ROOT/name).read_bytes()
        if name == 'README.md':
            old = subprocess.check_output(['git','show',BASE+':README.md'], cwd=ROOT)
            prefix, remainder = old.split(b'\n\n',1)
            need(data.startswith(prefix+b'\n\n') and data.endswith(remainder),
                 'root README preserves inherited content')
        else:
            actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            need(actual == expected, 'inherited source changed: '+name)
        count += 1
    return count


def manifest():
    values = [json.loads((HERE/receipt).read_text()) for _, receipt in PROGRAMS]
    validate(*values)
    for (program, _), value in zip(PROGRAMS, values):
        need(value['source_sha256'] == digest(HERE/program), 'program source binding')
    artifacts = DOCS + ['verify.py'] + [x for pair in PROGRAMS for x in pair]
    return dict(schema=1, status='PASS', base_main=BASE,
                inherited_tracked_files=preserved_base(),
                inherited_exception='additive root README entry only',
                artifact_sha256={name:digest(HERE/name) for name in sorted(artifacts)},
                root_readme_sha256=digest(ROOT/'README.md'),
                rejected_corruptions=corruption_controls(values),
                named_family_count=262, last_family_exponent=1597,
                next_family_exponent=1603, moving_position_verdict='OPEN',
                whole_length_endpoint_inclusive=1000002000000,
                Lean_verification_performed=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--record', action='store_true', help='create initial manifest')
    args = parser.parse_args()
    if args.run:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        for program, receipt in PROGRAMS:
            cmd = [sys.executable] + (['-O'] if sys.flags.optimize else []) + [str(HERE/program)]
            output = subprocess.check_output(cmd, cwd=ROOT, env=env)
            need(output == (HERE/receipt).read_bytes(), 'fresh receipt mismatch: '+program)
    result = json.dumps(manifest(), indent=2, sort_keys=True)+'\n'
    if args.record:
        (HERE/'verification.json').write_text(result)
    else:
        need(result == (HERE/'verification.json').read_text(), 'manifest mismatch')
    print(result, end='')


if __name__ == '__main__':
    main()
