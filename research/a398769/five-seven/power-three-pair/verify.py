#!/usr/bin/env python3
"""Compare full independent receipts, base archive, and exact source bindings."""
import argparse
from copy import deepcopy
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = '42e6a151c5279905a3e02b859c6fae737178fd7d'
PROGRAMS = [('pair_checks.py', 'pair-checks.json'),
            ('independent_modular.py', 'independent-modular.json'),
            ('logarithm_checks.py', 'logarithm-checks.json'),
            ('individual_check.py', 'individual.json'),
            ('root_log_check.py', 'root-log.json')]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((HERE/name).read_text())


def compare(p, m, log, individual, root):
    ks = list(range(42, 469, 49))
    need(p['k_values'] == m['depth_three']['surviving_k'] == ks, 'nine increments')
    need(p['transitions'] == [{key:r[key] for key in ('u','k')}
                              for r in m['depth_three']['rows']] ==
         [dict(u=u, k=ks) for u in range(7)], 'all seven complete transition rows')
    need(p['transition_checks'] == m['depth_three']['tests'] == 3283 and
         m['depth_three']['k_inclusive_bounds'] == [0,468] and
         m['depth_three']['u_period'] == 7, 'complete transition domain')
    classes = list(range(4,294,6))
    need(p['derivative_classes'] == classes, 'complete derivative classes')
    expected = [dict(k=k, residues=[49]*49) for k in ks]
    need(p['derivative_rows'] == expected, 'primary derivative table')
    need(m['derivative']['rows'] == [dict(k=k,w_mod_294=w,derivative_mod_343=49)
                                    for k in ks for w in classes], 'finite-difference table')
    need(log['derivative_rows'] == [dict(k=k,w_classes=classes,derivative_mod343=[49]*49)
                                   for k in ks], 'third derivative table')
    need(p['derivative_checks'] == m['derivative']['tests'] == log['derivative_cases'] == 441,
         'derivative completeness counts')
    need(log['independent_constant'] == 832*6561**4*15*70000 < 10**30-2, 'logarithm constant')
    c = log['crossover']
    need(c['a'] == 100 and int(c['left']) == 3**100 and
         int(c['right']) == 7*10**30*120**2+10 and
         int(c['positive_gap']) == int(c['left'])-int(c['right']) > 0 and
         c['induction_coefficients_ascending'] == [759,78,2], 'strict crossover and induction')
    need([r['k'] for r in log['strong_hensel_controls']] == ks and
         all(r['t'] == r['q']+2 and r['q']>=3 for r in log['strong_hensel_controls']),
         'nonvacuous Hensel controls and exact loss')
    starts = list(range(31,100,6))
    need(individual['finite_pair_starts'] == log['finite_starts_below_cutoff'] == starts and
         individual['cutoff_crossing_pair'] == [97,103], 'complete finite starts')
    rows = individual['finite_rows_including_crossing_successor']
    need([r['a'] for r in rows] == starts+[103], 'crossing successor')
    old = json.loads((HERE.parent/'power-three'/'individuals.json').read_text())
    new = individual['new_a1567']
    need(new['a'] == root['case']['a'] == 1567 and new['actual'] and
         new['s'] == root['case']['s'] < new['L'], 'same actual new position')
    for r in rows+[new]:
        a,s,L = r['a'],r['s'],r['L']
        need(r['S'] == 3**a and 7*L == 3**a+4 and r['d'] == 3**(a-2) and
             r['D'] == 2*r['d'] and 3<=s<r['D'] and s%6 == 3, 'exact candidate domain')
        comparison = root['case'] if a == 1567 else next(x for x in old['cases'] if x['a'] == a)
        for key in ('a','L','S','d','D','s','i','t','first_fail_depth','first_fail_n_residue'):
            need(r[key] == comparison[key], 'independent individual '+key)
        if s>=L:
            need(r['i'] is None and r['t'] is None and not r['actual'], 'class miss')
        else:
            t = r['t']
            need(r['i'] == s and r['n_mod_S'] == r['n_mod_25S'] == 0 and
                 r['first_fail_depth'] == t+1 <= L-2 and
                 r['seven_residues'] == [0]*t+[r['first_fail_n_residue']] and
                 0<r['first_fail_n_residue']<7**(t+1) and
                 r['first_fail_n_residue'] % 7**t == 0, 'same-position original failure')
    need(new['t'] == 1 and new['first_fail_n_residue'] == 7, 'a1567 verdict')
    control = individual['controls']['a25']
    need((control['s'],control['t'],control['seven_residues'],control['n_mod_S']) ==
         (40582608819,2,[0,0,294],0), 'a25 sum-positive control')
    nine = individual['controls']['lost_factor_nine']
    need((nine['L'],nine['s'],nine['F_mod_S'],nine['F_mod_9S'],nine['n_mod_S']) ==
         (313,51,0,17496,1944), 'lost-nine negative')


