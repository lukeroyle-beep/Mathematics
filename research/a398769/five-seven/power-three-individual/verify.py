#!/usr/bin/env python3
"""Reproduce four exact receipts, cross-check methods, and bind the base tree."""
import argparse
from collections import Counter
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
BASE = 'a9edeb0a96bd56d55f3c96767f5154e69cb8ceda'
PROGRAMS = [('root_log.py','root_log.json'),
            ('independent_decimal.py','independent_decimal.json'),
            ('math_checks.py','math-checks.json'),
            ('index_lift.py','index_lift.json')]
DOCS = ['README.md','COMMON_FACTOR.md','MOVING_POSITION.md','INDIVIDUAL.md','SOURCES.md']


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def compare(primary, independent, math, index):
    exponents = [25]+list(range(31,100,6))+[1231,1567,1573,1579]
    need(primary['exponents'] == independent['exponents'] == exponents, 'complete new domain')
    need([r['a'] for r in primary['cases']] == [r['a'] for r in independent['rows']] == exponents,
         'ordered case completeness')
    p = {r['a']:r for r in primary['cases']}
    d = {r['a']:r for r in independent['rows']}
    fields = ('a','L','S','d','D','s','i','actual','s_mod_126','g','q','t',
              'first_fail_depth','first_fail_n_residue','n_mod_S','n_mod_25S','seven_residues')
    for a in exponents:
        r, b = p[a], d[a]
        need(all(r[k] == b[k] for k in fields), 'independent agreement at '+str(a))
        L,s,S = r['L'],r['s'],r['S']
        need(S == 3**a and 7*L == S+4 and r['d'] == 3**(a-2) and
             r['D'] == 2*r['d'] and 3<=s<r['D'] and s%6 == 3 and L<r['D'], 'exact family')
        need(r['F_mod_9S'] == 0 and r['actual'] == (3<=s<L), 'full sum and actual range')
        if r['actual']:
            need(b['F_mod_9S'] == r['n_mod_S'] == r['n_mod_25S'] == 0, 'same-position factors')
            need(r['g']*r['q'] == L and r['g']*r['p'] == s and
                 r['q_fourth_gt_L'] == (r['q']**4>L), 'reduced ratio')
            t,m,res = r['t'],r['first_fail_depth'],r['first_fail_n_residue']
            need(m == t+1 <= L-2 and 0<res<7**m and res%7**t == 0 and
                 r['seven_residues'] == [0]*t+[res], 'exact failure and inclusive deadline')
            need(b['first_fail_modulus'] == 7**m and b['full_witness'] is False,
                 'original predicate disproved')
        else:
            need(s>=L and r['i'] is None and r['t'] is None and b['F_mod_9S'] is None,
                 'class miss is not an evaluated word')
    need(not p[1573]['actual'] and p[1573]['s_mod_126'] == 123, '1573 class miss')
    need(p[1579]['g'] == 1 and p[1579]['seven_residues'] == [0,14], '1579 actual result')
    need(p[1231]['actual'] and p[1231]['seven_residues'] == [0,0,0,0,14406], 'depth-four control')
    need(p[25]['seven_residues'] == [0,0,294], 'positive sum control')
    nine = independent['controls']['lost_factor_nine']
    need((nine['F_mod_S'],nine['F_mod_9S'],nine['n_mod_S']) == (0,17496,1944)
         and not nine['PS_divides_n'] and not nine['full_F_divides'], 'factor nine control')
    need(independent['controls']['literal_pairs'] == 2015 and
         independent['controls']['complete_a7']['eligible'] == [159], 'original-word controls')

    small = list(range(31,100,6))
    need(math['finite_exponents'] == small and [r['a'] for r in math['finite_rows']] == small,
         'complete finite analytic remainder')
    for r in math['finite_rows']:
        need(all(r[k] == p[r['a']][k] for k in ('L','s','i','t','first_fail_n_residue')),
             'fresh finite reconstruction matches theorem certificate')
    need(math['valuation_constant'] == 312000 and math['cutoff_a'] == 100,
         'theorem constant and cutoff')
    need(math['crossover_left'] == 3**100 and
         math['crossover_right'] == 7*(624000*120**2)**4 and
         math['crossover_margin'] == math['crossover_left']-math['crossover_right'] > 0,
         'strict exact crossover')
    need(math['induction_margin_3_times_20_to_8_minus_21_to_8'] == 3*20**8-21**8 > 0,
         'induction propagation')
    need(math['depth_two_surviving_s_mod42'] == [39] and
         len(math['depth_two_F_residues_mod49']) == 42, 'complete depth-two period')
    need(len(math['synthetic_hensel_controls']) == 4 and
         all(r['t']>=2 and r['derivative_mod7'] != 0 for r in math['synthetic_hensel_controls']),
         'nonvacuous Hensel controls')

    need(index['depth_two_and_three_cases'] == 49*294 and
         index['direct_exponentiation_comparisons'] == 4200 and
         index['exact_difference_pairs'] == 4950, 'declared index audit domains')
    perms = index['complete_permutations']
    need([(r['s'],r['j'],r['classes']) for r in perms] ==
         [(s,j,7**j) for s in (39,81,123,165,207,249,291) for j in range(1,4)],
         'complete permutation domains')
    need([r['s'] for r in index['digit_lift_controls']] == [39,123,291], 'lift controls')
    for control in index['digit_lift_controls']:
        rows=control['roots']
        need([r['depth'] for r in rows] == list(range(2,11)), 'complete lift depths')
        for old,new in zip(rows,rows[1:]):
            need(new['modulus'] == 7*old['modulus'] and
                 new['residue'] == old['residue']+new['digit']*old['modulus'] and
                 0<=new['digit']<7 and new['digit'] == -4*new['carry']%7, 'exact index digit')
    need([r['a'] for r in index['ternary_controls']] == [97,1231,1573,1579], 'ternary index controls')
    for r in index['ternary_controls']:
        need(all(r[k] == p[r['a']][k] for k in ('a','L','s','actual')), 'third ternary method')
        need(r['ternary_relation_mod_d'] == 0, 'ternary rational-position relation')
        if r['actual']:
            need(r['g'] == p[r['a']]['g'] and r['q'] == p[r['a']]['q'], 'third reduced ratio')
    depth4 = next(r for r in index['ternary_controls'] if r['a'] == 1231)
    need(depth4['F_mod_7_powers'][:3] == [0,0,0] and
         depth4['index_mismatches'] == [5,6,7,8], 'actual unique-class survival control')


