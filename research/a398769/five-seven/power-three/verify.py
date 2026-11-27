#!/usr/bin/env python3
"""Bind sources, compare complete independent results, optionally rerun them."""
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = '0a47180b889b392c2323bc1614a473af51f38d78'
PROGRAMS = [('individuals.py','individuals.json'),
            ('individuals_independent.py','individuals-independent.json'),
            ('transitions.py','transitions.json'),
            ('transitions_independent.py','transitions-independent.json')]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((HERE/name).read_text())


def compare(p, q, direct, lifted):
    need(p['specified_exponents'] == q['specified_exponents'] ==
         dict(first=31,step=6,count=256,last=1561,next=1567), 'declared exponent scope')
    need(len(p['cases']) == len(q['cases']) == 256 and p['cases'] == q['cases'],
         'complete independent individual rows')
    need(p['control_a25'] == q['control_a25'], 'independent positive control')
    need((p['control_a25']['i'],p['control_a25']['t'],p['control_a25']['first_fail_n_residue']) ==
         (40582608819,2,294), 'nonvacuous a25 control')
    need(q['controls']['literal_words'] == 25440 and q['controls']['sum_passes'] > 0,
         'literal and sum-positive coverage')
    negative = p['factor_nine_negative']
    for field, expected in dict(L=313,i=51,S=2187,F_mod_S=0,F_mod_9S=17496,n_mod_S=1944).items():
        need(negative[field] == q['controls']['factor_nine_negative'][field] == expected,
             'factor-nine negative '+field)
    for u, row in enumerate(p['cases']):
        a = 31+6*u
        need(row['a'] == a and row['S'] == 3**a and 7*row['L'] == 3**a+4, 'ordered length coverage')
        s,L,d,D = (row[f] for f in ('s','L','d','D'))
        need(d == 3**(a-2) and D == 2*d and D>L and 3<=s<D and s%6==3, 'exact unique class')
        need(row['class_residue'] == s, 'canonical representative')
        if s>=L:
            need(all(row[f] is None for f in ('i','t','first_fail_depth','first_fail_n_residue')),
                 'class miss cannot claim an actual word')
        else:
            need(row['i'] == s and row['t']>=1, 'actual position')
            m,r = row['first_fail_depth'],row['first_fail_n_residue']
            need(m == row['t']+1 and m <= L-2 and 0<r<7**m and r%7**(m-1)==0,
                 'exact nonzero original-word residue before deadline')
    misses=sum(r['i'] is None for r in p['cases'])
    hist=dict(sorted(Counter(str(r['t']) for r in p['cases'] if r['i'] is not None).items()))
    for receipt in (p,q):
        need(receipt['class_misses']==misses==84 and receipt['actual_candidates']==256-misses==172,
             'derived individual counts')
        need(receipt['valuation_histogram']==hist=={'1':150,'2':18,'3':3,'4':1}, 'derived histogram')
    need(len(p['recurrence_digits'])==256, 'complete recurrence links')
    for old,new,k in zip([p['control_a25']]+p['cases'][:-1],p['cases'],p['recurrence_digits']):
        need(new['s']==old['s']+old['D']*k and 0<=k<=728, 'exact successive lift digit')
    need(direct['increment_domain']==lifted['increment_range_inclusive']==[0,728], 'all increment bounds')
    need(direct['wraparound_included'], 'wraparound coverage')
    need([r['m'] for r in direct['levels']]==list(range(5,10)), 'all direct depths')
    need([r['m'] for r in lifted['levels']]==list(range(2,10)), 'all independent lift depths')
    for m,expected in zip(range(5,10),(35,14,14,7,0)):
        x=direct['levels'][m-5];y=lifted['levels'][m-2]
        need(x['period']==y['period']==x['visited_starts']==7**(m-2), 'complete period')
        need(x['starts']==y['starts'] and len(x['starts'])==x['two_transition_start_count']==y['start_count']==expected,
             'all projected starts and increments agree')
        need([r['u'] for r in x['starts']]==sorted(set(r['u'] for r in x['starts'])), 'unique ordered starts')
        for r in x['starts']:
            need(0<=r['u']<x['period'] and r['first_increments'] and r['second_increments'], 'bounded start')
            need(all(0<=k<=728 for k in r['first_increments']+r['second_increments']), 'bounded increments')
    control=dict(u=14984,first_increments=[189],second_increments=[42])
    need(control in direct['levels'][3]['starts'] and lifted['positive_control']==control, 'projected positive control')
    need(direct['depth_nine_has_no_projected_starts'] and lifted['depth_nine_projected_start_count']==0,
         'depth-nine conclusion')