def corruption_checks(values):
    names = ('missing_transition', 'lost_increment_endpoint', 'missing_derivative',
             'false_derivative', 'false_cutoff', 'missing_crossing_start',
             'wrong_a1567_residue', 'lost_nine', 'false_hensel_loss')
    rejected = []
    for name in names:
        p,m,log,individual,root = deepcopy(values)
        if name == 'missing_transition': p['transitions'].pop()
        elif name == 'lost_increment_endpoint': m['depth_three']['k_inclusive_bounds'][0] = 1
        elif name == 'missing_derivative': m['derivative']['rows'].pop()
        elif name == 'false_derivative': p['derivative_rows'][0]['residues'][0] = 0
        elif name == 'false_cutoff': log['crossover']['positive_gap'] = '0'
        elif name == 'missing_crossing_start': individual['finite_pair_starts'].pop()
        elif name == 'wrong_a1567_residue': individual['new_a1567']['first_fail_n_residue'] = 0
        elif name == 'lost_nine': individual['controls']['lost_factor_nine']['F_mod_9S'] = 0
        elif name == 'false_hensel_loss': log['strong_hensel_controls'][0]['q'] += 1
        try:
            compare(p,m,log,individual,root)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('corruption accepted: '+name)
    return rejected


def audit(run):
    subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=ROOT,check=True)
    baseline = read('baseline.json')
    need(baseline['starting_main'] == baseline['requested_pr28_merge'] == BASE, 'base identity')
    parents = subprocess.check_output(['git','show','-s','--format=%P',BASE],cwd=ROOT,text=True).split()
    need(parents[0] == baseline['pr28_first_parent'] == '0a47180b889b392c2323bc1614a473af51f38d78',
         'PR28 parent')
    archive = subprocess.check_output(['git','archive',BASE],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        inherited = {m.name:tar.extractfile(m).read() for m in tar if m.isfile()}
    need({p:sha256(b).hexdigest() for p,b in inherited.items()} == baseline['inherited_sha256'],
         'complete exact base archive manifest')
    for path, data in inherited.items():
        current = (ROOT/path).read_bytes()
        if path == 'README.md':
            prefix,rest = data.split(b'\n\n',1)
            need(current.startswith(prefix+b'\n\n') and current.endswith(rest), 'preserved root README')
        else:
            need(current == data, 'inherited file changed: '+path)
    if run:
        for program, receipt in PROGRAMS:
            command = [sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(HERE/program)]
            result = subprocess.check_output(command,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
            need(result == (HERE/receipt).read_bytes(), 'fresh byte receipt '+program)
    values = [read(receipt) for _,receipt in PROGRAMS]
    p,m,log,individual,root = values
    for value, program in ((p,'pair_checks.py'),(individual,'individual_check.py'),(root,'root_log_check.py')):
        need(value['source_sha256'] == digest(HERE/program), 'arithmetic source hash '+program)
    for path, expected in m['source_sha256'].items():
        need(digest(ROOT/path) == expected, 'independent source '+path)
    for name, expected in log['bindings'].items():
        need(digest(HERE/name) == expected, 'logarithm source '+name)
    for name, expected in individual['inherited_receipt_sha256'].items():
        need(digest(HERE.parent/'power-three'/name) == expected, 'inherited individual receipt')
    need(root['inherited_source_sha256'] == digest(HERE.parent/'power-three'/'individuals.py') and
         root['compared_receipt_sha256'] == digest(HERE/'individual.json'), 'root adapter bindings')
    compare(*values)
    names = ['README.md','PAIR.md','LOGARITHMS.md','INDIVIDUAL.md','ELIMINANT_REVIEW.md',
             'SOURCES.md','baseline.json','verify.py']+[n for pair in PROGRAMS for n in pair]
    return dict(status='PASS', base_main=BASE, inherited_files_bound=len(inherited),
                unchanged_inherited_files=len(inherited)-1, only_inherited_change='README.md addition',
                artifact_sha256={name:digest(HERE/name) for name in names},
                root_README_sha256=digest(ROOT/'README.md'),
                corruption_controls_rejected=corruption_checks(values),
                pair_theorem='PROVED for every u>=0', cutoff_a=100,
                complete_transition_checks=3283, complete_derivative_checks_per_method=441,
                individual_family='OPEN', named_excluded_lengths=257, next_individual_exponent=1573,
                a1567=dict(actual=True,t=1,n_mod49=7),
                whole_length_endpoint_inclusive=1000002000000, unrestricted_five_seven='OPEN',
                wider_digit_one='OPEN', new_Lean_formalization=False, Lean_build_performed=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = audit(args.run)
    if args.write:
        (HERE/'verification.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        need(result == read('verification.json'), 'verification receipt')
    print(json.dumps({k:v for k,v in result.items() if k not in ('artifact_sha256','root_README_sha256')},
                     indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
