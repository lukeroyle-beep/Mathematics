#!/usr/bin/env python3
"""Reproduce arithmetic, compare complete coverage, and bind inherited evidence."""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = '9d958f86fc81188de68af97909614e23a186df9f'
B = 1_000_002_000_000
FIELDS = ('a', 'L', 'S', 'd', 'D', 'class_residue', 's', 'i', 't',
          'first_fail_depth', 'first_fail_n_residue')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def compare(primary, independent):
    require(len(primary['cases']) == len(independent['cases']) == 128, 'exact case count')
    for index, (left, right) in enumerate(zip(primary['cases'], independent['cases'])):
        a = 31 + 6*index
        require(left['a'] == right['a'] == a, 'complete ordered exponent coverage')
        for field in FIELDS:
            require(left[field] == right[field], f'case {a}: {field}')
        L,S,d,D,s = (left[k] for k in ('L','S','d','D','s'))
        require(S==3**a and 7*L==S+4 and d==3**(a-2) and D==2*d, 'case parameters')
        require(3<=s<D and s%6==3 and D>L and L>B, 'bounded class')
        if s>=L:
            require(left['i'] is None and left['t'] is None and
                    left['first_fail_depth'] is None and left['first_fail_n_residue'] is None,
                    'miss cannot claim actual residue')
        else:
            require(left['i']==s and left['t']>=1, 'actual candidate')
            m=left['first_fail_depth']
            require(m==left['t']+1 and m<=L-2, 'failure before witness threshold')
            require(0<left['first_fail_n_residue']<7**m and
                    left['first_fail_n_residue']%(7**(m-1))==0, 'first failure precision')
            require(left['t']<left['K'], 'finite result rejects before K')
    for field in FIELDS:
        require(primary['control_a25'][field]==independent['inherited_control'][field], 'positive control '+field)
    require(primary['control_a25']['t']==2 and primary['control_a25']['first_fail_n_residue']==294,
            'nonzero full-sum inherited control')
    require(primary['literal_checks']['counts']['full_witnesses']==0, 'putative witness needs review')
    require(primary['literal_checks']['factor_nine_negative']==independent['controls']['factor_nine_negative'],
            'factor-nine control agreement')
    require(primary['literal_checks']['counts']['words']==independent['controls']['literal_words']==25440,
            'literal coverage')
    require(len(primary['transitions'])==len(independent['compatibility'])==128, 'recurrence coverage')
    for index, (left,right) in enumerate(zip(primary['transitions'],independent['compatibility'])):
        require(left['a']==right['a']==25+6*index and left['next_a']==right['next_a']==31+6*index,
                'ordered recurrence coverage')
        require(0<=left['class_digit']<=728, 'base729 digit')


def mutation_checks(primary, independent):
    rejected=[]
    for name in ('missing_case','duplicate_exponent','false_position','wrong_failure','bad_depth','wrong_control'):
        p,q=deepcopy(primary),deepcopy(independent)
        if name=='missing_case': p['cases'].pop()
        elif name=='duplicate_exponent': p['cases'][1]['a']=31
        elif name=='false_position': q['cases'][0]['i']+=6
        elif name=='wrong_failure': q['cases'][0]['first_fail_n_residue']=0
        elif name=='bad_depth': p['cases'][0]['t']+=1
        elif name=='wrong_control': q['inherited_control']['t']=1
        try:
            compare(p,q)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('corrupted receipt accepted: '+name)
    return rejected


def audit():
    baseline=json.loads((HERE/'baseline-inputs.json').read_text())
    require(baseline['starting_main']==baseline['requested_pr26_merge']==BASE,'requested baseline')
    for name,expected in baseline['inherited_sha256'].items():
        require(digest(ROOT/name)==expected,'inherited input changed: '+name)
    subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=ROOT,check=True,capture_output=True)
    runs=[]
    for program,receipt in [('primary.py','primary.json'),('independent.py','independent.json')]:
        expected=(HERE/receipt).read_bytes()
        normal=subprocess.check_output([sys.executable,str(HERE/program)])
        optimized=subprocess.check_output([sys.executable,'-O',str(HERE/program)])
        require(normal==optimized==expected,'fresh normal/optimized mismatch: '+program)
        require(json.loads(expected)['source_sha256']==digest(HERE/program),'checker source binding')
        runs.append(dict(program=program,receipt=receipt,normal_and_optimized_match=True))
    p=json.loads((HERE/'primary.json').read_text())
    q=json.loads((HERE/'independent.json').read_text())
    compare(p,q)
    rejected=mutation_checks(p,q)
    names=['README.md','MATH_REVIEW.md','INHERITED.md','baseline-inputs.json',
           'primary.py','primary.json','independent.py','independent.json','verify.py']
    return dict(status='PASS',base_main=BASE,inherited_files_bound=len(baseline['inherited_sha256']),
                fresh_reproductions=runs,arithmetic_case_agreement=128,recurrence_links=128,
                counts=p['counts'],actual_valuation_histogram=p['actual_valuation_histogram'],
                corruption_controls_rejected=rejected,
                artifact_sha256={name:digest(HERE/name) for name in names},
                whole_length_endpoint_inclusive=B,new_consecutive_lengths=0,
                family_exponents={'first':31,'step':6,'count':128,'last':793,'next_unchecked':799},
                infinite_power_of_three_family='OPEN',unrestricted_five_seven='OPEN',wider_A398769='OPEN',
                full_witness_found=False,global_escape_proved=False,effective_cutoff_obtained=False,
                historical_large_searches_rerun=False,new_Lean_formalization=False,Lean_build_performed=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='explicitly regenerate verification receipt')
    args=parser.parse_args()
    result=audit()
    path=HERE/'verification.json'
    if args.write:
        path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        require(json.loads(path.read_text())==result,'verification receipt mismatch')
    print(json.dumps({k:result[k] for k in ['status','arithmetic_case_agreement','counts',
          'actual_valuation_histogram','inherited_files_bound','whole_length_endpoint_inclusive',
          'corruption_controls_rejected']},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