def corruption_checks(values):
    names=('missing_member','false_actual','wrong_nine','wrong_residue','wrong_histogram',
           'missing_projected_control','wrong_period','excluded_increment','false_depth_nine')
    rejected=[]
    for name in names:
        p,q,d,l=deepcopy(values)
        if name=='missing_member':p['cases'].pop()
        elif name=='false_actual':q['cases'][0]['i']+=6
        elif name=='wrong_nine':p['factor_nine_negative']['F_mod_9S']=0
        elif name=='wrong_residue':p['cases'][0]['first_fail_n_residue']=0
        elif name=='wrong_histogram':p['valuation_histogram']['4']=0
        elif name=='missing_projected_control':d['levels'][3]['starts'].pop(0)
        elif name=='wrong_period':d['levels'][4]['period']+=1
        elif name=='excluded_increment':l['increment_range_inclusive']=[1,728]
        elif name=='false_depth_nine':l['levels'][-1]['start_count']=1
        try:
            compare(p,q,d,l)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('corruption accepted: '+name)
    return rejected


def audit(run=False):
    baseline=read('baseline.json')
    need(baseline['starting_main']==baseline['requested_pr27_merge']==BASE,'base main')
    need(not baseline['later_main_commits_at_start'],'initial later-work accounting')
    subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=ROOT,check=True,capture_output=True)
    old_readme=subprocess.check_output(['git','show',BASE+':README.md'],cwd=ROOT)
    for path,expected in baseline['inherited_sha256'].items():
        current=old_readme if path=='README.md' else (ROOT/path).read_bytes()
        need(sha256(current).hexdigest()==expected,'inherited source changed: '+path)
    # Preserve every original root paragraph in order; only the introductory
    # power-three paragraph is added immediately after the old two-line header.
    old_prefix,old_rest=old_readme.split(b'\n\n',1)
    current=(ROOT/'README.md').read_bytes()
    need(current.startswith(old_prefix+b'\n\n') and current.endswith(old_rest),'preserved inherited root README')
    for program,receipt in PROGRAMS:
        expected=(HERE/receipt).read_bytes()
        need(json.loads(expected)['source_sha256']==digest(HERE/program),'source binding: '+program)
        if run:
            command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(HERE/program)]
            actual=subprocess.check_output(command,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
            need(actual==expected,'fresh receipt mismatch: '+program)
    p,q,d,l=[read(name) for name in ('individuals.json','individuals-independent.json','transitions.json','transitions-independent.json')]
    need(q['inherited_source_sha256']==baseline['inherited_sha256']['research/a398769/five-seven/sum-position-escape/independent.py'],
         'independent inherited source pinned to base')
    for path,expected in d['inherited_inputs_sha256'].items():
        need(expected==digest(HERE.parent/path),'transition inherited source binding')
    compare(p,q,d,l)
    old= json.loads((HERE.parent/'sum-position-escape'/'independent.json').read_text())
    need(p['cases'][:128]==old['cases'],'all PR27 individual rows preserved')
    names=['README.md','INDIVIDUAL.md','THREE_LENGTH.md','baseline.json','verify.py']
    names += [name for pair in PROGRAMS for name in pair]
    return dict(status='PASS',base_main=BASE,inherited_files_bound=len(baseline['inherited_sha256']),
                artifact_sha256={name:digest(HERE/name) for name in names},
                root_README_sha256=digest(ROOT/'README.md'),
                corruption_controls_rejected=corruption_checks((p,q,d,l)),
                individual_exponents=p['specified_exponents'],class_misses=84,actual_candidates=172,
                exact_valuation_histogram=p['valuation_histogram'],
                projected_periods=[r['period'] for r in d['levels']],
                projected_start_counts=[r['two_transition_start_count'] for r in d['levels']],
                positive_control=dict(m=8,u=14984,k=189,j=42),
                three_length_theorem_proved=True,individual_family='OPEN',effective_cutoff=None,
                full_witness_found=False,whole_length_endpoint_inclusive=1000002000000,
                new_consecutive_lengths=0,unrestricted_five_seven='OPEN',wider_digit_one='OPEN',
                historical_large_enumerations_rerun=False,new_Lean_formalization=False,Lean_build_performed=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',action='store_true',help='rerun all arithmetic in current optimization mode')
    parser.add_argument('--write',action='store_true',help='explicitly regenerate retained verification receipt')
    args=parser.parse_args()
    result=audit(args.run)
    if args.write:
        (HERE/'verification.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        need(read('verification.json')==result,'verification receipt mismatch')
    print(json.dumps({k:result[k] for k in ('status','individual_exponents','class_misses','actual_candidates',
          'exact_valuation_histogram','projected_start_counts','inherited_files_bound','corruption_controls_rejected')},
          indent=2,sort_keys=True))


if __name__=='__main__':
    main()