def corruption_checks(values):
    names=['missing_new_member','false_range','lost_nine','false_residue','missing_small_exponent',
           'false_cutoff','wrong_digit','missing_permutation','false_depth_four_control']
    for name in names:
        p,d,m,i=deepcopy(values)
        if name=='missing_new_member': p['cases'].pop()
        elif name=='false_range': next(r for r in p['cases'] if r['a']==1573)['actual']=True
        elif name=='lost_nine': d['controls']['lost_factor_nine']['F_mod_9S']=0
        elif name=='false_residue': d['rows'][-1]['first_fail_n_residue']=0
        elif name=='missing_small_exponent': m['finite_exponents'].pop()
        elif name=='false_cutoff': m['crossover_margin']=0
        elif name=='wrong_digit': i['digit_lift_controls'][0]['roots'][1]['digit']+=1
        elif name=='missing_permutation': i['complete_permutations'].pop()
        elif name=='false_depth_four_control': i['ternary_controls'][1]['index_mismatches']=[4,5,6,7,8]
        try:
            compare(p,d,m,i)
        except ValueError:
            continue
        raise ValueError('corruption accepted: '+name)
    return names


def audit(run):
    subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=ROOT,check=True)
    baseline=read(HERE/'baseline.json')
    need(baseline['starting_main'] == baseline['requested_pr29_merge'] == BASE, 'base identity')
    archive=subprocess.check_output(['git','archive',BASE],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        inherited={m.name:tar.extractfile(m).read() for m in tar if m.isfile()}
    need({p:sha256(b).hexdigest() for p,b in inherited.items()} == baseline['inherited_sha256'],
         'exact base archive bindings')
    for path,data in inherited.items():
        current=(ROOT/path).read_bytes()
        if path=='README.md':
            prefix,rest=data.split(b'\n\n',1)
            need(current.startswith(prefix+b'\n\n') and current.endswith(rest), 'root README addition only')
        else:
            need(current==data, 'inherited file changed: '+path)
    if run:
        for program,receipt in PROGRAMS:
            command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(HERE/program)]
            result=subprocess.check_output(command,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
            need(result==(HERE/receipt).read_bytes(), 'fresh byte-identical receipt '+program)
    values=[read(HERE/receipt) for _,receipt in PROGRAMS]
    for value,(program,_) in zip(values,PROGRAMS):
        need(value['source_sha256']==digest(HERE/program), 'program source binding')
    p,d,m,i=values
    need(p['inherited_source_sha256']==digest(ROOT/p['inherited_source_path']), 'Newton source binding')
    need(m['proof_sha256']==digest(HERE/'COMMON_FACTOR.md'), 'common-factor proof binding')
    for path,expected in m['inherited_sha256'].items():
        need(digest(HERE.parent/path)==expected, 'inherited math input '+path)
    compare(*values)
    # Historical whole-family coverage is inherited, not a rerun of its search.
    old=[read(HERE.parent/'power-three'/name) for name in ('individuals.json','individuals-independent.json')]
    need([r['a'] for r in old[0]['cases']] == [r['a'] for r in old[1]['cases']] == list(range(31,1562,6)),
         'all 256 inherited rows')
    for x,y in zip(old[0]['cases'],old[1]['cases']):
        need(all(x[k]==y[k] for k in ('a','L','s','i','t','first_fail_depth','first_fail_n_residue')),
             'all inherited independent fields')
    pair=read(HERE.parent/'power-three-pair'/'individual.json')['new_a1567']
    row1567=next(r for r in p['cases'] if r['a']==1567)
    need(all(pair[k]==row1567[k] for k in ('L','s','i','t','first_fail_n_residue')), 'a1567 inherited match')
    complete=old[0]['cases']+[row1567]+[r for r in p['cases'] if r['a'] in (1573,1579)]
    need([r['a'] for r in complete] == list(range(31,1580,6)), '259 consecutive family exponents')
    misses=sum(r['i'] is None for r in complete)
    histogram=dict(sorted(Counter(str(r['t']) for r in complete if r['i'] is not None).items()))
    need(misses==85 and histogram=={'1':152,'2':18,'3':3,'4':1}, 'combined finite coverage')
    artifacts=DOCS+['baseline.json','verify.py']+[x for pair in PROGRAMS for x in pair]
    return dict(status='PASS',base_main=BASE,inherited_files_bound=len(inherited),
                unchanged_inherited_files=len(inherited)-1,only_inherited_change='README.md addition',
                artifact_sha256={n:digest(HERE/n) for n in artifacts},root_README_sha256=digest(ROOT/'README.md'),
                corruption_controls_rejected=corruption_checks(values),
                common_factor_theorem='PROVED: every full witness has q^4>L',
                valuation_constant=312000,cutoff_a=100,smaller_admissible_exponents=12,
                fixed_position_index_theorem='PROVED: one class modulo 7^(m-2) at each m>=2',
                individual_family='OPEN for remaining moving positions',new_exponents=[1573,1579],
                named_excluded_lengths=len(complete),class_misses=misses,actual_candidates=259-misses,
                valuation_histogram=histogram,next_individual_exponent=1585,
                whole_length_endpoint_inclusive=1000002000000,unrestricted_five_seven='OPEN',
                wider_digit_one='OPEN',Lean_verification_performed=False,historical_large_searches_rerun=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    result=audit(args.run)
    if args.write:
        (HERE/'verification.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        need(result==read(HERE/'verification.json'), 'verification receipt')
    print(json.dumps({k:v for k,v in result.items() if k not in ('artifact_sha256','root_README_sha256')},
                     indent=2,sort_keys=True))


if __name__=='__main__':
    main()
